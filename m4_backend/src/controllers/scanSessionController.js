import {
  createUserSession,
  getSessionDetails,
  listUserSessions,
  saveSimulationResult,
  updateSessionDetails,
} from '../services/sessionService.js'

export async function getMySessions(req, res) {
  try {
    const sessions = await listUserSessions(req.user._id)
    return res.status(200).json({ sessions })
  } catch (error) {
    console.error('Get sessions error:', error)
    return res.status(500).json({ message: 'Unable to fetch sessions.' })
  }
}

export async function createSession(req, res) {
  try {
    const session = await createUserSession({
      userId: req.user._id,
      title: req.body?.title,
      scenario: req.body?.scenario,
      status: req.body?.status,
      summary: req.body?.summary,
    })

    return res.status(201).json({ message: 'Session created successfully.', session })
  } catch (error) {
    console.error('Create session error:', error)
    return res.status(400).json({ message: error.message || 'Unable to create session.' })
  }
}

export async function getSessionById(req, res) {
  try {
    const session = await getSessionDetails(req.user._id, req.params.id)

    if (!session) {
      return res.status(404).json({ message: 'Session not found.' })
    }

    return res.status(200).json({ session })
  } catch (error) {
    console.error('Get session by id error:', error)
    return res.status(500).json({ message: 'Unable to fetch session.' })
  }
}

export async function updateSession(req, res) {
  try {
    const session = await updateSessionDetails(req.user._id, req.params.id, req.body || {})

    if (!session) {
      return res.status(404).json({ message: 'Session not found.' })
    }

    return res.status(200).json({ message: 'Session updated.', session })
  } catch (error) {
    console.error('Update session error:', error)
    return res.status(400).json({ message: error.message || 'Unable to update session.' })
  }
}

export async function addSimulationResult(req, res) {
  try {
    const result = await saveSimulationResult({
      userId: req.user._id,
      sessionId: req.params.id,
      region: req.body?.region,
      strategy: req.body?.strategy,
      confidence: req.body?.confidence,
      metrics: req.body?.metrics,
    })

    return res.status(201).json({ message: 'Simulation result saved.', result })
  } catch (error) {
    console.error('Add simulation result error:', error)
    const status = error.message === 'Session not found.' ? 404 : 400
    return res.status(status).json({ message: error.message || 'Unable to save simulation result.' })
  }
}
