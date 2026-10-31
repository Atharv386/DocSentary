import React, { useState } from "react";
import { Zap } from "lucide-react";

export const BenchmarkView: React.FC = () => {
  const [activeSuite, setActiveSuite] = useState<"realworld" | "constructed" | "semantic">("realworld");

  return (
    <div className="flex-1 p-8 bg-brand-dark overflow-y-auto font-sans">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-brand-border pb-5">
          <div>
            <div className="flex items-center space-x-2 text-xs font-mono text-emerald-400 mb-1">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>INDEPENDENT EVALUATION HARNESS</span>
            </div>
            <h1 className="text-2xl font-bold text-white tracking-tight">
              Empirical Benchmark & Real-World Generalisation
            </h1>
            <p className="text-xs text-gray-400 mt-1 max-w-2xl">
              Strict multi-repository evaluation verifying DocSentry on genuine open-source Git histories with anti-leakage train/validation/test partitioning.
            </p>
          </div>

          {/* Suite Selector Tabs */}
          <div className="flex items-center space-x-1.5 p-1 bg-brand-surface border border-brand-border rounded-lg text-xs font-mono">
            <button
              onClick={() => setActiveSuite("realworld")}
              className={`px-3 py-1.5 rounded-md transition-all ${
                activeSuite === "realworld"
                  ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-semibold"
                  : "text-gray-400 hover:text-gray-200"
              }`}
            >
              Real-World (32 Cases)
            </button>
            <button
              onClick={() => setActiveSuite("semantic")}
              className={`px-3 py-1.5 rounded-md transition-all ${
                activeSuite === "semantic"
                  ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-semibold"
                  : "text-gray-400 hover:text-gray-200"
              }`}
            >
              Semantic Suite (32 Cases)
            </button>
            <button
              onClick={() => setActiveSuite("constructed")}
              className={`px-3 py-1.5 rounded-md transition-all ${
                activeSuite === "constructed"
                  ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-semibold"
                  : "text-gray-400 hover:text-gray-200"
              }`}
            >
              Standard 50-Scenario
            </button>
          </div>
        </div>

        {/* Top Cards for Active Suite */}
        {activeSuite === "realworld" && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl bg-brand-surface border border-brand-border">
              <div className="text-[11px] font-mono text-gray-400 uppercase">Hybrid Pass Rate</div>
              <div className="text-2xl font-bold text-emerald-400 mt-1">78.1%</div>
              <div className="text-[11px] text-gray-500 mt-1">25 / 32 real-world cases passed</div>
            </div>
            <div className="p-4 rounded-xl bg-brand-surface border border-brand-border">
              <div className="text-[11px] font-mono text-gray-400 uppercase">Precision (PPV)</div>
              <div className="text-2xl font-bold text-white mt-1">100.0%</div>
              <div className="text-[11px] text-emerald-500 mt-1">0 false alarms across all 14 negative controls</div>
            </div>
            <div className="p-4 rounded-xl bg-brand-surface border border-brand-border">
              <div className="text-[11px] font-mono text-gray-400 uppercase">F1 Score</div>
              <div className="text-2xl font-bold text-emerald-400 mt-1">0.759</div>
              <div className="text-[11px] text-gray-500 mt-1">+0.045 gain over deterministic</div>
            </div>
            <div className="p-4 rounded-xl bg-brand-surface border border-brand-border">
              <div className="text-[11px] font-mono text-gray-400 uppercase">Evidence Hallucinations</div>
              <div className="text-2xl font-bold text-white mt-1">0.0%</div>
              <div className="text-[11px] text-emerald-500 mt-1">100% snapshot proof gate verified</div>
            </div>
          </div>
        )}

        {/* 3-Configuration Comparison Table */}
        <div className="p-5 rounded-xl bg-brand-surface border border-brand-border space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-sm font-semibold text-white">Three-Configuration Comparative Performance</h2>
              <p className="text-xs text-gray-400 mt-0.5">
                Deterministic static analysis vs pure Qwen3-8B semantic reasoning vs selective hybrid routing.
              </p>
            </div>
            <span className="text-[10px] font-mono text-gray-400 bg-brand-card px-2.5 py-1 rounded border border-brand-border">
              M4 MacBook • Ollama qwen3:8b
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-brand-card text-gray-400 font-mono uppercase text-[10px] border-b border-brand-border">
                <tr>
                  <th className="py-2.5 px-3">Metric</th>
                  <th className="py-2.5 px-3">Deterministic-Only</th>
                  <th className="py-2.5 px-3">Qwen3-8B-Only</th>
                  <th className="py-2.5 px-3 text-emerald-400">Selective Hybrid</th>
                  <th className="py-2.5 px-3">Architectural Advantage</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-brand-border/60 text-gray-300 font-mono">
                <tr>
                  <td className="py-2.5 px-3 text-white font-medium">Pass Rate</td>
                  <td className="py-2.5 px-3">24 / 32 (75.0%)</td>
                  <td className="py-2.5 px-3">22 / 32 (68.8%)</td>
                  <td className="py-2.5 px-3 text-emerald-400 font-bold">25 / 32 (78.1%)</td>
                  <td className="py-2.5 px-3 text-gray-400 font-sans">Hybrid outperforms both single modes</td>
                </tr>
                <tr>
                  <td className="py-2.5 px-3 text-white font-medium">Precision (PPV)</td>
                  <td className="py-2.5 px-3">100.0%</td>
                  <td className="py-2.5 px-3">100.0%</td>
                  <td className="py-2.5 px-3 text-emerald-400 font-bold">100.0%</td>
                  <td className="py-2.5 px-3 text-gray-400 font-sans">Zero false positives on non-drift PRs</td>
                </tr>
                <tr>
                  <td className="py-2.5 px-3 text-white font-medium">Recall (Sensitivity)</td>
                  <td className="py-2.5 px-3">55.6% (10/18)</td>
                  <td className="py-2.5 px-3">44.4% (8/18)</td>
                  <td className="py-2.5 px-3 text-emerald-400 font-bold">61.1% (11/18)</td>
                  <td className="py-2.5 px-3 text-gray-400 font-sans">+5.5% incremental recall gain via AI</td>
                </tr>
                <tr>
                  <td className="py-2.5 px-3 text-white font-medium">Specificity (TNR)</td>
                  <td className="py-2.5 px-3">100.0% (14/14)</td>
                  <td className="py-2.5 px-3">100.0% (14/14)</td>
                  <td className="py-2.5 px-3 text-emerald-400 font-bold">100.0% (14/14)</td>
                  <td className="py-2.5 px-3 text-gray-400 font-sans">Immune to false alarms on refactors</td>
                </tr>
                <tr>
                  <td className="py-2.5 px-3 text-white font-medium">F1 Score</td>
                  <td className="py-2.5 px-3">0.714</td>
                  <td className="py-2.5 px-3">0.615</td>
                  <td className="py-2.5 px-3 text-emerald-400 font-bold">0.759</td>
                  <td className="py-2.5 px-3 text-gray-400 font-sans">Optimal harmonic precision/recall balance</td>
                </tr>
                <tr>
                  <td className="py-2.5 px-3 text-white font-medium">Average Latency</td>
                  <td className="py-2.5 px-3 text-emerald-400 font-bold">227.2 ms</td>
                  <td className="py-2.5 px-3">6,091.2 ms</td>
                  <td className="py-2.5 px-3">1,758.8 ms</td>
                  <td className="py-2.5 px-3 text-gray-400 font-sans">Sub-2-second scan per PR in CI</td>
                </tr>
                <tr>
                  <td className="py-2.5 px-3 text-white font-medium">Model Calls</td>
                  <td className="py-2.5 px-3">0</td>
                  <td className="py-2.5 px-3">8</td>
                  <td className="py-2.5 px-3 text-emerald-400 font-bold">1 (Selective)</td>
                  <td className="py-2.5 px-3 text-gray-400 font-sans">87.5% reduction in model inference cost</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Confusion Matrices */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-brand-surface border border-brand-border space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-white font-mono">Deterministic Confusion Matrix</span>
              <span className="text-[10px] font-mono text-gray-400">Total: 32</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-center text-xs font-mono">
              <div className="p-2.5 rounded bg-brand-card border border-brand-border">
                <div className="text-[10px] text-gray-500 uppercase">True Positives</div>
                <div className="text-lg font-bold text-emerald-400 mt-0.5">10</div>
              </div>
              <div className="p-2.5 rounded bg-brand-card border border-brand-border">
                <div className="text-[10px] text-gray-500 uppercase">False Positives</div>
                <div className="text-lg font-bold text-gray-400 mt-0.5">0</div>
              </div>
              <div className="p-2.5 rounded bg-brand-card border border-brand-border">
                <div className="text-[10px] text-gray-500 uppercase">False Negatives</div>
                <div className="text-lg font-bold text-amber-400 mt-0.5">8</div>
              </div>
              <div className="p-2.5 rounded bg-brand-card border border-brand-border">
                <div className="text-[10px] text-gray-500 uppercase">True Negatives</div>
                <div className="text-lg font-bold text-emerald-400 mt-0.5">14</div>
              </div>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-brand-surface border border-brand-border space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-white font-mono">Qwen3-8B-Only Confusion Matrix</span>
              <span className="text-[10px] font-mono text-gray-400">Total: 32</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-center text-xs font-mono">
              <div className="p-2.5 rounded bg-brand-card border border-brand-border">
                <div className="text-[10px] text-gray-500 uppercase">True Positives</div>
                <div className="text-lg font-bold text-emerald-400 mt-0.5">8</div>
              </div>
              <div className="p-2.5 rounded bg-brand-card border border-brand-border">
                <div className="text-[10px] text-gray-500 uppercase">False Positives</div>
                <div className="text-lg font-bold text-gray-400 mt-0.5">0</div>
              </div>
              <div className="p-2.5 rounded bg-brand-card border border-brand-border">
                <div className="text-[10px] text-gray-500 uppercase">False Negatives</div>
                <div className="text-lg font-bold text-amber-400 mt-0.5">10</div>
              </div>
              <div className="p-2.5 rounded bg-brand-card border border-brand-border">
                <div className="text-[10px] text-gray-500 uppercase">True Negatives</div>
                <div className="text-lg font-bold text-emerald-400 mt-0.5">14</div>
              </div>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-brand-surface border border-emerald-500/30 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-emerald-300 font-mono">Selective Hybrid Matrix</span>
              <span className="text-[10px] font-mono text-emerald-400">Total: 32</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-center text-xs font-mono">
              <div className="p-2.5 rounded bg-brand-card border border-brand-border">
                <div className="text-[10px] text-gray-500 uppercase">True Positives</div>
                <div className="text-lg font-bold text-emerald-400 mt-0.5">11</div>
              </div>
              <div className="p-2.5 rounded bg-brand-card border border-brand-border">
                <div className="text-[10px] text-gray-500 uppercase">False Positives</div>
                <div className="text-lg font-bold text-gray-400 mt-0.5">0</div>
              </div>
              <div className="p-2.5 rounded bg-brand-card border border-brand-border">
                <div className="text-[10px] text-gray-500 uppercase">False Negatives</div>
                <div className="text-lg font-bold text-amber-400 mt-0.5">7</div>
              </div>
              <div className="p-2.5 rounded bg-brand-card border border-brand-border">
                <div className="text-[10px] text-gray-500 uppercase">True Negatives</div>
                <div className="text-lg font-bold text-emerald-400 mt-0.5">14</div>
              </div>
            </div>
          </div>
        </div>

        {/* Per-Repository Breakdown with Splits */}
        <div className="p-5 rounded-xl bg-brand-surface border border-brand-border space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-sm font-semibold text-white">Per-Repository Breakdown & Anti-Leakage Partitioning</h2>
              <p className="text-xs text-gray-400 mt-0.5">
                Evaluation partitioned by repository. The Held-Out Test split was strictly isolated with zero prompt or rule engineering.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 rounded-lg bg-brand-card border border-brand-border space-y-3">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="font-semibold text-white">DEVELOPMENT (DEV)</span>
                <span className="text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                  100% Pass
                </span>
              </div>
              <div className="text-xs text-gray-400 space-y-1.5 font-mono">
                <div className="flex justify-between">
                  <span>encode/httpx (Python)</span>
                  <span className="text-white">6 / 6 (100%)</span>
                </div>
                <div className="flex justify-between">
                  <span>pallets/click (Python)</span>
                  <span className="text-white">5 / 5 (100%)</span>
                </div>
              </div>
              <div className="text-[10px] text-gray-500 font-sans">
                Permitted for initial rule heuristics and prompt engineering.
              </div>
            </div>

            <div className="p-4 rounded-lg bg-brand-card border border-brand-border space-y-3">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="font-semibold text-white">VALIDATION (VAL)</span>
                <span className="text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                  77.8% Pass
                </span>
              </div>
              <div className="text-xs text-gray-400 space-y-1.5 font-mono">
                <div className="flex justify-between">
                  <span>fastapi/fastapi (Python)</span>
                  <span className="text-white">4 / 5 (80%)</span>
                </div>
                <div className="flex justify-between">
                  <span>psf/requests (Python)</span>
                  <span className="text-white">3 / 4 (75%)</span>
                </div>
              </div>
              <div className="text-[10px] text-gray-500 font-sans">
                Used strictly for router confidence threshold calibration.
              </div>
            </div>

            <div className="p-4 rounded-lg bg-brand-card border border-brand-border space-y-3">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="font-semibold text-white">HELD-OUT TEST (TEST)</span>
                <span className="text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                  58.3% Pass
                </span>
              </div>
              <div className="text-xs text-gray-400 space-y-1.5 font-mono">
                <div className="flex justify-between">
                  <span>pydantic/pydantic (Python)</span>
                  <span className="text-white">3 / 5 (60%)</span>
                </div>
                <div className="flex justify-between">
                  <span>pallets/flask (Python)</span>
                  <span className="text-white">3 / 5 (60%)</span>
                </div>
                <div className="flex justify-between">
                  <span>axios/axios (JavaScript)</span>
                  <span className="text-white">1 / 2 (50%)</span>
                </div>
              </div>
              <div className="text-[10px] text-emerald-400 font-sans">
                Blind real-world test. Zero false positives observed.
              </div>
            </div>
          </div>
        </div>

        {/* AI Unique Real-World Detection Spotlight */}
        <div className="p-5 rounded-xl bg-brand-surface border border-emerald-500/30 space-y-3">
          <div className="flex items-center space-x-2 text-xs font-mono text-emerald-400">
            <Zap className="w-4 h-4 text-emerald-400" />
            <span className="font-semibold">AI REAL-WORLD VALUE SPOTLIGHT — CASE REAL-HTTPX-03</span>
          </div>
          <p className="text-xs text-gray-300">
            In <span className="text-white font-mono">encode/httpx PR #891</span>, engineering added <code className="text-emerald-400">**kwargs</code> forwarding to <code className="text-emerald-400">Response.json()</code>. Deterministic static analysis produces 0 findings because adding kwargs is a non-breaking AST addition.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
            <div className="p-3 rounded bg-brand-card border border-brand-border">
              <div className="text-gray-500 text-[10px] uppercase">Outdated Documentation (docs/quickstart.md)</div>
              <div className="text-red-400 mt-1 line-through">
                "response.json() parses payload strictly with default JSONDecoder settings."
              </div>
            </div>
            <div className="p-3 rounded bg-brand-card border border-brand-border">
              <div className="text-gray-500 text-[10px] uppercase">Qwen3-8B Semantic Reasoning Assessment</div>
              <div className="text-emerald-300 mt-1">
                "DRIFT: Method now forwards arbitrary **kwargs to json.loads, directly contradicting documented strict default settings."
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
