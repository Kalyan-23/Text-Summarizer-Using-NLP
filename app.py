import streamlit as st
import pandas as pd
import re
import time
import math
from collections import Counter
from heapq import nlargest


# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title  = "TEXT SUMMARIZE · NLP TEXT SUMMARIZATION · PURE PYTHON",
    page_icon   = "⚡",
    layout      = "wide",
    initial_sidebar_state = "expanded",
)


# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS  —  Neon-Cyber theme
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@300;400;600&display=swap');

:root {
    --neon-cyan   : #00f5ff;
    --neon-pink   : #ff006e;
    --neon-green  : #39ff14;
    --neon-purple : #bf00ff;
    --neon-yellow : #fff700;
    --bg-dark     : #020408;
    --bg-panel    : #060d14;
    --bg-card     : #0a1628;
    --border      : rgba(0, 245, 255, 0.25);
    --text-dim    : rgba(0, 245, 255, 0.55);
}

html, body, [data-testid="stAppViewContainer"] {
    background  : var(--bg-dark)    !important;
    color       : var(--neon-cyan)  !important;
    font-family : 'Rajdhani', sans-serif !important;
}

[data-testid="stAppViewContainer"]::before {
    content          : '';
    position         : fixed;
    inset            : 0;
    background-image :
        linear-gradient(rgba(0, 245, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 245, 255, 0.03) 1px, transparent 1px);
    background-size  : 40px 40px;
    pointer-events   : none;
    z-index          : 0;
}

[data-testid="stSidebar"] {
    background   : var(--bg-panel) !important;
    border-right : 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--neon-cyan) !important; }

h1, h2, h3 { font-family: 'Orbitron', monospace !important; }
h1 {
    color       : var(--neon-cyan) !important;
    text-shadow : 0 0 20px var(--neon-cyan), 0 0 40px rgba(0, 245, 255, 0.4) !important;
}
h2 {
    color       : var(--neon-pink) !important;
    text-shadow : 0 0 15px var(--neon-pink) !important;
}
h3 {
    color       : var(--neon-green) !important;
    text-shadow : 0 0 10px var(--neon-green) !important;
}

.stButton > button {
    background   : transparent !important;
    border       : 1px solid var(--neon-cyan) !important;
    color        : var(--neon-cyan) !important;
    font-family  : 'Orbitron', monospace !important;
    font-size    : 0.75rem !important;
    letter-spacing : 2px !important;
    text-transform : uppercase !important;
    padding      : 0.6rem 1.5rem !important;
    transition   : all 0.2s ease !important;
    box-shadow   : 0 0 10px rgba(0, 245, 255, 0.2),
                   inset 0 0 10px rgba(0, 245, 255, 0.05) !important;
}
.stButton > button:hover {
    background : rgba(0, 245, 255, 0.1) !important;
    box-shadow : 0 0 25px rgba(0, 245, 255, 0.5),
                 inset 0 0 15px rgba(0, 245, 255, 0.1) !important;
    transform  : translateY(-1px) !important;
}

textarea, .stTextArea textarea {
    background  : var(--bg-card) !important;
    border      : 1px solid var(--border) !important;
    color       : #e0f7ff !important;
    font-family : 'Share Tech Mono', monospace !important;
    font-size   : 0.85rem !important;
    caret-color : var(--neon-cyan) !important;
}
textarea:focus, .stTextArea textarea:focus {
    border-color : var(--neon-cyan) !important;
    box-shadow   : 0 0 15px rgba(0, 245, 255, 0.3) !important;
}

.stSlider [data-baseweb="slider"] { background: rgba(0, 245, 255, 0.1) !important; }
.stSelectbox [data-baseweb="select"] > div {
    background : var(--bg-card) !important;
    border     : 1px solid var(--border) !important;
    color      : var(--neon-cyan) !important;
}

[data-testid="stMetric"] {
    background    : var(--bg-card) !important;
    border        : 1px solid var(--border) !important;
    border-radius : 4px !important;
    padding       : 1rem !important;
    box-shadow    : 0 0 15px rgba(0, 245, 255, 0.1) !important;
}
[data-testid="stMetricLabel"] {
    color       : var(--text-dim) !important;
    font-family : 'Orbitron', monospace !important;
    font-size   : 0.65rem !important;
}
[data-testid="stMetricValue"] {
    color       : var(--neon-cyan) !important;
    font-family : 'Orbitron', monospace !important;
    text-shadow : 0 0 10px var(--neon-cyan) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background    : transparent !important;
    border-bottom : 1px solid var(--border) !important;
    gap           : 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background     : transparent !important;
    color          : var(--text-dim) !important;
    font-family    : 'Orbitron', monospace !important;
    font-size      : 0.65rem !important;
    letter-spacing : 1.5px !important;
    border         : none !important;
}
.stTabs [aria-selected="true"] {
    color         : var(--neon-cyan) !important;
    background    : rgba(0, 245, 255, 0.08) !important;
    border-bottom : 2px solid var(--neon-cyan) !important;
    text-shadow   : 0 0 8px var(--neon-cyan) !important;
}

.stProgress > div > div {
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-pink)) !important;
}
.stAlert {
    background   : var(--bg-card) !important;
    border-left  : 3px solid var(--neon-cyan) !important;
    color        : var(--neon-cyan) !important;
}
.streamlit-expanderHeader {
    color       : var(--neon-pink) !important;
    font-family : 'Orbitron', monospace !important;
    font-size   : 0.7rem !important;
}
::-webkit-scrollbar       { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-dark); }
::-webkit-scrollbar-thumb { background: var(--neon-cyan); border-radius: 2px; }

.dataframe { background: var(--bg-card) !important; color: var(--neon-cyan) !important; }
thead th {
    background  : rgba(0, 245, 255, 0.1) !important;
    color       : var(--neon-pink) !important;
    font-family : 'Orbitron', monospace !important;
    font-size   : 0.65rem !important;
}
.stRadio label { color: var(--neon-cyan) !important; }
hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  NLP ENGINE
# ═════════════════════════════════════════════════════════════════════════════

def sent_tokenize(text: str) -> list:
    text    = text.strip()
    pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s+'
    parts   = re.split(pattern, text)
    return [s.strip() for s in parts if s.strip()]


STOPWORDS = set("""
a an the and or but if in on at to for of with by from as is was are were be been
being have has had do does did will would could should may might shall can
not no nor so yet both either neither each few more most other some such only own
same than too very s t just don doesn didn wasn isn aren wouldn couldn hadn shouldn
mustn i me my myself we our ours ourselves you your yours yourself he him his
himself she her hers herself it its itself they them their theirs themselves what
which who whom this that these those am about above after again against all also
any because before between both down during further how into once since still
through under until upon when where while who with i'd i'll i'm i've let's
she'd she'll she's that'll that's there's they'd they'll they're they've
we'd we'll we're we've what's when's where's who'd who'll who's why's
you'd you'll you're you've
""".split())


def clean_word(w: str) -> str:
    return re.sub(r'[^a-z]', '', w.lower())


def word_freq(sentences: list) -> dict:
    freq = {}
    for sent in sentences:
        for word in sent.split():
            w = clean_word(word)
            if w and w not in STOPWORDS and len(w) > 1:
                freq[w] = freq.get(w, 0) + 1
    if not freq:
        return freq
    max_f = max(freq.values())
    return {w: v / max_f for w, v in freq.items()}


def sentence_scores(sentences: list, freq: dict) -> dict:
    scores = {}
    for sent in sentences:
        for word in sent.split():
            w = clean_word(word)
            if w in freq:
                scores[sent] = scores.get(sent, 0) + freq[w]
    return scores


def tfidf_scores(sentences: list) -> dict:
    n       = len(sentences)
    tf_list = []
    df      = {}
    for sent in sentences:
        words = [
            clean_word(w) for w in sent.split()
            if clean_word(w) and clean_word(w) not in STOPWORDS
        ]
        total = len(words) or 1
        tf    = {w: words.count(w) / total for w in set(words)}
        tf_list.append(tf)
        for w in set(words):
            df[w] = df.get(w, 0) + 1

    scores = {}
    for i, sent in enumerate(sentences):
        score = 0.0
        for w, tf_val in tf_list[i].items():
            idf    = math.log((n + 1) / (df.get(w, 0) + 1))
            score += tf_val * idf
        scores[sent] = score
    return scores


def cosine_sim(vec1: dict, vec2: dict) -> float:
    common = set(vec1) & set(vec2)
    if not common:
        return 0.0
    num = sum(vec1[w] * vec2[w] for w in common)
    den = (
        math.sqrt(sum(v ** 2 for v in vec1.values())) *
        math.sqrt(sum(v ** 2 for v in vec2.values()))
    )
    return num / den if den else 0.0


def sent_vector(sent: str, freq: dict) -> dict:
    vec = {}
    for w in sent.split():
        cw = clean_word(w)
        if cw in freq:
            vec[cw] = vec.get(cw, 0) + freq[cw]
    return vec


def lexrank_scores(sentences: list, freq: dict, iterations: int = 20) -> dict:
    vecs = [sent_vector(s, freq) for s in sentences]
    n    = len(sentences)
    sim  = [[cosine_sim(vecs[i], vecs[j]) for j in range(n)] for i in range(n)]
    for i in range(n):
        row_sum = sum(sim[i]) or 1
        sim[i]  = [v / row_sum for v in sim[i]]

    scores = [1.0 / n] * n
    d      = 0.85
    for _ in range(iterations):
        scores = [
            (1 - d) / n + d * sum(sim[j][i] * scores[j] for j in range(n))
            for i in range(n)
        ]
    return {sentences[i]: scores[i] for i in range(n)}


def textrank_scores(sentences: list) -> dict:
    freq = word_freq(sentences)
    return lexrank_scores(sentences, freq)


def summarize(text: str, method: str, ratio: float = 0.3, max_sentences: int = 5) -> dict:
    sentences = sent_tokenize(text)
    if len(sentences) < 2:
        return {
            "summary"       : text,
            "selected"      : sentences,
            "all_sentences" : sentences,
            "scores"        : {},
        }

    n_select = max(1, min(max_sentences, round(len(sentences) * ratio)))

    if method == "Frequency (Baseline)":
        freq   = word_freq(sentences)
        scores = sentence_scores(sentences, freq)
    elif method == "TF-IDF":
        scores = tfidf_scores(sentences)
    elif method == "TextRank":
        scores = textrank_scores(sentences)
    elif method == "LexRank":
        freq   = word_freq(sentences)
        scores = lexrank_scores(sentences, freq)
    else:
        freq   = word_freq(sentences)
        scores = sentence_scores(sentences, freq)

    selected = nlargest(n_select, sentences, key=lambda s: scores.get(s, 0))
    ordered  = [s for s in sentences if s in selected]
    summary  = " ".join(ordered)

    return {
        "summary"       : summary,
        "selected"      : set(ordered),
        "all_sentences" : sentences,
        "scores"        : scores,
    }


def text_stats(text: str) -> dict:
    words   = text.split()
    sents   = sent_tokenize(text)
    chars   = len(text)
    unique  = len(set(clean_word(w) for w in words if clean_word(w)))
    avg_wps = len(words) / len(sents) if sents else 0
    lexical = unique / len(words) if words else 0
    return {
        "words"              : len(words),
        "sentences"          : len(sents),
        "chars"              : chars,
        "unique_words"       : unique,
        "avg_words_per_sent" : round(avg_wps, 1),
        "lexical_diversity"  : round(lexical, 3),
    }


# ═════════════════════════════════════════════════════════════════════════════
#  NEW FEATURE ENGINES
# ═════════════════════════════════════════════════════════════════════════════

# ── 1. TOP KEYWORDS (TF-IDF based) ──────────────────────────────────────────

def top_keywords(text: str, n: int = 3) -> list:
    """Return top-n keywords by aggregated TF-IDF score."""
    sentences  = sent_tokenize(text)
    if not sentences:
        return []
    scores     = tfidf_scores(sentences)
    word_score: dict = {}
    for sent in sentences:
        s = scores.get(sent, 0)
        for word in sent.split():
            w = clean_word(word)
            if w and w not in STOPWORDS and len(w) > 2:
                word_score[w] = word_score.get(w, 0) + s
    return nlargest(n, word_score, key=lambda w: word_score[w])


# ── 2. READING TIME ESTIMATOR ────────────────────────────────────────────────

def reading_time(text: str, wpm: int = 200) -> dict:
    """Estimate reading time at given words-per-minute."""
    words   = len(text.split())
    minutes = words / wpm
    if minutes < 1:
        label = f"{int(minutes * 60)}s"
    else:
        m = int(minutes)
        s = int((minutes - m) * 60)
        label = f"{m}m {s}s" if s else f"{m} min"
    return {"minutes": round(minutes, 2), "label": label, "words": words}


# ── 3. SENTIMENT ANALYZER (lexicon-based, pure Python) ──────────────────────

POSITIVE_WORDS = set("""
good great excellent amazing wonderful fantastic outstanding brilliant superb
remarkable positive success successful achieve achievement improve improvement
benefit beneficial advantage gain advance progress innovation effective efficient
strong powerful leading top best better significant notable impressive valuable
important useful helpful clear simple easy robust accurate reliable fast quick
smart intelligent creative innovative diverse inclusive sustainable growth
optimistic hopeful confident proud happy joyful pleased delighted thrilled
exciting exciting revolutionary breakthrough pioneering transformative""".split())

NEGATIVE_WORDS = set("""
bad poor terrible awful horrible dreadful disappointing failure fail failed
problem problematic issue concern concerning risk risky dangerous harmful
negative loss losing difficult hard challenging complex complicated slow weak
limited restriction restrict barrier obstacle threat threatening wrong incorrect
error mistake flawed broken damage damaged crisis critical severe serious
concerning worrying alarming frustrating challenging uncertain unclear
ineffective inefficient costly expensive controversial controversial bias biased
unfair unjust dangerous harmful toxic corrupt corruption scandal""".split())

def analyze_sentiment(text: str) -> dict:
    """Lexicon-based sentiment: returns label, score, pos/neg counts."""
    words  = [clean_word(w) for w in text.split()]
    pos    = sum(1 for w in words if w in POSITIVE_WORDS)
    neg    = sum(1 for w in words if w in NEGATIVE_WORDS)
    total  = pos + neg or 1
    score  = (pos - neg) / total  # range -1 to +1
    if score > 0.15:
        label = "POSITIVE"
        color = "#39ff14"
        icon  = "▲"
    elif score < -0.15:
        label = "NEGATIVE"
        color = "#ff006e"
        icon  = "▼"
    else:
        label = "NEUTRAL"
        color = "#fff700"
        icon  = "◆"
    return {
        "label" : label,
        "color" : color,
        "icon"  : icon,
        "score" : round(score, 3),
        "pos"   : pos,
        "neg"   : neg,
    }


# ── 4. NAMED ENTITY EXTRACTOR (regex heuristics, no spaCy) ──────────────────

def extract_entities(text: str) -> dict:
    """
    Heuristic NER — no external libraries.
    Finds capitalised multi-word sequences and classifies by context.
    """
    # Organisations: known suffixes
    org_pattern    = r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\s+(?:Inc|Corp|Ltd|LLC|Co|Group|Institute|University|Foundation|Association|Organization|Agency|Bureau|Department|Ministry|Council|Committee|Commission|Authority|Bank|Fund)\b'
    # Locations: preceded by in/at/from/near or known geo words
    loc_pattern    = r'(?:in|at|from|near|across|throughout|within)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,2})'
    # Person-like: Title + Capitalised Name
    person_pattern = r'\b(?:Mr|Mrs|Ms|Dr|Prof|President|CEO|Minister|Senator|Director|Chief|Officer|Secretary|General|Colonel|Captain|Mayor)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\b'
    # Fallback capitalised phrases (2+ words) not caught above
    caps_pattern   = r'\b([A-Z][a-zA-Z]{2,}(?:\s+[A-Z][a-zA-Z]{2,})+)\b'

    orgs    = list(set(re.findall(org_pattern,    text)))
    locs    = list(set(m.strip() for m in re.findall(loc_pattern,    text)))
    persons = list(set(re.findall(person_pattern, text)))
    caps    = list(set(re.findall(caps_pattern,   text)))

    # Remove items already captured
    captured = set(orgs + locs + persons)
    misc     = [c for c in caps if c not in captured][:5]

    return {
        "persons": persons[:5],
        "orgs"   : orgs[:5],
        "locs"   : locs[:5],
        "misc"   : misc,
    }


# ═════════════════════════════════════════════════════════════════════════════
#  DATASET LOADER
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def load_dataset(file) -> pd.DataFrame:
    for enc in ('utf-8', 'utf-8-sig', 'latin-1', 'cp1252'):
        try:
            file.seek(0)
            df = pd.read_csv(file, encoding=enc)
            break
        except (UnicodeDecodeError, LookupError):
            continue
    else:
        file.seek(0)
        df = pd.read_csv(file, encoding='latin-1', errors='replace')

    df.columns = [c.strip().lower() for c in df.columns]
    rename = {}
    for col in df.columns:
        if col in ('article', 'body', 'content'):
            rename[col] = 'article'
        elif col in ('highlights', 'abstract', 'reference'):
            rename[col] = 'highlights'
        elif col == 'ctext':
            rename[col] = 'article'
        elif col == 'text':
            rename[col] = 'highlights'
    df.rename(columns=rename, inplace=True)
    return df


# ═════════════════════════════════════════════════════════════════════════════
#  HEADER
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="text-align:center; padding:1.5rem 0 0.5rem;">
  <div style="font-family:'Orbitron',monospace; font-size:0.65rem;
              letter-spacing:6px; color:rgba(0,245,255,0.5); margin-bottom:0.4rem;">
    ⚡ &nbsp; NLP ·  PROJECT · TEXT INTELLIGENCE SYSTEM &nbsp; ⚡
  </div>
  <h1 style="font-family:'Orbitron',monospace; font-size:2.8rem; margin:0;
             background:linear-gradient(90deg,#00f5ff,#ff006e,#00f5ff);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent;
             background-clip:text; text-shadow:none !important;">
    TEXT SUMMARIZE
  </h1>
  <div style="font-family:'Share Tech Mono',monospace; font-size:0.8rem;
              color:rgba(0,245,255,0.6); letter-spacing:3px;">
    NEURAL &nbsp; EXTRACTION &amp; UNDERSTANDING &nbsp; OF &nbsp;
    RELEVANT &nbsp; OPTIMISED &nbsp; NEWS
  </div>
  <div style="width:60%; height:1px;
              background:linear-gradient(90deg,transparent,#00f5ff,#ff006e,transparent);
              margin:1rem auto;"></div>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace; font-size:0.7rem; letter-spacing:3px;
                color:#ff006e; text-shadow:0 0 10px #ff006e; padding:0.5rem 0 1rem;">
      ▸ &nbsp; CONTROL MATRIX
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**ALGORITHM**")
    method = st.selectbox(
        "Select NLP Method",
        ["Frequency (Baseline)", "TF-IDF", "TextRank", "LexRank"],
        label_visibility="collapsed",
    )

    method_info = {
        "Frequency (Baseline)" : "Scores sentences by normalised term frequency. Fast & interpretable.",
        "TF-IDF"               : "Weights terms by frequency × inverse document frequency. Rewards rare informative terms.",
        "TextRank"             : "Graph-based ranking via cosine similarity — inspired by PageRank.",
        "LexRank"              : "Stochastic graph walk over sentence similarity matrix (power iteration).",
    }
    st.caption(method_info[method])

    st.markdown("---")
    st.markdown("**READING SPEED**")
    wpm = st.slider("Words per minute", 100, 400, 200, step=50)

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Orbitron',monospace; font-size:0.65rem; letter-spacing:2px;
                color:#39ff14; text-shadow:0 0 8px #39ff14;">
      ▸ &nbsp; DATASET UPLOAD
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload news_summary or CNN / DailyMail CSV",
        type=["csv"],
        help="Supports news_summary.csv (ctext / text) or CNN/DailyMail (article / highlights)",
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace; font-size:0.65rem;
                color:rgba(0,245,255,0.35); line-height:2;">
    STACK &nbsp; · &nbsp; Pure Python NLP<br>
    TOKENISER &nbsp; · &nbsp; Regex<br>
    SCORING &nbsp; · &nbsp; TF / TF-IDF<br>
    GRAPH &nbsp; · &nbsp; TextRank / LexRank<br>
    FEATURES &nbsp; · &nbsp; Keywords / Sentiment / NER / Time<br>
    UI &nbsp; · &nbsp; Streamlit + CSS<br>
    DATASET &nbsp; · &nbsp; news_summary / CNN-DM
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  TABS
# ═════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "⚡  SUMMARISE",
    "📡  DATASET EXPLORER",
    "🔬  ALGORITHM LAB",
    "🕘  HISTORY",
])


# ─────────────────────────────────────────────────────────────────────────────
#  TAB 1 · SUMMARISE
# ─────────────────────────────────────────────────────────────────────────────

DEMO_TEXT = (
    "The development of artificial intelligence has accelerated dramatically over the past decade, "
    "transforming industries from healthcare to finance. Researchers at leading universities and "
    "technology companies have made remarkable strides in natural language processing, enabling "
    "machines to understand and generate human language with unprecedented accuracy. Deep learning "
    "models, particularly transformer architectures, have become the backbone of modern AI systems. "
    "These models are trained on vast datasets containing billions of words, allowing them to capture "
    "complex linguistic patterns and contextual relationships. Despite these advances, significant "
    "challenges remain. AI systems still struggle with common-sense reasoning and can produce "
    "confident but incorrect outputs, a phenomenon researchers call hallucination. Questions about "
    "bias, fairness, and transparency in AI decision-making have also come to the forefront. "
    "Regulators worldwide are now exploring frameworks to ensure responsible AI deployment. "
    "The economic impact of AI is equally profound. Automation is reshaping labour markets, with "
    "some jobs disappearing while new roles emerge. Studies suggest that workers who collaborate "
    "effectively with AI tools see significant productivity gains. However, the transition requires "
    "substantial investment in retraining and education. Looking ahead, experts predict that AI "
    "capabilities will continue to expand, potentially achieving human-level performance across a "
    "broader range of cognitive tasks within the next two decades. The societal implications of "
    "such progress are immense, touching on questions of identity, creativity, and the very nature "
    "of intelligence."
)

with tab1:
    col_a, col_b = st.columns([1, 1], gap="medium")

    # ── Input panel ──────────────────────────────────────────────────────────
    with col_a:
        st.markdown("""
        <div style="font-family:'Orbitron',monospace; font-size:0.7rem; letter-spacing:3px;
                    color:#ff006e; text-shadow:0 0 10px #ff006e; margin-bottom:0.5rem;">
          INPUT &nbsp; TERMINAL
        </div>
        """, unsafe_allow_html=True)

        input_text = st.text_area(
            "Paste article text here",
            height=320,
            placeholder="// PASTE NEWS ARTICLE HERE\n// OR LOAD FROM DATASET →",
            label_visibility="collapsed",
        )

        c1, c2, c3 = st.columns(3)
        run_btn  = c1.button("⚡ PROCESS", use_container_width=True)
        clr_btn  = c2.button("↺ CLEAR",   use_container_width=True)
        demo_btn = c3.button("◈ DEMO",    use_container_width=True)

        if clr_btn:
            st.session_state.pop("summary_result",    None)
            st.session_state.pop("input_text_cache",  None)

        if demo_btn:
            st.session_state["demo_text"] = DEMO_TEXT
            st.rerun()

        if "demo_text" in st.session_state:
            input_text = st.session_state.pop("demo_text")

    # ── Output panel ─────────────────────────────────────────────────────────
    with col_b:
        st.markdown("""
        <div style="font-family:'Orbitron',monospace; font-size:0.7rem; letter-spacing:3px;
                    color:#00f5ff; text-shadow:0 0 10px #00f5ff; margin-bottom:0.5rem;">
          OUTPUT &nbsp; TERMINAL
        </div>
        """, unsafe_allow_html=True)

        if run_btn and input_text.strip():
            with st.spinner(""):
                prog = st.progress(0)
                for i in range(100):
                    time.sleep(0.005)
                    prog.progress(i + 1)
                result = summarize(input_text, method, 0.3, 5)
                st.session_state["summary_result"]   = result
                st.session_state["input_text_cache"] = input_text

                # ── Save to history ───────────────────────────────────────
                import datetime
                if "history" not in st.session_state:
                    st.session_state["history"] = []
                kws_h        = top_keywords(input_text, 3)
                sent_h       = analyze_sentiment(input_text)
                rt_h         = reading_time(input_text, wpm)
                orig_stats_h = text_stats(input_text)
                summ_stats_h = text_stats(result["summary"])
                st.session_state["history"].insert(0, {
                    "timestamp"  : datetime.datetime.now().strftime("%H:%M:%S"),
                    "method"     : method,
                    "orig_words" : orig_stats_h["words"],
                    "summ_words" : summ_stats_h["words"],
                    "sentences"  : summ_stats_h["sentences"],
                    "keywords"   : kws_h,
                    "sentiment"  : sent_h,
                    "read_time"  : rt_h["label"],
                    "snippet"    : input_text[:120].replace("\n", " ") + "…",
                    "summary"    : result["summary"],
                })
                prog.empty()

        if "summary_result" in st.session_state:
            res  = st.session_state["summary_result"]
            orig = st.session_state.get("input_text_cache", "")
            summ = res["summary"]

            st.markdown(f"""
            <div style="background:#0a1628; border:1px solid rgba(0,245,255,0.3);
                        border-left:3px solid #00f5ff; padding:1rem 1.2rem;
                        font-family:'Share Tech Mono',monospace; font-size:0.82rem;
                        line-height:1.8; color:#e0f7ff; min-height:200px;
                        box-shadow:0 0 20px rgba(0,245,255,0.1);">
              {summ}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Row 1: Core stats ─────────────────────────────────────────
            orig_stats = text_stats(orig)
            summ_stats = text_stats(summ)
            m1, m2, m3 = st.columns(3)
            m1.metric("ORIG WORDS",  orig_stats["words"])
            m2.metric("SUMM WORDS",  summ_stats["words"])
            m3.metric("SENTENCES",   summ_stats["sentences"])

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Row 2: New features panel ─────────────────────────────────
            st.markdown("""
            <div style="font-family:'Orbitron',monospace; font-size:0.6rem; letter-spacing:3px;
                        color:#bf00ff; text-shadow:0 0 8px #bf00ff; margin-bottom:0.6rem;">
              ▸ &nbsp; INTELLIGENCE &nbsp; FEATURES
            </div>
            """, unsafe_allow_html=True)

            fa, fb, fc, fd = st.columns(4)

            # -- Feature 1: Top Keywords --
            kws = top_keywords(orig, n=3)
            kw_html = " &nbsp;·&nbsp; ".join(
                f'<span style="color:#00f5ff;">{k}</span>' for k in kws
            ) if kws else "—"
            fa.markdown(f"""
            <div style="background:#0a1628; border:1px solid rgba(0,245,255,0.25);
                        border-top:2px solid #00f5ff; padding:0.8rem; border-radius:4px;
                        box-shadow:0 0 10px rgba(0,245,255,0.1);">
              <div style="font-family:'Orbitron',monospace; font-size:0.55rem;
                          letter-spacing:2px; color:rgba(0,245,255,0.55); margin-bottom:0.4rem;">
                TOP KEYWORDS
              </div>
              <div style="font-family:'Share Tech Mono',monospace; font-size:0.78rem;
                          line-height:1.8;">
                {kw_html}
              </div>
            </div>
            """, unsafe_allow_html=True)

            # -- Feature 2: Reading Time --
            orig_rt = reading_time(orig, wpm)
            summ_rt = reading_time(summ, wpm)
            fb.markdown(f"""
            <div style="background:#0a1628; border:1px solid rgba(57,255,20,0.25);
                        border-top:2px solid #39ff14; padding:0.8rem; border-radius:4px;
                        box-shadow:0 0 10px rgba(57,255,20,0.1);">
              <div style="font-family:'Orbitron',monospace; font-size:0.55rem;
                          letter-spacing:2px; color:rgba(57,255,20,0.6); margin-bottom:0.4rem;">
                READING TIME
              </div>
              <div style="font-family:'Share Tech Mono',monospace; font-size:0.78rem;
                          color:#39ff14; line-height:1.8;">
                Original &nbsp;→&nbsp; <b>{orig_rt['label']}</b><br>
                Summary &nbsp;→&nbsp; <b>{summ_rt['label']}</b>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # -- Feature 3: Sentiment --
            sent_data = analyze_sentiment(orig)
            fc.markdown(f"""
            <div style="background:#0a1628; border:1px solid rgba(255,0,110,0.25);
                        border-top:2px solid {sent_data['color']}; padding:0.8rem; border-radius:4px;
                        box-shadow:0 0 10px rgba(255,0,110,0.1);">
              <div style="font-family:'Orbitron',monospace; font-size:0.55rem;
                          letter-spacing:2px; color:rgba(255,0,110,0.6); margin-bottom:0.4rem;">
                SENTIMENT
              </div>
              <div style="font-family:'Orbitron',monospace; font-size:1rem;
                          color:{sent_data['color']}; text-shadow:0 0 8px {sent_data['color']};">
                {sent_data['icon']} &nbsp; {sent_data['label']}
              </div>
              <div style="font-family:'Share Tech Mono',monospace; font-size:0.68rem;
                          color:rgba(0,245,255,0.5); margin-top:0.2rem;">
                +{sent_data['pos']} pos &nbsp; -{sent_data['neg']} neg
              </div>
            </div>
            """, unsafe_allow_html=True)

            # -- Feature 4: Named Entities --
            entities = extract_entities(orig)
            all_ents = []
            for label, elist in [("P", entities["persons"]), ("O", entities["orgs"]), ("L", entities["locs"])]:
                color_map = {"P": "#bf00ff", "O": "#fff700", "L": "#00f5ff"}
                for e in elist[:2]:
                    all_ents.append(
                        f'<span style="background:rgba(0,245,255,0.08); color:{color_map[label]}; '
                        f'padding:0.1rem 0.35rem; border-radius:3px; font-size:0.7rem; '
                        f'border:1px solid {color_map[label]}44; margin:1px; display:inline-block;">'
                        f'[{label}] {e}</span>'
                    )
            ent_html = " ".join(all_ents) if all_ents else '<span style="color:rgba(0,245,255,0.4);">none detected</span>'
            fd.markdown(f"""
            <div style="background:#0a1628; border:1px solid rgba(191,0,255,0.25);
                        border-top:2px solid #bf00ff; padding:0.8rem; border-radius:4px;
                        box-shadow:0 0 10px rgba(191,0,255,0.1);">
              <div style="font-family:'Orbitron',monospace; font-size:0.55rem;
                          letter-spacing:2px; color:rgba(191,0,255,0.6); margin-bottom:0.4rem;">
                NAMED ENTITIES
              </div>
              <div style="line-height:1.9;">
                {ent_html}
              </div>
              <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem;
                          color:rgba(0,245,255,0.35); margin-top:0.3rem;">
                [P] person &nbsp; [O] org &nbsp; [L] location
              </div>
            </div>
            """, unsafe_allow_html=True)

        elif run_btn and not input_text.strip():
            st.warning("⚠  No input text detected. Paste an article or press DEMO.")

    # ── Sentence saliency map ─────────────────────────────────────────────────
    if "summary_result" in st.session_state:
        st.markdown("---")
        st.markdown("""
        <div style="font-family:'Orbitron',monospace; font-size:0.65rem; letter-spacing:3px;
                    color:#bf00ff; text-shadow:0 0 10px #bf00ff; margin-bottom:0.5rem;">
          ▸ &nbsp; SENTENCE &nbsp; SALIENCY &nbsp; MAP
        </div>
        """, unsafe_allow_html=True)

        res       = st.session_state["summary_result"]
        selected  = res["selected"]
        scores    = res["scores"]
        max_score = max(scores.values()) if scores else 1

        html_parts = []
        for sent in res["all_sentences"]:
            sc   = scores.get(sent, 0)
            norm = sc / max_score if max_score else 0

            if sent in selected:
                opacity = 0.15 + 0.35 * norm
                color   = "#00f5ff"
                border  = "border-left:3px solid #00f5ff;"
                glow    = f"box-shadow:0 0 {int(norm * 15) + 5}px rgba(0,245,255,{norm * 0.6:.2f});"
            else:
                opacity = 0.1
                color   = "rgba(0,245,255,0.4)"
                border  = "border-left:3px solid rgba(0,245,255,0.15);"
                glow    = ""

            html_parts.append(
                f'<span style="display:block; background:rgba(0,245,255,{opacity:.2f}); '
                f'{border} {glow} color:{color}; padding:0.4rem 0.8rem; margin:0.2rem 0; '
                f'font-family:Share Tech Mono,monospace; font-size:0.78rem; border-radius:2px;">'
                f'[{norm:.2f}] &nbsp; {sent}</span>'
            )

        st.markdown(
            '<div style="background:#060d14; padding:0.8rem; '
            'border:1px solid rgba(0,245,255,0.15); max-height:300px; overflow-y:auto;">'
            + "".join(html_parts) + "</div>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
#  TAB 2 · DATASET EXPLORER
# ─────────────────────────────────────────────────────────────────────────────

with tab2:
    if uploaded_file is None:
        st.markdown("""
        <div style="text-align:center; padding:3rem;
                    border:1px dashed rgba(0,245,255,0.25);
                    background:#060d14; border-radius:4px;">
          <div style="font-family:'Orbitron',monospace; font-size:1rem; color:#ff006e;
                      text-shadow:0 0 10px #ff006e; margin-bottom:0.5rem;">
            NO &nbsp; DATASET &nbsp; LOADED
          </div>
          <div style="font-family:'Share Tech Mono',monospace; font-size:0.78rem;
                      color:rgba(0,245,255,0.5); line-height:2;">
            Upload your CSV from the sidebar.<br>
            Supports: &nbsp; <b>news_summary.csv</b> &nbsp; (ctext / text columns)<br>
            or &nbsp; CNN / DailyMail &nbsp; (article / highlights columns).
          </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        with st.spinner("Parsing dataset …"):
            df = load_dataset(uploaded_file)

        st.markdown(f"""
        <div style="font-family:'Orbitron',monospace; font-size:0.65rem; letter-spacing:3px;
                    color:#39ff14; text-shadow:0 0 8px #39ff14;">
          ▸ &nbsp; DATASET LOADED &nbsp; · &nbsp; {len(df):,} RECORDS &nbsp; · &nbsp;
          COLUMNS: {list(df.columns)}
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TOTAL ROWS", f"{len(df):,}")
        c2.metric("COLUMNS",    len(df.columns))
        if 'article' in df.columns:
            avg_art = int(df['article'].dropna().apply(len).mean())
            c3.metric("AVG ARTICLE LEN", f"{avg_art:,} chars")
        if 'highlights' in df.columns:
            avg_hl = int(df['highlights'].dropna().apply(len).mean())
            c4.metric("AVG SUMMARY LEN", f"{avg_hl:,} chars")

        st.markdown("<br>", unsafe_allow_html=True)

        if 'article' in df.columns:
            idx = st.slider("Select sample article", 0, min(len(df) - 1, 999), 0)
            row = df.iloc[idx]

            headline = row.get('headlines', row.get('headline', ''))
            author   = row.get('author', '')
            if headline:
                author_span = (
                    f"<span style='color:rgba(0,245,255,0.4); font-size:0.6rem; "
                    f"margin-left:1rem;'>{author}</span>" if author else ""
                )
                st.markdown(f"""
                <div style="font-family:'Orbitron',monospace; font-size:0.75rem; color:#fff700;
                            text-shadow:0 0 8px #fff700; margin-bottom:0.3rem;">
                  {headline} {author_span}
                </div>
                """, unsafe_allow_html=True)

            col_x, col_y = st.columns(2, gap="medium")

            with col_x:
                st.markdown("""
                <div style="font-family:'Orbitron',monospace; font-size:0.65rem;
                            letter-spacing:2px; color:#ff006e;">
                  FULL &nbsp; ARTICLE
                </div>""", unsafe_allow_html=True)
                art = str(row.get('article', ''))
                st.markdown(f"""
                <div style="background:#0a1628; border:1px solid rgba(0,245,255,0.2);
                            padding:1rem; font-family:'Share Tech Mono',monospace;
                            font-size:0.75rem; line-height:1.7; color:#cce8f0;
                            height:300px; overflow-y:auto;">
                  {art[:3000]}{'…' if len(art) > 3000 else ''}
                </div>""", unsafe_allow_html=True)

            with col_y:
                st.markdown("""
                <div style="font-family:'Orbitron',monospace; font-size:0.65rem;
                            letter-spacing:2px; color:#00f5ff;">
                  SHORT &nbsp; SUMMARY &nbsp; (REFERENCE)
                </div>""", unsafe_allow_html=True)
                hl = str(row.get('highlights', 'N/A'))
                st.markdown(f"""
                <div style="background:#0a1628; border:1px solid rgba(0,245,255,0.2);
                            padding:1rem; font-family:'Share Tech Mono',monospace;
                            font-size:0.75rem; line-height:1.7; color:#cce8f0;
                            height:300px; overflow-y:auto;">
                  {hl}
                </div>""", unsafe_allow_html=True)

            if st.button("⚡ SUMMARISE THIS ARTICLE", use_container_width=True):
                result    = summarize(art, method, 0.3, 5)
                sent_data = analyze_sentiment(art)
                kws       = top_keywords(art, 3)
                rt_orig   = reading_time(art, wpm)
                rt_summ   = reading_time(result['summary'], wpm)
                entities  = extract_entities(art)

                st.markdown("""
                <div style="font-family:'Orbitron',monospace; font-size:0.65rem;
                            letter-spacing:2px; color:#39ff14; margin-top:1rem;">
                  GENERATED &nbsp; SUMMARY
                </div>""", unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background:#0a1628; border:1px solid rgba(57,255,20,0.3);
                            border-left:3px solid #39ff14; padding:1rem;
                            font-family:'Share Tech Mono',monospace; font-size:0.8rem;
                            line-height:1.8; color:#e0f7ff;
                            box-shadow:0 0 15px rgba(57,255,20,0.1);">
                  {result['summary']}
                </div>""", unsafe_allow_html=True)

                da, db, dc, dd = st.columns(4)
                da.metric("METHOD",       method.split()[0])
                db.metric("SENTENCES",    len(result['selected']))
                dc.metric("SENTIMENT",    f"{sent_data['icon']} {sent_data['label']}")
                dd.metric("READING TIME", f"{rt_orig['label']} → {rt_summ['label']}")

                kw_str = "  ·  ".join(kws) if kws else "—"
                st.caption(f"Keywords: {kw_str}")

        with st.expander("RAW DATA TABLE"):
            st.dataframe(df.head(50), use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
#  TAB 3 · ALGORITHM LAB
# ─────────────────────────────────────────────────────────────────────────────

with tab3:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace; font-size:0.65rem; letter-spacing:3px;
                color:#bf00ff; text-shadow:0 0 10px #bf00ff; margin-bottom:1rem;">
      ▸ &nbsp; COMPARE &nbsp; ALL &nbsp; 4 &nbsp; ALGORITHMS &nbsp; SIDE &nbsp; BY &nbsp; SIDE
    </div>
    """, unsafe_allow_html=True)

    lab_text = st.text_area(
        "Input text for comparison",
        height=150,
        placeholder="// ENTER TEXT TO COMPARE ALL METHODS …",
    )

    if st.button("⚡ RUN ALL ALGORITHMS", use_container_width=True):
        if lab_text.strip():
            methods   = ["Frequency (Baseline)", "TF-IDF", "TextRank", "LexRank"]
            results   = {}
            prog2     = st.progress(0)
            for i, m in enumerate(methods):
                results[m] = summarize(lab_text, m, 0.3, 5)
                prog2.progress(int((i + 1) / len(methods) * 100))
            prog2.empty()

            # Global features computed once
            sent_data = analyze_sentiment(lab_text)
            kws       = top_keywords(lab_text, 3)
            rt        = reading_time(lab_text, wpm)
            entities  = extract_entities(lab_text)

            # Global feature banner
            kw_html = " &nbsp;·&nbsp; ".join(
                f'<span style="color:#00f5ff;">{k}</span>' for k in kws
            ) if kws else "—"

            all_ents = []
            for label, elist, col in [("P", entities["persons"], "#bf00ff"),
                                       ("O", entities["orgs"],    "#fff700"),
                                       ("L", entities["locs"],    "#00f5ff")]:
                for e in elist[:2]:
                    all_ents.append(
                        f'<span style="background:rgba(0,245,255,0.06); color:{col}; '
                        f'padding:0.1rem 0.3rem; border-radius:3px; font-size:0.68rem; '
                        f'border:1px solid {col}44;">[{label}] {e}</span>'
                    )
            ent_html = " ".join(all_ents) if all_ents else "none detected"

            st.markdown(f"""
            <div style="background:#0a1628; border:1px solid rgba(191,0,255,0.3);
                        border-left:3px solid #bf00ff; padding:0.8rem 1.2rem;
                        margin-bottom:1rem; box-shadow:0 0 10px rgba(191,0,255,0.1);">
              <div style="font-family:'Orbitron',monospace; font-size:0.58rem;
                          letter-spacing:2px; color:#bf00ff; margin-bottom:0.5rem;">
                INTELLIGENCE SCAN &nbsp;·&nbsp; APPLIED TO INPUT TEXT
              </div>
              <div style="display:flex; gap:2rem; flex-wrap:wrap; font-family:'Share Tech Mono',monospace; font-size:0.75rem;">
                <span>
                  <span style="color:rgba(0,245,255,0.5);">KEYWORDS </span>{kw_html}
                </span>
                <span>
                  <span style="color:rgba(0,245,255,0.5);">SENTIMENT </span>
                  <span style="color:{sent_data['color']};">{sent_data['icon']} {sent_data['label']}</span>
                  <span style="color:rgba(0,245,255,0.4); font-size:0.65rem;">
                    &nbsp;(+{sent_data['pos']} / -{sent_data['neg']})
                  </span>
                </span>
                <span>
                  <span style="color:rgba(0,245,255,0.5);">READ TIME </span>
                  <span style="color:#39ff14;">{rt['label']}</span>
                </span>
                <span>
                  <span style="color:rgba(0,245,255,0.5);">ENTITIES </span>{ent_html}
                </span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            color_map = {
                "Frequency (Baseline)" : "#ff006e",
                "TF-IDF"               : "#00f5ff",
                "TextRank"             : "#39ff14",
                "LexRank"              : "#bf00ff",
            }
            for m in methods:
                summ    = results[m]["summary"]
                rt_summ = reading_time(summ, wpm)
                n_sents = len(results[m]["selected"])
                c       = color_map[m]
                st.markdown(f"""
                <div style="background:#0a1628; border:1px solid {c}33;
                            border-left:3px solid {c}; padding:0.8rem 1rem;
                            margin:0.6rem 0; box-shadow:0 0 10px {c}22;">
                  <div style="font-family:'Orbitron',monospace; font-size:0.6rem;
                              letter-spacing:2px; color:{c}; margin-bottom:0.4rem;">
                    {m.upper()} &nbsp;·&nbsp; {n_sents} SENTENCES &nbsp;·&nbsp; READ: {rt_summ['label']}
                  </div>
                  <div style="font-family:'Share Tech Mono',monospace; font-size:0.8rem;
                              color:#e0f7ff; line-height:1.75;">
                    {summ}
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Enter text first.")

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Orbitron',monospace; font-size:0.65rem; letter-spacing:3px;
                color:#fff700; text-shadow:0 0 8px #fff700; margin-bottom:0.8rem;">
      ▸ &nbsp; ALGORITHM &nbsp; EXPLAINER
    </div>
    """, unsafe_allow_html=True)

    explainers = {
        "Frequency (Baseline)" : {
            "complexity" : "O(n · m)",
            "desc"       : (
                "Counts how often each non-stopword appears in the document. "
                "Normalises by the maximum count. A sentence's score is the sum "
                "of its words' normalised frequencies. Simple, fast, and "
                "surprisingly effective for news text."
            ),
            "pros" : ["Very fast", "No parameters", "Easy to interpret"],
            "cons" : ["Ignores word importance across documents", "Biased toward long sentences"],
        },
        "TF-IDF" : {
            "complexity" : "O(n · m · log n)",
            "desc"       : (
                "Term Frequency × Inverse Document Frequency. Rewards words that "
                "are frequent in a sentence but rare across the whole document, "
                "emphasising distinctive and informative content."
            ),
            "pros" : ["Penalises common filler words", "Document-aware scoring"],
            "cons" : ["Treats document as a corpus of sentences (small IDF signal)", "Still bag-of-words"],
        },
        "TextRank" : {
            "complexity" : "O(n² · iter)",
            "desc"       : (
                "Builds a graph where nodes are sentences and edges are cosine "
                "similarity weights. Runs power iteration (similar to PageRank) "
                "to find the most 'central' sentences in the document."
            ),
            "pros" : ["Fully unsupervised", "Captures inter-sentence relationships", "Robust"],
            "cons" : ["O(n²) similarity matrix", "Slow on very long documents"],
        },
        "LexRank" : {
            "complexity" : "O(n² · iter)",
            "desc"       : (
                "Like TextRank but uses a stochastic adjacency matrix with a "
                "damping factor (0.85), making it a proper random-walk model "
                "over the sentence similarity graph."
            ),
            "pros" : ["Mathematically grounded", "Handles redundancy well", "Diverse summaries"],
            "cons" : ["Same quadratic bottleneck as TextRank", "Damping factor is a hyperparameter"],
        },
    }

    for alg, info in explainers.items():
        with st.expander(f"◈  {alg}  ·  {info['complexity']}"):
            pros = " &nbsp; · &nbsp; ".join(info["pros"])
            cons = " &nbsp; · &nbsp; ".join(info["cons"])
            st.markdown(f"""
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.78rem;
                        color:#cce8f0; line-height:1.8;">
              {info['desc']}<br><br>
              <span style="color:#39ff14;">✓ &nbsp; PROS :</span> &nbsp; {pros}<br>
              <span style="color:#ff006e;">✗ &nbsp; CONS :</span> &nbsp; {cons}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Orbitron',monospace; font-size:0.65rem; letter-spacing:3px;
                color:#00f5ff; text-shadow:0 0 8px #00f5ff; margin-bottom:0.8rem;">
      ▸ &nbsp; FEATURE &nbsp; EXPLAINER
    </div>
    """, unsafe_allow_html=True)

    feature_explainers = {
        "Top Keywords (TF-IDF)" : {
            "desc" : (
                "Aggregates per-word TF-IDF scores across all sentences, then returns "
                "the top-N highest scoring non-stopwords. These represent the most "
                "distinctive and informative terms in the document — the words that "
                "are common here but rare across other contexts."
            ),
            "use"  : "Topic identification, tag generation, search indexing.",
        },
        "Reading Time Estimator" : {
            "desc" : (
                "Divides word count by the configured words-per-minute (WPM) rate. "
                "Average adult silent reading speed is ~200–250 WPM. The sidebar "
                "slider lets you calibrate for your audience. Shown for both the "
                "original article and the generated summary."
            ),
            "use"  : "Content planning, UX copy, newsletter scheduling.",
        },
        "Sentiment Analyzer" : {
            "desc" : (
                "Pure lexicon-based approach: counts positive and negative keyword "
                "matches from curated word lists, computes a normalised score in "
                "[-1, +1], and classifies as POSITIVE / NEUTRAL / NEGATIVE. "
                "No model required — fast and transparent."
            ),
            "use"  : "News tone analysis, brand monitoring, editorial triage.",
        },
        "Named Entity Extractor" : {
            "desc" : (
                "Regex heuristic NER — no spaCy or NLTK needed. Detects persons "
                "(by title prefix), organisations (by legal suffix), and locations "
                "(by preposition context). Capitalised multi-word phrases not "
                "caught by the above rules are surfaced as MISC entities."
            ),
            "use"  : "Knowledge graph construction, article tagging, fact extraction.",
        },
    }

    for feat, info in feature_explainers.items():
        with st.expander(f"◈  {feat}"):
            st.markdown(f"""
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.78rem;
                        color:#cce8f0; line-height:1.8;">
              {info['desc']}<br><br>
              <span style="color:#fff700;">USE CASES :</span> &nbsp; {info['use']}
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  TAB 4 · HISTORY
# ─────────────────────────────────────────────────────────────────────────────

with tab4:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace; font-size:0.65rem; letter-spacing:3px;
                color:#fff700; text-shadow:0 0 8px #fff700; margin-bottom:1rem;">
      ▸ &nbsp; SUMMARISATION &nbsp; HISTORY &nbsp; · &nbsp; SESSION LOG
    </div>
    """, unsafe_allow_html=True)

    history = st.session_state.get("history", [])

    if not history:
        st.markdown("""
        <div style="text-align:center; padding:3rem;
                    border:1px dashed rgba(255,247,0,0.2);
                    background:#060d14; border-radius:4px;">
          <div style="font-family:'Orbitron',monospace; font-size:0.9rem; color:#fff700;
                      text-shadow:0 0 10px #fff700; margin-bottom:0.5rem;">
            NO &nbsp; HISTORY &nbsp; YET
          </div>
          <div style="font-family:'Share Tech Mono',monospace; font-size:0.75rem;
                      color:rgba(0,245,255,0.45); line-height:2;">
            Process an article in the SUMMARISE tab<br>
            and it will appear here automatically.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Clear history button
        hcol1, hcol2 = st.columns([4, 1])
        with hcol2:
            if st.button("✕ CLEAR HISTORY", use_container_width=True):
                st.session_state["history"] = []
                st.rerun()
        with hcol1:
            st.markdown(
                f'<div style="font-family:\'Share Tech Mono\',monospace; font-size:0.72rem; '
                f'color:rgba(0,245,255,0.5); padding-top:0.6rem;">'
                f'{len(history)} record(s) this session</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        for i, h in enumerate(history):
            sentiment_color = h["sentiment"]["color"]
            kw_str = " · ".join(h["keywords"]) if h["keywords"] else "—"
            method_colors = {
                "Frequency (Baseline)" : "#ff006e",
                "TF-IDF"               : "#00f5ff",
                "TextRank"             : "#39ff14",
                "LexRank"              : "#bf00ff",
            }
            mc = method_colors.get(h["method"], "#00f5ff")

            with st.expander(
                f"[{h['timestamp']}]  {h['method'].upper()}  ·  "
                f"{h['orig_words']} → {h['summ_words']} words  ·  "
                f"{h['sentiment']['icon']} {h['sentiment']['label']}  ·  {kw_str}"
            ):
                # Stat row
                ha, hb, hc, hd = st.columns(4)
                ha.metric("ORIG WORDS",  h["orig_words"])
                hb.metric("SUMM WORDS",  h["summ_words"])
                hc.metric("SENTENCES",   h["sentences"])
                hd.metric("READ TIME",   h["read_time"])

                st.markdown("<br>", unsafe_allow_html=True)

                # Feature badges row
                kw_badge = " &nbsp;·&nbsp; ".join(
                    f'<span style="color:#00f5ff;">{k}</span>' for k in h["keywords"]
                ) if h["keywords"] else "—"

                sent = h["sentiment"]
                ent_parts = []
                st.markdown(f"""
                <div style="display:flex; gap:1.5rem; flex-wrap:wrap;
                            font-family:'Share Tech Mono',monospace; font-size:0.73rem;
                            background:#060d14; padding:0.6rem 0.9rem; border-radius:4px;
                            border:1px solid rgba(0,245,255,0.1); margin-bottom:0.6rem;">
                  <span>
                    <span style="color:rgba(0,245,255,0.45); font-size:0.6rem;
                                 font-family:'Orbitron',monospace; letter-spacing:1px;">
                      ALGORITHM&nbsp;
                    </span>
                    <span style="color:{mc};">{h['method']}</span>
                  </span>
                  <span>
                    <span style="color:rgba(0,245,255,0.45); font-size:0.6rem;
                                 font-family:'Orbitron',monospace; letter-spacing:1px;">
                      KEYWORDS&nbsp;
                    </span>
                    {kw_badge}
                  </span>
                  <span>
                    <span style="color:rgba(0,245,255,0.45); font-size:0.6rem;
                                 font-family:'Orbitron',monospace; letter-spacing:1px;">
                      SENTIMENT&nbsp;
                    </span>
                    <span style="color:{sent['color']};">
                      {sent['icon']} {sent['label']} (+{sent['pos']} / -{sent['neg']})
                    </span>
                  </span>
                </div>
                """, unsafe_allow_html=True)

                # Article snippet
                st.markdown(f"""
                <div style="font-family:'Share Tech Mono',monospace; font-size:0.7rem;
                            color:rgba(0,245,255,0.4); background:#060d14; padding:0.5rem 0.8rem;
                            border-left:2px solid rgba(0,245,255,0.2); margin-bottom:0.5rem;
                            font-style:italic;">
                  {h['snippet']}
                </div>
                """, unsafe_allow_html=True)

                # Generated summary
                st.markdown(f"""
                <div style="background:#0a1628; border:1px solid {mc}33;
                            border-left:3px solid {mc}; padding:0.8rem 1rem;
                            font-family:'Share Tech Mono',monospace; font-size:0.8rem;
                            line-height:1.75; color:#e0f7ff;
                            box-shadow:0 0 10px {mc}22;">
                  <div style="font-family:'Orbitron',monospace; font-size:0.55rem;
                              letter-spacing:2px; color:{mc}; margin-bottom:0.4rem;">
                    GENERATED SUMMARY
                  </div>
                  {h['summary']}
                </div>
                """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div style="text-align:center; padding:2rem 0 0.5rem; margin-top:2rem;
            border-top:1px solid rgba(0,245,255,0.1);">
  <div style="font-family:'Share Tech Mono',monospace; font-size:0.65rem;
              color:rgba(0,245,255,0.3); letter-spacing:2px; line-height:2;">
    TEXT SUMMARIZE &nbsp; · &nbsp; NLP TEXT SUMMARIZATION &nbsp; · &nbsp; PURE PYTHON<br>
    ALGORITHMS : &nbsp; FREQUENCY &nbsp; · &nbsp; TF-IDF &nbsp; · &nbsp;
    TEXTRANK &nbsp; · &nbsp; LEXRANK<br>
    FEATURES : &nbsp; KEYWORDS &nbsp; · &nbsp; READING TIME &nbsp; · &nbsp;
    SENTIMENT &nbsp; · &nbsp; NAMED ENTITIES<br>
    DATASET : &nbsp; NEWS SUMMARY &nbsp; / &nbsp; CNN-DAILYMAIL
  </div>
</div>
""", unsafe_allow_html=True)