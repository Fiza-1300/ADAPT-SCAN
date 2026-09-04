import mongoose from 'mongoose'

const simulationResultSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    sessionId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'ScanSession',
      required: true,
    },
    region: {
      type: String,
      required: true,
    },
    strategy: {
      type: String,
      required: true,
    },
    confidence: {
      type: Number,
      default: 0,
    },
    metrics: {
      type: Object,
      default: {},
    },
  },
  {
    timestamps: true,
  },
)

export const SimulationResult = mongoose.model('SimulationResult', simulationResultSchema)
