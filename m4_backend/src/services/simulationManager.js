const simulations = new Map()

const defaultRegions = [
  { region_id: 'R1', existence: 0.12, uncertainty: 0.81, threat_relevance: 0.10, last_observed: 1, status: 'uncertain' },
  { region_id: 'R7', existence: 0.81, uncertainty: 0.67, threat_relevance: 0.82, last_observed: 4, status: 'scanning' },
  { region_id: 'R12', existence: 0.58, uncertainty: 0.54, threat_relevance: 0.64, last_observed: 2, status: 'detected' },
]

function createObservation(regionId, timestep, seed) {
  const detected = (seed + timestep + regionId.length) % 5 !== 0
  return {
    region_id: regionId,
    detected,
    strength: detected ? 0.63 : 0.18,
    bandwidth: 0.41,
    snr: detected ? 7.2 : 2.1,
    confidence: detected ? 0.72 : 0.31,
    features: ['synthetic', detected ? 'signal-present' : 'noise-dominant'],
  }
}

function chooseRegion(simulation) {
  return [...simulation.regions]
    .sort((left, right) => (right.uncertainty + right.threat_relevance) - (left.uncertainty + left.threat_relevance))[0]
}

function buildState(simulation) {
  return {
    sim_id: simulation.sim_id,
    scenario: simulation.scenario,
    seed: simulation.seed,
    strategy: simulation.strategy,
    timestep: simulation.timestep,
    budget_total: simulation.budget_total,
    budget_remaining: simulation.budget_remaining,
    budget_remaining_frac: simulation.budget_remaining / simulation.budget_total,
    current_scan: simulation.current_scan,
    intelligence: {
      detected_count: simulation.regions.filter((region) => region.existence >= 0.5).length,
      high_priority_count: simulation.regions.filter((region) => region.threat_relevance >= 0.7).length,
      uncertainty_hotspots: simulation.regions.filter((region) => region.uncertainty >= 0.6).length,
    },
    regions: simulation.regions,
    observation: simulation.observation,
    decision: simulation.decision,
    metrics: simulation.metrics,
  }
}

function getSimulation(simId) {
  const simulation = simulations.get(simId)
  if (!simulation) throw new Error('Simulation not found.')
  return simulation
}

export function startSimulation(payload = {}) {
  const budgetTotal = Number(payload.budget_total) || 100
  const simulation = {
    sim_id: payload.sim_id || `sim-${Date.now()}`,
    scenario: payload.scenario || 'S7',
    seed: Number.isInteger(payload.seed) ? payload.seed : 42,
    strategy: payload.strategy || 'adapt_scan',
    timestep: 0,
    budget_total: budgetTotal,
    budget_remaining: budgetTotal,
    current_scan: null,
    regions: defaultRegions.map((region) => ({ ...region, status: 'uncertain' })),
    observation: null,
    decision: null,
    metrics: {
      detection_rate: null,
      time_to_detection: null,
      information_gain: 0,
      resource_consumption: 0,
      scan_reduction: null,
      tracking_quality: null,
      efficiency: null,
    },
  }

  simulations.set(simulation.sim_id, simulation)
  console.info(JSON.stringify({ event: 'simulation_started', sim_id: simulation.sim_id, scenario: simulation.scenario, seed: simulation.seed }))
  return buildState(simulation)
}

export function stepSimulation(simId, action) {
  const simulation = getSimulation(simId)
  const selectedAction = action || chooseRegion(simulation).region_id
  const region = simulation.regions.find((candidate) => candidate.region_id === selectedAction)
  if (!region) throw new Error('Unknown scan region.')
  if (simulation.budget_remaining < 1) throw new Error('Insufficient scan budget.')

  simulation.timestep += 1
  simulation.budget_remaining -= 1
  simulation.current_scan = selectedAction
  simulation.regions = simulation.regions.map((candidate) => ({
    ...candidate,
    status: candidate.region_id === selectedAction ? 'scanning' : candidate.status,
    last_observed: candidate.region_id === selectedAction ? simulation.timestep : candidate.last_observed,
  }))
  simulation.observation = createObservation(selectedAction, simulation.timestep, simulation.seed)
  const informationGain = Number((region.uncertainty * 0.9).toFixed(2))
  simulation.decision = {
    selected_action: selectedAction,
    utility: Number((informationGain * 0.6 + region.threat_relevance * 0.4).toFixed(2)),
    information_gain: informationGain,
    threat_score: region.threat_relevance,
    uncertainty: region.uncertainty,
    tracking_value: region.existence,
    scan_cost: 0.12,
    reason: `Selected ${selectedAction} because it has high uncertainty and expected information value relative to its scan cost.`,
  }
  simulation.metrics.information_gain = informationGain
  simulation.metrics.resource_consumption = Number((1 - simulation.budget_remaining / simulation.budget_total).toFixed(2))
  simulation.metrics.efficiency = informationGain
  console.info(JSON.stringify({ event: 'simulation_step', sim_id: simId, timestep: simulation.timestep, action: selectedAction, observation: simulation.observation, budget_remaining: simulation.budget_remaining }))
  return buildState(simulation)
}

export function resetSimulation(simId) {
  const simulation = getSimulation(simId)
  const reset = startSimulation({ sim_id: simulation.sim_id, scenario: simulation.scenario, seed: simulation.seed, strategy: simulation.strategy, budget_total: simulation.budget_total })
  console.info(JSON.stringify({ event: 'simulation_reset', sim_id: simId }))
  return reset
}

export function getSimulationState(simId) {
  return buildState(getSimulation(simId))
}

export function getDecision(simId) {
  return getSimulation(simId).decision
}

export function getMetrics(simId) {
  return getSimulation(simId).metrics
}