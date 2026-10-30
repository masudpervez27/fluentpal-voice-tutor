import React, { useState } from 'react'
import { sendTurn, startSession } from './lib/api'

export default function App() {
  const [learnerName, setLearnerName] = useState('Learner')
  const [level, setLevel] = useState('B1')
  const [scenario, setScenario] = useState('casual chat')
  const [sessionId, setSessionId] = useState('')
  const [openingPrompt, setOpeningPrompt] = useState('')
  const [transcript, setTranscript] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleStartSession() {
    setError('')
    setLoading(true)
    try {
      const data = await startSession({
        learner_name: learnerName,
        level,
        scenario,
      })
      setSessionId(data.session_id)
      setOpeningPrompt(data.opening_prompt)
      setResult(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleSendTurn() {
    setError('')
    setLoading(true)
    try {
      const data = await sendTurn({ session_id: sessionId, transcript })
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ maxWidth: 860, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>FluentPal Voice Tutor</h1>
      <p>Session-based English tutoring with grammar corrections, fluency scoring, and feedback.</p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.5rem' }}>
        <input value={learnerName} onChange={(e) => setLearnerName(e.target.value)} placeholder="Learner name" />
        <select value={level} onChange={(e) => setLevel(e.target.value)}>
          <option>A1</option><option>A2</option><option>B1</option><option>B2</option><option>C1</option><option>C2</option>
        </select>
        <select value={scenario} onChange={(e) => setScenario(e.target.value)}>
          <option value="casual chat">Casual Chat</option>
          <option value="job interview">Job Interview</option>
          <option value="business meeting">Business Meeting</option>
        </select>
      </div>

      <button onClick={handleStartSession} style={{ marginTop: '1rem' }} disabled={loading}>
        {loading ? 'Starting...' : 'Start Session'}
      </button>

      {sessionId ? <p><strong>Session:</strong> {sessionId}</p> : null}
      {openingPrompt ? <p><strong>Tutor:</strong> {openingPrompt}</p> : null}

      <textarea
        value={transcript}
        onChange={(e) => setTranscript(e.target.value)}
        rows={6}
        style={{ width: '100%' }}
        placeholder="Type a spoken transcript turn..."
      />
      <button onClick={handleSendTurn} style={{ marginTop: '1rem' }} disabled={!sessionId || loading}>
        {loading ? 'Evaluating...' : 'Send Turn'}
      </button>
      {error ? <pre style={{ color: 'crimson' }}>{error}</pre> : null}
      {result ? (
        <section style={{ marginTop: '1rem' }}>
          <h3>Fluency Score: {result.fluency_score}</h3>
          <p><strong>Corrected:</strong> {result.corrected_text}</p>
          <p><strong>Tutor Reply:</strong> {result.tutor_reply}</p>
          <h4>Grammar Notes</h4>
          <ul>{result.grammar_notes.map((n, i) => (<li key={i}>{n}</li>))}</ul>
          <h4>Vocabulary Tips</h4>
          <ul>{result.vocabulary_tips.map((n, i) => (<li key={i}>{n}</li>))}</ul>
        </section>
      ) : null}
    </main>
  )
}
