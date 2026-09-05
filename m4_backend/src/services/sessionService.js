import { ScanSession } from '../models/ScanSession.js'
import { SimulationResult } from '../models/SimulationResult.js'
import { validateSessionPayload } from '../utils/validation.js'

export async function createUserSession({ userId, title, scenario, status, summary }) {
  validateSessionPayload({ title, scenario, status, summary })

  return ScanSession.create({
    userId,
    title: title.trim(),
    scenario: Number(scenario) || 1,
    status: status || 'draft',
    summary: summary || '',
  })
}

export async function listUserSessions(userId) {
  return ScanSession.find({ userId }).sort({ createdAt: -1 })
}

export async function getSessionDetails(userId, sessionId) {
  return ScanSession.findOne({ _id: sessionId, userId })
}

export async function updateSessionDetails(userId, sessionId, updates) {
  const session = await ScanSession.findOne({ _id: sessionId, userId })
  if (!session) return null

  if (updates.title !== undefined || updates.scenario !== undefined || updates.status !== undefined || updates.summary !== undefined) {
    validateSessionPayload({
      title: updates.title ?? session.title,
      scenario: updates.scenario ?? session.scenario,
      status: updates.status ?? session.status,
      summary: updates.summary ?? session.summary,
    })
  }

  if (updates.title !== undefined) session.title = updates.title.trim()
  if (updates.scenario !== undefined) session.scenario = Number(updates.scenario)
  if (updates.status !== undefined) session.status = updates.status
  if (updates.summary !== undefined) session.summary = updates.summary
  if (updates.results !== undefined) session.results = updates.results

  await session.save()
  return session
}

export async function saveSimulationResult({ userId, sessionId, region, strategy, confidence, metrics }) {
  if (!region || !strategy) {
    throw new Error('Region and strategy are required.')
  }

  const session = await ScanSession.findOne({ _id: sessionId, userId })
  if (!session) {
    throw new Error('Session not found.')
  }

  return SimulationResult.create({
    userId,
    sessionId,
    region,
    strategy,
    confidence: Number(confidence) || 0,
    metrics: metrics || {},
  })
}
