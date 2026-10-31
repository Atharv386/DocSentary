import React, { useState } from "react";
import { LandingPage } from "./components/LandingPage";
import { Sidebar } from "./components/Sidebar";
import { PRAnalysisView } from "./components/PRAnalysisView";
import { BenchmarkView } from "./components/BenchmarkView";
import { ExternalLink } from "lucide-react";

export const App: React.FC = () => {
  const [viewMode, setViewMode] = useState<"landing" | "app">("app");
  const [currentTab, setCurrentTab] = useState<string>("pr");

  if (viewMode === "landing") {
    return <LandingPage onEnterApp={() => setViewMode("app")} />;
  }

  return (
    <div className="flex h-screen bg-brand-dark text-gray-100 font-sans overflow-hidden">
      {/* Persistent Left Sidebar */}
      <Sidebar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        onOpenLanding={() => setViewMode("landing")}
      />

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Top App Bar */}
        <header className="h-14 border-b border-brand-border bg-brand-surface/60 backdrop-blur px-6 flex items-center justify-between flex-shrink-0">
          <div className="flex items-center space-x-3 text-xs font-mono text-gray-400">
            <span className="text-gray-200 font-medium">DocSentry</span>
            <span>/</span>
            <span className="text-emerald-400 font-semibold uppercase">{currentTab}</span>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={() => setViewMode("landing")}
              className="text-xs text-gray-400 hover:text-white transition-colors font-mono"
            >
              Marketing Website
            </button>
            <a
              href="https://github.com/Atharv386/DocSentary"
              target="_blank"
              rel="noreferrer"
              className="px-2.5 py-1 rounded bg-brand-card hover:bg-brand-border text-xs font-mono text-gray-300 border border-brand-border transition-colors flex items-center space-x-1"
            >
              <span>GitHub</span>
              <ExternalLink className="w-3 h-3 text-gray-400" />
            </a>
          </div>
        </header>

        {/* Tab Views */}
        {currentTab === "pr" && <PRAnalysisView />}
        {currentTab === "evaluations" && <BenchmarkView />}

        {currentTab === "findings" && (
          <div className="flex-1 p-8 bg-brand-dark overflow-y-auto">
            <div className="max-w-4xl space-y-4">
              <h2 className="text-lg font-bold text-white">Repository Findings</h2>
              <p className="text-sm text-gray-400">
                All confirmed and potential documentation drift across active branches and PRs.
              </p>
              <div className="pt-4">
                <PRAnalysisView />
              </div>
            </div>
          </div>
        )}

        {currentTab === "repos" && (
          <div className="flex-1 p-8 bg-brand-dark overflow-y-auto">
            <div className="max-w-3xl space-y-4">
              <h2 className="text-lg font-bold text-white">Connected Repositories</h2>
              <div className="p-4 rounded-xl bg-brand-surface border border-brand-border flex items-center justify-between">
                <div>
                  <div className="font-semibold text-white">Atharv386/DocSentary</div>
                  <div className="text-xs text-gray-400 font-mono mt-0.5">Default branch: main • GitHub Actions active</div>
                </div>
                <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                  Connected
                </span>
              </div>
            </div>
          </div>
        )}

        {currentTab === "history" && (
          <div className="flex-1 p-8 bg-brand-dark overflow-y-auto">
            <div className="max-w-3xl space-y-4">
              <h2 className="text-lg font-bold text-white">Scan History</h2>
              <div className="space-y-2">
                <div className="p-3 rounded-lg bg-brand-surface border border-brand-border flex items-center justify-between text-xs font-mono">
                  <div>
                    <span className="text-emerald-400">scan-2026-10-31-001</span>
                    <span className="text-gray-400 ml-2">• PR #42 (timeout=60)</span>
                  </div>
                  <span className="text-red-400">1 Drift</span>
                </div>
                <div className="p-3 rounded-lg bg-brand-surface border border-brand-border flex items-center justify-between text-xs font-mono">
                  <div>
                    <span className="text-emerald-400">scan-2026-10-31-002</span>
                    <span className="text-gray-400 ml-2">• PR #89 (username ➔ email)</span>
                  </div>
                  <span className="text-red-400">1 Drift</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {currentTab === "settings" && (
          <div className="flex-1 p-8 bg-brand-dark overflow-y-auto">
            <div className="max-w-3xl space-y-6">
              <h2 className="text-lg font-bold text-white">Configuration & Preferences</h2>
              <div className="p-5 rounded-xl bg-brand-surface border border-brand-border space-y-4">
                <div className="space-y-1">
                  <h3 className="text-sm font-semibold text-white">Model Configuration</h3>
                  <p className="text-xs text-gray-400">
                    DocSentry uses deterministic rules first and queries open-weight model endpoints for ambiguous semantic behavior.
                  </p>
                </div>
                <div className="grid grid-cols-2 gap-3 text-xs font-mono">
                  <div className="p-3 rounded bg-brand-card border border-brand-border">
                    <div className="text-gray-500">Provider</div>
                    <div className="text-emerald-400 mt-1">organizer_server</div>
                  </div>
                  <div className="p-3 rounded bg-brand-card border border-brand-border">
                    <div className="text-gray-500">Timeout</div>
                    <div className="text-gray-200 mt-1">30 seconds</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};
export default App;
