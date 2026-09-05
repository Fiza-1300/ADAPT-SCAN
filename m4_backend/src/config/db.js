import mongoose from 'mongoose'
import { env } from './env.js'

export async function connectDB() {
  try {
    await mongoose.connect(env.MONGODB_URI)
    console.log('MongoDB connected successfully')
  } catch (error) {
    console.error('MongoDB connection failed:', error.message)
    console.log('Continuing without database connection for local setup. Add MongoDB to resume full data functionality.')
  }
}
