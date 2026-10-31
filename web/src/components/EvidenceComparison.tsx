import React from "react";
import { Finding } from "../data/mockScenarios";
import { FileText, Code2, ArrowRight, ShieldCheck } from "lucide-react";

interface EvidenceComparisonProps {
  finding: Finding;
}

export const EvidenceComparison: React.FC<EvidenceComparisonProps> = ({ finding }) => {
  const codeEvidence = finding.evidence.find((e) => e.role === "code");
  const docEvidence = finding.evidence.find((e) => e.role === "documentation");

  return (
    <div className="space-y-4">
      {/* Side-by-Side Comparison Container */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Left: Documentation Evidence */}
        <div className="bg-brand-dark/80 border border-brand-border rounded-lg overflow-hidden flex flex-col">
          <div className="px-4 py-2.5 bg-brand-surface border-b border-brand-border flex items-center justify-between text-xs">
            <div className="flex items-center space-x-2 text-gray-300 font-mono">
              <FileText className="w-3.5 h-3.5 text-amber-400" />
              <span>{docEvidence?.path || "Documentation"}</span>
            </div>
            {docEvidence && (
              <span className="font-mono text-gray-400 text-[11px] bg-brand-card px-2 py-0.5 rounded border border-brand-border">
                Lines {docEvidence.line_start}–{docEvidence.line_end}
              </span>
            )}
          </div>
          <div className="p-4 flex-1 flex flex-col justify-between">
            <div className="space-y-2">
              <div className="text-[11px] font-mono uppercase tracking-wider text-amber-400/90 font-medium">
                [Outdated Documentation Statement]
              </div>
              <div className="p-3 bg-amber-500/5 border border-amber-500/20 rounded-md text-sm text-gray-200 leading-relaxed font-sans">
                <span className="text-amber-200 font-medium">
                  "{docEvidence?.quote}"
                </span>
              </div>
            </div>
            <div className="mt-3 pt-3 border-t border-brand-border/40 text-[11px] text-gray-400 font-mono flex items-center justify-between">
              <span>Source: Markdown AST span</span>
              <span className="text-amber-400">Contradicts Head Code</span>
            </div>
          </div>
        </div>

        {/* Right: Code Evidence */}
        <div className="bg-brand-dark/80 border border-brand-border rounded-lg overflow-hidden flex flex-col">
          <div className="px-4 py-2.5 bg-brand-surface border-b border-brand-border flex items-center justify-between text-xs">
            <div className="flex items-center space-x-2 text-gray-300 font-mono">
              <Code2 className="w-3.5 h-3.5 text-emerald-400" />
              <span>{codeEvidence?.path || "Source Code"}</span>
            </div>
            {codeEvidence && (
              <span className="font-mono text-gray-400 text-[11px] bg-brand-card px-2 py-0.5 rounded border border-brand-border">
                Line {codeEvidence.line_start}
              </span>
            )}
          </div>
          <div className="p-4 flex-1 flex flex-col justify-between">
            <div className="space-y-2">
              <div className="text-[11px] font-mono uppercase tracking-wider text-emerald-400/90 font-medium">
                [Actual Code Evidence in HEAD]
              </div>
              <div className="p-3 bg-emerald-500/5 border border-emerald-500/20 rounded-md text-sm font-mono text-emerald-300">
                <code>{codeEvidence?.quote}</code>
              </div>
            </div>
            <div className="mt-3 pt-3 border-t border-brand-border/40 text-[11px] text-gray-400 font-mono flex items-center justify-between">
              <span>Source: Python AST snapshot</span>
              <span className="text-emerald-400">Verified Commit State</span>
            </div>
          </div>
        </div>
      </div>

      {/* Analysis Metadata Footer */}
      <div className="p-4 bg-brand-surface border border-brand-border rounded-lg space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-brand-border/60">
          <div className="flex items-center space-x-3 text-xs">
            <span className="text-gray-400">Detection Method:</span>
            <span className="font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
              {finding.verification}
            </span>
            <span className="text-gray-400">Rule:</span>
            <span className="font-mono text-gray-200 bg-brand-card px-2 py-0.5 rounded border border-brand-border">
              {finding.rule_id}
            </span>
          </div>
          <div className="flex items-center space-x-1.5 text-xs text-emerald-400 font-mono">
            <ShieldCheck className="w-4 h-4" />
            <span>Zero-Hallucination Verified</span>
          </div>
        </div>

        <div>
          <div className="text-xs font-semibold text-gray-300 mb-1">Why DocGuard Flagged This</div>
          <p className="text-sm text-gray-300 leading-relaxed">{finding.explanation}</p>
        </div>

        {finding.suggested_action && (
          <div className="pt-2 flex items-start space-x-2 text-xs text-emerald-300 bg-emerald-500/5 p-2.5 rounded border border-emerald-500/15">
            <ArrowRight className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
            <div>
              <span className="font-semibold text-emerald-400">Recommended Action: </span>
              <span>{finding.suggested_action}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
