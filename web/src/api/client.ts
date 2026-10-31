/**
 * DocSentry API Client
 * Typed REST API client providing contracts with the FastAPI backend.
 */

const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string | null;
  avatar_url?: string | null;
  is_active: boolean;
  created_at: string;
  organization?: {
    id: string;
    slug: string;
    name: string;
    role: string;
  } | null;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface Repository {
  id: string;
  organization_id: string;
  github_repo_id: number;
  full_name: string;
  default_branch: string;
  is_private: boolean;
  clone_url: string;
  is_active: boolean;
  config_override?: Record<string, any> | null;
  open_findings_count: number;
  active_prs_count: number;
  last_analysis_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface PullRequest {
  id: string;
  repository_id: string;
  pr_number: number;
  title: string;
  state: string;
  author_username: string;
  base_ref: string;
  base_sha: string;
  head_ref: string;
  head_sha: string;
  html_url: string;
  latest_analysis?: {
    id: string;
    status: string;
    drift_count: number;
    potential_drift_count: number;
    duration_ms: number;
    completed_at?: string | null;
  } | null;
  created_at: string;
  updated_at: string;
}

export interface Evidence {
  id: string;
  evidence_external_id: string;
  role: "code" | "documentation";
  path: string;
  line_start: number;
  line_end: number;
  quote: string;
  source_kind: "ast_fact" | "diff_hunk" | "doc_span";
  metadata_json?: Record<string, any> | null;
  created_at: string;
}

export interface Finding {
  id: string;
  analysis_run_id: string;
  finding_external_id: string;
  status: "DRIFT" | "POTENTIAL_DRIFT" | "NO_DRIFT" | "UNCERTAIN";
  resolution_status: "open" | "acknowledged" | "dismissed" | "resolved";
  resolution_reason?: string | null;
  resolved_by_user_id?: string | null;
  resolved_at?: string | null;
  severity: "critical" | "high" | "medium" | "low" | "info";
  rule_id: string;
  category: string;
  title: string;
  explanation: string;
  confidence: number | null;
  verification: "deterministic" | "model_assisted" | "human_fixture";
  suggested_action?: string | null;
  evidence: Evidence[];
  created_at: string;
}

export interface AnalysisRun {
  id: string;
  organization_id: string;
  repository_id: string;
  pull_request_id?: string | null;
  trigger_type: string;
  status: "queued" | "processing" | "completed" | "failed" | "cancelled";
  base_sha: string;
  head_sha: string;
  merge_base_sha: string;
  tool_version: string;
  model_id?: string | null;
  duration_ms: number;
  summary?: Record<string, any> | null;
  error_message?: string | null;
  created_at: string;
  started_at?: string | null;
  completed_at?: string | null;
}

export interface HealthStatus {
  status: string;
  version: string;
  database: string;
  worker_queue: string;
  environment: string;
}

class ApiClient {
  private token: string | null = null;

  constructor() {
    this.token = localStorage.getItem("docsentry_token");
  }

  setToken(token: string | null) {
    this.token = token;
    if (token) {
      localStorage.setItem("docsentry_token", token);
    } else {
      localStorage.removeItem("docsentry_token");
    }
  }

  getToken(): string | null {
    return this.token;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const headers = new Headers(options.headers || {});
    headers.set("Content-Type", "application/json");
    if (this.token) {
      headers.set("Authorization", `Bearer ${this.token}`);
    }

    const res = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
    });

    if (!res.ok) {
      let errorMsg = `HTTP Error ${res.status}`;
      try {
        const errJson = await res.json();
        errorMsg = errJson.detail || errorMsg;
      } catch {
        // Fall back to status text
      }
      throw new Error(errorMsg);
    }

    return res.json();
  }

  // Health
  async getHealth(): Promise<HealthStatus> {
    return this.request<HealthStatus>("/health");
  }

  // Auth
  async directLogin(username: string): Promise<AuthResponse> {
    const res = await this.request<AuthResponse>("/auth/direct", {
      method: "POST",
      body: JSON.stringify({ username }),
    });
    this.setToken(res.access_token);
    return res;
  }

  async githubLogin(code: string, redirect_uri?: string): Promise<AuthResponse> {
    const res = await this.request<AuthResponse>("/auth/github", {
      method: "POST",
      body: JSON.stringify({ code, redirect_uri }),
    });
    this.setToken(res.access_token);
    return res;
  }

  async getMe(): Promise<User> {
    return this.request<User>("/auth/me");
  }

  async logout(): Promise<void> {
    try {
      if (this.token) {
        await this.request("/auth/logout", { method: "POST" });
      }
    } finally {
      this.setToken(null);
    }
  }

  // Repositories
  async listRepositories(): Promise<Repository[]> {
    return this.request<Repository[]>("/repositories");
  }

  async getRepository(id: string): Promise<Repository> {
    return this.request<Repository>(`/repositories/${id}`);
  }

  async createRepository(data: {
    full_name: string;
    default_branch?: string;
    clone_url: string;
    is_private?: boolean;
  }): Promise<Repository> {
    return this.request<Repository>("/repositories", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async updateRepository(
    id: string,
    data: { is_active?: boolean; config_override?: Record<string, any> }
  ): Promise<Repository> {
    return this.request<Repository>(`/repositories/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  }

  async deleteRepository(id: string): Promise<{ status: string }> {
    return this.request<{ status: string }>(`/repositories/${id}`, {
      method: "DELETE",
    });
  }

  async listRepositoryPRs(repoId: string, state?: string): Promise<PullRequest[]> {
    const query = state ? `?state=${encodeURIComponent(state)}` : "";
    return this.request<PullRequest[]>(`/repositories/${repoId}/pull-requests${query}`);
  }

  async listRepositoryAnalyses(repoId: string): Promise<AnalysisRun[]> {
    return this.request<AnalysisRun[]>(`/repositories/${repoId}/analyses`);
  }

  // Pull Requests
  async getPullRequest(id: string): Promise<PullRequest> {
    return this.request<PullRequest>(`/pull-requests/${id}`);
  }

  async triggerAnalysis(
    prId: string,
    options: { no_model?: boolean; force_rescan?: boolean } = {}
  ): Promise<{ analysis_run_id: string; status: string; message: string }> {
    return this.request(`/pull-requests/${prId}/analyze`, {
      method: "POST",
      body: JSON.stringify(options),
    });
  }

  // Analyses
  async getAnalysis(id: string): Promise<AnalysisRun> {
    return this.request<AnalysisRun>(`/analyses/${id}`);
  }

  async getAnalysisFindings(id: string): Promise<Finding[]> {
    return this.request<Finding[]>(`/analyses/${id}/findings`);
  }

  // Findings
  async getFinding(id: string): Promise<Finding> {
    return this.request<Finding>(`/findings/${id}`);
  }

  async updateFindingStatus(
    id: string,
    resolution_status: "open" | "acknowledged" | "dismissed" | "resolved",
    resolution_reason?: string
  ): Promise<Finding> {
    return this.request<Finding>(`/findings/${id}/status`, {
      method: "PATCH",
      body: JSON.stringify({ resolution_status, resolution_reason }),
    });
  }

  // Organizations
  async getActivity(orgId: string): Promise<{ items: any[]; total: number }> {
    return this.request(`/organizations/${orgId}/activity`);
  }
}

export const api = new ApiClient();
