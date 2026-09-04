import app from './src/app.js'
import { connectDB } from './src/config/db.js'
import { env } from './src/config/env.js'

async function startServer() {
  await connectDB()

  app.listen(env.PORT, () => {
    console.log(`Backend server running on http://localhost:${env.PORT}`)
  })
}

startServer()
