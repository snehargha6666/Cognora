def summarize_text(text: str, max_length: int = 200):
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."