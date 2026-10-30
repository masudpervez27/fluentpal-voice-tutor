import logging
import re
import uuid

from ..models.schemas import StartSessionRequest, StartSessionResponse, TutorTurnResponse

logger = logging.getLogger(__name__)

SESSIONS: dict[str, dict] = {}

GRAMMAR_RULES = [
    (r"\bi is\b", "I am"),
    (r"\bi was go\b", "I went"),
    (r"\bhe don't\b", "he doesn't"),
    (r"\bshe don't\b", "she doesn't"),
    (r"\bcan to\b", "can"),
    (r"\bdiscuss about\b", "discuss"),
]


def _opening_prompt(level: str, scenario: str) -> str:
    if scenario == "job interview":
        return f"Welcome. At {level} level, please introduce yourself and describe one project you are proud of."
    if scenario == "business meeting":
        return f"Welcome. At {level} level, summarize your weekly progress and one blocker."
    return f"Welcome. At {level} level, tell me how your day is going and ask one follow-up question."


def start_session(payload: StartSessionRequest) -> StartSessionResponse:
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {
        "learner_name": payload.learner_name,
        "level": payload.level,
        "scenario": payload.scenario,
        "turns": [],
    }
    prompt = _opening_prompt(payload.level, payload.scenario)
    logger.info("Started tutoring session %s (%s, %s)", session_id, payload.level, payload.scenario)
    return StartSessionResponse(session_id=session_id, opening_prompt=prompt)


def _correct_text(text: str) -> tuple[str, list[str]]:
    corrected = text
    notes: list[str] = []
    for pattern, replacement in GRAMMAR_RULES:
        if re.search(pattern, corrected, flags=re.IGNORECASE):
            corrected = re.sub(pattern, replacement, corrected, flags=re.IGNORECASE)
            notes.append(f"Adjusted phrase '{pattern}' to '{replacement}'.")
    return corrected, notes


def _fluency_score(text: str) -> int:
    words = re.findall(r"[a-zA-Z']+", text)
    fillers = len(re.findall(r"\b(um|uh|like|you know)\b", text.lower()))
    sentence_count = max(1, len(re.findall(r"[.!?]", text)))
    words_per_sentence = len(words) / sentence_count

    score = 70
    if words_per_sentence >= 10:
        score += 8
    if words_per_sentence >= 14:
        score += 6
    score -= fillers * 4
    return max(0, min(100, int(score)))


def _vocab_tips(text: str) -> list[str]:
    tips: list[str] = []
    if "good" in text.lower():
        tips.append("Replace 'good' with more precise words like 'effective', 'valuable', or 'impactful'.")
    if "very" in text.lower():
        tips.append("Try reducing 'very' and use stronger adjectives directly.")
    if not tips:
        tips.append("Use one transition phrase, for example: 'In addition', 'However', or 'As a result'.")
    return tips


def _tutor_reply(session: dict, corrected_text: str, score: int) -> str:
    scenario = session["scenario"]
    if scenario == "job interview":
        return (
            f"Nice answer. Your fluency score is {score}. "
            "Now explain one technical decision you made and the business impact."
        )
    if scenario == "business meeting":
        return (
            f"Clear update. Your fluency score is {score}. "
            "Next, summarize your blocker and propose one concrete mitigation."
        )
    return (
        f"Great practice. Your fluency score is {score}. "
        "Ask me one follow-up question and respond with two complete sentences."
    )


def process_turn(session_id: str, transcript: str) -> TutorTurnResponse:
    session = SESSIONS.get(session_id)
    if not session:
        raise ValueError("Session not found. Start a session first.")

    corrected, grammar_notes = _correct_text(transcript)
    score = _fluency_score(transcript)
    vocab = _vocab_tips(transcript)
    reply = _tutor_reply(session, corrected, score)

    session["turns"].append({
        "transcript": transcript,
        "corrected": corrected,
        "score": score,
    })

    logger.info("Processed turn for session %s (score=%d, notes=%d)", session_id, score, len(grammar_notes))

    return TutorTurnResponse(
        session_id=session_id,
        corrected_text=corrected,
        grammar_notes=grammar_notes,
        fluency_score=score,
        vocabulary_tips=vocab,
        tutor_reply=reply,
    )
