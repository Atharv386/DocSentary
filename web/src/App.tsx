import React, { useState } from "react";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { LandingPage } from "./components/LandingPage";
import { Sidebar } from "./components/Sidebar";
import { DashboardView } from "./components/DashboardView";
import { PRAnalysisView } from "./components/PRAnalysisView";
import { RepositoryDetailView } from "./components/RepositoryDetailView";
import { AnalysisHistoryView } from "./components/AnalysisHistoryView";
import { BenchmarkView } from "./components/BenchmarkView";
import { SettingsView } from "./components/SettingsView";
import { AuthModal } from "./components/AuthModal";
import { ExternalLink, User } from "lucide-react";

const MainApp: React.FC = () => {
  const [viewMode, setViewMode] = useState<"landing" | "app">("app");
  const [currentTab, setCurrentTab] = useState<string>("dashboard");
  const [selectedRepoId, setSelectedRepoId] = useState<string | undefined>(undefined);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState<boolean>(false);
  const { user } = useAuth();

  const handleNavigateTab = (tab: string, contextId?: string) => {
    setCurrentTab(tab);
    if (contextId) {
      setSelectedRepoId(contextId);
    }
  };

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
        onOpenAuth={() => setIsAuthModalOpen(true)}
      />

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Top App Bar */}
        <header className="h-14 border-b border-brand-border bg-brand-surface/60 backdrop-blur px-6 flex items-center justify-between flex-shrink-0">
          <div className="flex items-center space-x-3 text-xs font-mono text-gray-400">
            <span className="text-gray-200 font-medium">DocSentry</span>
            <span>/</span>
            <span className="text-emerald-400 font-semibold uppercase">{currentTab}</span>
            {user?.organization && (
              <>
                <span>/</span>
                <span className="text-gray-400">{user.organization.name}</span>
              </>
            )}
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={() => setViewMode("landing")}
              className="text-xs text-gray-400 hover:text-white transition-colors font-mono"
            >
              Marketing Website
            </button>

            <button
              onClick={() => setIsAuthModalOpen(true)}
              className="px-2.5 py-1 rounded bg-brand-card hover:bg-brand-border text-xs font-mono text-gray-300 border border-brand-border transition-colors flex items-center space-x-1.5"
            >
              <User className="w-3 h-3 text-emerald-400" />
              <span>{user ? user.username : "Sign In"}</span>
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
        {currentTab === "dashboard" && <DashboardView onNavigateTab={handleNavigateTab} />}
        {currentTab === "pr" && <PRAnalysisView />}
        {currentTab === "repos" && (
          <RepositoryDetailView
            repositoryId={selectedRepoId}
            onBack={() => setCurrentTab("dashboard")}
            onInspectPR={() => setCurrentTab("pr")}
          />
        )}
        {currentTab === "history" && <AnalysisHistoryView />}
        {currentTab === "evaluations" && <BenchmarkView />}
        {currentTab === "settings" && <SettingsView />}
      </main>

      {/* Auth Modal */}
      <AuthModal isOpen={isAuthModalOpen} onClose={() => setIsAuthModalOpen(false)} />
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  );
};
