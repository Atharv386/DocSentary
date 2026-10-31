import json
import os
from pathlib import Path

import httpx

from docguard.ai.protocol import EvidenceBundle, ModelAssessment


def _load_env_file() -> None:
    """Loads key-value pairs from .env into os.environ if not already set."""
    for candidate in (Path(".env"), Path("../.env")):
        if candidate.is_file():
            try:
                for line in candidate.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip().strip("'\"")
                    if k not in os.environ:
                        os.environ[k] = v
            except Exception:
                pass


_load_env_file()

SYSTEM_PROMPT = """You are DocGuard's documentation-consistency verifier.
You do not write documentation and do not infer facts outside the evidence.
Classify whether the supplied documentation remains accurate after the supplied code change.
Use only evidence IDs included in the input.

DRIFT requires a direct contradiction supported by code and documentation.
POTENTIAL_DRIFT means a relevant statement may be stale but the contradiction is not fully proven.
NO_DRIFT means the documentation remains compatible with the supplied change.
UNCERTAIN means evidence is incomplete or behavior is dynamic/ambiguous.

Never invent a path, line number, quote, identifier, default, or runtime fact.
If a fact is not explicit in the supplied code evidence, return UNCERTAIN.
Return ONLY valid JSON matching this schema:
{
  "status": "DRIFT | POTENTIAL_DRIFT | NO_DRIFT | UNCERTAIN",
  "severity": "high | medium | low | info",
  "explanation": "One or two sentences.",
  "evidence_ids": ["CODE-1", "DOC-2"],
  "reasoning_type": "direct_contradiction | likely_outdated | no_change | insufficient_context",
  "suggested_action": "Optional review instruction"
}
"""


class ModelClient:
    """HTTP client supporting Ollama and organizer-provided open-weight model endpoints."""

    def __init__(self) -> None:
        self.enabled = os.environ.get("DOCGUARD_MODEL_ENABLED", "true").lower() == "true"
        self.provider = os.environ.get("DOCGUARD_MODEL_PROVIDER", "ollama").lower()
        self.base_url = os.environ.get("DOCGUARD_MODEL_BASE_URL", "http://localhost:11434").rstrip("/")
        self.api_key = os.environ.get("DOCGUARD_MODEL_API_KEY", "")
        self.model_name = os.environ.get("DOCGUARD_MODEL_NAME", "qwen3:8b")
        timeout_val = os.environ.get("DOCGUARD_MODEL_TIMEOUT_SECONDS", "60")
        self.timeout = float(timeout_val) if timeout_val.isdigit() else 60.0

    def is_configured(self) -> bool:
        return bool(self.enabled and self.base_url)

    def verify_bundle(self, bundle: EvidenceBundle) -> ModelAssessment:
        if not self.is_configured():
            return ModelAssessment(
                status="UNCERTAIN",
                severity="info",
                explanation=(
                    "Model verifier endpoint not configured; "
                    "semantic candidate marked UNCERTAIN."
                ),
                evidence_ids=[i.evidence_id for i in bundle.evidence_items[:2]],
                reasoning_type="insufficient_context",
            )

        is_ollama_native = "11434" in self.base_url and not self.base_url.endswith("/v1")

        if is_ollama_native:
            # Native Ollama /api/chat with format: "json"
            url = f"{self.base_url}/api/chat"
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": bundle.model_dump_json()},
                ],
                "stream": False,
                "format": "json",
                "options": {"temperature": 0.0},
            }
        else:
            # OpenAI-compatible /v1/chat/completions
            endpoint = (
                "/chat/completions"
                if self.base_url.endswith("/v1")
                else "/v1/chat/completions"
            )
            url = f"{self.base_url}{endpoint}"
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": bundle.model_dump_json()},
                ],
                "temperature": 0.0,
                "response_format": {"type": "json_object"},
            }

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.post(url, json=payload, headers=headers)
                if res.status_code in (401, 403):
                    return ModelAssessment(
                        status="UNCERTAIN",
                        severity="info",
                        explanation=(
                            f"Model authentication failed ({res.status_code}); "
                            "semantic candidate marked UNCERTAIN."
                        ),
                        evidence_ids=[i.evidence_id for i in bundle.evidence_items[:2]],
                        reasoning_type="insufficient_context",
                    )
                res.raise_for_status()
                data = res.json()

                raw_content = ""
                if "message" in data and "content" in data["message"]:
                    # Native Ollama response
                    raw_content = data["message"]["content"]
                elif "choices" in data and data["choices"]:
                    # OpenAI-compatible response
                    raw_content = data["choices"][0]["message"]["content"]
                elif "response" in data:
                    raw_content = data["response"]
                else:
                    raw_content = str(data)

                # Parse JSON block
                clean_json = raw_content.strip()
                if clean_json.startswith("```"):
                    clean_json = clean_json.split("\n", 1)[1]
                    if clean_json.endswith("```"):
                        clean_json = clean_json.rsplit("\n", 1)[0]

                parsed = json.loads(clean_json)
                return ModelAssessment.model_validate(parsed)

        except Exception as exc:
            return ModelAssessment(
                status="UNCERTAIN",
                severity="info",
                explanation=f"Model verification failed ({type(exc).__name__}); marked UNCERTAIN.",
                evidence_ids=[i.evidence_id for i in bundle.evidence_items[:2]],
                reasoning_type="insufficient_context",
            )
