import re

def clean_output(output):
    cleaned = re.sub(r'\r\n|\r', '\n', output)
    cleaned = cleaned.strip()
    max_length = 10000
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length] + "\n... (output truncated)"
    return cleaned
