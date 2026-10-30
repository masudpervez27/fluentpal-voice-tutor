const API = import.meta.env.VITE_API_URL || ''

const LOG_LEVELS = { debug: 10, info: 20, warn: 30, error: 40 }
const ACTIVE_LEVEL = LOG_LEVELS[(import.meta.env.VITE_LOG_LEVEL || (import.meta.env.DEV ? 'debug' : 'info')).toLowerCase()] || LOG_LEVELS.info

function log(level, message, context) {
  if ((LOG_LEVELS[level] || LOG_LEVELS.info) < ACTIVE_LEVEL) return
  const writer = console[level] || console.log
  if (context === undefined) writer('[FluentPal Voice Tutor] ' + message)
  else writer('[FluentPal Voice Tutor] ' + message, context)
}

export async function startSession(payload) {
  log('info', 'Calling session endpoint')
  const response = await fetch(API + '/api/session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const text = await response.text()
    log('error', 'session endpoint failed', { status: response.status, body: text })
    throw new Error(text)
  }

  return response.json()
}

export async function sendTurn(payload) {
  log('info', 'Calling turn endpoint')
  const response = await fetch(API + '/api/turn', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const text = await response.text()
    log('error', 'turn endpoint failed', { status: response.status, body: text })
    throw new Error(text)
  }

  return response.json()
}
