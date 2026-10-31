import React from "react";
import {
  ShieldAlert,
  LayoutDashboard,
  GitPullRequest,
  BookOpen,
  History,
  Settings,
  Layers,
  Activity,
  User as UserIcon,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";

interface SidebarProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
  onOpenLanding: () => void;
  onOpenAuth: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentTab,
  setCurrentTab,
  onOpenLanding,
  onOpenAuth,
}) => {
  const { user } = useAuth();

  const navItems = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "pr", label: "PR Analysis", icon: GitPullRequest, badge: "Live" },
    { id: "repos", label: "Repositories", icon: BookOpen },
    { id: "history", label: "Scan History", icon: History },
    { id: "evaluations", label: "Evaluations", icon: Activity, badge: "78.1%" },
    { id: "settings", label: "Settings & GitHub", icon: Settings },
  ];

  return (
    <aside className="w-64 border-r border-brand-border bg-brand-surface flex flex-col justify-between h-screen select-none font-sans">
      <div>
        {/* Brand */}
        <div className="p-5 border-b border-brand-border flex items-center justify-between">
          <div className="flex items-center space-x-2.5 cursor-pointer" onClick={onOpenLanding}>
            <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <span className="font-semibold tracking-tight text-white text-base">DocSentry</span>
              <span className="block text-[10px] text-gray-500 font-mono tracking-wider uppercase">
                Drift Reliability
              </span>
            </div>
          </div>
          <span className="text-[11px] font-mono text-emerald-400/90 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
            v0.2.0
          </span>
        </div>

        {/* Navigation */}
        <nav className="p-3 space-y-1">
          <div className="px-3 py-2 text-[11px] font-medium text-gray-400 tracking-wider uppercase">
            Platform
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentTab(item.id)}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-md text-sm font-medium transition-all ${
                  isActive
                    ? "bg-brand-card text-emerald-400 border border-brand-border"
                    : "text-gray-400 hover:text-gray-200 hover:bg-brand-card/50"
                }`}
              >
                <div className="flex items-center space-x-2.5">
                  <Icon className={`w-4 h-4 ${isActive ? "text-emerald-400" : "text-gray-400"}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Architecture Specs quick link */}
        <div className="px-4 py-3 mx-3 my-2 bg-brand-dark/50 border border-brand-border/60 rounded-md">
          <div className="flex items-center justify-between text-xs text-gray-300 font-medium mb-1">
            <span className="flex items-center space-x-1.5">
              <Layers className="w-3.5 h-3.5 text-emerald-400" />
              <span>Core Engine</span>
            </span>
            <span className="text-[10px] text-emerald-400 font-mono">AST+GFM</span>
          </div>
          <p className="text-[11px] text-gray-500 leading-tight">
            Deterministic rule boundary with zero untrusted code execution.
          </p>
        </div>
      </div>

      {/* User Profile & Footer */}
      <div className="p-3 border-t border-brand-border space-y-2">
        <button
          onClick={onOpenAuth}
          className="w-full flex items-center justify-between p-2 rounded-lg bg-brand-dark hover:bg-brand-card border border-brand-border text-xs transition-colors"
        >
          <div className="flex items-center space-x-2.5 truncate">
            <div className="w-7 h-7 rounded-full bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <UserIcon className="w-3.5 h-3.5" />
            </div>
            <div className="text-left truncate">
              <div className="text-white font-medium truncate">{user?.username || "Sign In"}</div>
              <div className="text-[10px] text-gray-400 truncate font-mono">
                {user?.organization?.name || "Developer Profile"}
              </div>
            </div>
          </div>
          <span className="text-[10px] font-mono text-emerald-400">
            {user ? "Active" : "Login"}
          </span>
        </button>

        <div className="flex items-center justify-between px-1 text-[11px] text-gray-500 border-t border-brand-border/40 pt-2 font-mono">
          <span>Engine: Python 3.12+</span>
          <span className="flex items-center text-emerald-400">● Live</span>
        </div>
      </div>
    </aside>
  );
};
