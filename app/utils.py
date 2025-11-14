def validate_text(text):
    if not text.strip():
        raise ValueError('Text cannot be empty.')
    return text
