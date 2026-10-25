import re


def clean_text(text):
    """Clean and normalize raw extracted text."""
    # Remove multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Collapse multiple spaces
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove lines that are just page numbers or short noise
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Skip very short noisy lines (page numbers etc.) unless they're headers
        if len(stripped) == 0:
            cleaned.append('')
        elif len(stripped) <= 3 and not stripped.isalpha():
            continue
        else:
            cleaned.append(stripped)
    return '\n'.join(cleaned).strip()
