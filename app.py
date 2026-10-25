"""color
WriteWell Research AI — AI-powered Research Paper Analysis Dashboard
Run:  streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from pdf_extractor import extract_text
from text_cleaner import clean_text
from section_detector import extract_sections, get_section_stats
from summarizer import summarize_sections
from analyzer import full_analysis
from report_generator import generate_report

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WriteWell Research AI — Research Paper Analyzer",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Initialize session state for dark mode ────────────────────────────────────
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# ── Custom CSS ────────────────────────────────────────────────────────────────
if st.session_state.dark_mode:
    # Dark mode styles
    st.markdown("""
    <style>
        /* Main background - Dark */
        .main {
            background: linear-gradient(120deg, #0d1117 0%, #0b1526 35%, #0d419d 100%);
            background-size: 200% 200%;
            animation: gradientShift 10s ease infinite;
        }

        /* Subtle animations */
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes softPulse {
            0%, 100% { filter: drop-shadow(0 0 0 rgba(88,166,255,0)); }
            50% { filter: drop-shadow(0 10px 22px rgba(88,166,255,0.25)); }
        }
        
        /* Main background + text color - Dark mode */
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stApp"] {
            background: linear-gradient(120deg, #0d1117 0%, #0b1526 50%, #0d1f4a 100%) !important;
            background-size: 200% 200% !important;
            animation: gradientShift 10s ease infinite !important;
            color: #e6edf3;
        }
        
        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            color: #58a6ff !important;
        }
        
        /* Body text */
        p, div, span {
            color: #c9d1d9 !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(160deg, #161b22 0%, #0d1117 100%);
        }
        section[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
        
        /* Sidebar text */
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] label {
            color: #c9d1d9 !important;
        }

        /* Cards */
        .metric-card {
            background: #161b22;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3);
            margin-bottom: 12px;

            animation: fadeUp 0.6s ease both;
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }
        .metric-card:hover{
            transform: translateY(-4px);
            box-shadow: 0 10px 26px rgba(0,0,0,0.35);
        }
        .metric-card * {
            color: #e6edf3 !important;
        }
        .score-big {
            font-size: 2.4rem;
            font-weight: 700;
            color: #58a6ff;
        }
        .score-label {
            font-size: 0.85rem;
            color: #8b949e !important;
            margin-top: -4px;
        }

        /* Section header */
        .section-header {
            background: linear-gradient(90deg, #0d419d, #1f6feb);
            color: white !important;
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        /* Issue card */
        .issue-card {
            background: #2d333b;
            border-left: 4px solid #d29922;
            padding: 10px 14px;
            border-radius: 6px;
            margin-bottom: 8px;
        }
        .issue-card * {
            color: #c9d1d9 !important;
        }

        /* Suggestion pill */
        .suggestion-pill {
            display: inline-block;
            background: #238636;
            border: 1px solid #3fb950;
            border-radius: 20px;
            padding: 3px 12px;
            margin: 4px;
            font-size: 0.85rem;
            color: #c9d1d9 !important;
        }
        
        /* Streamlit elements text */
        .stMarkdown p,
        .stText,
        .stCaption {
            color: #c9d1d9 !important;
        }
        
        /* Metric value text */
        [data-testid="stMetricValue"] {
            color: #58a6ff !important;
        }
        
        /* Metric label text */
        [data-testid="stMetricLabel"] {
            color: #8b949e !important;
        }

        /* Hide sidebar completely (we moved controls to the top header) */
        section[data-testid="stSidebar"] { display: none !important; }
        section[data-testid="stSidebar"] * { display: none !important; }

        /* Floating background FX */
        .bg-fx {
            position: fixed;
            inset: 0;
            z-index: -1;
            pointer-events: none;
            overflow: hidden;
        }
        .bg-blob {
            position: absolute;
            width: 480px;
            height: 480px;
            border-radius: 999px;
            filter: blur(42px);
            opacity: 0.28;
            animation: blobDrift 14s ease-in-out infinite;
        }
        .bg-blob.b1 { left: -140px; top: -160px; background: #1f6feb; animation-duration: 16s; }
        .bg-blob.b2 { right: -180px; top: 40px; background: #22c55e; animation-duration: 18s; }
        .bg-blob.b3 { left: 15%; bottom: -240px; background: #f59e0b; animation-duration: 20s; }

        @keyframes blobDrift {
            0%   { transform: translate(0px, 0px) scale(1); }
            50%  { transform: translate(40px, -30px) scale(1.04); }
            100% { transform: translate(0px, 0px) scale(1); }
        }

        /* Creative header bar (top controls) */
        .paperiq-header {
            position: sticky;
            top: 0;
            z-index: 999;
            backdrop-filter: blur(10px);
            background: rgba(10, 13, 20, 0.55);
            border-bottom: 1px solid rgba(88, 166, 255, 0.18);
            border-top: 1px solid rgba(88, 166, 255, 0.10);
            padding: 14px 14px 10px 14px;
            margin: -10px -10px 10px -10px; /* stick nicely to viewport */
            animation: fadeUp 0.6s ease both;
        }
        .paperiq-header .title {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        .paperiq-brand {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            font-weight: 800;
            font-size: 1.15rem;
            color: #e6edf3;
        }
        .paperiq-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 10px;
            border-radius: 999px;
            border: 1px solid rgba(88,166,255,0.22);
            color: #c9d1d9;
            background: rgba(31,111,235,0.10);
            margin-top: 6px;
        }

        .paperiq-widgets {
            margin-top: 10px;
        }
        .paperiq-widgets > div { margin-bottom: 6px; }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
else:
    # Light mode styles (original)
    st.markdown("""
    <style>
        /* Main background */
        .main {
            background: linear-gradient(120deg, #f0f4ff 0%, #eef2ff 40%, #dbeafe 100%);
            background-size: 200% 200%;
            animation: gradientShift 10s ease infinite;
        }

        /* Subtle animations */
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes softPulse {
            0%, 100% { filter: drop-shadow(0 0 0 rgba(30,100,200,0)); }
            50% { filter: drop-shadow(0 10px 22px rgba(30,100,200,0.18)); }
        }
        
        /* Main background + text color - Light mode */
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stApp"] {
            background: linear-gradient(120deg, #f0f4ff 0%, #eef2ff 40%, #dbeafe 100%) !important;
            background-size: 200% 200% !important;
            animation: gradientShift 10s ease infinite !important;
            color: #1a1a2e;
        }
        
        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            color: #1e3c72 !important;
        }
        
        /* Body text */
        p, div, span {
            color: #2d3748 !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(160deg, #1e3c72 0%, #2a5298 100%);
        }
        section[data-testid="stSidebar"] * { color: #e8f0ff !important; }
        
        /* Sidebar text */
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] label {
            color: #e8f0ff !important;
        }

        /* Cards */
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 12px rgba(30,60,114,0.10);
            margin-bottom: 12px;

            animation: fadeUp 0.6s ease both;
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }
        .metric-card:hover{
            transform: translateY(-4px);
            box-shadow: 0 14px 30px rgba(30,60,114,0.16);
        }
        .metric-card * {
            color: #1a1a2e !important;
        }
        .score-big {
            font-size: 2.4rem;
            font-weight: 700;
            color: #1e3c72;
        }
        .score-label {
            font-size: 0.85rem;
            color: #4a5568 !important;
            margin-top: -4px;
        }

        /* Section header */
        .section-header {
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            color: white !important;
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        /* Issue card */
        .issue-card {
            background: #fff8e1;
            border-left: 4px solid #f59e0b;
            padding: 10px 14px;
            border-radius: 6px;
            margin-bottom: 8px;
        }
        .issue-card * {
            color: #2d3748 !important;
        }

        /* Suggestion pill */
        .suggestion-pill {
            display: inline-block;
            background: #e8f5e9;
            border: 1px solid #66bb6a;
            border-radius: 20px;
            padding: 3px 12px;
            margin: 4px;
            font-size: 0.85rem;
            color: #2e7d32 !important;
        }
        
        /* Streamlit elements text */
        .stMarkdown p,
        .stText,
        .stCaption {
            color: #2d3748 !important;
        }
        
        /* Metric value text */
        [data-testid="stMetricValue"] {
            color: #1e3c72 !important;
        }
        
        /* Metric label text */
        [data-testid="stMetricLabel"] {
            color: #4a5568 !important;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# ── Global UI Enhancements (header + background + sidebar hide) ─────────────
st.markdown("""
<style>
    /* Always hide sidebar completely (UI moved to header) */
    section[data-testid="stSidebar"] { display: none !important; }
    section[data-testid="stSidebar"] * { display: none !important; }

    /* Floating background FX */
    .bg-fx {
        position: fixed;
        inset: 0;
        z-index: -1;
        pointer-events: none;
        overflow: hidden;
    }
    .bg-blob {
        position: absolute;
        width: 520px;
        height: 520px;
        border-radius: 999px;
        filter: blur(48px);
        opacity: 0.22;
        animation: blobDrift 16s ease-in-out infinite;
    }
    .bg-blob.b1 { left: -180px; top: -210px; background: #1f6feb; animation-duration: 18s; }
    .bg-blob.b2 { right: -210px; top: 60px; background: #22c55e; animation-duration: 20s; }
    .bg-blob.b3 { left: 10%; bottom: -280px; background: #f59e0b; animation-duration: 22s; }

    @keyframes blobDrift {
        0%   { transform: translate(0px, 0px) scale(1); }
        50%  { transform: translate(46px, -34px) scale(1.05); }
        100% { transform: translate(0px, 0px) scale(1); }
    }

    /* Sticky creative top header */
    .paperiq-header {
        position: sticky;
        top: 0;
        z-index: 999;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        background: rgba(10, 13, 20, 0.58);
        border-bottom: 1px solid rgba(88, 166, 255, 0.20);
        padding: 14px 18px 10px 18px;
        margin: -10px -10px 16px -10px;
        animation: fadeUp 0.55s ease both;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .paperiq-header .title {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
    }

    .paperiq-brand {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        font-weight: 900;
        font-size: 1.2rem;
        color: #e6edf3;
        letter-spacing: 0.2px;
    }

    .paperiq-chip {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 7px 12px;
        border-radius: 999px;
        border: 1px solid rgba(88, 166, 255, 0.25);
        background: rgba(31, 111, 235, 0.10);
        color: #c9d1d9;
        box-shadow: 0 10px 25px rgba(0,0,0,0.10);
        animation: softPulse 2.8s ease-in-out infinite;
    }

    @keyframes softPulse {
        0%, 100% { transform: translateY(0px); filter: saturate(1); }
        50% { transform: translateY(-2px); filter: saturate(1.2); }
    }

    /* Make the main content feel “below header” */
    div[data-testid="stAppViewContainer"] {
        padding-top: 0px;
    }
</style>
""", unsafe_allow_html=True)

# Animated background blobs
st.markdown("""
<div class="bg-fx" aria-hidden="true">
  <div class="bg-blob b1"></div>
  <div class="bg-blob b2"></div>
  <div class="bg-blob b3"></div>
</div>
""", unsafe_allow_html=True)

# ── Helper: score colour ──────────────────────────────────────────────────────
def score_color(score):
    if score >= 75:
        return "#22c55e"
    elif score >= 50:
        return "#f59e0b"
    else:
        return "#ef4444"


def score_badge(label, value):
    color = score_color(value)
    return f"""
    <div class="metric-card" style="text-align:center; border-top: 4px solid {color};">
        <div class="score-big" style="color:{color};">{value:.0f}</div>
        <div class="score-label">{label}</div>
    </div>
    """


# ── Top header controls (replaces sidebar) ───────────────────────────────────
st.markdown("""
<div class="paperiq-header">
  <div class="title">
    <div class="paperiq-brand">✍️ WriteWell Research AI</div>
    <div class="paperiq-pill">📑 Research Paper Writing Quality Analyzer</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Controls directly under the sticky header
with st.container():
    col_theme, col_upload = st.columns([1, 3])

    with col_theme:
        st.markdown("### 🌓 Theme")
        if st.button("🌙" if not st.session_state.dark_mode else "☀️", help="Toggle dark/light mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    with col_upload:
        uploaded_file = st.file_uploader(
            "📂 Upload Research Paper",
            type=["pdf", "docx", "txt"],
            help="Supported: PDF, DOCX, TXT"
        )

    st.markdown("---")

    col_opt1, col_opt2 = st.columns([2, 1])
    with col_opt1:
        st.markdown("### ⚙️ Options")
        num_summary_sentences = st.slider("Summary sentences per section", 1, 6, 3)

    with col_opt2:
        show_raw_text = st.checkbox("Show extracted raw text", value=False)

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
WriteWell Research AI analyzes research papers and provides:
- 📊 Writing quality scores
- 🗂️ Section detection
- 📝 Auto-summaries
- ⚠️ Issue detection
- 📄 PDF report export
    """)


# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("# ✍️ WriteWell Research AI — Research Paper Analyzer")
st.markdown("Upload a research paper to get an instant AI-powered writing quality analysis and summary.")

if uploaded_file is None:
    # Landing state
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card" style="text-align:center; padding:30px;">
            <div style="font-size:2.5rem;">📄</div>
            <strong>Upload Paper</strong><br/>
            <small>PDF, DOCX, or TXT</small>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card" style="text-align:center; padding:30px;">
            <div style="font-size:2.5rem;">🧠</div>
            <strong>AI Analysis</strong><br/>
            <small>Scores, summaries & insights</small>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card" style="text-align:center; padding:30px;">
            <div style="font-size:2.5rem;">📥</div>
            <strong>Export Report</strong><br/>
            <small>Download PDF report</small>
        </div>
        """, unsafe_allow_html=True)

    st.info("👆 Use the top header to upload your research paper and get started.")
    st.stop()


# ── Processing pipeline ───────────────────────────────────────────────────────
with st.spinner("🔄 Extracting text from document…"):
    raw_text = extract_text(uploaded_file)

if not raw_text or len(raw_text.strip()) < 100:
    st.error("❌ Could not extract enough text from this file. Please try a different document.")
    st.stop()

with st.spinner("🧹 Cleaning and preprocessing text…"):
    clean = clean_text(raw_text)

with st.spinner("🗂️ Detecting sections…"):
    sections = extract_sections(clean)
    section_stats = get_section_stats(sections)

with st.spinner("📝 Generating summaries…"):
    summaries = summarize_sections(sections, num_sentences=num_summary_sentences)

with st.spinner("📊 Analyzing writing quality…"):
    analysis = full_analysis(clean)

st.success(f"✅ Analysis complete! Detected **{len(sections)}** sections, **{analysis['word_count']:,}** words.")


# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📊 Dashboard",
    "🗂️ Sections & Summaries",
    "⚠️ Issues & Suggestions",
    "🔑 Keywords",
    "📄 Export Report",
    "🔍 Raw Text",
])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("## 📊 Writing Quality Dashboard")

    # Score badges row
    cols = st.columns(5)
    metrics = [
        ("Language", analysis['language']),
        ("Coherence", analysis['coherence']),
        ("Reasoning", analysis['reasoning']),
        ("Lexical", analysis['lexical']),
        ("Readability", analysis['readability']),
    ]
    for col, (label, val) in zip(cols, metrics):
        with col:
            st.markdown(score_badge(label, val), unsafe_allow_html=True)

    st.markdown("---")
    col_left, col_right = st.columns([1, 1])

    # Radar chart
    with col_left:
        st.markdown("### 🕸️ Quality Radar")
        labels = [m[0] for m in metrics]
        values = [m[1] for m in metrics]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill='toself',
            fillcolor='rgba(30,100,200,0.15)',
            line=dict(color='#1e64c8', width=2),
            name='Scores'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100],
                                tickfont=dict(size=9), gridcolor='#dde'),
                angularaxis=dict(tickfont=dict(size=11, color='#333'))
            ),
            showlegend=False,
            margin=dict(t=20, b=20, l=40, r=40),
            height=340,
            paper_bgcolor='white',
            plot_bgcolor='white',
        )
        st.plotly_chart(fig_radar, width='stretch')

    # Bar chart
    with col_right:
        st.markdown("### 📈 Score Breakdown")
        df_scores = pd.DataFrame({'Metric': labels, 'Score': values})
        fig_bar = px.bar(
            df_scores, x='Score', y='Metric', orientation='h',
            color='Score',
            color_continuous_scale=['#ef4444', '#f59e0b', '#22c55e'],
            range_color=[0, 100],
            text='Score'
        )
        fig_bar.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        fig_bar.update_layout(
            xaxis=dict(range=[0, 110], title=''),
            yaxis=dict(title=''),
            coloraxis_showscale=False,
            margin=dict(t=10, b=10, l=10, r=40),
            height=340,
            paper_bgcolor='white',
            plot_bgcolor='#f8faff',
        )
        st.plotly_chart(fig_bar, width='stretch')

    # Quick stats
    st.markdown("---")
    st.markdown("### 📋 Document Statistics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📄 Words", f"{analysis['word_count']:,}")
    c2.metric("✏️ Sentences", f"{analysis['sentence_count']:,}")
    c3.metric("🗂️ Sections", len(sections))
    sentiment_emoji = {'Positive': '😊', 'Negative': '😟', 'Neutral': '😐'}
    c4.metric("🧭 Sentiment", f"{sentiment_emoji.get(analysis['sentiment_label'], '')} {analysis['sentiment_label']}")

    # Section word counts
    if section_stats:
        st.markdown("### 📏 Section Length Distribution")
        df_sections = pd.DataFrame(
            list(section_stats.items()), columns=['Section', 'Words']
        ).sort_values('Words', ascending=False)
        fig_sec = px.bar(
            df_sections, x='Section', y='Words',
            color='Words', color_continuous_scale='Blues',
            text='Words'
        )
        fig_sec.update_traces(textposition='outside')
        fig_sec.update_layout(
            coloraxis_showscale=False,
            margin=dict(t=10, b=10),
            height=280,
            paper_bgcolor='white',
            plot_bgcolor='#f8faff',
        )
        st.plotly_chart(fig_sec, width='stretch')


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SECTIONS & SUMMARIES
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("## 🗂️ Detected Sections & Summaries")

    if not sections:
        st.warning("No standard academic sections were detected. Showing full-text summary.")
    else:
        for section, content in sections.items():
            if section.lower() == 'references':
                continue
            with st.expander(f"📌 {section}  —  {section_stats.get(section, 0):,} words", expanded=False):
                col_s, col_c = st.columns([1, 1])
                with col_s:
                    st.markdown("**📝 Summary**")
                    summary = summaries.get(section, '')
                    if summary:
                        st.info(summary)
                    else:
                        st.caption("Summary not available.")
                with col_c:
                    st.markdown("**📖 Original Text (first 800 chars)**")
                    st.text_area(
                        label="Original text",
                        value=content[:800] + ('…' if len(content) > 800 else ''),
                        height=160,
                        disabled=True,
                        key=f"sec_{section}",
                        label_visibility="collapsed"
                    )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ISSUES & SUGGESTIONS
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("## ⚠️ Writing Issues & Vocabulary Suggestions")

    col_i, col_v = st.columns([1, 1])

    with col_i:
        st.markdown("### 🔍 Issues Detected")
        if analysis['issues']:
            for issue in analysis['issues']:
                st.markdown(f"""
                <div class="issue-card">
                    <strong>{issue['type']}</strong> &nbsp;
                    <span style="background:#fde68a;border-radius:10px;padding:1px 8px;font-size:0.8rem;">{issue['count']}</span><br/>
                    <small>{issue['detail']}</small>
                </div>
                """, unsafe_allow_html=True)
                if issue.get('examples'):
                    for ex in issue['examples']:
                        with st.expander("Example sentence"):
                            st.write(ex)
        else:
            st.success("✅ No major writing issues detected!")

    with col_v:
        st.markdown("### 💡 Vocabulary Suggestions")
        suggestions = analysis['vocab_suggestions']
        if suggestions:
            st.markdown("Consider replacing these words for a more academic tone:")
            for weak, strong in suggestions:
                st.markdown(f"""
                <span class="suggestion-pill">
                    <del style="color:#999;">{weak}</del> → <strong>{strong}</strong>
                </span>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Vocabulary looks strong!")

        st.markdown("---")
        st.markdown("### 🧭 Sentiment Analysis")
        sent_label = analysis['sentiment_label']
        sent_score = analysis['sentiment_score']
        sent_colors = {'Positive': '#22c55e', 'Negative': '#ef4444', 'Neutral': '#f59e0b'}
        color = sent_colors.get(sent_label, '#888')
        sent_emoji_map = {'Positive': '😊', 'Negative': '😟', 'Neutral': '😐'}
        sent_emoji = sent_emoji_map.get(sent_label, '')
        st.markdown(f"""
        <div style="text-align:center; padding:20px;">
            <div style="font-size:3rem;">{sent_emoji}</div>
            <div style="font-size:1.4rem; font-weight:700; color:{color};">{sent_label}</div>
            <div style="color:#666; font-size:0.9rem;">Polarity score: {sent_score:+.2f}</div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — KEYWORDS
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("## 🔑 Top Keywords & Frequency Analysis")

    word_freq = analysis['word_freq']
    if word_freq:
        df_wf = pd.DataFrame(word_freq, columns=['Word', 'Count'])

        col_wf1, col_wf2 = st.columns([1, 1])

        with col_wf1:
            st.markdown("### 📊 Top 15 Keywords")
            fig_wf = px.bar(
                df_wf.head(15), x='Count', y='Word', orientation='h',
                color='Count', color_continuous_scale='Blues',
                text='Count'
            )
            fig_wf.update_traces(textposition='outside')
            fig_wf.update_layout(
                yaxis=dict(autorange='reversed'),
                coloraxis_showscale=False,
                margin=dict(t=10, b=10),
                height=380,
                paper_bgcolor='white',
                plot_bgcolor='#f8faff',
            )
            st.plotly_chart(fig_wf, width='stretch')

        with col_wf2:
            st.markdown("### ☁️ Keyword Table")
            st.dataframe(
                df_wf,
                width='stretch',
                hide_index=True,
            )
    else:
        st.warning("No keyword data available.")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — EXPORT REPORT
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("## 📄 Export Analysis Report")

    st.markdown("""
    Generate a comprehensive PDF report containing:
    - 📊 All writing quality scores
    - 🗂️ Section summaries
    - ⚠️ Writing issues
    - 💡 Vocabulary suggestions
    - 🔑 Top keywords
    """)

    # Store generated PDF in session state so download_button persists across reruns
    if 'pdf_report_bytes' not in st.session_state:
        st.session_state.pdf_report_bytes = None
    if 'pdf_report_name' not in st.session_state:
        st.session_state.pdf_report_name = None

    if st.button("🚀 Generate PDF Report", type="primary", use_container_width=True):
        with st.spinner("Generating PDF report…"):
            try:
                pdf_bytes = generate_report(
                    filename=uploaded_file.name,
                    analysis=analysis,
                    sections=sections,
                    summaries=summaries,
                )
                st.session_state.pdf_report_bytes = pdf_bytes
                st.session_state.pdf_report_name = f"WriteWell_Research_AI_Report_{uploaded_file.name.rsplit('.', 1)[0]}.pdf"
                st.success("✅ Report generated! Click the button below to download.")
            except Exception as e:
                st.session_state.pdf_report_bytes = None
                st.error(f"Report generation failed: {e}")

    if st.session_state.pdf_report_bytes is not None:
        st.download_button(
            label="📥 Download PDF Report",
            data=st.session_state.pdf_report_bytes,
            file_name=st.session_state.pdf_report_name,
            mime="application/pdf",
            use_container_width=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 — RAW TEXT
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("## 🔍 Extracted Text")
    st.caption(f"Total characters: {len(clean):,}")
    st.text_area(
        "Cleaned text",
        value=clean,
        height=500,
        disabled=not show_raw_text,
        key="raw_text_area"
    )
    if not show_raw_text:
        st.caption("Enable 'Show extracted raw text' in the top header options to edit.")
