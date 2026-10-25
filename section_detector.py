import re

SECTION_HEADERS = [
    "abstract",
    "introduction",
    "background",
    "related work",
    "literature review",
    "methodology",
    "methods",
    "materials and methods",
    "experimental setup",
    "results",
    "results and discussion",
    "discussion",
    "conclusion",
    "conclusions",
    "future work",
    "references",
    "acknowledgements",
    "acknowledgments",
]


def _normalize(line):
    return re.sub(r'[^a-z\s]', '', line.lower()).strip()


def extract_sections(text):
    """Detect and extract standard academic sections from paper text."""
    sections = {}
    lines = text.split('\n')
    current_header = 'Full Text'
    content = []

    for line in lines:
        norm = _normalize(line)
        # Check if this line is a known section header (allow trailing numbers like "1. Introduction")
        matched = None
        for header in SECTION_HEADERS:
            if norm == header or norm.endswith(header) and len(norm) - len(header) <= 4:
                matched = header.title()
                break

        if matched:
            # Save previous section
            block = ' '.join(content).strip()
            if block:
                sections[current_header] = block
            current_header = matched
            content = []
        else:
            if line.strip():
                content.append(line.strip())

    # Save final section
    block = ' '.join(content).strip()
    if block:
        sections[current_header] = block

    return sections


def get_section_stats(sections):
    """Return word counts per section."""
    return {k: len(v.split()) for k, v in sections.items()}
