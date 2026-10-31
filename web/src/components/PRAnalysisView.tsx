import React, { useState } from "react";
import { SCENARIOS } from "../data/mockScenarios";
import { EvidenceComparison } from "./EvidenceComparison";
import {
  GitPullRequest,
  CheckCircle2,
  FileCode,
  Clock,
  ChevronDown,
  ChevronUp,
  Download,
  Search,
  AlertCircle
} from "lucide-react";

export const PRAnalysisView: React.FC = () => {
  const [selectedScenarioId, setSelectedScenarioId] = useState<string>("stale-default");
  const [expandedFindingId, setExpandedFindingId] = useState<string | null>("DG-0001");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [showJsonModal, setShowJsonModal] = useState<boolean>(false);

  const scenario = SCENARIOS.find((s) => s.id === selectedScenarioId) || SCENARIOS[0];
  const report = scenario.report;

  const filteredFindings = report.findings.filter((f) => {
    if (statusFilter !== "all" && f.status !== statusFilter) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      const matchTitle = f.title.toLowerCase().includes(q);
      const matchRule = f.rule_id.toLowerCase().includes(q);
      const matchExpl = f.explanation.toLowerCase().includes(q);
      return matchTitle || matchRule || matchExpl;
    }
    return true;
  });

  const driftCount = report.summary.drift || 0;
  const potentialCount = report.summary.potential_drift || 0;

  return (
    <div className="flex-1 overflow-y-auto bg-brand-dark p-6 space-y-6">
      {/* Top Scenario Selector */}
      <div className="bg-brand-surface border border-brand-border rounded-xl p-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-3">
          <div>
            <span className="text-xs font-mono uppercase tracking-wider text-emerald-400 font-semibold">
              Live Evaluation Scenarios
            </span>
            <h2 className="text-base font-semibold text-white">Select a Pull Request to Inspect</h2>
          </div>
          <button
            onClick={() => setShowJsonModal(true)}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-md bg-brand-card hover:bg-brand-border text-xs font-mono text-gray-300 border border-brand-border transition-colors self-start md:self-auto"
          >
            <Download className="w-3.5 h-3.5 text-gray-400" />
            <span>Inspect report.json</span>
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
          {SCENARIOS.map((s) => {
            const isSelected = s.id === selectedScenarioId;
            const hasDrift = s.report.summary.drift > 0;
            return (
              <button
                key={s.id}
                onClick={() => {
                  setSelectedScenarioId(s.id);
                  setExpandedFindingId(s.report.findings[0]?.finding_id || null);
                }}
                className={`p-3 text-left rounded-lg border transition-all ${
                  isSelected
                    ? "bg-brand-card border-emerald-500/50 shadow-sm"
                    : "bg-brand-dark/50 border-brand-border hover:bg-brand-card/50"
                }`}
              >
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="font-mono text-gray-400">PR #{s.prNumber}</span>
                  <span
                    className={`text-[10px] font-mono px-1.5 py-0.2 rounded ${
                      hasDrift
                        ? "bg-red-500/20 text-red-400 border border-red-500/30"
                        : "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                    }`}
                  >
                    {hasDrift ? "DRIFT DETECTED" : "NO DRIFT"}
                  </span>
                </div>
                <div className="text-xs font-medium text-gray-200 truncate">{s.prTitle}</div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Pull Request Header Banner */}
      <div className="bg-brand-surface border border-brand-border rounded-xl p-5 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2.5">
              <span className="flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <GitPullRequest className="w-3.5 h-3.5" />
                <span>PR #{scenario.prNumber}</span>
              </span>
              <h1 className="text-lg font-bold text-white tracking-tight">{scenario.prTitle}</h1>
            </div>
            <div className="flex flex-wrap items-center gap-3 text-xs text-gray-400 font-mono">
              <span>Author: <strong className="text-gray-300 font-normal">@{scenario.author}</strong></span>
              <span>•</span>
              <span>Branch: <span className="text-emerald-400">{scenario.branch}</span> ➔ {scenario.targetBranch}</span>
              <span>•</span>
              <span>Base: <code className="text-gray-300">{report.base_sha.slice(0, 7)}</code></span>
              <span>•</span>
              <span>Head: <code className="text-cyan-300">{report.head_sha.slice(0, 7)}</code></span>
            </div>
          </div>

          <div className="flex items-center space-x-2 self-start md:self-auto">
            <span className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-mono bg-brand-card border border-brand-border text-gray-300">
              <Clock className="w-3.5 h-3.5 text-gray-400" />
              <span>{report.duration_ms} ms</span>
            </span>
            <span
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold ${
                driftCount > 0
                  ? "bg-red-500/10 text-red-400 border border-red-500/30"
                  : "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30"
              }`}
            >
              {driftCount > 0 ? (
                <>
                  <AlertCircle className="w-4 h-4" />
                  <span>Drift Detected</span>
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Docs In Sync</span>
                </>
              )}
            </span>
          </div>
        </div>

        {/* Summary Metric Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-3 border-t border-brand-border/60">
          <div className="bg-brand-card/60 p-3 rounded-lg border border-brand-border">
            <div className="text-[11px] font-mono uppercase text-gray-400">Confirmed Drift</div>
            <div className={`text-2xl font-bold font-mono mt-0.5 ${driftCount > 0 ? "text-red-400" : "text-gray-200"}`}>
              {driftCount}
            </div>
          </div>
          <div className="bg-brand-card/60 p-3 rounded-lg border border-brand-border">
            <div className="text-[11px] font-mono uppercase text-gray-400">Potential Drift</div>
            <div className="text-2xl font-bold font-mono mt-0.5 text-amber-400">
              {potentialCount}
            </div>
          </div>
          <div className="bg-brand-card/60 p-3 rounded-lg border border-brand-border">
            <div className="text-[11px] font-mono uppercase text-gray-400">Files Changed</div>
            <div className="text-2xl font-bold font-mono mt-0.5 text-gray-200">
              {report.summary.changed_files}
            </div>
          </div>
          <div className="bg-brand-card/60 p-3 rounded-lg border border-brand-border">
            <div className="text-[11px] font-mono uppercase text-gray-400">Docs Inspected</div>
            <div className="text-2xl font-bold font-mono mt-0.5 text-emerald-400">
              {report.summary.doc_spans || 12}
            </div>
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex items-center space-x-2 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-64">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-gray-500" />
            <input
              type="text"
              placeholder="Search findings or rule ID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs bg-brand-surface border border-brand-border rounded-lg text-gray-200 placeholder-gray-500 focus:outline-none focus:border-emerald-500/50"
            />
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-1.5 text-xs bg-brand-surface border border-brand-border rounded-lg text-gray-300 focus:outline-none focus:border-emerald-500/50"
          >
            <option value="all">All Statuses</option>
            <option value="DRIFT">Confirmed Drift</option>
            <option value="POTENTIAL_DRIFT">Potential Drift</option>
            <option value="UNCERTAIN">Uncertain</option>
          </select>
        </div>

        <div className="text-xs text-gray-500 font-mono self-end sm:self-auto">
          Showing {filteredFindings.length} of {report.findings.length} findings
        </div>
      </div>

      {/* Findings List */}
      <div className="space-y-4">
        {filteredFindings.length === 0 ? (
          <div className="bg-brand-surface border border-brand-border rounded-xl p-8 text-center space-y-2">
            <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
            <h3 className="text-sm font-semibold text-white">No Documentation Drift Detected</h3>
            <p className="text-xs text-gray-400 max-w-md mx-auto">
              All modified symbols, parameters, and defaults in this pull request remain consistent with existing documentation.
            </p>
          </div>
        ) : (
          filteredFindings.map((finding) => {
            const isExpanded = expandedFindingId === finding.finding_id;
            return (
              <div
                key={finding.finding_id}
                className="bg-brand-surface border border-brand-border rounded-xl overflow-hidden transition-all shadow-sm"
              >
                {/* Finding Header */}
                <div
                  onClick={() => setExpandedFindingId(isExpanded ? null : finding.finding_id)}
                  className="p-4 flex items-center justify-between cursor-pointer hover:bg-brand-card/40 transition-colors"
                >
                  <div className="flex items-center space-x-3">
                    <span
                      className={`text-xs font-mono font-bold px-2 py-0.5 rounded border ${
                        finding.status === "DRIFT"
                          ? "bg-red-500/10 text-red-400 border-red-500/30"
                          : "bg-amber-500/10 text-amber-400 border-amber-500/30"
                      }`}
                    >
                      {finding.status}
                    </span>
                    <div>
                      <h3 className="text-sm font-semibold text-gray-100">{finding.title}</h3>
                      <div className="flex items-center space-x-2 text-[11px] font-mono text-gray-400 mt-0.5">
                        <span className="text-gray-300">{finding.rule_id}</span>
                        <span>•</span>
                        <span>{finding.category}</span>
                        <span>•</span>
                        <span>Severity: <strong className="text-gray-200">{finding.severity}</strong></span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3">
                    <span className="text-xs font-mono text-gray-500 hidden sm:inline">
                      {finding.evidence.length} evidence refs
                    </span>
                    {isExpanded ? (
                      <ChevronUp className="w-4 h-4 text-gray-400" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-gray-400" />
                    )}
                  </div>
                </div>

                {/* Expanded Detail with Side-by-Side Comparison */}
                {isExpanded && (
                  <div className="p-4 pt-0 border-t border-brand-border/40">
                    <EvidenceComparison finding={finding} />
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Raw JSON Modal */}
      {showJsonModal && (
        <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4">
          <div className="bg-brand-surface border border-brand-border rounded-xl max-w-3xl w-full max-h-[85vh] flex flex-col overflow-hidden">
            <div className="p-4 border-b border-brand-border flex items-center justify-between">
              <div className="flex items-center space-x-2 font-mono text-sm text-gray-200">
                <FileCode className="w-4 h-4 text-emerald-400" />
                <span>ScanReport Artifact: {report.scan_id}.json</span>
              </div>
              <button
                onClick={() => setShowJsonModal(false)}
                className="text-gray-400 hover:text-white text-xs font-mono"
              >
                Close [ESC]
              </button>
            </div>
            <pre className="p-4 overflow-y-auto text-xs font-mono text-gray-300 bg-brand-dark/90 leading-relaxed flex-1">
              {JSON.stringify(report, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};
