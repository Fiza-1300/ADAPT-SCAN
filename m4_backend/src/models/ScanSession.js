import mongoose from 'mongoose'

const scanSessionSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    title: {
      type: String,
      required: true,
      trim: true,
    },
    scenario: {
      type: Number,
      default: 1,
    },
    status: {
      type: String,
      enum: ['draft', 'active', 'completed'],
      default: 'draft',
    },
    results: {
      type: Object,
      default: {},
    },
    summary: {
      type: String,
      default: '',
    },
  },
  {
    timestamps: true,
  },
)

export const ScanSession = mongoose.model('ScanSession', scanSessionSchema)
