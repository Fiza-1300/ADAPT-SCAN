import bcrypt from 'bcryptjs'
import jwt from 'jsonwebtoken'
import { User } from '../models/User.js'
import { env } from '../config/env.js'
import { validateEmail, validatePassword } from '../utils/validation.js'

function sanitizeUser(user) {
  const userObject = user.toObject ? user.toObject() : user
  const { passwordHash, ...safeUser } = userObject
  return safeUser
}

function createToken(userId) {
  return jwt.sign({ userId }, env.JWT_SECRET, { expiresIn: '7d' })
}

export async function registerUser(req, res) {
  try {
    const { name, email, password, role } = req.body || {}

    if (!name || !email || !password) {
      return res.status(400).json({ message: 'Name, email, and password are required.' })
    }

    if (!validateEmail(email)) {
      return res.status(400).json({ message: 'Please provide a valid email address.' })
    }

    if (!validatePassword(password)) {
      return res.status(400).json({ message: 'Password must be at least 6 characters long.' })
    }

    const existingUser = await User.findOne({ email: email.toLowerCase().trim() })
    if (existingUser) {
      return res.status(409).json({ message: 'User with this email already exists.' })
    }

    const passwordHash = await bcrypt.hash(password, 10)
    const user = await User.create({
      name: name.trim(),
      email: email.toLowerCase().trim(),
      passwordHash,
      role: role === 'admin' ? 'admin' : 'user',
    })

    const token = createToken(user._id)

    return res.status(201).json({
      message: 'User registered successfully.',
      token,
      user: sanitizeUser(user),
    })
  } catch (error) {
    console.error('Register error:', error)
    return res.status(500).json({ message: 'Server error during registration.' })
  }
}

export async function loginUser(req, res) {
  try {
    const { email, password } = req.body || {}

    if (!email || !password) {
      return res.status(400).json({ message: 'Email and password are required.' })
    }

    if (!validateEmail(email)) {
      return res.status(400).json({ message: 'Please provide a valid email address.' })
    }

    const user = await User.findOne({ email: email.toLowerCase().trim() })
    if (!user) {
      return res.status(401).json({ message: 'Invalid email or password.' })
    }

    const isMatch = await bcrypt.compare(password, user.passwordHash)
    if (!isMatch) {
      return res.status(401).json({ message: 'Invalid email or password.' })
    }

    const token = createToken(user._id)

    return res.status(200).json({
      message: 'Login successful.',
      token,
      user: sanitizeUser(user),
    })
  } catch (error) {
    console.error('Login error:', error)
    return res.status(500).json({ message: 'Server error during login.' })
  }
}

export async function getCurrentUser(req, res) {
  try {
    return res.status(200).json({ user: sanitizeUser(req.user) })
  } catch (error) {
    return res.status(500).json({ message: 'Unable to load current user.' })
  }
}
