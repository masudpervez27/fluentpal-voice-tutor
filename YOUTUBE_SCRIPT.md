# FluentPal Voice Tutor - YouTube Transcript Script

## Title
Build a Session-Based English Tutor with Grammar and Fluency Feedback (Project 11)

## Intro
This project implements FluentPal from the portfolio roadmap.

In this feature slice we deliver:
- session creation with level and scenario,
- turn evaluation from transcript text,
- grammar correction notes,
- fluency scoring,
- tutor follow-up replies.

## Backend
We use two endpoints:
- POST /api/session
- POST /api/turn

Session state is stored in-memory for the demo. Each turn returns structured feedback for UI rendering.

## Analysis logic
For each transcript we run:
1. grammar-pattern fixes,
2. filler-word and sentence-length fluency scoring,
3. vocabulary enhancement tips,
4. scenario-aware tutor reply generation.

## Frontend
The frontend flow is:
1. start a session,
2. read opening tutor prompt,
3. submit transcript turns,
4. see corrected text, notes, score, and next tutor prompt.

## Logging
Backend logs session starts and turn processing.
Frontend logs API lifecycle and errors with VITE_LOG_LEVEL.

## Outro
This creates a practical conversational core and prepares the project for real-time STT/TTS integration next.
