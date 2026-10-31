import React, { useState } from "react";
import { Settings, Shield, Github, Sliders, Check, Copy } from "lucide-react";

export const SettingsView: React.FC = () => {
  const [modelEnabled, setModelEnabled] = useState(true);
  const [timeoutSecs, setTimeoutSecs] = useState("120");
  const [copiedUrl, setCopiedUrl] = useState(false);
  const webhookUrl = `${window.location.origin.replace("5173", "8000")}/api/v1/webhooks/github`;

  const handleCopyWebhook = () => {
    navigator.clipboard.writeText(webhookUrl);
    setCopiedUrl(true);
    setTimeout(() => setCopiedUrl(false), 2000);
  };

  return (
    <div className="flex-1 overflow-y-auto bg-brand-dark p-8 space-y-8 font-sans max-w-4xl">
      <div className="border-b border-brand-border/60 pb-6">
        <h1 className="text-2xl font-bold tracking-tight text-white flex items-center space-x-2.5">
          <Settings className="w-6 h-6 text-emerald-400" />
          <span>Platform Settings & GitHub App Integration</span>
        </h1>
        <p className="text-sm text-gray-400 mt-1">
          Configure continuous documentation drift detection, GitHub App webhooks, and reasoning models.
        </p>
      </div>

      {/* GitHub App Integration Section */}
      <div className="p-6 rounded-xl bg-brand-surface border border-brand-border space-y-4">
        <div className="flex items-center justify-between border-b border-brand-border pb-3">
          <div className="flex items-center space-x-2.5">
            <Github className="w-5 h-5 text-white" />
            <h2 className="text-sm font-bold text-white">GitHub App Integration</h2>
          </div>
          <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
            INTEGRATION READY
          </span>
        </div>

        <p className="text-xs text-gray-300 leading-relaxed">
          DocSentry connects as a GitHub App to receive pull request events, run AST-based documentation drift
          analysis asynchronously, and report findings directly into GitHub Check Runs.
        </p>

        <div className="space-y-3 pt-2">
          <div className="space-y-1.5">
            <label className="text-xs font-mono text-gray-400">Inbound Webhook URL</label>
            <div className="flex items-center space-x-2">
              <input
                type="text"
                readOnly
                value={webhookUrl}
                className="flex-1 px-3 py-2 bg-brand-dark border border-brand-border rounded-lg text-xs font-mono text-gray-200"
              />
              <button
                onClick={handleCopyWebhook}
                className="px-3 py-2 bg-brand-card hover:bg-brand-border border border-brand-border rounded-lg text-xs font-mono text-gray-300 flex items-center space-x-1.5 transition-colors"
              >
                {copiedUrl ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedUrl ? "Copied" : "Copy"}</span>
              </button>
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-mono text-gray-400">HMAC Webhook Secret</label>
            <input
              type="text"
              readOnly
              value="••••••••••••••••••••••••••••••••"
              className="w-full px-3 py-2 bg-brand-dark border border-brand-border rounded-lg text-xs font-mono text-gray-400"
            />
            <p className="text-[11px] text-gray-400 font-mono">
              Configured via <code className="text-emerald-400">DOCSENTRY_GITHUB_WEBHOOK_SECRET</code> in <code className="text-gray-300">.env</code>.
            </p>
          </div>
        </div>
      </div>

      {/* Analysis Engine & Model Preferences */}
      <div className="p-6 rounded-xl bg-brand-surface border border-brand-border space-y-4">
        <div className="flex items-center space-x-2.5 border-b border-brand-border pb-3">
          <Sliders className="w-5 h-5 text-emerald-400" />
          <h2 className="text-sm font-bold text-white">Detection Engine Configuration</h2>
        </div>

        <div className="space-y-4 text-xs font-mono">
          <div className="flex items-center justify-between p-3 rounded-lg bg-brand-dark border border-brand-border">
            <div>
              <div className="text-gray-200 font-medium">Selective AI Model Verification (Qwen3-8B)</div>
              <div className="text-gray-400 text-[11px] mt-0.5">
                Uses local Ollama Qwen3-8B for complex semantic claims while preserving 100% deterministic AST rules.
              </div>
            </div>
            <button
              onClick={() => setModelEnabled(!modelEnabled)}
              className={`w-12 h-6 rounded-full transition-colors relative flex items-center px-1 ${
                modelEnabled ? "bg-emerald-500" : "bg-gray-700"
              }`}
            >
              <span
                className={`w-4 h-4 rounded-full bg-brand-dark transition-transform ${
                  modelEnabled ? "translate-x-6" : "translate-x-0"
                }`}
              />
            </button>
          </div>

          <div className="space-y-1.5">
            <label className="text-gray-300 block">Analysis Timeout (seconds)</label>
            <input
              type="number"
              value={timeoutSecs}
              onChange={(e) => setTimeoutSecs(e.target.value)}
              className="w-32 px-3 py-1.5 bg-brand-dark border border-brand-border rounded text-white"
            />
          </div>
        </div>
      </div>

      {/* Security & Code Isolation Banner */}
      <div className="p-5 rounded-xl bg-emerald-500/5 border border-emerald-500/20 flex items-start space-x-3 text-xs">
        <Shield className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
        <div className="space-y-1">
          <span className="font-semibold text-emerald-400">Strict Zero Untrusted Code Execution Guarantee</span>
          <p className="text-gray-300 leading-relaxed">
            DocSentry operates strictly through static AST analysis and Git object parsing. It never imports,
            executes, builds, or runs code from analyzed repositories, eliminating Remote Code Execution (RCE) vectors.
          </p>
        </div>
      </div>
    </div>
  );
};
