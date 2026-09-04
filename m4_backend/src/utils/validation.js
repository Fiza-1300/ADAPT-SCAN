export function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

export function validatePassword(password) {
  return typeof password === 'string' && password.length >= 6
}

export function validateSessionPayload(payload = {}) {
  const { title, scenario, status, summary } = payload

  if (!title || !String(title).trim()) {
    throw new Error('Session title is required.')
  }

  if (scenario !== undefined && Number.isNaN(Number(scenario))) {
    throw new Error('Scenario must be a number.')
  }

  if (status && !['draft', 'active', 'completed'].includes(status)) {
    throw new Error('Invalid session status.')
  }

  if (summary !== undefined && typeof summary !== 'string') {
    throw new Error('Summary must be a string.')
  }

  return true
}
