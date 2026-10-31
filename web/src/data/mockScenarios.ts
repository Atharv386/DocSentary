export interface EvidenceRef {
  evidence_id: string;
  role: "code" | "documentation";
  path: string;
  line_start: number;
  line_end: number;
  quote: string;
  source_kind: "ast_fact" | "diff_hunk" | "doc_span";
}

export interface Finding {
  finding_id: string;
  status: "DRIFT" | "POTENTIAL_DRIFT" | "NO_DRIFT" | "UNCERTAIN";
  severity: "critical" | "high" | "medium" | "low" | "info";
  rule_id: string;
  category: string;
  title: string;
  explanation: string;
  evidence: EvidenceRef[];
  confidence: number | null;
  verification: "deterministic" | "model_assisted" | "human_fixture";
  suggested_action?: string;
}

export interface ChangedFile {
  path_before: string | null;
  path_after: string | null;
  change_type: "added" | "modified" | "deleted" | "renamed";
  is_binary: boolean;
  hunks: Array<{
    old_start: number | null;
    old_count: number | null;
    new_start: number | null;
    new_count: number | null;
    header?: string;
    added_lines: string[];
    removed_lines: string[];
  }>;
}

export interface ScanReport {
  schema_version: string;
  scan_id: string;
  base_sha: string;
  head_sha: string;
  merge_base_sha: string;
  tool_version: string;
  model_id: string | null;
  summary: {
    changed_files: number;
    findings: number;
    drift: number;
    potential_drift?: number;
    uncertain?: number;
    code_facts?: number;
    doc_spans?: number;
  };
  changed_files: ChangedFile[];
  findings: Finding[];
  warnings: string[];
  duration_ms: number;
}

export interface Scenario {
  id: string;
  prNumber: number;
  prTitle: string;
  author: string;
  branch: string;
  targetBranch: string;
  description: string;
  report: ScanReport;
}

export const SCENARIOS: Scenario[] = [
  {
    id: "stale-default",
    prNumber: 42,
    prTitle: "perf: increase default client connection timeout to 60s",
    author: "alex-chen",
    branch: "feat/timeout-increase",
    targetBranch: "main",
    description: "Increases default network timeout from 30 to 60 seconds in client.py. Documentation was overlooked.",
    report: {
      schema_version: "1.0",
      scan_id: "scan-2026-10-31-001",
      base_sha: "e47d19ba921e548231c552098b6710b18201a4bc",
      head_sha: "776ee2c85b461f8a84cd8a1a364be2eb814d4812",
      merge_base_sha: "e47d19ba921e548231c552098b6710b18201a4bc",
      tool_version: "0.1.0",
      model_id: "organizer-open-weight-verifier",
      summary: {
        changed_files: 1,
        code_facts: 1,
        doc_spans: 14,
        findings: 1,
        drift: 1,
        potential_drift: 0,
        uncertain: 0
      },
      changed_files: [
        {
          path_before: "src/client.py",
          path_after: "src/client.py",
          change_type: "modified",
          is_binary: false,
          hunks: [
            {
              old_start: 12,
              old_count: 3,
              new_start: 12,
              new_count: 3,
              header: "def connect(timeout=30):",
              added_lines: ["def connect(timeout=60):"],
              removed_lines: ["def connect(timeout=30):"]
            }
          ]
        }
      ],
      findings: [
        {
          finding_id: "DG-0001",
          status: "DRIFT",
          severity: "high",
          rule_id: "PY-DEFAULT-001",
          category: "default_value_mismatch",
          title: "Documented timeout default is outdated",
          explanation: "The documentation in docs/config.md states the default timeout is 30 seconds, but the updated function in src/client.py defaults timeout to 60.",
          evidence: [
            {
              evidence_id: "E1",
              role: "code",
              path: "src/client.py",
              line_start: 12,
              line_end: 12,
              quote: "def connect(..., timeout=60): ...",
              source_kind: "ast_fact"
            },
            {
              evidence_id: "E2",
              role: "documentation",
              path: "docs/config.md",
              line_start: 23,
              line_end: 23,
              quote: "The default timeout is 30 seconds.",
              source_kind: "doc_span"
            }
          ],
          confidence: 1.0,
          verification: "deterministic",
          suggested_action: "Update 'docs/config.md:23' to reflect default timeout=60."
        }
      ],
      warnings: [],
      duration_ms: 412
    }
  },
  {
    id: "param-renamed",
    prNumber: 89,
    prTitle: "refactor(auth): rename login parameter 'username' to 'email'",
    author: "sarah-dev",
    branch: "refactor/email-login",
    targetBranch: "main",
    description: "Switches authentication credentials from username to email. Documentation still references username parameter.",
    report: {
      schema_version: "1.0",
      scan_id: "scan-2026-10-31-002",
      base_sha: "3b18c028a01124ef91bca7e8c08ef1284a0d9f4e",
      head_sha: "9ac281ef5610bcde824b01e9128fba50a891c784",
      merge_base_sha: "3b18c028a01124ef91bca7e8c08ef1284a0d9f4e",
      tool_version: "0.1.0",
      model_id: "organizer-open-weight-verifier",
      summary: {
        changed_files: 1,
        code_facts: 2,
        doc_spans: 19,
        findings: 1,
        drift: 1,
        potential_drift: 0,
        uncertain: 0
      },
      changed_files: [
        {
          path_before: "src/auth.py",
          path_after: "src/auth.py",
          change_type: "modified",
          is_binary: false,
          hunks: [
            {
              old_start: 18,
              old_count: 2,
              new_start: 18,
              new_count: 2,
              header: "def login():",
              added_lines: ["def login(email, password):"],
              removed_lines: ["def login(username, password):"]
            }
          ]
        }
      ],
      findings: [
        {
          finding_id: "DG-0002",
          status: "DRIFT",
          severity: "high",
          rule_id: "PY-PARAM-002",
          category: "stale_parameter",
          title: "Documentation references removed parameter 'username'",
          explanation: "Parameter 'username' was removed from login() in src/auth.py, but documentation still requires it.",
          evidence: [
            {
              evidence_id: "E1",
              role: "code",
              path: "src/auth.py",
              line_start: 18,
              line_end: 18,
              quote: "Parameter 'username' was removed from login()",
              source_kind: "ast_fact"
            },
            {
              evidence_id: "E2",
              role: "documentation",
              path: "docs/auth.md",
              line_start: 15,
              line_end: 15,
              quote: "Pass the `username` and password to authenticate your session.",
              source_kind: "doc_span"
            }
          ],
          confidence: 0.95,
          verification: "deterministic",
          suggested_action: "Update 'docs/auth.md:15' to reference 'email' instead of 'username'."
        }
      ],
      warnings: [],
      duration_ms: 388
    }
  },
  {
    id: "internal-refactor",
    prNumber: 104,
    prTitle: "optimize: internal buffer allocation for payload checksums",
    author: "marcus-sys",
    branch: "perf/buffer-tuning",
    targetBranch: "main",
    description: "Refactors internal chunking logic in crypto.py. Zero API or documentation contract changes.",
    report: {
      schema_version: "1.0",
      scan_id: "scan-2026-10-31-003",
      base_sha: "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b",
      head_sha: "9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e",
      merge_base_sha: "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b",
      tool_version: "0.1.0",
      model_id: "organizer-open-weight-verifier",
      summary: {
        changed_files: 1,
        code_facts: 0,
        doc_spans: 12,
        findings: 0,
        drift: 0,
        potential_drift: 0,
        uncertain: 0
      },
      changed_files: [
        {
          path_before: "src/crypto.py",
          path_after: "src/crypto.py",
          change_type: "modified",
          is_binary: false,
          hunks: [
            {
              old_start: 45,
              old_count: 5,
              new_start: 45,
              new_count: 4,
              header: "def _hash_chunks():",
              added_lines: ["    buf = bytearray(8192)"],
              removed_lines: ["    buf = bytes()"]
            }
          ]
        }
      ],
      findings: [],
      warnings: [],
      duration_ms: 295
    }
  },
  {
    id: "docs-fixed-together",
    prNumber: 112,
    prTitle: "feat: update MAX_RETRIES to 5 and sync settings documentation",
    author: "rachel-lead",
    branch: "feat/retries-bump",
    targetBranch: "main",
    description: "Both code constant and markdown guide were updated in the same PR. DocGuard verifies sync.",
    report: {
      schema_version: "1.0",
      scan_id: "scan-2026-10-31-004",
      base_sha: "7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b",
      head_sha: "2d3e4f5a6b7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c",
      merge_base_sha: "7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b",
      tool_version: "0.1.0",
      model_id: "organizer-open-weight-verifier",
      summary: {
        changed_files: 2,
        code_facts: 1,
        doc_spans: 22,
        findings: 0,
        drift: 0,
        potential_drift: 0,
        uncertain: 0
      },
      changed_files: [
        {
          path_before: "src/settings.py",
          path_after: "src/settings.py",
          change_type: "modified",
          is_binary: false,
          hunks: [
            {
              old_start: 5,
              old_count: 1,
              new_start: 5,
              new_count: 1,
              header: "MAX_RETRIES",
              added_lines: ["MAX_RETRIES = 5"],
              removed_lines: ["MAX_RETRIES = 3"]
            }
          ]
        },
        {
          path_before: "docs/settings.md",
          path_after: "docs/settings.md",
          change_type: "modified",
          is_binary: false,
          hunks: [
            {
              old_start: 12,
              old_count: 1,
              new_start: 12,
              new_count: 1,
              header: "Settings",
              added_lines: ["The default retry limit is 5 attempts."],
              removed_lines: ["The default retry limit is 3 attempts."]
            }
          ]
        }
      ],
      findings: [],
      warnings: [],
      duration_ms: 360
    }
  }
];
