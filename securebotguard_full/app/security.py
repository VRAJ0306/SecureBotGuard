import re

SENSITIVE_PATTERNS = [
    r"\b\d{3}-\d{2}-\d{4}\b",
    r"\b\d{16}\b",
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
]

BLOCKED_KEYWORDS = ["ignore previous", "bypass", "admin override"]

def sanitize_input(text):
    for pattern in SENSITIVE_PATTERNS:
        text = re.sub(pattern, "[REDACTED]", text)
    return text

def check_prompt_injection(text):
    for keyword in BLOCKED_KEYWORDS:
        if keyword.lower() in text.lower():
            return True
    return False
