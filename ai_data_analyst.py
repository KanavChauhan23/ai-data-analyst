import streamlit as st
import pandas as pd
import numpy as np
import requests
import re
import io
import json

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
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;600;700;800;900&family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500&display=swap');

:root {
    --electric: #00E5FF;
    --violet:   #A855F7;
    --neon:     #00FF88;
    --amber:    #FFB300;
    --red:      #FF3366;
    --bg:       #030508;
    --panel:    rgba(8,12,24,0.97);
    --border-e: rgba(0,229,255,0.18);
    --text-hi:  #EEF2FF;
    --text-mid: #7986A3;
    --text-lo:  #2D3550;
}

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main .block-container { padding: 1rem 2rem 4rem; max-width: 1440px; }
.stApp { background: var(--bg); color: var(--text-hi); }
.stApp::before {
    content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse 80% 50% at 15% -5%, rgba(0,229,255,0.06) 0%, transparent 55%),
        radial-gradient(ellipse 60% 40% at 85% 105%, rgba(168,85,247,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 40% 30% at 50% 55%, rgba(0,255,136,0.025) 0%, transparent 50%);
}
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: rgba(0,229,255,0.3); border-radius: 4px; }

/* File uploader - dark bg, visible text and button */
[data-testid="stFileUploader"] {
    background: rgba(8,12,28,0.95) !important;
    border: 1px solid rgba(0,229,255,0.25) !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploader"] section {
    background: rgba(8,12,28,0.95) !important;
    border: 1px dashed rgba(0,229,255,0.3) !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploader"] section > div {
    background: transparent !important;
}
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] small {
    color: #7986A3 !important;
}
[data-testid="stFileUploader"] button {
    background: rgba(0,229,255,0.12) !important;
    border: 1px solid rgba(0,229,255,0.4) !important;
    color: #00E5FF !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}
[data-testid="stFileUploaderFileName"] { color: #EEF2FF !important; }

@keyframes data-stream { 0%{background-position:0% 50%} 100%{background-position:200% 50%} }
@keyframes pulse-glow  { 0%,100%{opacity:.5} 50%{opacity:1} }
@keyframes float-in    { 0%{transform:translateY(10px);opacity:0} 100%{transform:translateY(0);opacity:1} }

section[data-testid="stSidebar"] {
    background: rgba(3,5,12,0.99) !important;
    border-right: 1px solid rgba(0,229,255,0.1) !important;
}
section[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
section[data-testid="stSidebar"] .block-container { padding: 0 0.5rem 2rem !important; }

/* Hero */
.hero { text-align:center; padding:1.8rem 1rem 0.8rem; animation:float-in .7s ease forwards; }
.hero-tag {
    display:inline-flex; align-items:center; gap:.5rem;
    font-family:'Space Mono',monospace; font-size:.58rem; letter-spacing:.38em;
    color:var(--electric); border:1px solid rgba(0,229,255,.3);
    padding:.22rem .9rem; border-radius:3px; background:rgba(0,229,255,.06);
    margin-bottom:.9rem; text-transform:uppercase;
    animation:pulse-glow 3s ease-in-out infinite;
}
.hero-title {
    font-family:'Exo 2',sans-serif; font-weight:900;
    font-size:clamp(2.2rem,5vw,3.8rem); line-height:1; letter-spacing:-.03em;
    background:linear-gradient(120deg,#fff 0%,#00E5FF 35%,#A855F7 70%,#00FF88 100%);
    background-size:200% auto; -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    animation:data-stream 4s linear infinite; margin-bottom:.5rem;
}
.hero-sub { color:var(--text-mid); font-size:.9rem; font-weight:300; max-width:100%; margin:0 auto 1.2rem; line-height:1.65; text-align:center; display:block; }
.hero-line { height:1px; background:linear-gradient(90deg,transparent,rgba(0,229,255,.4),rgba(168,85,247,.4),transparent); margin-bottom:1.5rem; }

/* Section header */
.sh { display:flex; align-items:center; gap:.7rem; margin:1.8rem 0 1rem; padding-bottom:.5rem; border-bottom:1px solid rgba(0,229,255,.08); }
.sh-icon { width:32px;height:32px;border-radius:6px; background:linear-gradient(135deg,rgba(0,229,255,.15),rgba(168,85,247,.1)); border:1px solid rgba(0,229,255,.25); display:flex;align-items:center;justify-content:center;font-size:.9rem;flex-shrink:0; }
.sh-title { font-family:'Exo 2',sans-serif; font-size:.72rem; font-weight:700; letter-spacing:.22em; color:var(--text-hi); text-transform:uppercase; }
.sh-line { flex:1; height:1px; background:linear-gradient(90deg,rgba(0,229,255,.15),transparent); }

/* Stat cards */
.sc { background:var(--panel); border-radius:12px; padding:1rem 1.1rem; position:relative; overflow:hidden; border:1px solid var(--sc-b,rgba(0,229,255,.15)); transition:border-color .2s,transform .2s; }
.sc:hover { border-color:var(--sc-h,rgba(0,229,255,.4)); transform:translateY(-2px); }
.sc::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:var(--sc-g,linear-gradient(90deg,#00E5FF,#A855F7)); opacity:.7; }
.sc-glow { position:absolute; top:-20px; right:-20px; width:60px; height:60px; border-radius:50%; opacity:.12; filter:blur(15px); background:var(--sc-c,#00E5FF); }
.sc-label { font-family:'Space Mono',monospace; font-size:.55rem; letter-spacing:.2em; color:var(--text-mid); text-transform:uppercase; margin-bottom:.4rem; }
.sc-val { font-family:'Exo 2',sans-serif; font-size:1.55rem; font-weight:800; line-height:1; color:var(--sc-c,#00E5FF); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.sc-unit { font-size:.7rem; color:var(--text-mid); margin-left:.2rem; font-family:'Inter',sans-serif; }

/* Chips */
.chip { display:inline-flex; align-items:center; font-family:'Space Mono',monospace; font-size:.56rem; padding:.15rem .55rem; border-radius:3px; font-weight:400; letter-spacing:.05em; white-space:nowrap; }
.ce { background:rgba(0,229,255,.1);  color:#00E5FF; border:1px solid rgba(0,229,255,.3); }
.cv { background:rgba(168,85,247,.1); color:#A855F7; border:1px solid rgba(168,85,247,.3); }
.cg { background:rgba(0,255,136,.1);  color:#00FF88; border:1px solid rgba(0,255,136,.3); }
.ca { background:rgba(255,179,0,.1);  color:#FFB300; border:1px solid rgba(255,179,0,.3); }
.cr { background:rgba(255,51,102,.1); color:#FF3366; border:1px solid rgba(255,51,102,.3); }

/* Panel */
.panel { background:var(--panel); border-radius:14px; padding:1.4rem 1.6rem; margin-bottom:1.2rem; position:relative; overflow:hidden; border:1px solid rgba(0,229,255,.12); }
.panel::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; }
.panel.el::before { background:linear-gradient(90deg,transparent,#00E5FF,#A855F7,transparent); }
.panel.vi::before { background:linear-gradient(90deg,transparent,#A855F7,transparent); }
.panel.gr::before { background:linear-gradient(90deg,transparent,#00FF88,transparent); }
.panel-title { font-family:'Exo 2',sans-serif; font-size:.72rem; font-weight:700; letter-spacing:.18em; text-transform:uppercase; margin-bottom:.85rem; }
.panel.el .panel-title { color:#00E5FF; }
.panel.vi .panel-title { color:#A855F7; }
.panel.gr .panel-title { color:#00FF88; }

/* Chat */
.msg { padding:.9rem 1.1rem; border-radius:10px; font-size:.87rem; line-height:1.7; margin-bottom:.7rem; }
.mu { background:rgba(0,229,255,.07); border-left:2px solid #00E5FF; }
.ma { background:rgba(168,85,247,.06); border-left:2px solid #A855F7; }
.mlbl { font-family:'Space Mono',monospace; font-size:.56rem; letter-spacing:.14em; opacity:.5; margin-bottom:.3rem; text-transform:uppercase; }
.sql-block { background:rgba(0,0,0,.5); border:1px solid rgba(0,255,136,.2); border-radius:6px; padding:.6rem .85rem; font-family:'Space Mono',monospace; font-size:.72rem; color:#00FF88; margin:.5rem 0; overflow-x:auto; white-space:pre-wrap; }

/* Insight */
.ins { background:rgba(0,229,255,.04); border:1px solid rgba(0,229,255,.12); border-radius:9px; padding:.75rem .9rem; font-size:.8rem; color:var(--text-mid); line-height:1.6; margin-bottom:.5rem; }
.ins strong { color:#00E5FF; font-family:'Space Mono',monospace; font-size:.62rem; display:block; letter-spacing:.1em; text-transform:uppercase; margin-bottom:.18rem; }

/* Sidebar */
.sb-logo { text-align:center; padding:1.3rem 1rem 1rem; border-bottom:1px solid rgba(0,229,255,.08); margin-bottom:1rem; }
.sb-name { font-family:'Exo 2',sans-serif; font-size:1.1rem; font-weight:900; letter-spacing:.12em; background:linear-gradient(120deg,#00E5FF,#A855F7); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.sb-sub  { font-family:'Space Mono',monospace; font-size:.48rem; letter-spacing:.3em; color:var(--text-lo); margin-top:.2rem; }
.sb-row  { padding:.6rem .9rem; background:rgba(0,229,255,.04); border:1px solid rgba(0,229,255,.08); border-radius:8px; margin-bottom:.45rem; display:flex; align-items:center; justify-content:space-between; }
.sb-lbl  { font-size:.72rem; color:var(--text-mid); }
.sb-val  { font-family:'Space Mono',monospace; font-size:.72rem; color:#00E5FF; font-weight:700; }
.sb-sec  { font-family:'Space Mono',monospace; font-size:.55rem; letter-spacing:.26em; color:var(--text-lo); text-transform:uppercase; margin:1rem 0 .5rem; }
.sb-tip  { background:rgba(168,85,247,.04); border:1px solid rgba(168,85,247,.12); border-radius:8px; padding:.65rem .8rem; margin-bottom:.45rem; font-size:.74rem; color:var(--text-mid); line-height:1.55; }
.sb-tip strong { color:#A855F7; display:block; font-size:.6rem; letter-spacing:.1em; text-transform:uppercase; margin-bottom:.15rem; font-family:'Space Mono',monospace; }

/* Streamlit overrides */
.stTextInput input, .stTextArea textarea {
    background:rgba(8,12,28,.95) !important; border:1px solid rgba(0,229,255,.22) !important;
    border-radius:8px !important; color:#EEF2FF !important; caret-color:#00E5FF !important;
    font-family:'Inter',sans-serif !important; font-size:.9rem !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder { color:rgba(121,134,163,.5) !important; }
.stTextInput input:focus, .stTextArea textarea:focus { border-color:rgba(0,229,255,.55) !important; box-shadow:0 0 0 3px rgba(0,229,255,.09) !important; }
.stSelectbox > div > div { background:rgba(8,12,28,.95) !important; border:1px solid rgba(0,229,255,.22) !important; border-radius:8px !important; color:#EEF2FF !important; }
.stButton > button { background:linear-gradient(135deg,rgba(0,229,255,.14),rgba(168,85,247,.1)) !important; border:1px solid rgba(0,229,255,.4) !important; color:#00E5FF !important; font-family:'Exo 2',sans-serif !important; font-size:.75rem !important; font-weight:700 !important; letter-spacing:.15em !important; border-radius:8px !important; padding:.6rem 1.2rem !important; transition:all .25s !important; width:100% !important; }
.stButton > button:hover { background:linear-gradient(135deg,rgba(0,229,255,.26),rgba(168,85,247,.2)) !important; box-shadow:0 0 20px rgba(0,229,255,.22) !important; transform:translateY(-1px) !important; }
/* Download button override */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg,rgba(0,229,255,.14),rgba(0,255,136,.08)) !important;
    border: 1px solid rgba(0,229,255,.4) !important;
    color: #00E5FF !important;
    font-family: 'Exo 2', sans-serif !important;
    font-size: .75rem !important; font-weight: 700 !important;
    letter-spacing: .12em !important; border-radius: 8px !important;
    width: 100% !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(135deg,rgba(0,229,255,.25),rgba(0,255,136,.15)) !important;
    box-shadow: 0 0 18px rgba(0,229,255,.22) !important;
}
div[data-testid="stForm"] button { color:#00E5FF !important; background:rgba(0,229,255,.1) !important; border:1px solid rgba(0,229,255,.4) !important; }
label, .stSelectbox label, .stTextInput label, .stTextArea label { color:#7986A3 !important; font-family:'Space Mono',monospace !important; font-size:.62rem !important; letter-spacing:.14em !important; text-transform:uppercase !important; }
.stTabs [data-baseweb="tab-list"] { background:rgba(255,255,255,.02) !important; border-radius:10px !important; padding:4px !important; gap:3px !important; }
.stTabs [data-baseweb="tab"] { border-radius:7px !important; font-family:'Exo 2',sans-serif !important; font-size:.8rem !important; font-weight:600 !important; color:#7986A3 !important; }
.stTabs [aria-selected="true"] { background:rgba(0,229,255,.12) !important; color:#00E5FF !important; }
.stExpander { background:var(--panel) !important; border:1px solid rgba(0,229,255,.12) !important; border-radius:10px !important; }
div[data-testid="stExpander"] div[role="button"] p { font-family:'Exo 2',sans-serif !important; font-size:.78rem !important; font-weight:700 !important; }
.stMetric { background:rgba(0,229,255,.03) !important; border:1px solid rgba(0,229,255,.1) !important; border-radius:9px !important; padding:.65rem .9rem !important; }
[data-testid="stMetricValue"] { font-family:'Exo 2',sans-serif !important; color:#00E5FF !important; font-weight:800 !important; }
[data-testid="stMetricLabel"] { font-family:'Space Mono',monospace !important; font-size:.6rem !important; color:#7986A3 !important; letter-spacing:.1em !important; }
hr { border-color:rgba(0,229,255,.08) !important; }
div[data-testid="stForm"] { border:none !important; padding:0 !important; }
</style>
""", unsafe_allow_html=True)


# ─── Groq API (pure requests) ──────────────────────────────────────────────────
def groq_call(api_key, messages, max_tokens=2000):
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "llama-3.3-70b-versatile", "messages": messages,
              "max_tokens": max_tokens, "temperature": 0.4},
        timeout=60
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


# ─── Data Helpers ──────────────────────────────────────────────────────────────
def load_file(f):
    try:
        if f.name.endswith(".csv"):
            df = pd.read_csv(f, na_values=["NA","N/A","","missing"])
        elif f.name.endswith((".xlsx", ".xls")):
            try:
                df = pd.read_excel(f, na_values=["NA","N/A","","missing"])
            except Exception as ex:
                err = str(ex).lower()
                if "openpyxl" in err or "xlrd" in err:
                    st.error("⚠️ Excel engine not available on this server. Please save your file as **CSV** and re-upload: File → Save As → CSV (Comma delimited).")
                else:
                    st.error(f"Excel load error: {ex}")
                return None
        elif f.name.endswith(".json"):
            df = pd.read_json(f)
        else:
            st.error("Unsupported format. Use CSV, Excel or JSON.")
            return None
        for col in df.columns:
            if any(k in col.lower() for k in ["date","time","dt"]):
                try: df[col] = pd.to_datetime(df[col], errors="coerce")
                except: pass
        return df
    except Exception as e:
        st.error(f"Load error: {e}"); return None

def profile(df):
    out = {}
    for c in df.columns:
        info = {"dtype": str(df[c].dtype), "nulls": int(df[c].isna().sum()), "unique": int(df[c].nunique())}
        if pd.api.types.is_numeric_dtype(df[c]) and df[c].notna().any():
            info.update({"min":float(df[c].min()),"max":float(df[c].max()),
                         "mean":float(df[c].mean()),"std":float(df[c].std())})
        out[c] = info
    return out

def schema_str(df):
    return "\n".join([f"  {c}: {df[c].dtype}, {df[c].isna().sum()} nulls, {df[c].nunique()} unique" for c in df.columns])

def run_query(df, sql):
    """Pandas-based SQL executor"""
    sql = sql.strip().rstrip(";")
    up = sql.upper()
    try:
        limit_m = re.search(r"LIMIT\s+(\d+)", sql, re.I)
        limit = int(limit_m.group(1)) if limit_m else None

        if re.search(r"SELECT\s+COUNT\(\*\)\s+FROM", sql, re.I) and "GROUP" not in up:
            return pd.DataFrame({"total_rows": [len(df)]}), None

        if "GROUP BY" in up:
            grp = re.search(r"GROUP BY\s+(\w+)", sql, re.I)
            agg = re.search(r"(SUM|AVG|COUNT|MAX|MIN)\((\w+|\*)\)", sql, re.I)
            if grp:
                gc = grp.group(1)
                if gc not in df.columns: return None, f"Column '{gc}' not found"
                fn = agg.group(1).lower() if agg else "count"
                ac = agg.group(2) if agg else None
                if fn == "count" or ac == "*":
                    res = df.groupby(gc).size().reset_index(name="count")
                elif ac and ac in df.columns:
                    res = df.groupby(gc)[ac].agg(fn).reset_index()
                else:
                    res = df.groupby(gc).size().reset_index(name="count")
                res = res.sort_values(res.columns[-1], ascending=False)
                return res.head(limit) if limit else res, None

        if "ORDER BY" in up and "WHERE" not in up and "GROUP" not in up:
            om = re.search(r"ORDER BY\s+(\w+)(\s+DESC)?", sql, re.I)
            if om:
                col, desc = om.group(1), bool(om.group(2))
                if col not in df.columns: return None, f"Column '{col}' not found"
                res = df.sort_values(col, ascending=not desc)
                return res.head(limit) if limit else res, None

        if "WHERE" in up and "GROUP" not in up:
            wm = re.search(r"WHERE\s+(.+?)(?:\s+ORDER BY|\s+LIMIT|$)", sql, re.I)
            if wm:
                try:
                    res = df.query(wm.group(1).strip())
                    om = re.search(r"ORDER BY\s+(\w+)(\s+DESC)?", sql, re.I)
                    if om and om.group(1) in df.columns:
                        res = res.sort_values(om.group(1), ascending=not bool(om.group(2)))
                    return res.head(limit) if limit else res, None
                except: pass

        if any(k in sql.lower() for k in ["null","missing"]):
            nd = [(c, int(df[c].isna().sum()), round(df[c].isna().mean()*100,1)) for c in df.columns]
            res = pd.DataFrame(nd, columns=["column","null_count","null_pct"])
            return res[res.null_count > 0].sort_values("null_count", ascending=False), None

        if "duplicate" in sql.lower():
            dups = df[df.duplicated()]
            return dups.head(limit or 100), None

        if any(k in sql.lower() for k in ["describe","statistics","stats","min(","max(","avg("]):
            nc = df.select_dtypes(include="number").columns.tolist()
            if nc:
                res = df[nc].describe().T[["min","max","mean","std"]].round(3)
                return res.reset_index().rename(columns={"index":"column"}), None

        if "distinct" in sql.lower() or "unique" in sql.lower():
            ud = [(c, int(df[c].nunique())) for c in df.columns]
            return pd.DataFrame(ud, columns=["column","unique_count"]).sort_values("unique_count", ascending=False), None

        return df.head(limit or 25), None
    except Exception as e:
        return None, str(e)

def auto_insights(df, prof):
    insights = []
    nc = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    cc = [c for c in df.columns if df[c].dtype == "object"]
    for col in df.columns:
        n = prof[col]["nulls"]
        if n > len(df)*0.1:
            insights.append(("⚠️ Missing Data", f"<b>{col}</b> has {n} missing values ({round(n/len(df)*100)}% of rows). Consider imputation or removal."))
    for col in nc[:4]:
        try:
            sk = float(df[col].skew())
            if sk and abs(sk) > 1:
                d = "positively" if sk > 0 else "negatively"
                insights.append(("📊 Skewed Distribution", f"<b>{col}</b> is {d} skewed (skew={round(sk,2)}). Log transform may help."))
        except: pass
    for col in cc[:3]:
        if prof[col]["unique"] > 50:
            insights.append(("🏷️ High Cardinality", f"<b>{col}</b> has {prof[col]['unique']} unique values. Consider grouping rare categories."))
    if len(nc) >= 2:
        try:
            corr = df[nc].corr()
            for i in range(len(nc)):
                for j in range(i+1, min(len(nc), 8)):
                    v = corr.iloc[i,j]
                    if abs(v) > 0.75:
                        insights.append(("🔗 Correlation", f"<b>{nc[i]}</b> & <b>{nc[j]}</b> strongly correlated (r={round(v,3)})."))
        except: pass
    return insights[:6]

def chip(text, cls="ce"): return f'<span class="chip {cls}">{text}</span>'


# ─── Session State ─────────────────────────────────────────────────────────────
for k, v in {"df":None,"prof":None,"chat":[],"fname":None,"insights":[]}.items():
    if k not in st.session_state: st.session_state[k] = v

groq_key = st.secrets.get("GROQ_API_KEY", "")


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div class="sb-logo">
        <div style="font-size:1.6rem;margin-bottom:.25rem;">🔬</div>
        <div class="sb-name">⚡ NOVA</div>
        <div class="sb-sub">AI DATA INTELLIGENCE</div>
        <div style="height:2px;width:70px;margin:.6rem auto 0;border-radius:100px;background:linear-gradient(90deg,#00E5FF,#A855F7,#00FF88);"></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">System Status</div>', unsafe_allow_html=True)
    if groq_key:
        for l,v in [("🟢 AI Engine","ONLINE"),("⚡ Model","LLaMA 3.3 70B"),("🔑 API","GROQ")]:
            st.markdown(f'<div class="sb-row"><span class="sb-lbl">{l}</span><span class="sb-val">{v}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sb-row" style="border-color:rgba(255,51,102,.3)"><span class="sb-lbl">🔴 AI Engine</span><span class="sb-val" style="color:#FF3366">OFFLINE</span></div>', unsafe_allow_html=True)
        groq_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
        st.markdown("[→ Get Free Key](https://console.groq.com)")

    if st.session_state.df is not None:
        df = st.session_state.df
        st.markdown('<div class="sb-sec">Dataset Info</div>', unsafe_allow_html=True)
        fname = st.session_state.fname or ""
        for l,v in [
            ("📁 File", fname[:16]+"…" if len(fname)>16 else fname),
            ("📏 Rows", f"{len(df):,}"),
            ("📐 Cols", str(len(df.columns))),
            ("💾 Size", f"{df.memory_usage(deep=True).sum()/1024:.1f} KB"),
            ("💬 Queries", str(len([m for m in st.session_state.chat if m["role"]=="user"]))),
        ]:
            st.markdown(f'<div class="sb-row"><span class="sb-lbl">{l}</span><span class="sb-val">{v}</span></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ CLEAR DATA"):
            for k in ["df","prof","chat","fname","insights"]: st.session_state[k] = None if k not in ["chat","insights"] else []
            st.rerun()

    st.markdown('<div class="sb-sec">Analysis Tips</div>', unsafe_allow_html=True)
    for t,tip in [
        ("💡 Questions","Try: 'Show top 10 by sales' or 'Count missing values per column'"),
        ("📈 Charts","Ask: 'Plot revenue trend' or 'Show category distribution'"),
        ("🔍 Insights","Ask: 'What are the key patterns?' or 'Summarize this data'"),
        ("🧹 Quality","Ask: 'Find duplicates' or 'Show columns with most nulls'"),
    ]:
        st.markdown(f'<div class="sb-tip"><strong>{t}</strong>{tip}</div>', unsafe_allow_html=True)


# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""<div class="hero">
    <div class="hero-tag">⚡ POWERED BY GROQ AI · LLAMA 3.3 70B · REAL-TIME ANALYSIS</div>
    <h1 class="hero-title">NOVA DATA ANALYST</h1>
    <div class="hero-sub">Upload any dataset. Ask anything in plain English.<br>Get instant analysis, charts &amp; AI insights.</div>
</div><div class="hero-line"></div>""", unsafe_allow_html=True)

if not groq_key:
    st.error("⚠️ GROQ_API_KEY missing — Streamlit Cloud → Settings → Secrets → GROQ_API_KEY = \"gsk_...\"")
    st.stop()


# ─── Upload ────────────────────────────────────────────────────────────────────
st.markdown('<div class="sh"><div class="sh-icon">📂</div><div class="sh-title">Data Source</div><div class="sh-line"></div></div>', unsafe_allow_html=True)

up1, up2 = st.columns([3,1])
with up1:
    uploaded = st.file_uploader("Upload Dataset", type=["csv","xlsx","xls","json"], label_visibility="collapsed")
with up2:
    st.markdown("""<div style="background:rgba(0,229,255,.04);border:1px solid rgba(0,229,255,.1);border-radius:10px;padding:.9rem;font-size:.75rem;color:#7986A3;line-height:1.7;margin-top:.1rem;">
    📎 <b style="color:#00E5FF">Formats:</b><br>CSV · Excel · JSON<br><span style="font-size:.65rem;color:#3D4A5C">Max ~200MB</span></div>""", unsafe_allow_html=True)

if uploaded and uploaded.name != st.session_state.fname:
    with st.spinner("🔬 Scanning dataset..."):
        df = load_file(uploaded)
        if df is not None:
            st.session_state.df      = df
            st.session_state.prof    = profile(df)
            st.session_state.fname   = uploaded.name
            st.session_state.chat    = []
            st.session_state.insights= auto_insights(df, st.session_state.prof)
            st.success(f"✅ Loaded {len(df):,} rows × {len(df.columns)} columns")
            st.rerun()


# ─── Dashboard ─────────────────────────────────────────────────────────────────
if st.session_state.df is not None:
    df   = st.session_state.df
    prof = st.session_state.prof
    nc   = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    cc   = [c for c in df.columns if df[c].dtype == "object"]
    nulls= int(df.isna().sum().sum())
    dups = int(df.duplicated().sum())

    # Stats row
    st.markdown('<div class="sh"><div class="sh-icon">📊</div><div class="sh-title">Dataset Overview</div><div class="sh-line"></div></div>', unsafe_allow_html=True)
    s1,s2,s3,s4,s5,s6 = st.columns(6)
    cards = [
        (s1,"Total Rows",f"{len(df):,}","","#00E5FF","rgba(0,229,255,.15)","rgba(0,229,255,.4)","linear-gradient(90deg,#00E5FF,#A855F7)"),
        (s2,"Columns",str(len(df.columns)),"","#A855F7","rgba(168,85,247,.15)","rgba(168,85,247,.4)","linear-gradient(90deg,#A855F7,#00E5FF)"),
        (s3,"Numeric",str(len(nc)),"cols","#00FF88","rgba(0,255,136,.12)","rgba(0,255,136,.4)","linear-gradient(90deg,#00FF88,#00E5FF)"),
        (s4,"Categorical",str(len(cc)),"cols","#FFB300","rgba(255,179,0,.12)","rgba(255,179,0,.4)","linear-gradient(90deg,#FFB300,#FF3366)"),
        (s5,"Nulls",f"{nulls:,}","cells","#FF3366" if nulls>0 else "#00FF88","rgba(255,51,102,.1)","rgba(255,51,102,.4)","linear-gradient(90deg,#FF3366,#A855F7)"),
        (s6,"Duplicates",str(dups),"rows","#FF3366" if dups>0 else "#00FF88","rgba(255,51,102,.1)","rgba(255,51,102,.4)","linear-gradient(90deg,#FF3366,#FFB300)"),
    ]
    for col,lbl,val,unit,color,border,hover,grad in cards:
        with col:
            st.markdown(f"""<div class="sc" style="--sc-c:{color};--sc-b:{border};--sc-h:{hover};--sc-g:{grad}">
            <div class="sc-glow" style="background:{color}"></div>
            <div class="sc-label">{lbl}</div>
            <div class="sc-val">{val}<span class="sc-unit">{unit}</span></div>
            </div>""", unsafe_allow_html=True)

    # Insights
    if st.session_state.insights:
        st.markdown('<div class="sh"><div class="sh-icon">💡</div><div class="sh-title">Auto Insights</div><div class="sh-line"></div></div>', unsafe_allow_html=True)
        ic1,ic2 = st.columns(2)
        for i,(title,text) in enumerate(st.session_state.insights):
            with (ic1 if i%2==0 else ic2):
                st.markdown(f'<div class="ins"><strong>{title}</strong>{text}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs
    t1,t2,t3,t4,t5 = st.tabs(["🔬  DATA EXPLORER","📈  VISUALIZATIONS","🧬  DATA PROFILE","🤖  AI ANALYST","⚗️  QUERY ENGINE"])

    # ── Tab 1 ──────────────────────────────────────────────────────────────────
    with t1:
        st.markdown('<div class="panel el"><div class="panel-title">📋 Dataset Preview</div></div>', unsafe_allow_html=True)
        fc1,fc2,fc3 = st.columns(3)
        with fc1: n_rows = st.selectbox("Show rows",[25,50,100,500,"All"])
        with fc2: sort_col = st.selectbox("Sort by",["None"]+list(df.columns))
        with fc3: sort_ord = st.selectbox("Order",["Ascending","Descending"])
        disp = df.copy()
        if sort_col != "None": disp = disp.sort_values(sort_col, ascending=sort_ord=="Ascending")
        if n_rows != "All": disp = disp.head(int(n_rows))
        st.dataframe(disp, use_container_width=True, height=380)
        dl1,_ = st.columns([1,3])
        with dl1:
            st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode(), "data_export.csv", "text/csv", use_container_width=True)

    # ── Tab 2 ──────────────────────────────────────────────────────────────────
    with t2:
        st.markdown('<div class="panel vi"><div class="panel-title">📈 Chart Builder</div></div>', unsafe_allow_html=True)
        cb1,cb2,cb3 = st.columns(3)
        with cb1: chart_type = st.selectbox("Chart Type",["Bar","Line","Area","Scatter","Histogram"])
        with cb2: x_col = st.selectbox("X / Category", df.columns)
        with cb3: y_col = st.selectbox("Y / Value", ["Count"]+[c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])])

        if st.button("📊 BUILD CHART"):
            try:
                if y_col == "Count":
                    data = df[x_col].value_counts().head(20)
                    chart_df = pd.DataFrame({"value": data.values}, index=data.index)
                else:
                    chart_df = df[[x_col, y_col]].dropna().set_index(x_col)[y_col]

                if chart_type == "Bar":       st.bar_chart(chart_df)
                elif chart_type == "Line":    st.line_chart(chart_df)
                elif chart_type == "Area":    st.area_chart(chart_df)
                elif chart_type == "Scatter": st.scatter_chart(df[[x_col,y_col]].dropna(), x=x_col, y=y_col)
                elif chart_type == "Histogram":
                    if y_col != "Count" and y_col in df.columns:
                        bins = pd.cut(df[y_col].dropna(), bins=20).value_counts().sort_index()
                        hist_df = pd.DataFrame({"count": bins.values}, index=bins.index.astype(str))
                        st.bar_chart(hist_df)
            except Exception as e:
                st.error(f"Chart error: {e}")

        # Auto charts
        st.markdown('<div class="sh"><div class="sh-icon">🤖</div><div class="sh-title">Auto Charts</div><div class="sh-line"></div></div>', unsafe_allow_html=True)
        if nc:
            for col in nc[:3]:
                with st.expander(f"📊 Distribution · {col}", expanded=False):
                    bins = pd.cut(df[col].dropna(), bins=20).value_counts().sort_index()
                    st.bar_chart(pd.DataFrame({"count":bins.values}, index=bins.index.astype(str)))
        if cc:
            for col in cc[:2]:
                if df[col].nunique() <= 20:
                    with st.expander(f"🏷️ Top Values · {col}", expanded=False):
                        vc = df[col].value_counts().head(12)
                        st.bar_chart(pd.DataFrame({"count":vc.values}, index=vc.index))
        if len(nc) >= 2:
            with st.expander("🔗 Numeric Correlation Matrix", expanded=False):
                try:
                    corr = df[nc[:8]].corr().round(3)
                    st.dataframe(corr, use_container_width=True)
                except Exception as e:
                    st.info(f"Correlation unavailable: {e}")

    # ── Tab 3 ──────────────────────────────────────────────────────────────────
    with t3:
        st.markdown('<div class="panel el"><div class="panel-title">🧬 Column Profile</div></div>', unsafe_allow_html=True)
        schema_rows = []
        for c, info in prof.items():
            null_pct = round(info["nulls"]/len(df)*100,1)
            schema_rows.append({"Column":c,"Type":info["dtype"],"Nulls":f"{info['nulls']} ({null_pct}%)","Unique":info["unique"],"Fill %":f"{round(100-null_pct,1)}%"})
        st.dataframe(pd.DataFrame(schema_rows), use_container_width=True, hide_index=True)

        if nc:
            st.markdown('<div class="sh"><div class="sh-icon">📐</div><div class="sh-title">Numeric Summary</div><div class="sh-line"></div></div>', unsafe_allow_html=True)
            desc = df[nc].describe().T[["min","max","mean","50%","std"]].rename(columns={"50%":"median"}).round(3)
            st.dataframe(desc, use_container_width=True)

        for col, info in prof.items():
            with st.expander(f"{'📊' if 'float' in info['dtype'] or 'int' in info['dtype'] else '🏷️'}  {col}  ·  {info['dtype']}  ·  {info['unique']} unique", expanded=False):
                p1,p2,p3,p4 = st.columns(4)
                p1.metric("Type", info["dtype"])
                p2.metric("Nulls", f"{info['nulls']} ({round(info['nulls']/len(df)*100,1)}%)")
                p3.metric("Unique", info["unique"])
                p4.metric("Fill", f"{round(100-info['nulls']/len(df)*100,1)}%")
                if "mean" in info:
                    pm1,pm2,pm3,pm4 = st.columns(4)
                    pm1.metric("Min", round(info["min"],3))
                    pm2.metric("Max", round(info["max"],3))
                    pm3.metric("Mean", round(info["mean"],3))
                    pm4.metric("Std", round(info["std"],3))
                    try:
                        col_data = df[col].dropna()
                        if len(col_data) > 0:
                            bins = pd.cut(col_data, bins=min(15, col_data.nunique())).value_counts().sort_index()
                            st.bar_chart(pd.DataFrame({"count":bins.values}, index=bins.index.astype(str)))
                    except: pass
                else:
                    vc = df[col].value_counts().head(8)
                    if len(vc):
                        st.bar_chart(pd.DataFrame({"count":vc.values}, index=vc.index.astype(str)))

    # ── Tab 4 ──────────────────────────────────────────────────────────────────
    with t4:
        st.markdown('<div class="panel vi"><div class="panel-title">🤖 AI Analyst — Ask Anything</div><div style="font-size:.82rem;color:#7986A3;line-height:1.6;">Ask in plain English. NOVA generates analysis queries, explains results, and surfaces insights.</div></div>', unsafe_allow_html=True)

        for msg in st.session_state.chat:
            cls = "mu" if msg["role"]=="user" else "ma"
            lbl = "🧑 YOU" if msg["role"]=="user" else "⚡ NOVA AI"
            content = msg["content"]
            sql_m = re.search(r"```(?:sql)?\n?(.*?)```", content, re.DOTALL)
            if sql_m and msg["role"]=="assistant":
                pre  = content[:content.find("```")].strip()
                post = content[content.rfind("```")+3:].strip()
                if pre: st.markdown(f'<div class="msg ma"><div class="mlbl">{lbl}</div>{pre}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="sql-block">{sql_m.group(1).strip()}</div>', unsafe_allow_html=True)
                if post: st.markdown(f'<div class="msg ma">{post}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="msg {cls}"><div class="mlbl">{lbl}</div>{content}</div>', unsafe_allow_html=True)
            if "result" in msg and msg["result"] is not None:
                st.dataframe(msg["result"], use_container_width=True, height=220)
                res = msg["result"]
                ncr = [c for c in res.columns if pd.api.types.is_numeric_dtype(res[c])]
                scr = [c for c in res.columns if res[c].dtype=="object"]
                if scr and ncr and 2 <= len(res) <= 30:
                    try: st.bar_chart(res.set_index(scr[0])[ncr[0]])
                    except: pass

        with st.form("chat_form", clear_on_submit=True):
            qc1,qc2 = st.columns([6,1])
            with qc1:
                user_q = st.text_input("", placeholder="e.g. Show top 10 rows by revenue · Find missing values · What are the key trends?", label_visibility="collapsed")
            with qc2:
                sub = st.form_submit_button("ASK →", use_container_width=True)

        if sub and user_q.strip():
            sys_prompt = f"""You are NOVA, an expert AI data analyst. The user has a dataset with this schema:
{schema_str(df)}

Sample (3 rows):
{df.head(3).to_string()}

Rules:
1. For data questions, write a query in ```sql ... ``` blocks using table 'data'
2. Explain what the query does and what insights it reveals
3. For visualization requests, provide the data query + suggest chart type
4. For general questions, give analytical insights based on the schema and data
5. Be concise, precise and insightful. Focus on business value."""

            with st.spinner("🧠 Analyzing..."):
                try:
                    msgs = [{"role":"system","content":sys_prompt}]
                    for m in st.session_state.chat[-6:]: msgs.append({"role":m["role"],"content":m["content"]})
                    msgs.append({"role":"user","content":user_q})
                    resp = groq_call(groq_key, msgs)

                    st.session_state.chat.append({"role":"user","content":user_q})
                    sql_m = re.search(r"```(?:sql)?\n?(.*?)```", resp, re.DOTALL)
                    result_df = None
                    if sql_m:
                        res, err = run_query(df, sql_m.group(1).strip())
                        if res is not None and len(res) > 0: result_df = res
                    st.session_state.chat.append({"role":"assistant","content":resp,"result":result_df})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

        if st.session_state.chat:
            _,cl,_ = st.columns([2,1,2])
            with cl:
                if st.button("🗑️ CLEAR CHAT"): st.session_state.chat = []; st.rerun()

    # ── Tab 5 ──────────────────────────────────────────────────────────────────
    with t5:
        st.markdown('<div class="panel gr"><div class="panel-title">⚗️ Query Engine · Pandas SQL</div><div style="font-size:.82rem;color:#7986A3;">Run SQL-like queries on your dataset. Supports SELECT, GROUP BY, ORDER BY, WHERE, LIMIT.</div></div>', unsafe_allow_html=True)

        tmpl = {
            "SELECT * (25 rows)":    "SELECT * FROM data LIMIT 25",
            "Row Count":             "SELECT COUNT(*) FROM data",
            "Null Summary":          "SELECT null counts FROM data",
            "Numeric Statistics":    "SELECT statistics FROM data",
            "Distinct Counts":       "SELECT distinct counts FROM data",
            "Duplicate Rows":        "SELECT duplicate rows FROM data",
        }
        sel = st.selectbox("Quick Templates", ["Custom"]+list(tmpl.keys()))
        sql_q = st.text_area("QUERY", value=tmpl.get(sel,"SELECT * FROM data LIMIT 25"), height=100)

        rc1,rc2 = st.columns([1,1])
        with rc1: run_btn = st.button("▶ RUN QUERY", use_container_width=True)
        with rc2: exp_btn = st.button("🤖 AI EXPLAIN", use_container_width=True)

        if run_btn and sql_q.strip():
            with st.spinner("⚡ Running..."):
                res, err = run_query(df, sql_q)
                if err: st.error(f"Error: {err}")
                elif res is not None:
                    st.markdown(f'<div style="font-family:\'Space Mono\',monospace;font-size:.65rem;color:#00FF88;margin-bottom:.5rem;">✓ {len(res):,} rows returned</div>', unsafe_allow_html=True)
                    st.dataframe(res, use_container_width=True, height=320)
                    ncr = [c for c in res.columns if pd.api.types.is_numeric_dtype(res[c])]
                    scr = [c for c in res.columns if res[c].dtype=="object"]
                    if scr and ncr and 2<=len(res)<=30:
                        try: st.bar_chart(res.set_index(scr[0])[ncr[0]])
                        except: pass
                    st.download_button("⬇️ Download Result", res.to_csv(index=False).encode(),"query_result.csv","text/csv")

        if exp_btn and sql_q.strip():
            with st.spinner("🧠 Explaining..."):
                try:
                    r = groq_call(groq_key,[
                        {"role":"system","content":f"You are a data query expert. Explain this query against a dataset with schema:\n{schema_str(df)}\nBe concise."},
                        {"role":"user","content":f"Explain: {sql_q}"}
                    ], max_tokens=400)
                    st.markdown(f'<div class="msg ma"><div class="mlbl">⚡ NOVA AI — Explanation</div>{r}</div>', unsafe_allow_html=True)
                except Exception as e: st.error(f"Error: {e}")

else:
    st.markdown("""<div style="text-align:center;padding:3rem 1rem;">
        <div style="font-size:3.5rem;margin-bottom:1rem;">🔬</div>
        <div style="font-family:'Exo 2',sans-serif;font-size:1.1rem;font-weight:700;color:#EEF2FF;letter-spacing:.08em;margin-bottom:.5rem;">AWAITING DATA</div>
        <div style="color:#7986A3;font-size:.85rem;max-width:400px;margin:0 auto;line-height:1.7;">
            Upload a CSV, Excel or JSON file above to activate the full analysis suite.
        </div>
        <div style="display:flex;justify-content:center;gap:.6rem;margin-top:1.2rem;">
            <span class="chip ce">CSV</span><span class="chip cv">Excel</span><span class="chip cg">JSON</span>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("""<div style="text-align:center;padding:2rem 0 .5rem;">
    <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(0,229,255,.3),rgba(168,85,247,.3),transparent);margin-bottom:1rem;"></div>
    <div style="font-family:'Space Mono',monospace;font-size:.5rem;letter-spacing:.3em;color:#2D3550;">
        NOVA · AI DATA INTELLIGENCE · GROQ + LLaMA 3.3 70B &nbsp;|&nbsp; VERIFY AI-GENERATED RESULTS BEFORE CRITICAL DECISIONS
    </div>
</div>""", unsafe_allow_html=True)
