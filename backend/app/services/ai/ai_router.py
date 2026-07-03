from app.config.settings import settings

def get_ai_response(messages: list) -> str:
    if settings.AI_PROVIDER == "groq":
        from app.services.ai.groq_service import get_ai_response
        return get_ai_response(messages)
    elif settings.AI_PROVIDER == "ollama":
        from app.services.ai.ollama_service import get_ai_response
        return get_ai_response(messages)
    else:
        raise ValueError(f"Unknown AI provider: {settings.AI_PROVIDER}")