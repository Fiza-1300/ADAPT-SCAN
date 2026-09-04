export function notFoundHandler(req, res) {
  return res.status(404).json({
    success: false,
    message: `Route not found: ${req.originalUrl}`,
  })
}

export function errorHandler(err, req, res, next) {
  console.error('Unhandled error:', err)

  const statusCode = err.statusCode || 500
  const message = err.message || 'Internal server error'

  return res.status(statusCode).json({
    success: false,
    message,
  })
}
