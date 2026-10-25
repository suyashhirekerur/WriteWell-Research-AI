# 🔬 WriteWell Research AI — AI Research Paper Analyzer

An AI-powered Streamlit application that reads research papers, analyzes writing quality, extracts sections, generates summaries, and produces downloadable PDF reports.

---

## 🚀 Quick Start

### 1. Create virtual environment

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

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 Upload | PDF, DOCX, TXT support |
| 🗂️ Section Detection | Auto-detects Abstract, Introduction, Methodology, Results, Discussion, Conclusion |
| 📝 Summarization | Extractive summarization per section |
| 📊 Quality Scores | Language, Coherence, Reasoning, Lexical, Readability |
| 🕸️ Radar Chart | Visual quality overview |
| ⚠️ Issue Detection | Long sentences, weak vocabulary, low diversity |
| 💡 Suggestions | Vocabulary improvement recommendations |
| 🔑 Keywords | Top keyword frequency analysis |
| 📥 PDF Export | Downloadable comprehensive report |

---

## 🗂️ Project Structure

```
WriteWell_Research_AI/
├── app.py                  # Main Streamlit application
├── analyzer.py             # Writing quality metrics
├── pdf_extractor.py        # PDF / DOCX / TXT extraction
├── text_cleaner.py         # Text preprocessing
├── section_detector.py     # Academic section detection
├── summarizer.py           # Extractive summarization
├── report_generator.py     # PDF report export
├── requirements.txt
└── README.md
```

---

## 📊 Writing Quality Metrics

- **Language Score** — sentence length variety + lexical diversity
- **Coherence Score** — transition word usage
- **Reasoning Score** — logical connective language
- **Lexical Sophistication** — academic vocabulary density
- **Readability** — Flesch Reading Ease index

---

## 🔮 Future Improvements

- BERT/BART neural summarization
- Research gap detection
- Citation network analysis
- Multi-paper comparison
- GPT-powered literature review generation
