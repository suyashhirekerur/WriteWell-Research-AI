# ✍️ WriteWell Research AI — AI-Powered Research Paper Analyzer

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered **Streamlit** web application that reads research papers (PDF, DOCX, TXT), analyzes writing quality using **Natural Language Processing (NLP)** techniques, extracts academic sections, generates extractive summaries, detects writing issues, and produces downloadable PDF reports — all without requiring any external API keys.

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack & Libraries](#-tech-stack--libraries)
- [Project Structure](#-project-structure)
- [Module Descriptions](#-module-descriptions)
- [Writing Quality Metrics — Algorithms & Formulas](#-writing-quality-metrics--algorithms--formulas)
- [NLP Techniques Used](#-nlp-techniques-used)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Screenshots](#-screenshots)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Multi-Format Upload** | Supports **PDF**, **DOCX**, and **TXT** research papers |
| 🗂️ **Section Detection** | Auto-detects standard academic sections — Abstract, Introduction, Background, Related Work, Literature Review, Methodology, Results, Discussion, Conclusion, Future Work, References, Acknowledgements |
| 📝 **Extractive Summarization** | Per-section summaries using word-frequency scoring (configurable sentence count) |
| 📊 **Writing Quality Scores** | Five metrics: Language, Coherence, Reasoning, Lexical Sophistication, Readability |
| 🕸️ **Radar Chart** | Interactive Plotly polar chart for visual quality overview |
| 📈 **Score Breakdown** | Horizontal bar chart comparing all five quality metrics |
| 📏 **Section Length Distribution** | Bar chart showing word count per detected section |
| 🧭 **Sentiment Analysis** | Rule-based polarity detection (Positive / Negative / Neutral) with polarity score |
| ⚠️ **Issue Detection** | Flags long sentences (>40 words), weak/vague vocabulary, low lexical diversity, short documents |
| 💡 **Vocabulary Suggestions** | Maps 20+ weak words to stronger academic alternatives |
| 🔑 **Keyword Extraction** | Top-15 keyword frequency analysis with stopword filtering |
| 📥 **PDF Export** | Downloadable comprehensive PDF report with scores, bar charts, summaries, issues, suggestions, and keywords |
| 🌓 **Dark / Light Mode** | Toggle between dark and light themes with animated gradient backgrounds |
| 🎨 **Animated UI** | Glassmorphism header, floating background blobs, hover card animations, soft-pulse effects |
| 📋 **Document Statistics** | Word count, sentence count, section count, and overall sentiment at a glance |

---

## 🛠️ Tech Stack & Libraries

### Core Framework

| Technology | Purpose |
|---|---|
| **[Streamlit](https://streamlit.io/)** `≥1.32.0` | Web application framework — handles UI, file uploads, layout, session state, theming |
| **[Python](https://www.python.org/)** `≥3.10` | Programming language |

### Data & Visualization

| Library | Purpose |
|---|---|
| **[Plotly](https://plotly.com/python/)** `≥5.20.0` | Interactive charts — `plotly.graph_objects` for radar/polar charts, `plotly.express` for bar charts |
| **[Pandas](https://pandas.pydata.org/)** `≥2.0.0` | DataFrames for structuring scores, keyword frequencies, and section stats |
| **[NumPy](https://numpy.org/)** `≥1.26.0` | Numerical support (transitive dependency) |

### Document Parsing

| Library | Purpose |
|---|---|
| **[pdfplumber](https://github.com/jsvine/pdfplumber)** `≥0.10.0` | PDF text extraction — page-by-page text parsing |
| **[python-docx](https://python-docx.readthedocs.io/)** `≥1.1.0` | DOCX text extraction — reads paragraphs from Word documents |

### Report Generation

| Library | Purpose |
|---|---|
| **[fpdf2](https://py-pdf.github.io/fpdf2/)** `≥2.7.0` | PDF report creation — custom headers/footers, metric bars, multi-cell text layout |

### Python Standard Library (no install needed)

| Module | Purpose |
|---|---|
| `re` | Regular expressions for sentence splitting, word tokenization, text normalization, section header matching |
| `math` | Mathematical utilities |
| `collections.Counter` | Word frequency counting for keyword extraction |
| `collections.defaultdict` | Accumulating word frequencies during summarization |
| `heapq` | Efficient top-N sentence selection for extractive summaries |
| `io` | In-memory byte streams for PDF generation |
| `datetime` | Timestamps in PDF report footers |

---

## 🗂️ Project Structure

```
WriteWell-Research-AI/
├── .streamlit/
│   └── config.toml             # Streamlit server, theme, and runner configuration
├── app.py                      # Main Streamlit application (UI, tabs, charts, CSS)
├── analyzer.py                 # Writing quality scoring & NLP analysis engine
├── pdf_extractor.py            # PDF / DOCX / TXT text extraction
├── text_cleaner.py             # Text preprocessing & noise removal
├── section_detector.py         # Academic section header detection & extraction
├── summarizer.py               # Extractive summarization via word-frequency scoring
├── report_generator.py         # PDF report generation (fpdf2)
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## 📦 Module Descriptions

### [`app.py`](app.py) — Main Application (944 lines)
The Streamlit dashboard. Orchestrates the entire pipeline:
1. **File Upload** — accepts PDF, DOCX, TXT via `st.file_uploader`
2. **Processing Pipeline** — calls extractor → cleaner → section detector → summarizer → analyzer
3. **Tabbed Dashboard** — six tabs: Dashboard, Sections & Summaries, Issues & Suggestions, Keywords, Export Report, Raw Text
4. **Theme Engine** — dark/light mode toggle via `st.session_state` with conditional CSS injection
5. **Custom CSS/HTML** — glassmorphism sticky header, animated gradient backgrounds, floating blob effects, card hover animations, all rendered via `st.markdown(unsafe_allow_html=True)`
6. **Interactive Charts** — Plotly radar chart (`go.Scatterpolar`), horizontal bar charts (`px.bar`), section distribution chart

### [`analyzer.py`](analyzer.py) — Analysis Engine (250 lines)
Contains all NLP scoring functions and curated word lists:
- **Sentence splitter** — regex-based, splits on `.!?` followed by whitespace
- **Word tokenizer** — regex `\b[a-zA-Z]+\b`
- **Syllable counter** — vowel-cluster heuristic for Flesch readability
- **Transition word list** — 30 transition/connecting words for coherence scoring
- **Logical word list** — 21 causal/logical connectives for reasoning scoring
- **Weak word dictionary** — 20 weak→strong word mappings for vocabulary suggestions
- **Academic vocabulary set** — 30 academic terms for lexical sophistication scoring
- **Sentiment word lists** — 10 positive + 10 negative terms for rule-based sentiment
- **Issue detection** — long sentences, weak vocabulary, low diversity, short documents
- **Keyword extraction** — stopword-filtered `Counter.most_common(15)`

### [`pdf_extractor.py`](pdf_extractor.py) — Document Extraction (46 lines)
Routes extraction by file extension:
- `.pdf` → `pdfplumber.open()` — page-by-page text extraction
- `.docx` → `docx.Document()` — paragraph-level text extraction
- `.txt` → `file.read().decode("utf-8")` — raw byte decoding

### [`text_cleaner.py`](text_cleaner.py) — Text Preprocessing (23 lines)
Cleans raw extracted text:
- Collapses multiple blank lines (`\n{3,}` → `\n\n`)
- Normalizes whitespace (`[ \t]+` → single space)
- Removes noisy short lines (page numbers, artifacts ≤3 chars)

### [`section_detector.py`](section_detector.py) — Section Detection (67 lines)
Identifies 18 standard academic section headers (case-insensitive, tolerates leading numbers like "1. Introduction"):
- Abstract, Introduction, Background, Related Work, Literature Review, Methodology, Methods, Materials and Methods, Experimental Setup, Results, Results and Discussion, Discussion, Conclusion, Conclusions, Future Work, References, Acknowledgements, Acknowledgments

### [`summarizer.py`](summarizer.py) — Extractive Summarization (74 lines)
Implements extractive summarization using **word-frequency scoring**:
1. Tokenize text into sentences and words
2. Build word frequency table (excluding 60+ stopwords)
3. Normalize frequencies by dividing by max frequency
4. Score each sentence as the mean of its constituent word scores
5. Select top-N sentences via `heapq.nlargest`
6. Return selected sentences in original document order

### [`report_generator.py`](report_generator.py) — PDF Report (114 lines)
Generates professional PDF reports using `fpdf2`:
- Custom `PaperIQReport` class extending `FPDF`
- Branded header bar (navy blue) and footer with page numbers and generation date
- Metric rows with progress bar visualizations
- Sections: Document Overview, Writing Quality Scores, Section Summaries, Writing Issues, Vocabulary Suggestions, Top Keywords
- Latin-1 safe encoding for font compatibility

---

## 📊 Writing Quality Metrics — Algorithms & Formulas

### 1. Readability Score (Flesch Reading Ease)
```
FRE = 206.835 − 1.015 × ASL − 84.6 × ASW
```
- **ASL** = Average Sentence Length (words per sentence)
- **ASW** = Average Syllables per Word
- Clamped to **0–100** range
- Higher score → easier to read

### 2. Language Score
```
Length Score  = max(0, 100 − |avg_sentence_length − 18| × 3)
Diversity    = (unique_words / total_words) × 150
Language     = (Length Score × 0.5) + (Diversity × 0.5)
```
- Penalizes sentence lengths deviating from the ideal 15–22 word range
- Rewards higher lexical diversity (Type-Token Ratio)

### 3. Coherence Score
```
Coherence = min(100, (transition_hits / expected) × 70 + 30)
expected  = max(1, sentence_count / 5)
```
- Counts occurrences of 30 transition words/phrases
- Expects roughly 1 transition per 5 sentences

### 4. Reasoning Score
```
Reasoning = min(100, logical_hits × 6 + 20)
```
- Counts occurrences of 21 logical/causal connectives (because, therefore, hence, etc.)

### 5. Lexical Sophistication Score
```
Lexical = min(100, (academic_hits / total_words) × 1000 + 20)
```
- Measures density of 30 curated academic vocabulary terms (analyze, hypothesis, empirical, etc.)

### 6. Sentiment Analysis
```
Polarity = (positive_count − negative_count) / (positive_count + negative_count)
```
- Uses 10 positive and 10 negative sentiment words
- Classified as **Positive** (>0.2), **Negative** (<−0.2), or **Neutral**

---

## 🧠 NLP Techniques Used

| Technique | Description | Module |
|---|---|---|
| **Regex-based Sentence Tokenization** | Splits text on `.!?` followed by whitespace using lookbehind assertions | `analyzer.py`, `summarizer.py` |
| **Regex-based Word Tokenization** | Extracts alphabetic tokens via `\b[a-zA-Z]+\b` | `analyzer.py`, `summarizer.py` |
| **Flesch Reading Ease** | Classic readability formula using syllable counting | `analyzer.py` |
| **Syllable Estimation** | Vowel-cluster heuristic with trailing-e correction | `analyzer.py` |
| **Type-Token Ratio (TTR)** | Lexical diversity measure: unique words / total words | `analyzer.py` |
| **Transition Word Detection** | Pattern matching against curated transition word list | `analyzer.py` |
| **Logical Connective Detection** | Pattern matching against causal/reasoning word list | `analyzer.py` |
| **Extractive Summarization** | TF-based sentence scoring with top-N selection via heap | `summarizer.py` |
| **Stopword Filtering** | 60+ English stopwords + domain-specific terms removed | `summarizer.py`, `analyzer.py` |
| **Academic Vocabulary Detection** | Matching against curated academic term set | `analyzer.py` |
| **Rule-based Sentiment Analysis** | Keyword counting with polarity calculation | `analyzer.py` |
| **Section Header Recognition** | Case-insensitive matching of 18 academic section patterns | `section_detector.py` |
| **Keyword Frequency Analysis** | `Counter.most_common()` with stopword filtering | `analyzer.py` |

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** installed
- **pip** package manager

### 1. Clone the repository
```bash
git clone https://github.com/suyashhirekerur/WriteWell-Research-AI.git
cd WriteWell-Research-AI
```

### 2. Create a virtual environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## ⚙️ Configuration

The app uses a Streamlit configuration file at [`.streamlit/config.toml`](.streamlit/config.toml):

| Setting | Value | Description |
|---|---|---|
| `server.port` | `8501` | Default port |
| `server.headless` | `true` | Prevents auto-opening browser |
| `server.enableXsrfProtection` | `true` | XSRF security enabled |
| `browser.gatherUsageStats` | `false` | Telemetry disabled |
| `theme.primaryColor` | `#1e3c72` | Navy blue primary |
| `theme.backgroundColor` | `#f0f4ff` | Light blue-white background |
| `theme.font` | `sans serif` | Default font family |
| `runner.fastReruns` | `true` | Optimized widget reruns |

---

## 📸 Screenshots

> Upload a research paper and explore the interactive dashboard with quality scores, radar charts, section summaries, issue detection, and PDF export.

*Run the app locally to see the full interactive experience.*

---

## 🔮 Future Improvements

- 🤖 **BERT/BART neural summarization** — replace extractive with abstractive summaries
- 🔍 **Research gap detection** — identify under-explored areas in the paper
- 🕸️ **Citation network analysis** — visualize reference relationships
- 📚 **Multi-paper comparison** — compare writing quality across multiple papers
- 💬 **GPT-powered literature review** — generate automated literature review sections
- 📊 **Advanced readability metrics** — Gunning Fog, SMOG, Coleman-Liau indices
- 🧪 **Grammar and spell checking** — integrate LanguageTool or similar
- 🏷️ **Named Entity Recognition (NER)** — extract key entities (authors, institutions, methods)

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/your-feature`)
3. **Commit** your changes (`git commit -m "Add your feature"`)
4. **Push** to the branch (`git push origin feature/your-feature`)
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Suyash Rajesh Hirekerur**

---

<p align="center">
  Made with ❤️ using Streamlit & Python
</p>
