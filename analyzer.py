import re
import math
from collections import Counter


# ── helpers ───────────────────────────────────────────────────────────────────

def _sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 5]

def _words(text):
    return re.findall(r'\b[a-zA-Z]+\b', text)

def _syllable_count(word):
    word = word.lower()
    count = len(re.findall(r'[aeiou]+', word))
    if word.endswith('e') and count > 1:
        count -= 1
    return max(1, count)


TRANSITION_WORDS = [
    'however','therefore','furthermore','moreover','consequently',
    'additionally','nevertheless','conversely','subsequently','accordingly',
    'thus','hence','meanwhile','specifically','notably','importantly',
    'in contrast','on the other hand','as a result','in addition',
    'for example','for instance','in conclusion','to summarize',
    'first','second','third','finally','initially','subsequently'
]

LOGICAL_WORDS = [
    'because','therefore','thus','hence','since','consequently',
    'if','unless','although','while','whereas','despite','due to',
    'as a result','in order to','given that','assuming that',
    'it follows that','this suggests','this indicates','evidence shows'
]

WEAK_WORDS = {
    'very': 'extremely',
    'good': 'beneficial',
    'bad': 'detrimental',
    'big': 'substantial',
    'small': 'minimal',
    'show': 'demonstrate',
    'use': 'utilize',
    'get': 'obtain',
    'make': 'construct',
    'look': 'examine',
    'find': 'discover',
    'help': 'facilitate',
    'important': 'critical',
    'many': 'numerous',
    'a lot': 'a significant number',
    'thing': 'element',
    'stuff': 'material',
    'nice': 'favorable',
    'really': 'substantially',
    'quite': 'considerably',
}

ACADEMIC_VOCAB = {
    'analyze','demonstrate','hypothesis','methodology','theoretical',
    'empirical','qualitative','quantitative','significant','correlation',
    'inference','parameter','variable','coefficient','algorithm',
    'framework','paradigm','criterion','synthesis','evaluate',
    'implement','establish','determine','investigate','examine',
    'indicate','suggest','conclude','validate','verify',
}


# ── scoring functions ─────────────────────────────────────────────────────────

def calculate_readability(text):
    """Flesch Reading Ease (0–100, higher = easier)."""
    sents = _sentences(text)
    words = _words(text)
    if not sents or not words:
        return 0
    syllables = sum(_syllable_count(w) for w in words)
    asl = len(words) / len(sents)           # avg sentence length
    asw = syllables / len(words)            # avg syllables per word
    score = 206.835 - 1.015 * asl - 84.6 * asw
    return max(0, min(100, round(score, 1)))


def calculate_language_score(text):
    """Score based on sentence length variety and word complexity."""
    sents = _sentences(text)
    words = _words(text)
    if not sents or not words:
        return 0

    lengths = [len(w_s.split()) for w_s in sents]
    avg_len = sum(lengths) / len(lengths)

    # Penalise extremes: ideal avg sentence length ~15–22 words
    length_score = max(0, 100 - abs(avg_len - 18) * 3)

    # Lexical diversity
    unique_ratio = len(set(w.lower() for w in words)) / len(words)
    diversity_score = min(100, unique_ratio * 150)

    return round((length_score * 0.5 + diversity_score * 0.5), 1)


def calculate_coherence_score(text):
    """Score based on presence of transition words."""
    text_lower = text.lower()
    hits = sum(1 for tw in TRANSITION_WORDS if tw in text_lower)
    sents = _sentences(text)
    if not sents:
        return 0
    # Expect roughly 1 transition per 5 sentences
    expected = max(1, len(sents) / 5)
    score = min(100, (hits / expected) * 70 + 30)
    return round(score, 1)


def calculate_reasoning_score(text):
    """Score based on logical connective words."""
    text_lower = text.lower()
    hits = sum(1 for lw in LOGICAL_WORDS if lw in text_lower)
    score = min(100, hits * 6 + 20)
    return round(score, 1)


def calculate_lexical_score(text):
    """Score based on academic vocabulary usage."""
    words_list = [w.lower() for w in _words(text)]
    if not words_list:
        return 0
    academic_hits = sum(1 for w in words_list if w in ACADEMIC_VOCAB)
    ratio = academic_hits / len(words_list)
    score = min(100, ratio * 1000 + 20)
    return round(score, 1)


def calculate_sentiment(text):
    """Simple rule-based sentiment polarity."""
    positive = ['significant','effective','novel','improved','accurate',
                'promising','robust','efficient','successful','innovative']
    negative = ['limited','problematic','poor','failed','insufficient',
                'unclear','inconsistent','weak','error','disadvantage']
    text_lower = text.lower()
    pos = sum(1 for w in positive if w in text_lower)
    neg = sum(1 for w in negative if w in text_lower)
    total = pos + neg
    if total == 0:
        return 'Neutral', 0.0
    polarity = (pos - neg) / total
    if polarity > 0.2:
        return 'Positive', round(polarity, 2)
    elif polarity < -0.2:
        return 'Negative', round(polarity, 2)
    return 'Neutral', round(polarity, 2)


def detect_writing_issues(text):
    """Flag writing problems."""
    issues = []
    sents = _sentences(text)
    words = _words(text)

    # Very long sentences
    long_sents = [s for s in sents if len(s.split()) > 40]
    if long_sents:
        issues.append({
            'type': '⚠️ Long Sentences',
            'count': len(long_sents),
            'detail': f'{len(long_sents)} sentence(s) exceed 40 words — consider splitting them.',
            'examples': long_sents[:2]
        })

    # Weak/vague words
    text_lower = text.lower()
    found_weak = [w for w in WEAK_WORDS if re.search(r'\b' + w + r'\b', text_lower)]
    if found_weak:
        issues.append({
            'type': '📝 Weak Vocabulary',
            'count': len(found_weak),
            'detail': f'Found {len(found_weak)} weak/vague word(s): {", ".join(found_weak[:8])}',
            'examples': []
        })

    # Low lexical diversity
    if words:
        diversity = len(set(w.lower() for w in words)) / len(words)
        if diversity < 0.4:
            issues.append({
                'type': '🔁 Low Lexical Diversity',
                'count': 1,
                'detail': f'Word diversity is {diversity:.0%}. Consider varying your vocabulary.',
                'examples': []
            })

    # Very short sections (possible missing content)
    if len(words) < 200:
        issues.append({
            'type': '📄 Short Document',
            'count': 1,
            'detail': 'Document has fewer than 200 words. Analysis may be limited.',
            'examples': []
        })

    return issues


def get_vocabulary_suggestions(text):
    """Return list of (found_word, suggestion) pairs."""
    text_lower = text.lower()
    suggestions = []
    for weak, strong in WEAK_WORDS.items():
        if re.search(r'\b' + weak + r'\b', text_lower):
            suggestions.append((weak, strong))
    return suggestions


def get_word_frequency(text, top_n=15):
    """Return top N content word frequencies."""
    stopwords = {
        'the','a','an','and','or','but','in','on','at','to','for','of','with',
        'is','was','are','were','be','been','being','have','has','had','this',
        'that','these','those','it','its','by','from','as','than','not','also',
        'i','we','our','their','they','he','she','his','her','us','which','who',
        'what','when','where','how','all','each','both','into','through','can',
        'paper','study','research','results','using','used','data','based',
        'method','methods','model','models','approach','approaches','shows','show'
    }
    words = [w.lower() for w in _words(text) if w.lower() not in stopwords and len(w) > 3]
    return Counter(words).most_common(top_n)


def full_analysis(text):
    """Run all metrics and return a summary dict."""
    sentiment_label, sentiment_score = calculate_sentiment(text)
    return {
        'readability': calculate_readability(text),
        'language': calculate_language_score(text),
        'coherence': calculate_coherence_score(text),
        'reasoning': calculate_reasoning_score(text),
        'lexical': calculate_lexical_score(text),
        'sentiment_label': sentiment_label,
        'sentiment_score': sentiment_score,
        'word_count': len(_words(text)),
        'sentence_count': len(_sentences(text)),
        'issues': detect_writing_issues(text),
        'vocab_suggestions': get_vocabulary_suggestions(text),
        'word_freq': get_word_frequency(text),
    }
