# Adapt Scan Backend

This is the backend for the Adapt Scan application.

## Setup

1. Create a `.env` file in this folder.
2. Add the required environment variables:

```env
PORT=5001
NODE_ENV=development
MONGODB_URI=mongodb://127.0.0.1:27017/adapt-scan
JWT_SECRET=your_secure_random_secret
```

3. Install dependencies:

```bash
npm install
```

4. Start the backend:

```bash
npm run dev
```

## API Routes

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me` (protected)

### Sessions
- `GET /api/sessions` (protected)
- `POST /api/sessions` (protected)
- `GET /api/sessions/:id` (protected)
- `PUT /api/sessions/:id` (protected)
- `POST /api/sessions/:id/results` (protected)

### Health
- `GET /api/health`

### Temporary Simulation Integration

The simulation manager currently provides a deterministic in-memory demo loop until Members 1-3 deliver their simulator, observation, belief, and decision modules. All simulation routes require a JWT Bearer token.

- `POST /api/simulation/start`
- `POST /api/simulation/step`
- `POST /api/simulation/reset`
- `GET /api/simulation/state?sim_id=demo-001`
- `GET /api/simulation/decision?sim_id=demo-001`
- `GET /api/simulation/metrics?sim_id=demo-001`

Start a simulation with:

```json
{
	"sim_id": "demo-001",
	"scenario": "S7",
	"seed": 42,
	"strategy": "adapt_scan",
	"budget_total": 100
}
```

Advance it with:

```json
{
	"sim_id": "demo-001",
	"action": "R7"
}
```

The response follows the shared contract: simulation metadata, intelligence summary, regions, observation, decision, and metrics. The temporary manager is intentionally isolated in `src/services/simulationManager.js` so it can later delegate to the real team modules without changing the frontend API.

## Notes

- Keep `.env` private and do not commit it to GitHub.
- The repo ignores `.env` files.
- MongoDB must be running locally for DB-dependent routes to work.
