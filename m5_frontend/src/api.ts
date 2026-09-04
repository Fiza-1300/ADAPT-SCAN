const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api'

export interface BackendRegion {
  region_id: string
  existence: number
  uncertainty: number
  threat_relevance: number
  last_observed: number
  status: string
}

export interface BackendState {
  sim_id: string
  scenario: string
  seed: number
  strategy: string
  timestep: number
  budget_total: number
  budget_remaining: number
  budget_remaining_frac: number
  current_scan: string | null
  regions: BackendRegion[]
  observation: {
    region_id: string
    detected: boolean
    strength: number
    bandwidth: number
    snr: number
    confidence: number
    features: string[]
  } | null
  decision: {
    selected_action: string
    utility: number
    information_gain: number
    threat_score: number
    uncertainty: number
    tracking_value: number
    scan_cost: number
    reason: string
  } | null
  metrics: Record<string, number | null>
}

interface AuthResponse {
  token: string
  user: { _id: string; name: string; email: string; role: string }
}

interface SessionResponse {
  session: { _id: string }
}

async function request<T>(path: string, options: RequestInit = {}, token?: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  })

  const body = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(body.message || `API request failed (${response.status})`)
  return body as T
}

export function register(name: string, email: string, password: string) {
  return request<AuthResponse>('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ name, email, password }),
  })
}

export function login(email: string, password: string) {
  return request<AuthResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

export function startSimulation(token: string, payload: Record<string, unknown>) {
  return request<BackendState>('/simulation/start', {
    method: 'POST',
    body: JSON.stringify(payload),
  }, token)
}

export function stepSimulation(token: string, simId: string, action?: string) {
  return request<BackendState>('/simulation/step', {
    method: 'POST',
    body: JSON.stringify({ sim_id: simId, action }),
  }, token)
}

export function resetSimulation(token: string, simId: string) {
  return request<BackendState>('/simulation/reset', {
    method: 'POST',
    body: JSON.stringify({ sim_id: simId }),
  }, token)
}

export function createSession(token: string, payload: Record<string, unknown>) {
  return request<SessionResponse>('/sessions', {
    method: 'POST',
    body: JSON.stringify(payload),
  }, token)
}

export function saveSimulationResult(token: string, sessionId: string, payload: Record<string, unknown>) {
  return request('/sessions/' + sessionId + '/results', {
    method: 'POST',
    body: JSON.stringify(payload),
  }, token)
}
