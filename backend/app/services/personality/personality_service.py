from sqlalchemy.orm import Session
from app.models.memory import Memory

class PersonalityService:
    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id

    def get_system_prompt(self) -> str:
        base_prompt = (
            "You are ARIA, a personal AI assistant. "
            "Be concise — max 2 lines unless detailed output is needed. "
            "You learn and adapt to your user's communication style."
        )

        recent = (
            self.db.query(Memory)
            .filter(Memory.user_id == self.user_id)
            .order_by(Memory.created_at.desc())
            .limit(20)
            .all()
        )

        if not recent:
            return base_prompt + " Default personality: polite, respectful, neutral."

        user_messages = " ".join([r.user_message for r in recent])

        casual_words = ["lol", "haha", "bro", "dude", "hey", "gonna", "wanna", "omg"]
        formal_words = ["please", "kindly", "could you", "would you", "thank you", "regards"]
        sarcastic_words = ["obviously", "clearly", "great job", "wow", "sure", "whatever"]

        casual_score = sum(1 for w in casual_words if w in user_messages.lower())
        formal_score = sum(1 for w in formal_words if w in user_messages.lower())
        sarcastic_score = sum(1 for w in sarcastic_words if w in user_messages.lower())

        if sarcastic_score >= 2:
            style = "The user is sarcastic. Match their wit with light sarcasm and humor."
        elif casual_score > formal_score:
            style = "The user is casual and friendly. Be warm, relaxed, and conversational."
        elif formal_score > casual_score:
            style = "The user is formal and professional. Be precise and professional."
        else:
            style = "Default personality: polite, respectful, neutral."

        return base_prompt + " " + style