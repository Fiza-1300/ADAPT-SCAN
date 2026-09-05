import express from 'express'
import { protect } from '../middleware/authMiddleware.js'
import {
  getDecision,
  getMetrics,
  getSimulationState,
  resetSimulation,
  startSimulation,
  stepSimulation,
} from '../services/simulationManager.js'

const router = express.Router()

router.use(protect)

function handleError(error, res) {
  const status = error.message === 'Simulation not found.' ? 404 : 400
  return res.status(status).json({ success: false, message: error.message })
}

router.post('/start', (req, res) => {
  try { return res.status(201).json(startSimulation(req.body)) } catch (error) { return handleError(error, res) }
})

router.post('/step', (req, res) => {
  try { return res.status(200).json(stepSimulation(req.body?.sim_id, req.body?.action)) } catch (error) { return handleError(error, res) }
})

router.post('/reset', (req, res) => {
  try { return res.status(200).json(resetSimulation(req.body?.sim_id)) } catch (error) { return handleError(error, res) }
})

router.get('/state', (req, res) => {
  try { return res.status(200).json(getSimulationState(req.query.sim_id)) } catch (error) { return handleError(error, res) }
})

router.get('/decision', (req, res) => {
  try { return res.status(200).json({ decision: getDecision(req.query.sim_id) }) } catch (error) { return handleError(error, res) }
})

router.get('/metrics', (req, res) => {
  try { return res.status(200).json({ metrics: getMetrics(req.query.sim_id) }) } catch (error) { return handleError(error, res) }
})

export default router