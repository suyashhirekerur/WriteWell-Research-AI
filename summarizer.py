import heapq
import re
from collections import defaultdict


def _tokenize_sentences(text):
    """Simple sentence tokenizer."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 20]


def _tokenize_words(text):
    """Simple word tokenizer — lowercase alphabetic tokens."""
    return re.findall(r'\b[a-z]{3,}\b', text.lower())


STOPWORDS = {
    'the','a','an','and','or','but','in','on','at','to','for','of','with',
    'is','was','are','were','be','been','being','have','has','had','do',
    'does','did','will','would','could','should','may','might','this',
    'that','these','those','it','its','by','from','as','than','not',
    'also','i','we','our','their','they','he','she','his','her','us',
    'which','who','what','when','where','how','all','each','both',
    'into','through','during','before','after','above','below','between'
}


def summarize_text(text, num_sentences=3):
    """Extractive summarization using word-frequency scoring."""
    if not text or len(text.strip()) < 50:
        return text

    sentences = _tokenize_sentences(text)
    if len(sentences) <= num_sentences:
        return text

    # Word frequencies (excluding stopwords)
    word_freq = defaultdict(int)
    for word in _tokenize_words(text):
        if word not in STOPWORDS:
            word_freq[word] += 1

    if not word_freq:
        return ' '.join(sentences[:num_sentences])

    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] /= max_freq

    # Score sentences
    sentence_scores = {}
    for sent in sentences:
        score = 0
        words = _tokenize_words(sent)
        for word in words:
            if word in word_freq:
                score += word_freq[word]
        sentence_scores[sent] = score / max(len(words), 1)

    # Pick top N
    top = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    # Preserve original order
    ordered = [s for s in sentences if s in top]
    return ' '.join(ordered)


def summarize_sections(sections, num_sentences=3):
    """Summarize each detected section."""
    return {
        section: summarize_text(content, num_sentences)
        for section, content in sections.items()
        if section.lower() != 'references'
    }
