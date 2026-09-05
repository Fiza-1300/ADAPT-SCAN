import express from 'express'
import { addSimulationResult, createSession, getMySessions, getSessionById, updateSession } from '../controllers/scanSessionController.js'
import { protect } from '../middleware/authMiddleware.js'

const router = express.Router()

router.use(protect)

router.get('/sessions', getMySessions)
router.post('/sessions', createSession)
router.get('/sessions/:id', getSessionById)
router.put('/sessions/:id', updateSession)
router.post('/sessions/:id/results', addSimulationResult)

export default router
