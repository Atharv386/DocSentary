import React, { useState } from "react";
import { Github, Key, AlertCircle, X } from "lucide-react";
import { useAuth } from "../context/AuthContext";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose }) => {
  const { user, login, logout } = useAuth();
  const [username, setUsername] = useState("octocat");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleDirectLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim()) return;
    setLoading(true);
    setErrorMsg(null);
    try {
      await login(username.trim());
      onClose();
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to log in");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 font-sans">
      <div className="bg-brand-surface border border-brand-border rounded-xl max-w-md w-full p-6 space-y-6 shadow-2xl">
        <div className="flex items-center justify-between border-b border-brand-border pb-3">
          <div className="flex items-center space-x-2">
            <Key className="w-5 h-5 text-emerald-400" />
            <h2 className="text-base font-bold text-white">Developer Authentication</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {user ? (
          <div className="space-y-4">
            <div className="p-4 rounded-lg bg-brand-dark border border-brand-border space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400 font-mono">CURRENTLY SIGNED IN</span>
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              </div>
              <div className="font-semibold text-white">{user.full_name || user.username}</div>
              <div className="text-xs text-gray-400 font-mono">Username: @{user.username}</div>
              <div className="text-xs text-emerald-400 font-mono">Workspace: {user.organization?.name}</div>
            </div>

            <button
              onClick={() => {
                logout();
                onClose();
              }}
              className="w-full py-2.5 rounded-lg bg-brand-card hover:bg-brand-border border border-brand-border text-xs font-mono text-gray-300 transition-colors"
            >
              Sign Out
            </button>
          </div>
        ) : (
          <div className="space-y-5">
            {errorMsg && (
              <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-xs text-red-400 flex items-start space-x-2">
                <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                <span>{errorMsg}</span>
              </div>
            )}

            {/* Direct Development Login */}
            <form onSubmit={handleDirectLogin} className="space-y-3">
              <div className="space-y-1">
                <label className="text-xs font-mono text-gray-300">Developer Username</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g. octocat, alice, admin"
                  className="w-full px-3 py-2 bg-brand-dark border border-brand-border rounded-lg text-white font-mono text-xs focus:outline-none focus:border-emerald-400"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-brand-dark font-semibold text-xs tracking-wide transition-colors flex items-center justify-center space-x-2"
              >
                <span>{loading ? "Authenticating..." : "Sign In with Developer Profile"}</span>
              </button>
            </form>

            <div className="relative flex py-2 items-center">
              <div className="flex-grow border-t border-brand-border"></div>
              <span className="flex-shrink mx-3 text-gray-500 text-[10px] font-mono uppercase">
                GitHub App OAuth
              </span>
              <div className="flex-grow border-t border-brand-border"></div>
            </div>

            {/* Honest GitHub Integration State */}
            <div className="p-3 bg-brand-dark border border-brand-border rounded-lg space-y-2 text-xs">
              <div className="flex items-center space-x-2 text-gray-300">
                <Github className="w-4 h-4 text-white" />
                <span className="font-semibold">GitHub App OAuth Status</span>
              </div>
              <p className="text-[11px] text-gray-400 leading-relaxed font-mono">
                Live GitHub OAuth requires <code className="text-emerald-400">DOCSENTRY_GITHUB_CLIENT_ID</code> and{" "}
                <code className="text-emerald-400">DOCSENTRY_GITHUB_CLIENT_SECRET</code> configured in your environment.
                Direct developer login provides 100% full platform access for local development.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
