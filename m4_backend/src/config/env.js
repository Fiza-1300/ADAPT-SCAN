import dotenv from 'dotenv'

dotenv.config()

export const env = {
  PORT: Number(process.env.PORT) || 5000,
  NODE_ENV: process.env.NODE_ENV || 'development',
  MONGODB_URI: process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/adapt-scan',
  JWT_SECRET: process.env.JWT_SECRET || 'dev-secret',
}
