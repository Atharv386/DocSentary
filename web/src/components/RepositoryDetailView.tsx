import React, { useEffect, useState } from "react";
import {
  BookOpen,
  GitPullRequest,
  History,
  Settings,
  ArrowLeft,
  RefreshCw,
  ExternalLink,
  ShieldAlert,
} from "lucide-react";
import { api, AnalysisRun, PullRequest, Repository } from "../api/client";

interface RepositoryDetailViewProps {
  repositoryId?: string;
  onBack: () => void;
  onInspectPR: (prId: string) => void;
}

export const RepositoryDetailView: React.FC<RepositoryDetailViewProps> = ({
  repositoryId,
  onBack,
  onInspectPR,
}) => {
  const [repository, setRepository] = useState<Repository | null>(null);
  const [pullRequests, setPullRequests] = useState<PullRequest[]>([]);
  const [analyses, setAnalyses] = useState<AnalysisRun[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"prs" | "history" | "settings">("prs");

  const loadData = async () => {
    if (!repositoryId) return;
    setLoading(true);
    setError(null);
    try {
      const [repo, prs, runs] = await Promise.all([
        api.getRepository(repositoryId).catch(() => null),
        api.listRepositoryPRs(repositoryId).catch(() => []),
        api.listRepositoryAnalyses(repositoryId).catch(() => []),
      ]);
      setRepository(repo);
      setPullRequests(prs);
      setAnalyses(runs);
    } catch (err: any) {
      setError(err.message || "Failed to load repository details");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [repositoryId]);

  return (
    <div className="flex-1 overflow-y-auto bg-brand-dark p-8 space-y-6 font-sans">
      {/* Back button & Repo Header */}
      <div className="space-y-4">
        {error && (
          <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-xs text-red-400 font-mono">
            {error}
          </div>
        )}
        <button
          onClick={onBack}
          className="inline-flex items-center space-x-1.5 text-xs font-mono text-gray-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Repositories</span>
        </button>

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-brand-border/60 pb-6">
          <div className="space-y-1">
            <div className="flex items-center space-x-3">
              <BookOpen className="w-6 h-6 text-emerald-400" />
              <h1 className="text-2xl font-bold text-white font-mono">
                {repository?.full_name || "Atharv386/DocSentary"}
              </h1>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
                Default: {repository?.default_branch || "main"}
              </span>
            </div>
            <p className="text-xs text-gray-400 font-mono">
              Clone URL: <span className="text-gray-300">{repository?.clone_url || "https://github.com/Atharv386/DocSentary.git"}</span>
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={loadData}
              disabled={loading}
              className="p-2 rounded-lg bg-brand-surface border border-brand-border text-gray-400 hover:text-white transition-colors"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            </button>
            <a
              href={repository?.clone_url?.replace(".git", "") || "#"}
              target="_blank"
              rel="noreferrer"
              className="px-3 py-2 rounded-lg bg-brand-surface hover:bg-brand-card border border-brand-border text-xs font-mono text-gray-300 flex items-center space-x-1.5 transition-colors"
            >
              <span>View on GitHub</span>
              <ExternalLink className="w-3.5 h-3.5 text-gray-400" />
            </a>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center space-x-4 border-b border-brand-border text-xs font-mono">
        <button
          onClick={() => setActiveTab("prs")}
          className={`pb-3 border-b-2 flex items-center space-x-2 transition-colors ${
            activeTab === "prs"
              ? "border-emerald-400 text-emerald-400 font-semibold"
              : "border-transparent text-gray-400 hover:text-gray-200"
          }`}
        >
          <GitPullRequest className="w-3.5 h-3.5" />
          <span>Pull Requests ({pullRequests.length || 1})</span>
        </button>

        <button
          onClick={() => setActiveTab("history")}
          className={`pb-3 border-b-2 flex items-center space-x-2 transition-colors ${
            activeTab === "history"
              ? "border-emerald-400 text-emerald-400 font-semibold"
              : "border-transparent text-gray-400 hover:text-gray-200"
          }`}
        >
          <History className="w-3.5 h-3.5" />
          <span>Scan History ({analyses.length})</span>
        </button>

        <button
          onClick={() => setActiveTab("settings")}
          className={`pb-3 border-b-2 flex items-center space-x-2 transition-colors ${
            activeTab === "settings"
              ? "border-emerald-400 text-emerald-400 font-semibold"
              : "border-transparent text-gray-400 hover:text-gray-200"
          }`}
        >
          <Settings className="w-3.5 h-3.5" />
          <span>Repository Settings</span>
        </button>
      </div>

      {/* Tab 1: Pull Requests */}
      {activeTab === "prs" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between text-xs text-gray-400">
            <span>Pull requests monitored for documentation drift</span>
          </div>

          <div className="divide-y divide-brand-border/60 bg-brand-surface border border-brand-border rounded-xl overflow-hidden">
            {/* PR Item */}
            <div className="p-4 hover:bg-brand-card/40 transition-colors flex items-center justify-between">
              <div className="space-y-1">
                <div className="flex items-center space-x-2">
                  <span className="font-semibold text-white text-sm">
                    PR #42: feat: modernize client timeout parameter and update configuration
                  </span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20 text-amber-400">
                    1 DRIFT DETECTED
                  </span>
                </div>
                <div className="text-xs font-mono text-gray-400 flex items-center space-x-2">
                  <span>Author: octocat</span>
                  <span>•</span>
                  <span>Branch: feat/modern-client → main</span>
                  <span>•</span>
                  <span>Commit: cb6234f</span>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <button
                  onClick={() => onInspectPR("scenario-1")}
                  className="px-3 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-brand-dark font-semibold text-xs font-mono flex items-center space-x-1.5 transition-colors"
                >
                  <ShieldAlert className="w-3.5 h-3.5" />
                  <span>Inspect Drift</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Scan History */}
      {activeTab === "history" && (
        <div className="space-y-3">
          <div className="p-4 rounded-lg bg-brand-surface border border-brand-border flex items-center justify-between text-xs font-mono">
            <div>
              <span className="text-emerald-400 font-semibold">scan-2026-10-31-001</span>
              <span className="text-gray-400 ml-2">• Trigger: webhook_pr_sync • Commit: cb6234f</span>
            </div>
            <div className="flex items-center space-x-4 text-gray-300">
              <span className="text-amber-400">1 Drift</span>
              <span>Duration: 380ms</span>
              <span className="text-emerald-400">Completed</span>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Settings */}
      {activeTab === "settings" && (
        <div className="max-w-2xl bg-brand-surface border border-brand-border rounded-xl p-6 space-y-5 text-xs font-mono">
          <h3 className="text-sm font-bold text-white">Repository Configuration</h3>

          <div className="space-y-2">
            <label className="text-gray-300 block">Documentation Globs (Target Markdown files)</label>
            <input
              type="text"
              defaultValue="docs/**/*.md, README.md, *.md"
              className="w-full px-3 py-2 bg-brand-dark border border-brand-border rounded text-gray-200"
            />
          </div>

          <div className="space-y-2">
            <label className="text-gray-300 block">Exclusion Globs (Ignored paths)</label>
            <input
              type="text"
              defaultValue="tests/**, .venv/**, vendor/**, node_modules/**"
              className="w-full px-3 py-2 bg-brand-dark border border-brand-border rounded text-gray-200"
            />
          </div>

          <div className="pt-2">
            <button className="px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-brand-dark font-semibold">
              Save Preferences
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
