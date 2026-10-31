import React from "react";
import {
  ShieldAlert,
  ArrowRight,
  FileText,
  Code2,
  Zap,
  Lock,
  ChevronRight,
  ExternalLink
} from "lucide-react";

interface LandingPageProps {
  onEnterApp: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onEnterApp }) => {
  return (
    <div className="min-h-screen bg-brand-dark text-gray-100 flex flex-col font-sans selection:bg-emerald-500/20 selection:text-emerald-400">
      {/* Top Navbar */}
      <header className="border-b border-brand-border/60 bg-brand-dark/80 backdrop-blur sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3 cursor-pointer" onClick={onEnterApp}>
            <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <span className="font-bold tracking-tight text-white text-lg">DocGuard</span>
          </div>

          <nav className="hidden md:flex items-center space-x-8 text-sm text-gray-400">
            <a href="#how-it-works" className="hover:text-white transition-colors">How It Works</a>
            <a href="#problem" className="hover:text-white transition-colors">The Problem</a>
            <a href="#checks" className="hover:text-white transition-colors">Supported Checks</a>
            <a href="https://github.com/Atharv386/DocSentary" target="_blank" rel="noreferrer" className="hover:text-white transition-colors flex items-center space-x-1">
              <span>GitHub</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </nav>

          <div className="flex items-center space-x-3">
            <button
              onClick={onEnterApp}
              className="px-4 py-2 rounded-lg bg-emerald-500 text-brand-dark font-semibold text-xs tracking-wide hover:bg-emerald-400 transition-all flex items-center space-x-1.5 shadow-sm"
            >
              <span>Launch App</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-20 pb-16 px-6 max-w-5xl mx-auto text-center space-y-6">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-mono bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Hacktoberfest 2026 Sonipat • PS5 Implementation</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight">
          Your code changed. <br />
          <span className="text-emerald-400">Did your docs?</span>
        </h1>

        <p className="text-lg text-gray-400 max-w-2xl mx-auto leading-relaxed">
          DocGuard detects documentation drift in pull requests, connects outdated statements to the code changes behind them, and helps engineering teams keep documentation trustworthy.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <button
            onClick={onEnterApp}
            className="w-full sm:w-auto px-6 py-3 rounded-lg bg-emerald-500 text-brand-dark font-semibold text-sm hover:bg-emerald-400 transition-all flex items-center justify-center space-x-2 shadow-lg shadow-emerald-500/10"
          >
            <span>Analyze a Pull Request</span>
            <ArrowRight className="w-4 h-4" />
          </button>
          <a
            href="#how-it-works"
            className="w-full sm:w-auto px-6 py-3 rounded-lg bg-brand-surface border border-brand-border text-gray-300 font-medium text-sm hover:bg-brand-card transition-all flex items-center justify-center space-x-2"
          >
            <span>See How It Works</span>
          </a>
        </div>

        {/* Hero Interactive Drift Preview Card */}
        <div className="pt-10 max-w-4xl mx-auto text-left">
          <div className="bg-brand-surface border border-brand-border rounded-xl shadow-2xl overflow-hidden">
            {/* Card Header */}
            <div className="px-4 py-3 bg-brand-card border-b border-brand-border flex items-center justify-between text-xs">
              <div className="flex items-center space-x-2">
                <span className="w-2.5 h-2.5 rounded-full bg-red-500/80"></span>
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500/80"></span>
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500/80"></span>
                <span className="font-mono text-gray-400 ml-2">DocGuard PR Analysis #42</span>
              </div>
              <span className="font-mono text-red-400 bg-red-500/10 border border-red-500/20 px-2 py-0.5 rounded text-[11px]">
                1 Confirmed Drift
              </span>
            </div>

            {/* Side-by-Side Hero Comparison */}
            <div className="p-5 grid grid-cols-1 md:grid-cols-2 gap-4 bg-brand-dark/50">
              <div className="p-3.5 rounded-lg bg-brand-dark border border-brand-border space-y-2">
                <div className="flex items-center justify-between text-xs font-mono text-amber-400">
                  <span className="flex items-center space-x-1">
                    <FileText className="w-3.5 h-3.5" />
                    <span>docs/config.md:23</span>
                  </span>
                  <span className="text-[10px] bg-brand-card px-1.5 py-0.5 rounded border border-brand-border">DocSpan</span>
                </div>
                <p className="text-xs text-gray-300 leading-relaxed font-sans">
                  "The default timeout is <span className="text-amber-300 font-semibold underline decoration-amber-500/50">30 seconds</span>."
                </p>
              </div>

              <div className="p-3.5 rounded-lg bg-brand-dark border border-brand-border space-y-2">
                <div className="flex items-center justify-between text-xs font-mono text-emerald-400">
                  <span className="flex items-center space-x-1">
                    <Code2 className="w-3.5 h-3.5" />
                    <span>src/client.py:12</span>
                  </span>
                  <span className="text-[10px] bg-brand-card px-1.5 py-0.5 rounded border border-brand-border">AST Fact</span>
                </div>
                <div className="text-xs font-mono text-emerald-300">
                  <code>def connect(..., <span className="font-bold underline decoration-emerald-500/50">timeout=60</span>):</code>
                </div>
              </div>
            </div>

            <div className="px-5 py-3 bg-brand-surface border-t border-brand-border flex items-center justify-between text-xs text-gray-400">
              <span>Rule: <code className="text-gray-300 font-mono">PY-DEFAULT-001</code> (Deterministic)</span>
              <button
                onClick={onEnterApp}
                className="text-emerald-400 hover:text-emerald-300 font-mono flex items-center space-x-1"
              >
                <span>Inspect full finding</span>
                <ChevronRight className="w-3 h-3" />
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* The Problem Section */}
      <section id="problem" className="py-20 border-t border-brand-border/60 bg-brand-surface/40">
        <div className="max-w-6xl mx-auto px-6 space-y-12">
          <div className="text-center space-y-3">
            <h2 className="text-xs font-mono uppercase tracking-wider text-emerald-400 font-semibold">The Core Problem</h2>
            <p className="text-3xl font-bold text-white">Documentation silently lies as software evolves.</p>
            <p className="text-sm text-gray-400 max-w-xl mx-auto">
              A developer updates code. The PR is reviewed for test passes and style. But no one knows which documentation pages referenced that exact signature or default.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-brand-card border border-brand-border space-y-3">
              <div className="w-10 h-10 rounded-lg bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-400">
                <FileText className="w-5 h-5" />
              </div>
              <h3 className="text-base font-semibold text-white">Silent API Drift</h3>
              <p className="text-xs text-gray-400 leading-relaxed">
                Default arguments, optional flags, and configuration keys change in code, while documentation pages continue advertising obsolete values.
              </p>
            </div>

            <div className="p-6 rounded-xl bg-brand-card border border-brand-border space-y-3">
              <div className="w-10 h-10 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
                <Zap className="w-5 h-5" />
              </div>
              <h3 className="text-base font-semibold text-white">Doc Linters Only Check Syntax</h3>
              <p className="text-xs text-gray-400 leading-relaxed">
                Traditional linters check markdown formatting, broken URLs, and typos. They cannot tell you if a statement in a document is still true in the code.
              </p>
            </div>

            <div className="p-6 rounded-xl bg-brand-card border border-brand-border space-y-3">
              <div className="w-10 h-10 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
                <Lock className="w-5 h-5" />
              </div>
              <h3 className="text-base font-semibold text-white">Zero-Hallucination Proof</h3>
              <p className="text-xs text-gray-400 leading-relaxed">
                DocGuard enforces a strict trust boundary. Every reported drift must bind directly to extracted AST facts and verified source lines.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 border-t border-brand-border/60">
        <div className="max-w-6xl mx-auto px-6 space-y-12">
          <div className="text-center space-y-3">
            <h2 className="text-xs font-mono uppercase tracking-wider text-emerald-400 font-semibold">Workflow</h2>
            <p className="text-3xl font-bold text-white">How DocGuard Protects Your Repositories</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="p-5 rounded-xl bg-brand-surface border border-brand-border space-y-3">
              <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Step 01</span>
              <h3 className="text-sm font-semibold text-white">PR Event Trigger</h3>
              <p className="text-xs text-gray-400 leading-relaxed">
                Runs automatically on GitHub Pull Requests via GitHub Actions or locally with the <code className="text-gray-300">docguard scan</code> CLI.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-brand-surface border border-brand-border space-y-3">
              <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Step 02</span>
              <h3 className="text-sm font-semibold text-white">Static AST & GFM Extraction</h3>
              <p className="text-xs text-gray-400 leading-relaxed">
                Extracts functions, parameters, defaults, and constants statically without ever executing target code.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-brand-surface border border-brand-border space-y-3">
              <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Step 03</span>
              <h3 className="text-sm font-semibold text-white">Deterministic Candidate Scoring</h3>
              <p className="text-xs text-gray-400 leading-relaxed">
                Ranks document passages by qualified symbol matching, parameter mentions, and heading contexts.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-brand-surface border border-brand-border space-y-3">
              <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Step 04</span>
              <h3 className="text-sm font-semibold text-white">Step Summary & Artifacts</h3>
              <p className="text-xs text-gray-400 leading-relaxed">
                Publishes side-by-side evidence directly to $GITHUB_STEP_SUMMARY and emits canonical <code className="text-gray-300">report.json</code>.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Supported Checks Grid */}
      <section id="checks" className="py-20 border-t border-brand-border/60 bg-brand-surface/40">
        <div className="max-w-6xl mx-auto px-6 space-y-8">
          <div className="text-center space-y-3">
            <h2 className="text-xs font-mono uppercase tracking-wider text-emerald-400 font-semibold">Rules Catalogue</h2>
            <p className="text-3xl font-bold text-white">Built-in Deterministic & Semantic Checks</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-lg bg-brand-card border border-brand-border space-y-1.5">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="text-emerald-400 font-semibold">PY-DEFAULT-001</span>
                <span className="text-red-400 bg-red-500/10 px-1.5 py-0.5 rounded">DRIFT</span>
              </div>
              <div className="text-sm font-semibold text-white">Stale Default Value</div>
              <p className="text-xs text-gray-400 leading-relaxed">
                Catches changes where a parameter's default literal changes, but documentation still quotes the old value.
              </p>
            </div>

            <div className="p-4 rounded-lg bg-brand-card border border-brand-border space-y-1.5">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="text-emerald-400 font-semibold">PY-PARAM-002</span>
                <span className="text-amber-400 bg-amber-500/10 px-1.5 py-0.5 rounded">DRIFT / POTENTIAL</span>
              </div>
              <div className="text-sm font-semibold text-white">Stale Parameter Mention</div>
              <p className="text-xs text-gray-400 leading-relaxed">
                Flags instances where a parameter was removed or renamed, but existing prose still instructs users to pass it.
              </p>
            </div>

            <div className="p-4 rounded-lg bg-brand-card border border-brand-border space-y-1.5">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="text-emerald-400 font-semibold">PY-SYMBOL-003</span>
                <span className="text-amber-400 bg-amber-500/10 px-1.5 py-0.5 rounded">POTENTIAL_DRIFT</span>
              </div>
              <div className="text-sm font-semibold text-white">Removed Symbol Reference</div>
              <p className="text-xs text-gray-400 leading-relaxed">
                Detects deleted functions or classes that are still cited in developer tutorials or API references.
              </p>
            </div>

            <div className="p-4 rounded-lg bg-brand-card border border-brand-border space-y-1.5">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="text-emerald-400 font-semibold">PY-CONFIG-004</span>
                <span className="text-red-400 bg-red-500/10 px-1.5 py-0.5 rounded">DRIFT</span>
              </div>
              <div className="text-sm font-semibold text-white">Stale CLI Flag or Config Key</div>
              <p className="text-xs text-gray-400 leading-relaxed">
                Alerts when command-line arguments (argparse) are renamed or deleted while tables in documentation stay untouched.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Bottom CTA */}
      <section className="py-20 border-t border-brand-border/60 text-center space-y-6">
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
          Keep your documentation as reliable as your code.
        </h2>
        <p className="text-gray-400 max-w-lg mx-auto text-sm">
          Integrate DocGuard in under 5 minutes with our native GitHub Actions workflow and local CLI.
        </p>
        <button
          onClick={onEnterApp}
          className="px-6 py-3 rounded-lg bg-emerald-500 text-brand-dark font-semibold text-sm hover:bg-emerald-400 transition-all inline-flex items-center space-x-2 shadow-lg shadow-emerald-500/20"
        >
          <span>Launch Interactive Dashboard</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </section>

      {/* Footer */}
      <footer className="border-t border-brand-border/60 py-8 bg-brand-surface text-center text-xs text-gray-500 font-mono">
        <p>DocGuard • Hacktoberfest 2026 Sonipat • Open Source under MIT License</p>
      </footer>
    </div>
  );
};
