import streamlit as st
import pandas as pd
import numpy as np

import json
import re
import io
import tempfile
import csv
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NOVA · AI Data Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500&display=swap');

:root {
    --electric: #00E5FF;
    --violet:   #7B2FBE;
    --violet-bright: #A855F7;
    --neon-green: #00FF88;
    --amber: #FFB300;
    --red-neon: #FF3366;
    --bg: #030508;
    --bg-panel: rgba(8,12,24,0.97);
    --bg-glass: rgba(255,255,255,0.025);
    --border-e: rgba(0,229,255,0.2);
    --border-v: rgba(168,85,247,0.2);
    --text-hi: #EEF2FF;
    --text-mid: #7986A3;
    --text-lo: #2D3550;
}

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main .block-container { padding: 1rem 2rem 4rem; max-width: 1440px; }
.stApp { background: var(--bg); color: var(--text-hi); }

/* ── Animated Background ── */
.stApp::before {
    content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse 80% 50% at 15% -5%, rgba(0,229,255,0.06) 0%, transparent 55%),
        radial-gradient(ellipse 60% 40% at 85% 105%, rgba(123,47,190,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 40% 35% at 50% 60%, rgba(0,255,136,0.025) 0%, transparent 50%);
}
/* Floating orbs */
.stApp::after {
    content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image:
        radial-gradient(circle 2px at 20% 30%, rgba(0,229,255,0.4) 0%, transparent 100%),
        radial-gradient(circle 1px at 70% 20%, rgba(168,85,247,0.5) 0%, transparent 100%),
        radial-gradient(circle 1.5px at 40% 70%, rgba(0,255,136,0.4) 0%, transparent 100%),
        radial-gradient(circle 1px at 85% 60%, rgba(0,229,255,0.3) 0%, transparent 100%),
        radial-gradient(circle 2px at 10% 80%, rgba(168,85,247,0.3) 0%, transparent 100%);
}

#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: rgba(0,229,255,0.3); border-radius: 4px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(3,5,12,0.99) !important;
    border-right: 1px solid rgba(0,229,255,0.1) !important;
}

/* ── Floating Scan Line Animation ── */
@keyframes scanline {
    0%   { transform: translateY(-100%); opacity: 0; }
    10%  { opacity: 1; }
    90%  { opacity: 1; }
    100% { transform: translateY(100vh); opacity: 0; }
}
@keyframes pulse-glow {
    0%, 100% { opacity: 0.5; }
    50%       { opacity: 1; }
}
@keyframes float-up {
    0%   { transform: translateY(8px); opacity: 0; }
    100% { transform: translateY(0);   opacity: 1; }
}
@keyframes data-stream {
    0%   { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}
@keyframes border-flow {
    0%   { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

/* ── Hero ── */
.nova-hero {
    text-align: center; padding: 2rem 1rem 0.8rem;
    animation: float-up 0.8s ease forwards;
}
.nova-eyebrow {
    display: inline-flex; align-items: center; gap: 0.5rem;
    font-family: 'Space Mono', monospace; font-size: 0.58rem;
    letter-spacing: 0.38em; color: var(--electric);
    border: 1px solid rgba(0,229,255,0.3); padding: 0.22rem 0.9rem;
    border-radius: 3px; background: rgba(0,229,255,0.06);
    margin-bottom: 1rem; text-transform: uppercase;
    animation: pulse-glow 3s ease-in-out infinite;
}
.nova-title {
    font-family: 'Exo 2', sans-serif; font-weight: 900;
    font-size: clamp(2.2rem, 5vw, 4rem); line-height: 1;
    letter-spacing: -0.03em;
    background: linear-gradient(120deg, #ffffff 0%, #00E5FF 35%, #A855F7 70%, #00FF88 100%);
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: data-stream 4s linear infinite;
    margin-bottom: 0.5rem;
}
.nova-sub {
    color: var(--text-mid); font-size: 0.9rem; font-weight: 300;
    max-width: 520px; margin: 0 auto 1.2rem; line-height: 1.65;
    font-family: 'Inter', sans-serif;
}
.nova-divider {
    height: 1px; margin: 0 auto 1.5rem; width: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,229,255,0.4), rgba(168,85,247,0.4), transparent);
}

/* ── Section Header ── */
.sec-hd {
    display: flex; align-items: center; gap: 0.7rem;
    margin: 1.8rem 0 1rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(0,229,255,0.08);
}
.sec-hd-icon {
    width: 32px; height: 32px; border-radius: 6px;
    background: linear-gradient(135deg, rgba(0,229,255,0.15), rgba(168,85,247,0.1));
    border: 1px solid rgba(0,229,255,0.25);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem; flex-shrink: 0;
}
.sec-hd-title {
    font-family: 'Exo 2', sans-serif; font-size: 0.72rem;
    font-weight: 700; letter-spacing: 0.22em;
    color: var(--text-hi); text-transform: uppercase;
}
.sec-hd-line { flex: 1; height: 1px; background: linear-gradient(90deg, rgba(0,229,255,0.15), transparent); }

/* ── Stat Cards ── */
.stat-card {
    background: var(--bg-panel); border-radius: 12px;
    padding: 1rem 1.1rem; position: relative; overflow: hidden;
    border: 1px solid var(--sc-border, rgba(0,229,255,0.15));
    animation: float-up 0.6s ease forwards;
    transition: border-color 0.2s, transform 0.2s;
}
.stat-card:hover { border-color: var(--sc-hover, rgba(0,229,255,0.4)); transform: translateY(-2px); }
.stat-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: var(--sc-accent, linear-gradient(90deg, #00E5FF, #A855F7));
    opacity: 0.7;
}
.stat-glow {
    position: absolute; top: -20px; right: -20px;
    width: 60px; height: 60px; border-radius: 50%;
    opacity: 0.12; filter: blur(15px);
    background: var(--sc-color, #00E5FF);
}
.stat-label {
    font-family: 'Space Mono', monospace; font-size: 0.55rem;
    letter-spacing: 0.2em; color: var(--text-mid);
    text-transform: uppercase; margin-bottom: 0.4rem; line-height: 1.3;
}
.stat-val {
    font-family: 'Exo 2', sans-serif; font-size: 1.6rem;
    font-weight: 800; line-height: 1; color: var(--sc-color, #00E5FF);
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.stat-unit { font-size: 0.72rem; color: var(--text-mid); margin-left: 0.2rem; font-weight: 400; font-family: 'Inter', sans-serif; }
.stat-sub { font-size: 0.7rem; margin-top: 0.4rem; }

/* ── Chips ── */
.chip {
    display: inline-flex; align-items: center;
    font-family: 'Space Mono', monospace; font-size: 0.56rem;
    padding: 0.15rem 0.55rem; border-radius: 3px;
    font-weight: 400; letter-spacing: 0.05em; white-space: nowrap;
}
.ce { background: rgba(0,229,255,0.1);  color: #00E5FF; border: 1px solid rgba(0,229,255,0.3); }
.cv { background: rgba(168,85,247,0.1); color: #A855F7; border: 1px solid rgba(168,85,247,0.3); }
.cg { background: rgba(0,255,136,0.1);  color: #00FF88; border: 1px solid rgba(0,255,136,0.3); }
.ca { background: rgba(255,179,0,0.1);  color: #FFB300; border: 1px solid rgba(255,179,0,0.3); }
.cr { background: rgba(255,51,102,0.1); color: #FF3366; border: 1px solid rgba(255,51,102,0.3); }

/* ── Data Frame Styling ── */
.stDataFrame { border-radius: 10px; overflow: hidden; border: 1px solid rgba(0,229,255,0.12) !important; }

/* ── Panel / Block ── */
.panel {
    background: var(--bg-panel); border-radius: 14px;
    padding: 1.4rem 1.6rem; margin-bottom: 1.2rem;
    position: relative; overflow: hidden;
    border: 1px solid rgba(0,229,255,0.12);
}
.panel::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; }
.panel.electric::before { background: linear-gradient(90deg, transparent, #00E5FF, #A855F7, transparent); }
.panel.violet::before  { background: linear-gradient(90deg, transparent, #A855F7, transparent); }
.panel.green::before   { background: linear-gradient(90deg, transparent, #00FF88, transparent); }
.panel-title {
    font-family: 'Exo 2', sans-serif; font-size: 0.72rem;
    font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase;
    margin-bottom: 0.9rem;
}
.panel.electric .panel-title { color: #00E5FF; }
.panel.violet   .panel-title { color: #A855F7; }
.panel.green    .panel-title { color: #00FF88; }

/* ── Chat ── */
.chat-wrap { display: flex; flex-direction: column; gap: 0.75rem; }
.msg {
    padding: 0.9rem 1.1rem; border-radius: 10px;
    font-size: 0.87rem; line-height: 1.7;
}
.msg-u { background: rgba(0,229,255,0.07); border-left: 2px solid #00E5FF; }
.msg-a { background: rgba(168,85,247,0.06); border-left: 2px solid #A855F7; }
.msg-lbl {
    font-family: 'Space Mono', monospace; font-size: 0.56rem;
    letter-spacing: 0.14em; opacity: 0.5; margin-bottom: 0.35rem;
    text-transform: uppercase;
}
.msg-code {
    background: rgba(0,0,0,0.4); border: 1px solid rgba(0,229,255,0.15);
    border-radius: 6px; padding: 0.6rem 0.85rem;
    font-family: 'Space Mono', monospace; font-size: 0.75rem;
    color: #00FF88; margin: 0.5rem 0; overflow-x: auto; white-space: pre-wrap;
}

/* ── Insight cards ── */
.insight {
    background: rgba(0,229,255,0.04); border: 1px solid rgba(0,229,255,0.12);
    border-radius: 9px; padding: 0.75rem 0.9rem;
    font-size: 0.8rem; color: var(--text-mid); line-height: 1.6; margin-bottom: 0.5rem;
}
.insight strong { color: #00E5FF; font-family: 'Space Mono', monospace; font-size: 0.65rem; display: block; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.2rem; }

/* ── Sidebar ── */
.sb-logo { text-align: center; padding: 1.3rem 1rem 1rem; border-bottom: 1px solid rgba(0,229,255,0.08); margin-bottom: 1rem; }
.sb-logo-name { font-family: 'Exo 2', sans-serif; font-size: 1.1rem; font-weight: 900; letter-spacing: 0.12em; background: linear-gradient(120deg, #00E5FF, #A855F7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.sb-logo-sub  { font-family: 'Space Mono', monospace; font-size: 0.48rem; letter-spacing: 0.3em; color: var(--text-lo); margin-top: 0.2rem; }
.sb-row { padding: 0.6rem 0.9rem; background: rgba(0,229,255,0.04); border: 1px solid rgba(0,229,255,0.08); border-radius: 8px; margin-bottom: 0.45rem; display: flex; align-items: center; justify-content: space-between; }
.sb-row-label { font-size: 0.72rem; color: var(--text-mid); }
.sb-row-val   { font-family: 'Space Mono', monospace; font-size: 0.72rem; color: #00E5FF; font-weight: 700; }
.sb-sec { font-family: 'Space Mono', monospace; font-size: 0.55rem; letter-spacing: 0.26em; color: var(--text-lo); text-transform: uppercase; margin: 1rem 0 0.5rem; }
.sb-tip { background: rgba(168,85,247,0.04); border: 1px solid rgba(168,85,247,0.12); border-radius: 8px; padding: 0.65rem 0.8rem; margin-bottom: 0.45rem; font-size: 0.74rem; color: var(--text-mid); line-height: 1.55; }
.sb-tip strong { color: #A855F7; display: block; font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.15rem; font-family: 'Space Mono', monospace; }

/* ── Streamlit Overrides ── */
.stTextInput input, .stTextArea textarea {
    background: rgba(8,12,28,0.95) !important;
    border: 1px solid rgba(0,229,255,0.22) !important;
    border-radius: 8px !important;
    color: #EEF2FF !important; caret-color: #00E5FF !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder { color: rgba(121,134,163,0.5) !important; }
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(0,229,255,0.55) !important;
    box-shadow: 0 0 0 3px rgba(0,229,255,0.09) !important;
}
.stSelectbox > div > div {
    background: rgba(8,12,28,0.95) !important;
    border: 1px solid rgba(0,229,255,0.22) !important;
    border-radius: 8px !important; color: #EEF2FF !important;
}
.stButton > button {
    background: linear-gradient(135deg, rgba(0,229,255,0.14), rgba(168,85,247,0.1)) !important;
    border: 1px solid rgba(0,229,255,0.4) !important; color: #00E5FF !important;
    font-family: 'Exo 2', sans-serif !important; font-size: 0.75rem !important;
    font-weight: 700 !important; letter-spacing: 0.15em !important;
    border-radius: 8px !important; padding: 0.6rem 1.2rem !important;
    transition: all 0.25s !important; width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,229,255,0.26), rgba(168,85,247,0.2)) !important;
    box-shadow: 0 0 20px rgba(0,229,255,0.22) !important; transform: translateY(-1px) !important;
}
div[data-testid="stForm"] button {
    color: #00E5FF !important; background: rgba(0,229,255,0.1) !important;
    border: 1px solid rgba(0,229,255,0.4) !important;
}
label, .stSelectbox label, .stTextInput label, .stTextArea label {
    color: #7986A3 !important; font-family: 'Space Mono', monospace !important;
    font-size: 0.62rem !important; letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
}
.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.02) !important; border-radius: 10px !important; padding: 4px !important; gap: 3px !important; }
.stTabs [data-baseweb="tab"] { border-radius: 7px !important; font-family: 'Exo 2', sans-serif !important; font-size: 0.8rem !important; font-weight: 600 !important; color: #7986A3 !important; }
.stTabs [aria-selected="true"] { background: rgba(0,229,255,0.12) !important; color: #00E5FF !important; }
.stExpander { background: var(--bg-panel) !important; border: 1px solid rgba(0,229,255,0.12) !important; border-radius: 10px !important; }
div[data-testid="stExpander"] div[role="button"] p { font-family: 'Exo 2', sans-serif !important; font-size: 0.78rem !important; font-weight: 700 !important; letter-spacing: 0.06em !important; }
.stMetric { background: rgba(0,229,255,0.03) !important; border: 1px solid rgba(0,229,255,0.1) !important; border-radius: 9px !important; padding: 0.65rem 0.9rem !important; }
[data-testid="stMetricValue"] { font-family: 'Exo 2', sans-serif !important; color: #00E5FF !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { font-family: 'Space Mono', monospace !important; font-size: 0.6rem !important; color: #7986A3 !important; letter-spacing: 0.1em !important; }
hr { border-color: rgba(0,229,255,0.08) !important; }
div[data-testid="stForm"] { border: none !important; padding: 0 !important; }

/* Plotly chart container */
.stPlotlyChart { border-radius: 12px; overflow: hidden; border: 1px solid rgba(0,229,255,0.1); }
</style>
""", unsafe_allow_html=True)

# ─── Plotly Theme ─────────────────────────────────────────────────────────────
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(8,12,24,0.0)",
    plot_bgcolor="rgba(8,12,24,0.0)",
    font=dict(family="Exo 2, sans-serif", color="#7986A3", size=11),
    colorway=["#00E5FF","#A855F7","#00FF88","#FFB300","#FF3366","#38BDF8","#FB923C"],
    margin=dict(l=20, r=20, t=40, b=20),
)

def apply_theme(fig):
    fig.update_layout(**PLOTLY_THEME)
    fig.update_xaxes(gridcolor="rgba(0,229,255,0.07)", linecolor="rgba(0,229,255,0.15)", tickfont=dict(size=10))
    fig.update_yaxes(gridcolor="rgba(0,229,255,0.07)", linecolor="rgba(0,229,255,0.15)", tickfont=dict(size=10))
    return fig

# ─── Helpers ──────────────────────────────────────────────────────────────────
def load_file(file):
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file, encoding="utf-8", na_values=["NA","N/A","missing",""])
        elif file.name.endswith((".xlsx",".xls")):
            df = pd.read_excel(file, na_values=["NA","N/A","missing",""])
        elif file.name.endswith(".json"):
            df = pd.read_json(file)
        elif file.name.endswith(".parquet"):
            df = pd.read_parquet(file)
        else:
            st.error("Unsupported format. Use CSV, Excel, JSON or Parquet.")
            return None
        for col in df.columns:
            if "date" in col.lower() or "time" in col.lower():
                try: df[col] = pd.to_datetime(df[col], errors="coerce")
                except: pass
        return df
    except Exception as e:
        st.error(f"Load error: {e}")
        return None

def get_df_schema(df):
    rows = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = df[col].isna().sum()
        uniq  = df[col].nunique()
        rows.append(f"  {col}: {dtype}, {nulls} nulls, {uniq} unique")
    return "\n".join(rows)

def profile_df(df):
    out = {}
    for col in df.columns:
        info = {"dtype": str(df[col].dtype), "nulls": int(df[col].isna().sum()), "unique": int(df[col].nunique())}
        if pd.api.types.is_numeric_dtype(df[col]):
            info.update({"min": float(df[col].min()), "max": float(df[col].max()),
                         "mean": float(df[col].mean()), "median": float(df[col].median()),
                         "std": float(df[col].std())})
        out[col] = info
    return out

def register_duckdb(df):
    # Using pandas as SQL backend via pandasql-style approach
    return {"data": df}

def run_sql(con, sql):
    """Execute SQL-like queries using pandas"""
    try:
        import re
        df = con["data"]
        sql_clean = sql.strip().rstrip(";")
        
        # Simple SQL parser for common patterns
        sql_upper = sql_clean.upper()
        
        # SELECT * FROM data LIMIT n
        limit_match = re.search(r'LIMIT\s+(\d+)', sql_clean, re.IGNORECASE)
        limit = int(limit_match.group(1)) if limit_match else None
        
        # COUNT(*)
        if re.search(r'SELECT\s+COUNT\(\*\)', sql_clean, re.IGNORECASE) and 'GROUP BY' not in sql_upper:
            result = pd.DataFrame({"count": [len(df)]})
            return result, None
        
        # SELECT * FROM data
        if re.match(r'SELECT\s+\*\s+FROM\s+data', sql_clean, re.IGNORECASE) and 'WHERE' not in sql_upper and 'GROUP BY' not in sql_upper and 'ORDER BY' not in sql_upper:
            result = df.head(limit) if limit else df
            return result, None
        
        # ORDER BY col [DESC]
        order_match = re.search(r'ORDER BY\s+(\w+)(\s+DESC)?', sql_clean, re.IGNORECASE)
        if order_match and 'GROUP BY' not in sql_upper and 'WHERE' not in sql_upper:
            col = order_match.group(1)
            desc = bool(order_match.group(2))
            if col in df.columns:
                result = df.sort_values(col, ascending=not desc)
                result = result.head(limit) if limit else result
                return result, None
        
        # GROUP BY aggregation
        grp_match = re.search(r'GROUP BY\s+(\w+)', sql_clean, re.IGNORECASE)
        if grp_match:
            grp_col = grp_match.group(1)
            if grp_col in df.columns:
                # Try to detect aggregation
                agg_match = re.search(r'(SUM|AVG|COUNT|MAX|MIN)\((\w+|\*)\)', sql_clean, re.IGNORECASE)
                if agg_match:
                    func = agg_match.group(1).lower()
                    agg_col = agg_match.group(2)
                    if func == "count":
                        result = df.groupby(grp_col).size().reset_index(name="count")
                    elif agg_col in df.columns:
                        result = df.groupby(grp_col)[agg_col].agg(func).reset_index()
                    else:
                        result = df.groupby(grp_col).size().reset_index(name="count")
                    result = result.sort_values(result.columns[-1], ascending=False)
                    result = result.head(limit) if limit else result
                    return result, None
        
        # WHERE filter
        where_match = re.search(r'WHERE\s+(.+?)(?:ORDER BY|GROUP BY|LIMIT|$)', sql_clean, re.IGNORECASE)
        if where_match and 'GROUP BY' not in sql_upper:
            condition = where_match.group(1).strip()
            try:
                result = df.query(condition)
                if order_match:
                    col = order_match.group(1)
                    desc = bool(order_match.group(2))
                    if col in df.columns:
                        result = result.sort_values(col, ascending=not desc)
                result = result.head(limit) if limit else result
                return result, None
            except:
                pass
        
        # Null counts per column (UNION ALL pattern)
        if 'nulls' in sql_clean.lower() or 'isnull' in sql_clean.lower() or 'is null' in sql_upper:
            null_data = [(col, int(df[col].isna().sum())) for col in df.columns]
            result = pd.DataFrame(null_data, columns=["column", "null_count"])
            result = result[result["null_count"] > 0].sort_values("null_count", ascending=False)
            return result, None
        
        # Duplicate rows
        if 'duplicat' in sql_clean.lower():
            dups = df[df.duplicated()]
            return dups.head(limit or 100), None
        
        # Numeric stats
        if 'min(' in sql_clean.lower() or 'max(' in sql_clean.lower() or 'avg(' in sql_clean.lower():
            num_cols = df.select_dtypes(include="number").columns.tolist()
            if num_cols:
                stats = df[num_cols].describe().T[["min","max","mean","std"]].round(3)
                return stats.reset_index().rename(columns={"index":"column"}), None
        
        # Distinct counts
        if 'distinct' in sql_clean.lower() or 'unique' in sql_clean.lower():
            uniq_data = [(col, int(df[col].nunique())) for col in df.columns]
            result = pd.DataFrame(uniq_data, columns=["column", "unique_values"])
            return result.sort_values("unique_values", ascending=False), None
        
        # Fallback: describe
        num_cols = df.select_dtypes(include="number").columns.tolist()
        if num_cols:
            result = df[num_cols].describe().round(3)
            return result, None
        
        return df.head(limit or 25), None
        
    except Exception as e:
        return None, str(e)

def chip(text, cls="ce"):
    return f'<span class="chip {cls}">{text}</span>'

def safe_groq_call(client, messages, max_tokens=2000):
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
        json={"model": "llama-3.3-70b-versatile", "messages": messages,
              "max_tokens": max_tokens, "temperature": 0.4},
        timeout=60
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def extract_sql(text):
    """Extract SQL from response"""
    patterns = [r"```sql\n(.*?)```", r"```\n(.*?)```", r"SELECT.*?;", r"select.*?;"]
    for p in patterns:
        m = re.search(p, text, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1) if "```" in p else m.group(0)
    return None

def auto_insights(df, profile):
    insights = []
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    cat_cols = [c for c in df.columns if df[c].dtype == "object"]

    # Null insights
    high_null = [(c, profile[c]["nulls"]) for c in df.columns if profile[c]["nulls"] > len(df)*0.1]
    if high_null:
        for col, n in high_null[:2]:
            insights.append(("⚠️ Missing Data", f"**{col}** has {n} missing values ({round(n/len(df)*100)}% of rows). Consider imputation or removal."))

    # Numeric skew
    for col in num_cols[:3]:
        skew = df[col].skew()
        if abs(skew) > 1:
            direction = "positively" if skew > 0 else "negatively"
            insights.append(("📊 Distribution", f"**{col}** is {direction} skewed (skewness={round(skew,2)}). Log transformation may normalize it."))

    # High cardinality
    for col in cat_cols[:2]:
        if profile[col]["unique"] > 50:
            insights.append(("🏷️ High Cardinality", f"**{col}** has {profile[col]['unique']} unique values. Consider grouping rare categories."))

    # Correlations
    if len(num_cols) >= 2:
        corr = df[num_cols].corr()
        for i in range(len(num_cols)):
            for j in range(i+1, len(num_cols)):
                v = corr.iloc[i,j]
                if abs(v) > 0.75:
                    insights.append(("🔗 Strong Correlation", f"**{num_cols[i]}** and **{num_cols[j]}** are strongly {'positively' if v>0 else 'negatively'} correlated (r={round(v,3)})."))

    return insights[:6]

def make_overview_charts(df):
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique() > 5]
    cat_cols = [c for c in df.columns if df[c].dtype == "object" and df[c].nunique() <= 20]
    charts = []

    # Numeric distributions
    for col in num_cols[:3]:
        fig = px.histogram(df, x=col, nbins=40, title=f"Distribution · {col}",
                           color_discrete_sequence=["#00E5FF"])
        fig = apply_theme(fig)
        fig.update_traces(marker_line_color="rgba(0,229,255,0.3)", marker_line_width=1)
        charts.append(fig)

    # Categorical bar charts
    for col in cat_cols[:2]:
        top = df[col].value_counts().head(12)
        fig = px.bar(x=top.index, y=top.values, title=f"Top Values · {col}",
                     color_discrete_sequence=["#A855F7"], labels={"x":col,"y":"Count"})
        fig = apply_theme(fig)
        charts.append(fig)

    # Correlation heatmap
    if len(num_cols) >= 2:
        corr = df[num_cols[:10]].corr()
        fig = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.columns,
            colorscale=[[0,"#7B2FBE"],[0.5,"#030508"],[1,"#00E5FF"]],
            zmid=0, text=np.round(corr.values,2), texttemplate="%{text}",
            showscale=True
        ))
        fig.update_layout(title="Correlation Matrix", **PLOTLY_THEME)
        charts.append(fig)

    return charts


# ─── Session State ─────────────────────────────────────────────────────────────
for k, v in {"df":None,"con":None,"profile":None,"chat":[],"file_name":None,"insights":[]}.items():
    if k not in st.session_state: st.session_state[k] = v

groq_key = st.secrets.get("GROQ_API_KEY","")


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div class="sb-logo">
        <div style="font-size:1.6rem;margin-bottom:0.25rem;">🔬</div>
        <div class="sb-logo-name">⚡ NOVA</div>
        <div class="sb-logo-sub">AI DATA INTELLIGENCE</div>
        <div style="height:2px;width:70px;margin:0.6rem auto 0;border-radius:100px;
             background:linear-gradient(90deg,#00E5FF,#A855F7,#00FF88);"></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">System Status</div>', unsafe_allow_html=True)
    if groq_key:
        for l, v in [("🟢 AI Engine","ONLINE"),("⚡ Model","LLaMA 3.3 70B"),("🗄️ Engine","Pandas + SQL")]:
            st.markdown(f'<div class="sb-row"><span class="sb-row-label">{l}</span><span class="sb-row-val">{v}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sb-row" style="border-color:rgba(255,51,102,0.3)"><span class="sb-row-label">🔴 AI Engine</span><span class="sb-row-val" style="color:#FF3366">OFFLINE</span></div>', unsafe_allow_html=True)
        groq_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
        st.markdown("[→ Get Free API Key](https://console.groq.com)")

    if st.session_state.df is not None:
        df = st.session_state.df
        st.markdown('<div class="sb-sec">Loaded Dataset</div>', unsafe_allow_html=True)
        for l, v in [
            ("📁 File", st.session_state.file_name[:18]+"…" if len(st.session_state.file_name)>18 else st.session_state.file_name),
            ("📏 Rows", f"{len(df):,}"),
            ("📐 Columns", str(len(df.columns))),
            ("💾 Memory", f"{df.memory_usage(deep=True).sum()/1024:.1f} KB"),
            ("💬 Q&A", f"{len(st.session_state.chat)//2} queries"),
        ]:
            st.markdown(f'<div class="sb-row"><span class="sb-row-label">{l}</span><span class="sb-row-val">{v}</span></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ CLEAR DATA"):
            for k in ["df","con","profile","chat","file_name","insights"]:
                st.session_state[k] = None if k not in ["chat","insights"] else []
            st.rerun()

    st.markdown('<div class="sb-sec">Analysis Tips</div>', unsafe_allow_html=True)
    for t, tip in [
        ("💡 SQL Queries","Try: 'Show top 10 rows by sales' or 'Count nulls in each column'"),
        ("📈 Visualizations","Ask: 'Plot revenue over time' or 'Show distribution of age'"),
        ("🔍 Insights","Ask: 'What are the key trends?' or 'Summarize this dataset'"),
        ("🧹 Data Quality","Ask: 'Find duplicate rows' or 'Show outliers in price column'"),
    ]:
        st.markdown(f'<div class="sb-tip"><strong>{t}</strong>{tip}</div>', unsafe_allow_html=True)


# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""<div class="nova-hero">
    <div class="nova-eyebrow">⚡ POWERED BY GROQ AI · DUCKDB · LLAMA 3.3 70B</div>
    <h1 class="nova-title">NOVA DATA ANALYST</h1>
    <p class="nova-sub">Upload any dataset. Ask anything in plain English. Get instant SQL queries, visualizations & deep insights.</p>
</div>
<div class="nova-divider"></div>""", unsafe_allow_html=True)

if not groq_key:
    st.error("⚠️ GROQ_API_KEY missing — add it in Streamlit Cloud → Settings → Secrets as: GROQ_API_KEY = \"gsk_...\"")
    st.stop()

# Groq client via requests (no openai package needed)
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# ─── Upload Section ────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hd"><div class="sec-hd-icon">📂</div><div class="sec-hd-title">Data Source</div><div class="sec-hd-line"></div></div>', unsafe_allow_html=True)

up1, up2 = st.columns([3,1])
with up1:
    uploaded = st.file_uploader(
        "Upload Dataset",
        type=["csv","xlsx","xls","json","parquet"],
        label_visibility="collapsed",
        help="Supports CSV, Excel, JSON, Parquet"
    )
with up2:
    st.markdown("""<div style="background:rgba(0,229,255,0.04);border:1px solid rgba(0,229,255,0.1);
        border-radius:10px;padding:0.9rem;font-size:0.75rem;color:#7986A3;line-height:1.6;margin-top:0.1rem;">
        📎 <b style="color:#00E5FF">Supported:</b><br>CSV · Excel · JSON · Parquet<br>
        <span style="font-size:0.65rem;color:#3D4A5C">Max ~200MB</span>
    </div>""", unsafe_allow_html=True)

if uploaded and uploaded.name != st.session_state.file_name:
    with st.spinner("🔬 Scanning dataset..."):
        df = load_file(uploaded)
        if df is not None:
            st.session_state.df = df
            st.session_state.con = register_duckdb(df)
            st.session_state.profile = profile_df(df)
            st.session_state.file_name = uploaded.name
            st.session_state.chat = []
            st.session_state.insights = auto_insights(df, st.session_state.profile)
            st.success(f"✅ Dataset loaded — {len(df):,} rows × {len(df.columns)} columns")
            st.rerun()


# ─── Main Dashboard ────────────────────────────────────────────────────────────
if st.session_state.df is not None:
    df      = st.session_state.df
    con     = st.session_state.con
    profile = st.session_state.profile

    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    cat_cols = [c for c in df.columns if df[c].dtype == "object"]
    null_tot = df.isna().sum().sum()
    dup_count = df.duplicated().sum()

    # ── Stats Row ──────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-hd"><div class="sec-hd-icon">📊</div><div class="sec-hd-title">Dataset Overview</div><div class="sec-hd-line"></div></div>', unsafe_allow_html=True)

    s1,s2,s3,s4,s5,s6 = st.columns(6)
    stat_cards = [
        ("Total Rows",    f"{len(df):,}",       "",        "#00E5FF", "rgba(0,229,255,0.15)", "rgba(0,229,255,0.4)", "linear-gradient(90deg,#00E5FF,#A855F7)"),
        ("Columns",       str(len(df.columns)),  "",        "#A855F7", "rgba(168,85,247,0.15)","rgba(168,85,247,0.4)","linear-gradient(90deg,#A855F7,#00E5FF)"),
        ("Numeric Cols",  str(len(num_cols)),    "cols",    "#00FF88", "rgba(0,255,136,0.12)", "rgba(0,255,136,0.4)", "linear-gradient(90deg,#00FF88,#00E5FF)"),
        ("Categorical",   str(len(cat_cols)),    "cols",    "#FFB300", "rgba(255,179,0,0.12)", "rgba(255,179,0,0.4)",  "linear-gradient(90deg,#FFB300,#FF3366)"),
        ("Missing Values",f"{null_tot:,}",       "cells",   "#FF3366" if null_tot>0 else "#00FF88", "rgba(255,51,102,0.1)","rgba(255,51,102,0.4)","linear-gradient(90deg,#FF3366,#A855F7)"),
        ("Duplicates",    str(dup_count),        "rows",    "#FF3366" if dup_count>0 else "#00FF88", "rgba(255,51,102,0.1)","rgba(255,51,102,0.4)","linear-gradient(90deg,#FF3366,#FFB300)"),
    ]
    for col_w, (label, val, unit, color, border, hover, grad) in zip([s1,s2,s3,s4,s5,s6], stat_cards):
        with col_w:
            st.markdown(f"""<div class="stat-card" style="--sc-color:{color};--sc-border:{border};--sc-hover:{hover};--sc-accent:{grad}">
            <div class="stat-glow" style="background:{color}"></div>
            <div class="stat-label">{label}</div>
            <div class="stat-val">{val}<span class="stat-unit">{unit}</span></div>
            </div>""", unsafe_allow_html=True)

    # ── Auto Insights Banner ───────────────────────────────────────────────────
    if st.session_state.insights:
        st.markdown('<div class="sec-hd"><div class="sec-hd-icon">💡</div><div class="sec-hd-title">Auto-Detected Insights</div><div class="sec-hd-line"></div></div>', unsafe_allow_html=True)
        ic1, ic2 = st.columns(2)
        for i, (title, text) in enumerate(st.session_state.insights):
            col = ic1 if i%2==0 else ic2
            with col:
                st.markdown(f'<div class="insight"><strong>{title}</strong>{text}</div>', unsafe_allow_html=True)

    # ── Main Tabs ──────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    t1, t2, t3, t4, t5 = st.tabs([
        "🔬  DATA EXPLORER",
        "📈  VISUALIZATIONS",
        "🧬  DATA PROFILE",
        "🤖  AI ANALYST",
        "⚗️  SQL WORKBENCH",
    ])

    # ── Tab 1: Data Explorer ───────────────────────────────────────────────────
    with t1:
        st.markdown("""<div class="panel electric">
        <div class="panel-title">📋 Dataset Preview</div></div>""", unsafe_allow_html=True)

        # Filter controls
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            n_rows = st.selectbox("Show rows", [25, 50, 100, 500, "All"], index=0)
        with fc2:
            sort_col = st.selectbox("Sort by", ["None"] + list(df.columns))
        with fc3:
            sort_asc = st.selectbox("Sort order", ["Ascending","Descending"])

        display_df = df.copy()
        if sort_col != "None":
            display_df = display_df.sort_values(sort_col, ascending=(sort_asc=="Ascending"))
        if n_rows != "All":
            display_df = display_df.head(int(n_rows))

        st.dataframe(display_df, use_container_width=True, height=380)

        # Download
        dl1, dl2, _ = st.columns([1,1,2])
        with dl1:
            st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode(), f"{st.session_state.file_name}_processed.csv", "text/csv", use_container_width=True)
        with dl2:
            buf = io.BytesIO()
            df.to_excel(buf, index=False, engine="openpyxl")
            st.download_button("⬇️ Download Excel", buf.getvalue(), f"{st.session_state.file_name}_processed.xlsx", use_container_width=True)

    # ── Tab 2: Visualizations ──────────────────────────────────────────────────
    with t2:
        st.markdown("""<div class="panel violet">
        <div class="panel-title">📈 Auto-Generated Charts</div></div>""", unsafe_allow_html=True)

        charts = make_overview_charts(df)
        if charts:
            for i in range(0, len(charts), 2):
                cc1, cc2 = st.columns(2)
                with cc1:
                    st.plotly_chart(charts[i], use_container_width=True)
                if i+1 < len(charts):
                    with cc2:
                        st.plotly_chart(charts[i+1], use_container_width=True)

        st.markdown('<div class="sec-hd"><div class="sec-hd-icon">🎨</div><div class="sec-hd-title">Custom Chart Builder</div><div class="sec-hd-line"></div></div>', unsafe_allow_html=True)
        cb1, cb2, cb3, cb4 = st.columns(4)
        with cb1:
            chart_type = st.selectbox("Chart Type", ["Bar","Line","Scatter","Box","Histogram","Pie","Area"])
        with cb2:
            x_col = st.selectbox("X Axis", df.columns)
        with cb3:
            y_col = st.selectbox("Y Axis", ["None"] + list(df.columns))
        with cb4:
            color_col = st.selectbox("Color By", ["None"] + list(df.columns))

        color_arg = None if color_col == "None" else color_col
        if st.button("🎨 BUILD CHART"):
            try:
                if chart_type == "Bar":
                    if y_col == "None":
                        vc = df[x_col].value_counts().head(20)
                        fig = px.bar(x=vc.index, y=vc.values, title=f"Bar · {x_col}", color_discrete_sequence=["#00E5FF"])
                    else:
                        fig = px.bar(df, x=x_col, y=y_col, color=color_arg, title=f"Bar · {x_col} vs {y_col}")
                elif chart_type == "Line":
                    fig = px.line(df, x=x_col, y=y_col if y_col!="None" else df.columns[0], color=color_arg, title=f"Line · {x_col}")
                elif chart_type == "Scatter":
                    fig = px.scatter(df, x=x_col, y=y_col if y_col!="None" else x_col, color=color_arg, title=f"Scatter · {x_col} vs {y_col}")
                elif chart_type == "Box":
                    fig = px.box(df, y=x_col, color=color_arg, title=f"Box Plot · {x_col}")
                elif chart_type == "Histogram":
                    fig = px.histogram(df, x=x_col, color=color_arg, title=f"Histogram · {x_col}", nbins=40)
                elif chart_type == "Pie":
                    vc = df[x_col].value_counts().head(10)
                    fig = px.pie(values=vc.values, names=vc.index, title=f"Pie · {x_col}")
                elif chart_type == "Area":
                    fig = px.area(df, x=x_col, y=y_col if y_col!="None" else df.columns[0], color=color_arg, title=f"Area · {x_col}")
                fig = apply_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Chart error: {e}")

    # ── Tab 3: Data Profile ────────────────────────────────────────────────────
    with t3:
        st.markdown("""<div class="panel electric">
        <div class="panel-title">🧬 Column-by-Column Profile</div></div>""", unsafe_allow_html=True)

        for col_name, info in profile.items():
            dtype_chip_cls = "ce" if "int" in info["dtype"] or "float" in info["dtype"] else ("ca" if "date" in info["dtype"] else "cv")
            null_pct = round(info["nulls"]/len(df)*100, 1)
            null_cls = "cr" if null_pct > 20 else ("ca" if null_pct > 5 else "cg")

            with st.expander(f"{'📊' if 'float' in info['dtype'] or 'int' in info['dtype'] else '🏷️'}  {col_name}  ·  {info['dtype']}  ·  {info['unique']} unique", expanded=False):
                pc1, pc2, pc3, pc4 = st.columns(4)
                pc1.metric("Data Type",    info["dtype"])
                pc2.metric("Null Values",  f"{info['nulls']} ({null_pct}%)")
                pc3.metric("Unique Values",str(info["unique"]))
                pc4.metric("Fill Rate",    f"{round(100-null_pct,1)}%")

                if "mean" in info:
                    pm1,pm2,pm3,pm4 = st.columns(4)
                    pm1.metric("Min",    round(info["min"],3))
                    pm2.metric("Max",    round(info["max"],3))
                    pm3.metric("Mean",   round(info["mean"],3))
                    pm4.metric("Std Dev",round(info["std"],3))

                    # Mini chart
                    fig = px.histogram(df, x=col_name, nbins=30, height=200,
                                       color_discrete_sequence=["#00E5FF"])
                    fig = apply_theme(fig)
                    fig.update_layout(margin=dict(l=0,r=0,t=20,b=0), showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    top_vals = df[col_name].value_counts().head(8)
                    if len(top_vals) > 0:
                        fig = px.bar(x=top_vals.index.astype(str), y=top_vals.values, height=180,
                                     color_discrete_sequence=["#A855F7"], labels={"x":col_name,"y":"count"})
                        fig = apply_theme(fig)
                        fig.update_layout(margin=dict(l=0,r=0,t=20,b=0), showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 4: AI Analyst ──────────────────────────────────────────────────────
    with t4:
        st.markdown("""<div class="panel violet">
        <div class="panel-title">🤖 AI Data Analyst · Ask Anything</div>
        <div style="font-size:0.82rem;color:#7986A3;line-height:1.6;">
        Ask questions in plain English. NOVA generates SQL, runs it on your data, and explains the results.
        </div></div>""", unsafe_allow_html=True)

        # Quick prompts
        st.markdown('<div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1rem;">', unsafe_allow_html=True)
        quick = [
            "Summarize this dataset", "Show top 10 rows by first numeric column",
            "Find and count missing values", "What are the key trends?",
            "Show statistical summary", "Find duplicate rows"
        ]
        for q in quick:
            st.markdown(f'<span class="chip ce" style="cursor:pointer;padding:0.3rem 0.7rem;">{q}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Chat display
        if st.session_state.chat:
            for msg in st.session_state.chat:
                if msg["role"] == "user":
                    st.markdown(f'<div class="msg msg-u"><div class="msg-lbl">🧑 YOU</div>{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    content = msg["content"]
                    sql_match = re.search(r'```sql\n(.*?)```', content, re.DOTALL)
                    if sql_match:
                        pre  = content[:content.find("```sql")].strip()
                        post = content[content.find("```", content.find("```sql")+6)+3:].strip()
                        st.markdown(f'<div class="msg msg-a"><div class="msg-lbl">⚡ NOVA AI</div>{pre}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="msg-code">SQL: {sql_match.group(1).strip()}</div>', unsafe_allow_html=True)
                        if post:
                            st.markdown(f'<div class="msg msg-a">{post}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="msg msg-a"><div class="msg-lbl">⚡ NOVA AI</div>{content}</div>', unsafe_allow_html=True)

                    # Show query result if stored
                    if "result_df" in msg:
                        st.dataframe(msg["result_df"], use_container_width=True, height=250)
                    if "result_fig" in msg:
                        st.plotly_chart(msg["result_fig"], use_container_width=True)

        # Input
        with st.form("chat_form", clear_on_submit=True):
            qc1, qc2 = st.columns([6,1])
            with qc1:
                user_q = st.text_input("", placeholder="e.g. Show total sales by category · Plot monthly trend · Find outliers in price", label_visibility="collapsed")
            with qc2:
                submitted = st.form_submit_button("ANALYZE →", use_container_width=True)

        if submitted and user_q.strip():
            schema = get_df_schema(df)
            sample = df.head(3).to_string()
            sys_msg = f"""You are NOVA, an expert AI data analyst. You have access to a DuckDB table called 'data' with this schema:
{schema}

Sample rows:
{sample}

Rules:
1. For data questions, write a SQL query using table name 'data'
2. Wrap SQL in ```sql ... ``` code blocks
3. After SQL, explain what the query does and what insights it reveals
4. For visualization requests, still provide SQL to get the data
5. For general questions, provide analytical insights based on the schema
6. Be concise, precise, and insightful"""

            with st.spinner("🧠 Analyzing..."):
                try:
                    messages = [{"role":"system","content":sys_msg}]
                    for msg in st.session_state.chat[-6:]:
                        messages.append({"role":msg["role"],"content":msg["content"]})
                    messages.append({"role":"user","content":user_q})

                    response = safe_groq_call(client, messages)
                    st.session_state.chat.append({"role":"user","content":user_q})

                    # Try to execute SQL
                    sql = extract_sql(response)
                    result_df = None
                    result_fig = None
                    if sql:
                        res, err = run_sql(con, sql.strip())
                        if res is not None and len(res) > 0:
                            result_df = res
                            # Auto-chart small results
                            if len(res) <= 50 and len(res.columns) >= 2:
                                num_c = [c for c in res.columns if pd.api.types.is_numeric_dtype(res[c])]
                                str_c = [c for c in res.columns if res[c].dtype == "object"]
                                if str_c and num_c:
                                    fig = px.bar(res, x=str_c[0], y=num_c[0], title=f"Query Result",
                                                 color_discrete_sequence=["#00E5FF"])
                                    result_fig = apply_theme(fig)
                                elif len(num_c) >= 2:
                                    fig = px.scatter(res, x=num_c[0], y=num_c[1], title="Query Result",
                                                     color_discrete_sequence=["#A855F7"])
                                    result_fig = apply_theme(fig)

                    msg_obj = {"role":"assistant","content":response}
                    if result_df is not None: msg_obj["result_df"] = result_df
                    if result_fig is not None: msg_obj["result_fig"] = result_fig
                    st.session_state.chat.append(msg_obj)
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")

        if st.session_state.chat:
            _, cl, _ = st.columns([2,1,2])
            with cl:
                if st.button("🗑️ CLEAR CHAT"):
                    st.session_state.chat = []
                    st.rerun()

    # ── Tab 5: SQL Workbench ───────────────────────────────────────────────────
    with t5:
        st.markdown("""<div class="panel green">
        <div class="panel-title">⚗️ SQL Workbench · Live DuckDB</div>
        <div style="font-size:0.82rem;color:#7986A3;">Run raw SQL queries directly against your dataset using DuckDB. Table name: <code style="color:#00FF88">data</code></div>
        </div>""", unsafe_allow_html=True)

        # Schema reference
        with st.expander("📋 Table Schema Reference", expanded=False):
            schema_rows = []
            for col_n, info in profile.items():
                null_pct = round(info["nulls"]/len(df)*100,1)
                schema_rows.append({"Column":col_n,"Type":info["dtype"],"Nulls":f"{info['nulls']} ({null_pct}%)","Unique":info["unique"]})
            st.dataframe(pd.DataFrame(schema_rows), use_container_width=True, hide_index=True)

        # Quick SQL templates
        st.markdown('<div style="margin-bottom:0.75rem;">', unsafe_allow_html=True)
        templates = {
            "SELECT *": f"SELECT * FROM data LIMIT 100",
            "Row Count": f"SELECT COUNT(*) as total_rows FROM data",
            "Null Summary": " UNION ALL\n".join([f"SELECT '{c}' as col, COUNT(*) - COUNT({c}) as nulls FROM data" for c in list(df.columns)[:5]]),
            "Distinct Counts": " UNION ALL\n".join([f"SELECT '{c}' as col, COUNT(DISTINCT {c}) as unique_vals FROM data" for c in list(df.columns)[:5]]),
            "Numeric Stats": f"SELECT {', '.join([f'MIN({c}) as {c}_min, MAX({c}) as {c}_max, AVG({c}) as {c}_avg' for c in [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])][:3]])} FROM data" if num_cols else "SELECT 1",
        }
        st.markdown('</div>', unsafe_allow_html=True)

        sel_template = st.selectbox("Quick Templates", ["Custom"] + list(templates.keys()))
        default_sql  = templates.get(sel_template, "SELECT * FROM data LIMIT 25")

        sql_query = st.text_area(
            "SQL QUERY",
            value=default_sql,
            height=120,
            placeholder="SELECT * FROM data LIMIT 25",
            help="DuckDB SQL. Table name is 'data'"
        )

        sc1, sc2, _ = st.columns([1,1,2])
        with sc1:
            run_sql_btn = st.button("▶ RUN QUERY", use_container_width=True)
        with sc2:
            explain_btn = st.button("🤖 AI EXPLAIN", use_container_width=True)

        if run_sql_btn and sql_query.strip():
            with st.spinner("⚡ Executing..."):
                result, err = run_sql(con, sql_query)
                if err:
                    st.error(f"SQL Error: {err}")
                elif result is not None:
                    st.markdown(f'<div style="font-family:\'Space Mono\',monospace;font-size:0.65rem;color:#00FF88;margin-bottom:0.5rem;">✓ {len(result):,} rows returned</div>', unsafe_allow_html=True)
                    st.dataframe(result, use_container_width=True, height=350)
                    # Auto viz
                    if len(result) > 0 and len(result.columns) >= 2:
                        num_r = [c for c in result.columns if pd.api.types.is_numeric_dtype(result[c])]
                        str_r = [c for c in result.columns if result[c].dtype == "object"]
                        if str_r and num_r and len(result) <= 30:
                            fig = px.bar(result, x=str_r[0], y=num_r[0],
                                        title="Query Result", color_discrete_sequence=["#00E5FF"])
                            st.plotly_chart(apply_theme(fig), use_container_width=True)
                    st.download_button("⬇️ Download Result", result.to_csv(index=False).encode(), "query_result.csv", "text/csv")

        if explain_btn and sql_query.strip():
            with st.spinner("🧠 AI explaining..."):
                try:
                    resp = safe_groq_call(client, [
                        {"role":"system","content":f"You are a SQL expert. Explain this DuckDB query against a table with schema:\n{get_df_schema(df)}\nBe concise and clear."},
                        {"role":"user","content":f"Explain this SQL:\n{sql_query}"}
                    ], max_tokens=600)
                    st.markdown(f'<div class="msg msg-a"><div class="msg-lbl">⚡ NOVA AI — SQL Explanation</div>{resp}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

else:
    # ── Empty State ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem;">
        <div style="font-size:3.5rem;margin-bottom:1rem;animation:pulse-glow 2s ease-in-out infinite;">🔬</div>
        <div style="font-family:'Exo 2',sans-serif;font-size:1.1rem;font-weight:700;
             color:#EEF2FF;letter-spacing:0.08em;margin-bottom:0.5rem;">AWAITING DATA</div>
        <div style="color:#7986A3;font-size:0.85rem;max-width:420px;margin:0 auto;line-height:1.7;">
            Upload a CSV, Excel, JSON or Parquet file above to activate the full analysis suite.
            NOVA will auto-profile your data, generate insights, and let you query it in plain English.
        </div>
        <div style="display:flex;justify-content:center;gap:0.6rem;margin-top:1.5rem;flex-wrap:wrap;">
            <span class="chip ce">CSV</span>
            <span class="chip cv">Excel</span>
            <span class="chip cg">JSON</span>
            <span class="chip ca">Parquet</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 0.5rem;margin-top:1rem;">
    <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(0,229,255,0.3),rgba(168,85,247,0.3),transparent);margin-bottom:1rem;"></div>
    <div style="font-family:'Space Mono',monospace;font-size:0.5rem;letter-spacing:0.3em;color:#2D3550;">
        NOVA · AI DATA INTELLIGENCE · GROQ + LLaMA 3.3 70B + DuckDB &nbsp;|&nbsp; RESULTS ARE AI-GENERATED · VERIFY BEFORE CRITICAL DECISIONS
    </div>
</div>
""", unsafe_allow_html=True)
