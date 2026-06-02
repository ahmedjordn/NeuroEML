# """
# NeuroEML Streamlit Dashboard — Aurora Redesign
# Public API, session_state keys, and report schema are unchanged.
# """

# import streamlit as st
# import pandas as pd
# import json
# import plotly.graph_objects as go
# from pathlib import Path
# from datetime import datetime
# import sys, os, tempfile

# sys.path.insert(0, str(Path(__file__).parent.parent))
# from models.analyzer import NeuroEMLAnalyzer

# st.set_page_config(
#     page_title="NeuroEML",
#     page_icon="🛡️",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ══════════════════════════════════════════════════════════════════════
# #  DESIGN SYSTEM — "Aurora"
# #  Deep indigo canvas · glassmorphism cards · cyan/violet aurora accents
# #  Type:  Space Grotesk (display) + Inter (UI) + JetBrains Mono (code)
# # ══════════════════════════════════════════════════════════════════════
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

# :root {
#   --bg-0:   #07091a;
#   --bg-1:   #0c1030;
#   --bg-2:   #11163d;
#   --surface:#141a45;
#   --glass:  rgba(255,255,255,.04);
#   --glass-bd:rgba(255,255,255,.08);
#   --ink-0:  #f5f7ff;
#   --ink-1:  #c7cbe8;
#   --ink-2:  #8b91c3;
#   --ink-3:  #5b6196;
#   --violet: #7c5cff;
#   --indigo: #5b7cff;
#   --cyan:   #22d3ee;
#   --magenta:#ec4899;
#   --emerald:#10d39e;
#   --amber:  #f6b73c;
#   --coral:  #ff6b6b;
#   --crit:   #ff5c7a;
#   --high:   #ffa24c;
#   --med:    #ffd84d;
#   --low:    #4ee0a0;
#   --safe:   #10d39e;
# }

# *, *::before, *::after { box-sizing: border-box; }
# html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

# /* ── Canvas: deep aurora gradient + soft mesh ── */
# .stApp {
#   background:
#     radial-gradient(1100px 700px at 88% -10%, rgba(124,92,255,.20), transparent 60%),
#     radial-gradient(900px 600px at -10% 110%, rgba(34,211,238,.16), transparent 60%),
#     radial-gradient(700px 500px at 50% 50%, rgba(236,72,153,.08), transparent 70%),
#     linear-gradient(180deg, #07091a 0%, #0a0d28 100%) !important;
#   color: var(--ink-0) !important;
# }
# .block-container {
#   padding: 1.8rem 2rem 3rem !important;
#   max-width: 1480px !important;
# }

# /* ── Sidebar ── */
# section[data-testid="stSidebar"] {
#   background: linear-gradient(180deg,#0a0d28 0%, #06081a 100%) !important;
#   border-right: 1px solid rgba(255,255,255,.06) !important;
#   box-shadow: inset -1px 0 0 rgba(124,92,255,.10);
# }
# section[data-testid="stSidebar"] > div { padding: 1.4rem 1.1rem !important; }
# section[data-testid="stSidebar"] * { color: var(--ink-1) !important; }
# section[data-testid="stSidebar"] strong,
# section[data-testid="stSidebar"] b { color: var(--ink-0) !important; }

# /* Sidebar file uploader */
# section[data-testid="stSidebar"] .stFileUploader > div {
#   background: rgba(255,255,255,.03) !important;
#   border: 1.5px dashed rgba(124,92,255,.45) !important;
#   border-radius: 14px !important;
#   transition: all .25s;
# }
# section[data-testid="stSidebar"] .stFileUploader > div:hover {
#   border-color: var(--cyan) !important;
#   background: rgba(34,211,238,.06) !important;
#   box-shadow: 0 0 0 3px rgba(34,211,238,.10);
# }
# section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] * {
#   color: var(--ink-2) !important; font-size: .8rem !important;
# }

# /* Sidebar download button */
# section[data-testid="stSidebar"] .stDownloadButton > button {
#   background: linear-gradient(135deg, rgba(124,92,255,.16), rgba(34,211,238,.10)) !important;
#   border: 1px solid rgba(124,92,255,.30) !important;
#   color: var(--ink-0) !important;
#   border-radius: 10px !important;
#   font-weight: 600 !important;
#   font-size: .8rem !important;
#   width: 100% !important;
#   padding: 10px 14px !important;
#   transition: all .2s !important;
#   text-align: left !important;
# }
# section[data-testid="stSidebar"] .stDownloadButton > button:hover {
#   border-color: var(--cyan) !important;
#   background: linear-gradient(135deg, rgba(124,92,255,.30), rgba(34,211,238,.20)) !important;
#   transform: translateY(-1px);
#   box-shadow: 0 8px 24px -8px rgba(124,92,255,.45);
# }

# /* Sidebar alerts */
# section[data-testid="stSidebar"] [data-testid="stAlert"] {
#   background: rgba(16,211,158,.10) !important;
#   border: 1px solid rgba(16,211,158,.30) !important;
#   border-radius: 10px !important;
# }
# section[data-testid="stSidebar"] [data-testid="stAlert"] * {
#   color: #6ef0c3 !important; font-size: .8rem !important;
# }
# section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.06) !important; }
# section[data-testid="stSidebar"] [data-testid="stSpinner"] * { color: var(--cyan) !important; }

# /* ── Headings ── */
# h1, h2, h3 { font-family:'Space Grotesk', 'Inter', sans-serif !important; color: var(--ink-0) !important; }
# h1 { font-size:1.85rem!important; font-weight:700!important; letter-spacing:-.5px!important; }
# h2 { font-size:1.1rem!important;  font-weight:600!important; }
# h3 { font-size:.95rem!important;  font-weight:600!important; color: var(--ink-1) !important; }
# p  { color: var(--ink-1); font-size:.88rem; line-height:1.65; }

# /* ── Tabs ── */
# .stTabs [data-baseweb="tab-list"] {
#   background: rgba(255,255,255,.03) !important;
#   border: 1px solid rgba(255,255,255,.07) !important;
#   backdrop-filter: blur(14px);
#   border-radius: 14px !important;
#   padding: 5px !important;
#   gap: 2px !important;
# }
# .stTabs [data-baseweb="tab"] {
#   border-radius: 10px !important;
#   font-weight: 500 !important;
#   font-size: .82rem !important;
#   color: var(--ink-2) !important;
#   padding: 8px 16px !important;
#   transition: all .2s;
# }
# .stTabs [data-baseweb="tab"]:hover { color: var(--ink-0) !important; }
# .stTabs [aria-selected="true"] {
#   background: linear-gradient(135deg, rgba(124,92,255,.28), rgba(34,211,238,.18)) !important;
#   color: #fff !important;
#   font-weight: 600 !important;
#   box-shadow: 0 4px 14px -4px rgba(124,92,255,.45), inset 0 1px 0 rgba(255,255,255,.08) !important;
# }
# .stTabs [data-baseweb="tab-highlight"] { background: transparent !important; }

# /* ── Expanders ── */
# .streamlit-expanderHeader, [data-testid="stExpander"] summary {
#   background: rgba(255,255,255,.03) !important;
#   border: 1px solid rgba(255,255,255,.07) !important;
#   border-radius: 10px !important;
#   color: var(--ink-0) !important;
#   font-weight: 500 !important;
#   font-size: .85rem !important;
#   padding: 12px 16px !important;
#   transition: all .2s;
# }
# [data-testid="stExpander"] summary:hover {
#   border-color: rgba(124,92,255,.40) !important;
#   background: rgba(124,92,255,.06) !important;
# }
# .streamlit-expanderContent, [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
#   background: rgba(255,255,255,.02) !important;
#   border: 1px solid rgba(255,255,255,.07) !important;
#   border-top: none !important;
#   border-radius: 0 0 10px 10px !important;
#   padding: 14px !important;
# }

# /* ── Alerts ── */
# [data-testid="stAlert"] {
#   border-radius: 12px !important;
#   border-width: 1px !important;
#   font-size: .85rem !important;
#   backdrop-filter: blur(10px);
# }

# /* ── Dividers ── */
# hr { border-color: rgba(255,255,255,.07) !important; }

# /* ── Code ── */
# code {
#   background: rgba(124,92,255,.12) !important;
#   color: #b7c5ff !important;
#   border-radius: 5px !important;
#   padding: 2px 7px !important;
#   font-family: 'JetBrains Mono', monospace !important;
#   font-size: .78rem !important;
#   border: 1px solid rgba(124,92,255,.20) !important;
# }

# /* ── Markdown text in main area ── */
# .main p, .main li, .main span, .main strong { color: var(--ink-1); }
# .main strong { color: var(--ink-0) !important; }

# /* ── Metrics (fallback) ── */
# [data-testid="stMetric"] {
#   background: var(--glass) !important;
#   border: 1px solid var(--glass-bd) !important;
#   border-radius: 14px !important;
#   padding: 16px 18px !important;
#   backdrop-filter: blur(14px);
# }
# [data-testid="stMetricLabel"] { font-size:.65rem!important; font-weight:700!important; text-transform:uppercase!important; letter-spacing:.10em!important; color: var(--ink-2) !important; }
# [data-testid="stMetricValue"] { font-size:1.45rem!important; font-weight:700!important; color: var(--ink-0) !important; font-family:'Space Grotesk', sans-serif !important; }

# /* ═══════════════════════════════════════
#    CUSTOM COMPONENTS
# ═══════════════════════════════════════ */

# /* ── Summary bar ── */
# .sum-bar {
#   background: linear-gradient(135deg, rgba(255,255,255,.04), rgba(255,255,255,.015));
#   border: 1px solid rgba(255,255,255,.08);
#   border-radius: 18px;
#   backdrop-filter: blur(18px);
#   box-shadow: 0 12px 40px -16px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.05);
#   display: grid;
#   grid-template-columns: auto 1px auto 1px auto 1px auto;
#   align-items: stretch;
#   overflow: hidden;
#   margin-bottom: 22px;
#   position: relative;
# }
# .sum-bar::before {
#   content:''; position:absolute; inset:0;
#   background: radial-gradient(600px 200px at 0% 0%, rgba(124,92,255,.10), transparent 60%);
#   pointer-events:none;
# }
# .sum-cell {
#   padding: 22px 32px; display:flex; flex-direction:column; justify-content:center;
#   position:relative; z-index:1;
# }
# .sum-cell.score-cell { padding: 22px 36px; }
# .sum-sep { background: linear-gradient(180deg, transparent, rgba(255,255,255,.10), transparent); width: 1px; }
# .sum-key {
#   font-size:.6rem; font-weight:700; text-transform:uppercase;
#   letter-spacing:.13em; color: var(--ink-2); margin-bottom:8px;
# }
# .sum-val {
#   font-family:'Space Grotesk', sans-serif;
#   font-size:1.4rem; font-weight:600; color: var(--ink-0); line-height:1.1;
# }
# .sum-score-num {
#   font-family:'Space Grotesk', sans-serif;
#   font-size: 3.2rem; font-weight: 700; line-height: 1; letter-spacing: -2px;
#   background-clip: text; -webkit-background-clip: text;
# }
# .sum-score-lbl {
#   font-size:.6rem; font-weight:700; text-transform:uppercase;
#   letter-spacing:.13em; margin-top:6px; opacity:.75;
# }

# /* ── Glass card ── */
# .w-card {
#   background: linear-gradient(135deg, rgba(255,255,255,.045), rgba(255,255,255,.015));
#   border: 1px solid rgba(255,255,255,.08);
#   border-radius: 16px;
#   backdrop-filter: blur(16px);
#   box-shadow: 0 8px 30px -12px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.04);
#   padding: 22px 24px;
#   margin-bottom: 18px;
#   transition: border-color .25s, transform .25s;
# }
# .w-card:hover { border-color: rgba(124,92,255,.25); }
# .card-label {
#   font-size:.62rem; font-weight:700; text-transform:uppercase;
#   letter-spacing:.14em; color: var(--ink-2); margin-bottom:14px;
#   display:flex; align-items:center; gap:8px;
# }
# .card-label::before {
#   content:''; width:6px; height:6px; border-radius:50%;
#   background: linear-gradient(135deg, var(--violet), var(--cyan));
#   box-shadow: 0 0 10px rgba(124,92,255,.7);
# }

# /* ── Auth pills ── */
# .auth-pill {
#   display:flex; align-items:center; gap:10px;
#   border-radius:10px; padding:11px 15px; margin:6px 0;
#   font-size:.84rem; font-weight:600;
#   backdrop-filter: blur(10px);
# }
# .auth-pill.pass    { background:rgba(16,211,158,.10); border:1px solid rgba(16,211,158,.30); color:#7ff0c5; }
# .auth-pill.fail    { background:rgba(255,92,122,.10); border:1px solid rgba(255,92,122,.30); color:#ffb1bf; }
# .auth-pill.unknown { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.10); color: var(--ink-1); }
# .auth-dot { width:9px; height:9px; border-radius:50%; flex-shrink:0; }
# .auth-dot.pass    { background: var(--safe);  box-shadow:0 0 10px rgba(16,211,158,.7); }
# .auth-dot.fail    { background: var(--crit);  box-shadow:0 0 10px rgba(255,92,122,.7); }
# .auth-dot.unknown { background: var(--ink-3); }

# /* ── Finding rows ── */
# .frow {
#   border-radius:8px; padding:10px 14px; margin:6px 0;
#   font-size:.83rem; line-height:1.55;
#   border-left:3px solid var(--violet);
#   background: rgba(124,92,255,.07); color: var(--ink-1);
# }
# .frow.crit { border-left-color: var(--crit); background: rgba(255,92,122,.10); color:#ffc1cd; }
# .frow.high { border-left-color: var(--high); background: rgba(255,162,76,.10); color:#ffd4a8; }
# .frow.med  { border-left-color: var(--med);  background: rgba(255,216,77,.10); color:#ffe999; }
# .frow.low  { border-left-color: var(--low);  background: rgba(78,224,160,.10); color:#9ff1c5; }

# /* ── Score chip ── */
# .score-chip {
#   display:inline-flex; align-items:baseline; gap:6px;
#   border-radius:12px; padding:11px 18px; margin-bottom:14px;
#   backdrop-filter: blur(8px);
# }
# .score-chip .n { font-family:'Space Grotesk', sans-serif; font-size:1.8rem; font-weight:700; line-height:1; }
# .score-chip .d { font-size:.72rem; font-weight:600; opacity:.75; text-transform:uppercase; letter-spacing:.08em; }

# /* ── Stat block ── */
# .stat-blk {
#   background: linear-gradient(135deg, rgba(255,255,255,.045), rgba(255,255,255,.015));
#   border: 1px solid rgba(255,255,255,.08);
#   border-radius: 16px; padding: 22px; text-align:center;
#   backdrop-filter: blur(14px);
#   box-shadow: 0 8px 24px -12px rgba(0,0,0,.5);
#   transition: transform .25s, border-color .25s;
# }
# .stat-blk:hover { transform: translateY(-2px); border-color: rgba(34,211,238,.30); }
# .stat-blk .n {
#   font-family:'Space Grotesk', sans-serif;
#   font-size:2.2rem; font-weight:700;
#   background: linear-gradient(135deg, var(--ink-0), var(--cyan));
#   -webkit-background-clip: text; background-clip: text; color: transparent;
# }
# .stat-blk .l {
#   font-size:.62rem; font-weight:700; text-transform:uppercase;
#   letter-spacing:.12em; color: var(--ink-2); margin-top:6px;
# }

# /* ── Rec rows ── */
# .rec-row {
#   border-radius:10px; padding:13px 16px; margin:7px 0;
#   font-size:.84rem; font-weight:500; line-height:1.6;
#   display:flex; gap:13px; align-items:flex-start;
#   backdrop-filter: blur(8px);
# }
# .rec-row.crit { background:rgba(255,92,122,.10); border:1px solid rgba(255,92,122,.30); color:#ffc1cd; }
# .rec-row.high { background:rgba(255,162,76,.10); border:1px solid rgba(255,162,76,.30); color:#ffd4a8; }
# .rec-row.med  { background:rgba(255,216,77,.10); border:1px solid rgba(255,216,77,.30); color:#ffe999; }
# .rec-row.info { background:rgba(91,124,255,.10); border:1px solid rgba(91,124,255,.30); color:#b9c5ff; }
# .rec-row.def  { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.10); color: var(--ink-1); }
# .rec-num {
#   flex-shrink:0; width:24px; height:24px; border-radius:7px;
#   background: linear-gradient(135deg, rgba(124,92,255,.30), rgba(34,211,238,.20));
#   font-family:'Space Grotesk', sans-serif;
#   font-size:.74rem; font-weight:700; color: var(--ink-0);
#   display:flex; align-items:center; justify-content:center; margin-top:1px;
#   border: 1px solid rgba(255,255,255,.08);
# }

# /* ── URL risk badge ── */
# .url-badge {
#   border-radius:14px; padding:20px; text-align:center;
#   backdrop-filter: blur(10px);
# }
# .url-badge .n { font-family:'Space Grotesk', sans-serif; font-size:2.2rem; font-weight:700; }
# .url-badge .l { font-size:.64rem; font-weight:700; text-transform:uppercase; letter-spacing:.11em; margin-top:6px; opacity:.85; }

# /* ── Sidebar nav label ── */
# .sb-section {
#   font-size:.6rem; font-weight:700; text-transform:uppercase;
#   letter-spacing:.14em; color: var(--ink-3); margin:18px 0 9px;
# }

# /* ── Hero ── */
# .hero-wrap {
#   background:
#     radial-gradient(700px 320px at 90% 0%, rgba(124,92,255,.30), transparent 60%),
#     radial-gradient(500px 300px at 0% 100%, rgba(34,211,238,.22), transparent 60%),
#     linear-gradient(135deg, rgba(20,26,69,.85), rgba(12,16,48,.92));
#   border: 1px solid rgba(255,255,255,.10);
#   border-radius: 22px;
#   padding: 58px 52px;
#   position: relative; overflow: hidden;
#   margin-bottom: 26px;
#   backdrop-filter: blur(18px);
#   box-shadow: 0 24px 60px -24px rgba(0,0,0,.7), inset 0 1px 0 rgba(255,255,255,.06);
# }
# .hero-wrap::after {
#   content:''; position:absolute; right:-80px; top:-80px;
#   width:360px; height:360px;
#   background: radial-gradient(circle, rgba(236,72,153,.18) 0%, transparent 65%);
#   pointer-events:none;
# }
# .hero-wrap * { position:relative; z-index:1; }
# .hero-badge {
#   display:inline-flex; align-items:center; gap:8px;
#   background: rgba(124,92,255,.18);
#   border: 1px solid rgba(124,92,255,.40);
#   border-radius:999px; padding:6px 14px;
#   font-size:.74rem; font-weight:600;
#   color:#c4b5fd; margin-bottom:18px;
#   backdrop-filter: blur(10px);
# }
# .hero-badge::before {
#   content:''; width:6px; height:6px; border-radius:50%;
#   background: var(--cyan); box-shadow:0 0 12px var(--cyan);
#   animation: pulse 2s ease-in-out infinite;
# }
# @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }
# .hero-title {
#   font-family:'Space Grotesk', sans-serif !important;
#   font-size:3rem !important; font-weight:700 !important;
#   letter-spacing:-1.2px !important; line-height:1.05 !important;
#   margin-bottom:14px !important;
#   background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 50%, #7dd3fc 100%);
#   -webkit-background-clip: text; background-clip: text;
#   -webkit-text-fill-color: transparent; color: transparent !important;
# }
# .hero-sub {
#   color: var(--ink-1) !important; font-size:1rem !important;
#   max-width:560px; line-height:1.7; margin-bottom:26px;
# }
# .hero-tag {
#   display:inline-block;
#   background: rgba(255,255,255,.05);
#   border:1px solid rgba(255,255,255,.10);
#   border-radius:8px; padding:5px 12px;
#   font-size:.74rem; color: var(--ink-1); margin:3px;
#   font-weight:500; transition: all .2s;
# }
# .hero-tag:hover { border-color: rgba(124,92,255,.40); color: var(--ink-0); }

# /* ── Feature card ── */
# .feat {
#   background: linear-gradient(135deg, rgba(255,255,255,.045), rgba(255,255,255,.015));
#   border:1px solid rgba(255,255,255,.08);
#   border-radius:16px; padding:24px; height:100%;
#   backdrop-filter: blur(14px);
#   box-shadow: 0 8px 24px -12px rgba(0,0,0,.5);
#   transition: transform .25s, border-color .25s;
# }
# .feat:hover { transform: translateY(-3px); border-color: rgba(124,92,255,.30); }
# .feat-icon {
#   font-size:1.6rem; margin-bottom:12px;
#   display:inline-flex; width:44px; height:44px; border-radius:12px;
#   align-items:center; justify-content:center;
#   background: linear-gradient(135deg, rgba(124,92,255,.20), rgba(34,211,238,.12));
#   border: 1px solid rgba(255,255,255,.08);
# }
# .feat-h {
#   font-family:'Space Grotesk', sans-serif;
#   font-size:1rem; font-weight:600; color: var(--ink-0); margin-bottom:8px;
# }
# .feat-p { font-size:.83rem; color: var(--ink-2); line-height:1.6; }

# /* ── Sidebar logo ── */
# .sb-logo {
#   display:flex; align-items:center; gap:12px;
#   padding-bottom:18px; border-bottom:1px solid rgba(255,255,255,.06);
#   margin-bottom:18px;
# }
# .sb-logo-icon {
#   width:40px; height:40px; border-radius:11px;
#   background: linear-gradient(135deg, var(--violet), var(--cyan));
#   display:flex; align-items:center; justify-content:center;
#   font-size:1.15rem; flex-shrink:0;
#   box-shadow: 0 4px 16px rgba(124,92,255,.5), inset 0 1px 0 rgba(255,255,255,.20);
# }
# .sb-logo-name {
#   font-family:'Space Grotesk', sans-serif !important;
#   font-size:1.1rem !important; font-weight:700 !important;
#   color: var(--ink-0) !important; letter-spacing:-.3px;
# }
# .sb-logo-sub { font-size:.7rem !important; color: var(--ink-3) !important; margin-top:2px; }
# </style>
# """, unsafe_allow_html=True)

# # ── Session ────────────────────────────────────────────────────────────────────
# if 'report'   not in st.session_state: st.session_state.report   = None
# if 'analyzer' not in st.session_state: st.session_state.analyzer = NeuroEMLAnalyzer()


# # ── Colour helpers (Aurora palette) ────────────────────────────────────────────
# _TIERS = {
#     'critical': ('#ff5c7a', 'rgba(255,92,122,.10)',  'rgba(255,92,122,.35)',  'crit'),
#     'high':     ('#ffa24c', 'rgba(255,162,76,.10)',  'rgba(255,162,76,.35)',  'high'),
#     'medium':   ('#ffd84d', 'rgba(255,216,77,.10)',  'rgba(255,216,77,.35)',  'med'),
#     'low':      ('#4ee0a0', 'rgba(78,224,160,.10)',  'rgba(78,224,160,.35)',  'low'),
#     'safe':     ('#10d39e', 'rgba(16,211,158,.10)',  'rgba(16,211,158,.35)',  'low'),
# }

# def _tier(score):
#     if score >= 80: return 'critical'
#     if score >= 60: return 'high'
#     if score >= 40: return 'medium'
#     if score >= 20: return 'low'
#     return 'safe'

# def rc(score): return _TIERS[_tier(score)][0]
# def rb(score): return _TIERS[_tier(score)][1]
# def rd(score): return _TIERS[_tier(score)][2]
# def rf(score): return _TIERS[_tier(score)][3]

# def rlabel(score):
#     return {'critical':'CRITICAL','high':'HIGH','medium':'MEDIUM','low':'LOW','safe':'SAFE'}[_tier(score)]

# def ricon(score):
#     return {'critical':'🚨','high':'⚠️','medium':'⚡','low':'✓','safe':'✅'}[_tier(score)]


# # ── Chart builders ─────────────────────────────────────────────────────────────

# def gauge(score):
#     color = rc(score)
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=score,
#         title={'text':'Risk Score','font':{'size':13,'color':'#8b91c3','family':'Inter'}},
#         number={'font':{'size':54,'color':color,'family':'Space Grotesk'}},
#         domain={'x':[0,1],'y':[0,1]},
#         gauge={
#             'axis':{'range':[0,100],'tickfont':{'color':'#8b91c3','size':9},'tickcolor':'rgba(255,255,255,.10)'},
#             'bar':{'color':color,'thickness':.24},
#             'bgcolor':'rgba(255,255,255,.03)',
#             'bordercolor':'rgba(255,255,255,.08)','borderwidth':1,
#             'steps':[
#                 {'range':[0,20], 'color':'rgba(16,211,158,.18)'},
#                 {'range':[20,40],'color':'rgba(78,224,160,.18)'},
#                 {'range':[40,60],'color':'rgba(255,216,77,.18)'},
#                 {'range':[60,80],'color':'rgba(255,162,76,.18)'},
#                 {'range':[80,100],'color':'rgba(255,92,122,.20)'},
#             ],
#             'threshold':{'line':{'color':color,'width':3},'thickness':.85,'value':score},
#         }
#     ))
#     fig.update_layout(
#         height=300, margin=dict(l=28,r=28,t=56,b=8),
#         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
#         font={'family':'Inter','color':'#c7cbe8'},
#     )
#     return fig


# def bar_chart(report):
#     scores = {
#         'Identity':   report.get('engines',{}).get('identity_engine',{}).get('risk_score',0),
#         'Header Auth':report.get('engines',{}).get('header_engine',{}).get('auth_risk_score',0),
#         'URLs':       report.get('engines',{}).get('url_engine',{}).get('overall_risk_score',0),
#         'AI Profiler':report.get('ai_analysis',{}).get('profiler',{}).get('overall_suspicion_score',0),
#         'AI Auditor': report.get('ai_analysis',{}).get('auditor',{}).get('technical_risk_score',0),
#         'OSINT':      report.get('osint_enrichment',{}).get('osint_risk_score',0),
#     }
#     vals   = list(scores.values())
#     labels = list(scores.keys())
#     colors = [rc(v) for v in vals]

#     fig = go.Figure(go.Bar(
#         y=labels, x=vals, orientation='h',
#         marker=dict(color=colors, line=dict(color='rgba(255,255,255,.08)',width=1)),
#         text=[str(v) for v in vals], textposition='outside',
#         textfont=dict(color='#c7cbe8',size=11,family='Space Grotesk'),
#     ))
#     fig.update_layout(
#         title=dict(text='Engine Scores', font=dict(size=13,color='#8b91c3',family='Inter')),
#         height=300, margin=dict(l=10,r=50,t=52,b=10),
#         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
#         xaxis=dict(range=[0,118],showgrid=True,gridcolor='rgba(255,255,255,.06)',
#                    tickfont=dict(color='#8b91c3',size=9), zeroline=False),
#         yaxis=dict(tickfont=dict(color='#c7cbe8',size=11,family='Inter')),
#     )
#     return fig


# # ── Section renderers ──────────────────────────────────────────────────────────

# def render_email_analysis(report):
#     identity = report.get('engines',{}).get('identity_engine',{})
#     auth     = report.get('engines',{}).get('header_engine',{}).get('authentication',{})

#     col1, col2 = st.columns(2, gap="large")

#     with col1:
#         st.markdown('<div class="w-card"><div class="card-label">📬 Email Identity</div>', unsafe_allow_html=True)
#         if identity:
#             st.markdown(f"**From** `{identity.get('email_address','N/A')}`")
#             st.markdown(f"**Name** {identity.get('display_name','N/A')}")
#             st.markdown(f"**Domain** `{identity.get('domain','N/A')}`")
#             if identity.get('homograph_check',{}).get('is_spoofing_attempt'):
#                 st.error("🚨 Spoofing Attempt")
#                 for ind in identity['homograph_check'].get('indicators',[]):
#                     st.markdown(f'<div class="frow crit">• {ind}</div>', unsafe_allow_html=True)
#             if identity.get('punycode_check',{}).get('is_suspicious'):
#                 st.error("🚨 Punycode / Homograph Attack")
#                 pc = identity['punycode_check']
#                 st.markdown(f'<div class="frow crit">Original: {pc.get("original","?")} → Decoded: {pc.get("decoded","?")}</div>',
#                             unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col2:
#         st.markdown('<div class="w-card"><div class="card-label">🔐 Authentication</div>', unsafe_allow_html=True)
#         for proto, data in [('SPF', auth.get('spf',{})), ('DKIM', auth.get('dkim',{})), ('DMARC', auth.get('dmarc',{}))]:
#             status = data.get('status','unknown')
#             domain = data.get('domain','')
#             detail = f" · {domain}" if domain else ""
#             if status == 'pass':
#                 cls, dot = 'pass', 'pass'
#             elif status in ('fail','none','softfail'):
#                 cls, dot = 'fail', 'fail'
#             else:
#                 cls, dot = 'unknown', 'unknown'
#             st.markdown(
#                 f'<div class="auth-pill {cls}">'
#                 f'<span class="auth-dot {dot}"></span>'
#                 f'<strong>{proto}</strong>&nbsp;{status.upper()}{detail}'
#                 f'</div>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#     # Attachments
#     attachments = report.get('parsing', {})
#     if attachments and attachments.get('attachments_count', 0) > 0:
#         st.info(f"📎 {attachments['attachments_count']} attachment(s) found")
#     else:
#         st.success("No attachments detected.")


# def render_url_analysis(report):
#     urls = report.get('engines',{}).get('url_engine',{}).get('urls',[])
#     if not urls:
#         st.info("No URLs found in this email.")
#         return
#     for url_data in urls:
#         score = url_data.get('risk_score', 0)
#         color = rc(score)
#         bg    = rb(score)
#         label = rlabel(score)
#         short = url_data['url'][:68] + ('…' if len(url_data['url'])>68 else '')
#         with st.expander(f"🔗  {short}"):
#             col1, col2 = st.columns([3, 1], gap="large")
#             with col1:
#                 st.code(url_data['url'], language=None)
#                 expanded = url_data.get('expanded',{})
#                 st.markdown(f"**Destination** `{expanded.get('final','Unknown')}`")
#                 st.markdown(f"**Redirects** {expanded.get('redirects',0)}")
#                 if expanded.get('redirect_chain'):
#                     for step in expanded['redirect_chain']:
#                         st.markdown(f'<div class="frow">→ {step}</div>', unsafe_allow_html=True)
#             with col2:
#                 st.markdown(
#                     f'<div class="url-badge" style="background:{bg};border:1.5px solid {rd(score)}">'
#                     f'<div class="n" style="color:{color}">{score}</div>'
#                     f'<div class="l" style="color:{color}">{label}</div>'
#                     f'</div>', unsafe_allow_html=True)
#                 suspicious = url_data.get('suspicious_check',{})
#                 for ind in suspicious.get('suspicious_indicators',[]):
#                     st.markdown(f'<div class="frow crit" style="font-size:.76rem;margin-top:8px">⚑ {ind}</div>',
#                                 unsafe_allow_html=True)


# def render_ai_analysis(report):
#     col1, col2 = st.columns(2, gap="large")

#     with col1:
#         profiler = report.get('ai_analysis',{}).get('profiler',{})
#         st.markdown('<div class="w-card"><div class="card-label">🧠 AI Profiler — Psychological</div>', unsafe_allow_html=True)
#         if profiler.get('error'):
#             st.error(profiler['error'])
#         else:
#             score = profiler.get('overall_suspicion_score',0)
#             st.markdown(
#                 f'<div class="score-chip" style="background:{rb(score)};border:1.5px solid {rd(score)}">'
#                 f'<span class="n" style="color:{rc(score)}">{score}</span>'
#                 f'<span class="d" style="color:{rc(score)}">/100 suspicion</span>'
#                 f'</div>', unsafe_allow_html=True)
#             if profiler.get('summary'):
#                 st.markdown(f'<p style="margin-bottom:12px">{profiler["summary"]}</p>', unsafe_allow_html=True)
#             tactics = profiler.get('tactics',{})
#             if tactics:
#                 st.markdown('<div class="card-label" style="margin-top:10px">Detected Tactics</div>', unsafe_allow_html=True)
#                 for tactic, data in tactics.items():
#                     if isinstance(data,dict) and data.get('score',0)>0:
#                         with st.expander(f"{tactic.replace('_',' ').title()} · {data.get('score',0)}/100"):
#                             for ind in data.get('indicators',[])[:3]:
#                                 st.markdown(f'<div class="frow high">• {ind}</div>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col2:
#         auditor = report.get('ai_analysis',{}).get('auditor',{})
#         st.markdown('<div class="w-card"><div class="card-label">🔒 AI Auditor — Technical</div>', unsafe_allow_html=True)
#         if auditor.get('error'):
#             st.error(auditor['error'])
#         else:
#             score = auditor.get('technical_risk_score',0)
#             st.markdown(
#                 f'<div class="score-chip" style="background:{rb(score)};border:1.5px solid {rd(score)}">'
#                 f'<span class="n" style="color:{rc(score)}">{score}</span>'
#                 f'<span class="d" style="color:{rc(score)}">/100 tech risk</span>'
#                 f'</div>', unsafe_allow_html=True)
#             if auditor.get('recommendations'):
#                 st.markdown("**Recommendations**")
#                 st.markdown(f'<p style="margin-bottom:12px">{auditor["recommendations"]}</p>', unsafe_allow_html=True)
#             for finding in auditor.get('critical_findings',[]):
#                 st.markdown(f'<div class="frow crit">⚑ {finding}</div>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)


# def render_osint(report):
#     osint = report.get('osint_enrichment',{})
#     col1, col2, col3 = st.columns(3)
#     for col, lbl, val in zip([col1,col2,col3],[
#         "Total IOCs","Flagged IOCs","OSINT Risk"],[
#         osint.get('total_iocs',0), osint.get('flagged_iocs',0), osint.get('osint_risk_score',0)]):
#         with col:
#             st.markdown(f'<div class="stat-blk"><div class="n">{val}</div><div class="l">{lbl}</div></div>',
#                         unsafe_allow_html=True)
#     st.markdown("<br>", unsafe_allow_html=True)
#     high_risk = osint.get('high_risk_indicators',[])
#     if high_risk:
#         st.error("High Risk Indicators Found")
#         for ind in high_risk:
#             ioc_type = ind.get('type','?').upper()
#             value    = ind.get('value','?')
#             detail   = (f"Detected by {ind.get('detections',0)} engines" if ioc_type=='URL'
#                         else f"Abuse Score: {ind.get('abuse_score',0)}" if ioc_type=='IP'
#                         else value)
#             st.markdown(
#                 f'<div class="frow crit"><strong>{ioc_type}</strong> — {detail}'
#                 f'<br><span style="font-size:.76rem;opacity:.7">{value}</span></div>',
#                 unsafe_allow_html=True)
#     else:
#         st.success("No high-risk IOCs detected.")


# def render_recommendations(report):
#     recs = report.get('recommendations',[])
#     if not recs:
#         st.info("No recommendations at this time.")
#         return
#     for idx, rec in enumerate(recs, 1):
#         if   '🚨' in rec:              cls = 'crit'
#         elif '⚠️' in rec or '🔴' in rec: cls = 'high'
#         elif '⚡' in rec:              cls = 'med'
#         elif 'ℹ' in rec or '🔵' in rec: cls = 'info'
#         else:                           cls = 'def'
#         st.markdown(
#             f'<div class="rec-row {cls}">'
#             f'<span class="rec-num">{idx}</span>'
#             f'<span>{rec}</span>'
#             f'</div>', unsafe_allow_html=True)


# # ── Main ──────────────────────────────────────────────────────────────────────
# def main():

#     # ── Sidebar ────────────────────────────────────────────────────────────
#     with st.sidebar:
#         st.markdown("""
#         <div class="sb-logo">
#           <div class="sb-logo-icon">🛡️</div>
#           <div>
#             <div class="sb-logo-name">NeuroEML</div>
#             <div class="sb-logo-sub">Security Analysis</div>
#           </div>
#         </div>
#         """, unsafe_allow_html=True)

#         st.markdown('<div class="sb-section">Upload</div>', unsafe_allow_html=True)
#         uploaded_file = st.file_uploader(
#             "eml", type=['eml'], label_visibility="collapsed",
#             help="Upload an .eml file for analysis")

#         if uploaded_file is not None:
#             with st.spinner("Analyzing…"):
#                 temp_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
#                 with open(temp_path,'wb') as f:
#                     f.write(uploaded_file.getbuffer())
#                 try:
#                     st.session_state.report = st.session_state.analyzer.analyze_email(temp_path)
#                     st.success("Analysis complete")
#                 except Exception as e:
#                     st.error(str(e))

#         if st.session_state.report:
#             st.markdown('<div class="sb-section">Export</div>', unsafe_allow_html=True)
#             json_str = json.dumps(st.session_state.report, indent=2)
#             st.download_button("📄  JSON Report", data=json_str,
#                 file_name=f"neuroeml_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
#                 mime="application/json")
#             osint = st.session_state.report.get('osint_enrichment',{})
#             if osint.get('high_risk_indicators'):
#                 df = pd.DataFrame(osint['high_risk_indicators'])
#                 st.download_button("📊  IOCs CSV", data=df.to_csv(index=False),
#                     file_name=f"iocs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
#                     mime="text/csv")

#     # ── Main area ──────────────────────────────────────────────────────────
#     if st.session_state.report is None:

#         st.markdown("""
#         <div class="hero-wrap">
#           <div class="hero-badge">Email Threat Intelligence</div>
#           <div class="hero-title">NeuroEML</div>
#           <p class="hero-sub">
#             Upload a <strong style="color:#e2e8f0">.eml</strong> file to run a full six-layer
#             threat analysis — identity spoofing, header auth, URL inspection, AI profiling,
#             and OSINT enrichment in one report.
#           </p>
#           <div>
#             <span class="hero-tag">Identity Engine</span>
#             <span class="hero-tag">SPF · DKIM · DMARC</span>
#             <span class="hero-tag">URL Analysis</span>
#             <span class="hero-tag">AI Profiler</span>
#             <span class="hero-tag">AI Auditor</span>
#             <span class="hero-tag">OSINT / VirusTotal</span>
#           </div>
#         </div>
#         """, unsafe_allow_html=True)

#         c1, c2, c3 = st.columns(3)
#         for col, icon, title, desc in zip([c1,c2,c3],
#             ['🔍','🤖','🌐'],
#             ['Six-Layer Analysis','AI-Driven Profiling','Live OSINT'],
#             ['Every dimension of an email is inspected independently — identity, headers, links, content, and metadata.',
#              'Psychological manipulation tactics and technical obfuscation detected using large language models.',
#              'Domains, IPs, and URLs are enriched in real time against VirusTotal and AbuseIPDB.']):
#             with col:
#                 st.markdown(f'<div class="feat"><div class="feat-icon">{icon}</div>'
#                             f'<div class="feat-h">{title}</div>'
#                             f'<div class="feat-p">{desc}</div></div>', unsafe_allow_html=True)

#     else:
#         report     = st.session_state.report
#         risk_score = report.get('final_risk_score', 0)
#         level      = rlabel(risk_score)
#         icon       = ricon(risk_score)
#         color      = rc(risk_score)
#         timestamp  = report.get('metadata',{}).get('analysis_timestamp','')
#         date_str   = timestamp.split('T')[0] if timestamp else '—'
#         status     = report.get('metadata',{}).get('status','Unknown').upper()

#         # ── Summary bar ────────────────────────────────────────────────────
#         st.markdown(f"""
#         <div class="sum-bar">
#           <div class="sum-cell score-cell">
#             <div class="sum-score-num" style="color:{color}">{risk_score}</div>
#             <div class="sum-score-lbl" style="color:{color}">Risk Score</div>
#           </div>
#           <div class="sum-sep"></div>
#           <div class="sum-cell">
#             <div class="sum-key">Risk Level</div>
#             <div class="sum-val" style="color:{color}">{icon}&nbsp;{level}</div>
#           </div>
#           <div class="sum-sep"></div>
#           <div class="sum-cell">
#             <div class="sum-key">Status</div>
#             <div class="sum-val">{status}</div>
#           </div>
#           <div class="sum-sep"></div>
#           <div class="sum-cell">
#             <div class="sum-key">Analyzed</div>
#             <div class="sum-val" style="font-size:1.05rem;font-weight:500;color:#c7cbe8">{date_str}</div>
#           </div>
#         </div>
#         """, unsafe_allow_html=True)

#         # ── Tab navigation ──────────────────────────────────────────────────
#         tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
#             "📊 Overview",
#             "📧 Email",
#             "🔗 URLs",
#             "🧠 AI Analysis",
#             "🌐 OSINT",
#             "📋 Recommendations",
#         ])

#         with tab1:
#             col1, col2 = st.columns(2, gap="large")
#             with col1:
#                 st.plotly_chart(gauge(risk_score), use_container_width=True)
#             with col2:
#                 st.plotly_chart(bar_chart(report), use_container_width=True)

#         with tab2:
#             render_email_analysis(report)

#         with tab3:
#             render_url_analysis(report)

#         with tab4:
#             render_ai_analysis(report)

#         with tab5:
#             render_osint(report)

#         with tab6:
#             st.markdown('<div class="w-card"><div class="card-label">📋 Security Recommendations</div>',
#                         unsafe_allow_html=True)
#             render_recommendations(report)
#             st.markdown('</div>', unsafe_allow_html=True)

#         st.markdown("""
#         <p style="text-align:center;color:#5b6196;font-size:.72rem;padding:30px 0 4px;letter-spacing:.05em">
#           NeuroEML v1.0 &nbsp;·&nbsp; Email Security Analysis Platform &nbsp;·&nbsp;
#           Authorized security testing only
#         </p>
#         """, unsafe_allow_html=True)


# if __name__ == "__main__":
#     main()

"""
NeuroEML Streamlit Dashboard — Aurora Redesign
Public API, session_state keys, and report schema are unchanged.
"""

import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import sys, os, tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))
from models.analyzer import NeuroEMLAnalyzer

st.set_page_config(
    page_title="NeuroEML",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════
#  DESIGN SYSTEM — "Aurora"
#  Deep indigo canvas · glassmorphism cards · cyan/violet aurora accents
#  Type:  Space Grotesk (display) + Inter (UI) + JetBrains Mono (code)
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg-0:   #07091a;
  --bg-1:   #0c1030;
  --bg-2:   #11163d;
  --surface:#141a45;
  --glass:  rgba(255,255,255,.04);
  --glass-bd:rgba(255,255,255,.08);
  --ink-0:  #f5f7ff;
  --ink-1:  #c7cbe8;
  --ink-2:  #8b91c3;
  --ink-3:  #5b6196;
  --violet: #7c5cff;
  --indigo: #5b7cff;
  --cyan:   #22d3ee;
  --magenta:#ec4899;
  --emerald:#10d39e;
  --amber:  #f6b73c;
  --coral:  #ff6b6b;
  --crit:   #ff5c7a;
  --high:   #ffa24c;
  --med:    #ffd84d;
  --low:    #4ee0a0;
  --safe:   #10d39e;
}

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* ── Canvas: deep aurora gradient + soft mesh ── */
.stApp {
  background:
    radial-gradient(1100px 700px at 88% -10%, rgba(124,92,255,.20), transparent 60%),
    radial-gradient(900px 600px at -10% 110%, rgba(34,211,238,.16), transparent 60%),
    radial-gradient(700px 500px at 50% 50%, rgba(236,72,153,.08), transparent 70%),
    linear-gradient(180deg, #07091a 0%, #0a0d28 100%) !important;
  color: var(--ink-0) !important;
}
.block-container {
  padding: 1.8rem 2rem 3rem !important;
  max-width: 1480px !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#0a0d28 0%, #06081a 100%) !important;
  border-right: 1px solid rgba(255,255,255,.06) !important;
  box-shadow: inset -1px 0 0 rgba(124,92,255,.10);
}
section[data-testid="stSidebar"] > div { padding: 1.4rem 1.1rem !important; }
section[data-testid="stSidebar"] * { color: var(--ink-1) !important; }
section[data-testid="stSidebar"] strong,
section[data-testid="stSidebar"] b { color: var(--ink-0) !important; }

/* Sidebar file uploader */
section[data-testid="stSidebar"] .stFileUploader > div {
  background: rgba(255,255,255,.03) !important;
  border: 1.5px dashed rgba(124,92,255,.45) !important;
  border-radius: 14px !important;
  transition: all .25s;
}
section[data-testid="stSidebar"] .stFileUploader > div:hover {
  border-color: var(--cyan) !important;
  background: rgba(34,211,238,.06) !important;
  box-shadow: 0 0 0 3px rgba(34,211,238,.10);
}
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] * {
  color: var(--ink-2) !important; font-size: .8rem !important;
}

/* Sidebar download button */
section[data-testid="stSidebar"] .stDownloadButton > button {
  background: linear-gradient(135deg, rgba(124,92,255,.16), rgba(34,211,238,.10)) !important;
  border: 1px solid rgba(124,92,255,.30) !important;
  color: var(--ink-0) !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  font-size: .8rem !important;
  width: 100% !important;
  padding: 10px 14px !important;
  transition: all .2s !important;
  text-align: left !important;
}
section[data-testid="stSidebar"] .stDownloadButton > button:hover {
  border-color: var(--cyan) !important;
  background: linear-gradient(135deg, rgba(124,92,255,.30), rgba(34,211,238,.20)) !important;
  transform: translateY(-1px);
  box-shadow: 0 8px 24px -8px rgba(124,92,255,.45);
}

/* Sidebar alerts */
section[data-testid="stSidebar"] [data-testid="stAlert"] {
  background: rgba(16,211,158,.10) !important;
  border: 1px solid rgba(16,211,158,.30) !important;
  border-radius: 10px !important;
}
section[data-testid="stSidebar"] [data-testid="stAlert"] * {
  color: #6ef0c3 !important; font-size: .8rem !important;
}
section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.06) !important; }
section[data-testid="stSidebar"] [data-testid="stSpinner"] * { color: var(--cyan) !important; }

/* ── Headings ── */
h1, h2, h3 { font-family:'Space Grotesk', 'Inter', sans-serif !important; color: var(--ink-0) !important; }
h1 { font-size:1.85rem!important; font-weight:700!important; letter-spacing:-.5px!important; }
h2 { font-size:1.1rem!important;  font-weight:600!important; }
h3 { font-size:.95rem!important;  font-weight:600!important; color: var(--ink-1) !important; }
p  { color: var(--ink-1); font-size:.88rem; line-height:1.65; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(255,255,255,.03) !important;
  border: 1px solid rgba(255,255,255,.07) !important;
  backdrop-filter: blur(14px);
  border-radius: 14px !important;
  padding: 5px !important;
  gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px !important;
  font-weight: 500 !important;
  font-size: .82rem !important;
  color: var(--ink-2) !important;
  padding: 8px 16px !important;
  transition: all .2s;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--ink-0) !important; }
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(124,92,255,.28), rgba(34,211,238,.18)) !important;
  color: #fff !important;
  font-weight: 600 !important;
  box-shadow: 0 4px 14px -4px rgba(124,92,255,.45), inset 0 1px 0 rgba(255,255,255,.08) !important;
}
.stTabs [data-baseweb="tab-highlight"] { background: transparent !important; }

/* ── Expanders ── */
.streamlit-expanderHeader, [data-testid="stExpander"] summary {
  background: rgba(255,255,255,.03) !important;
  border: 1px solid rgba(255,255,255,.07) !important;
  border-radius: 10px !important;
  color: var(--ink-0) !important;
  font-weight: 500 !important;
  font-size: .85rem !important;
  padding: 12px 16px !important;
  transition: all .2s;
}
[data-testid="stExpander"] summary:hover {
  border-color: rgba(124,92,255,.40) !important;
  background: rgba(124,92,255,.06) !important;
}
.streamlit-expanderContent, [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
  background: rgba(255,255,255,.02) !important;
  border: 1px solid rgba(255,255,255,.07) !important;
  border-top: none !important;
  border-radius: 0 0 10px 10px !important;
  padding: 14px !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
  border-radius: 12px !important;
  border-width: 1px !important;
  font-size: .85rem !important;
  backdrop-filter: blur(10px);
}

/* ── Dividers ── */
hr { border-color: rgba(255,255,255,.07) !important; }

/* ── Code ── */
code {
  background: rgba(124,92,255,.12) !important;
  color: #b7c5ff !important;
  border-radius: 5px !important;
  padding: 2px 7px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: .78rem !important;
  border: 1px solid rgba(124,92,255,.20) !important;
}

/* ── Markdown text in main area ── */
.main p, .main li, .main span, .main strong { color: var(--ink-1); }
.main strong { color: var(--ink-0) !important; }

/* ── Metrics (fallback) ── */
[data-testid="stMetric"] {
  background: var(--glass) !important;
  border: 1px solid var(--glass-bd) !important;
  border-radius: 14px !important;
  padding: 16px 18px !important;
  backdrop-filter: blur(14px);
}
[data-testid="stMetricLabel"] { font-size:.65rem!important; font-weight:700!important; text-transform:uppercase!important; letter-spacing:.10em!important; color: var(--ink-2) !important; }
[data-testid="stMetricValue"] { font-size:1.45rem!important; font-weight:700!important; color: var(--ink-0) !important; font-family:'Space Grotesk', sans-serif !important; }

/* ═══════════════════════════════════════
   CUSTOM COMPONENTS
═══════════════════════════════════════ */

/* ── Summary bar ── */
.sum-bar {
  background: linear-gradient(135deg, rgba(255,255,255,.04), rgba(255,255,255,.015));
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 18px;
  backdrop-filter: blur(18px);
  box-shadow: 0 12px 40px -16px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.05);
  display: grid;
  grid-template-columns: auto 1px auto 1px auto 1px auto;
  align-items: stretch;
  overflow: hidden;
  margin-bottom: 22px;
  position: relative;
}
.sum-bar::before {
  content:''; position:absolute; inset:0;
  background: radial-gradient(600px 200px at 0% 0%, rgba(124,92,255,.10), transparent 60%);
  pointer-events:none;
}
.sum-cell {
  padding: 22px 32px; display:flex; flex-direction:column; justify-content:center;
  position:relative; z-index:1;
}
.sum-cell.score-cell { padding: 22px 36px; }
.sum-sep { background: linear-gradient(180deg, transparent, rgba(255,255,255,.10), transparent); width: 1px; }
.sum-key {
  font-size:.6rem; font-weight:700; text-transform:uppercase;
  letter-spacing:.13em; color: var(--ink-2); margin-bottom:8px;
}
.sum-val {
  font-family:'Space Grotesk', sans-serif;
  font-size:1.4rem; font-weight:600; color: var(--ink-0); line-height:1.1;
}
.sum-score-num {
  font-family:'Space Grotesk', sans-serif;
  font-size: 3.2rem; font-weight: 700; line-height: 1; letter-spacing: -2px;
  background-clip: text; -webkit-background-clip: text;
}
.sum-score-lbl {
  font-size:.6rem; font-weight:700; text-transform:uppercase;
  letter-spacing:.13em; margin-top:6px; opacity:.75;
}

/* ── Glass card ── */
.w-card {
  background: linear-gradient(135deg, rgba(255,255,255,.045), rgba(255,255,255,.015));
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 16px;
  backdrop-filter: blur(16px);
  box-shadow: 0 8px 30px -12px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.04);
  padding: 22px 24px;
  margin-bottom: 18px;
  transition: border-color .25s, transform .25s;
}
.w-card:hover { border-color: rgba(124,92,255,.25); }
.card-label {
  font-size:.62rem; font-weight:700; text-transform:uppercase;
  letter-spacing:.14em; color: var(--ink-2); margin-bottom:14px;
  display:flex; align-items:center; gap:8px;
}
.card-label::before {
  content:''; width:6px; height:6px; border-radius:50%;
  background: linear-gradient(135deg, var(--violet), var(--cyan));
  box-shadow: 0 0 10px rgba(124,92,255,.7);
}

/* ── Auth pills ── */
.auth-pill {
  display:flex; align-items:center; gap:10px;
  border-radius:10px; padding:11px 15px; margin:6px 0;
  font-size:.84rem; font-weight:600;
  backdrop-filter: blur(10px);
}
.auth-pill.pass    { background:rgba(16,211,158,.10); border:1px solid rgba(16,211,158,.30); color:#7ff0c5; }
.auth-pill.fail    { background:rgba(255,92,122,.10); border:1px solid rgba(255,92,122,.30); color:#ffb1bf; }
.auth-pill.unknown { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.10); color: var(--ink-1); }
.auth-dot { width:9px; height:9px; border-radius:50%; flex-shrink:0; }
.auth-dot.pass    { background: var(--safe);  box-shadow:0 0 10px rgba(16,211,158,.7); }
.auth-dot.fail    { background: var(--crit);  box-shadow:0 0 10px rgba(255,92,122,.7); }
.auth-dot.unknown { background: var(--ink-3); }

/* ── Finding rows ── */
.frow {
  border-radius:8px; padding:10px 14px; margin:6px 0;
  font-size:.83rem; line-height:1.55;
  border-left:3px solid var(--violet);
  background: rgba(124,92,255,.07); color: var(--ink-1);
}
.frow.crit { border-left-color: var(--crit); background: rgba(255,92,122,.10); color:#ffc1cd; }
.frow.high { border-left-color: var(--high); background: rgba(255,162,76,.10); color:#ffd4a8; }
.frow.med  { border-left-color: var(--med);  background: rgba(255,216,77,.10); color:#ffe999; }
.frow.low  { border-left-color: var(--low);  background: rgba(78,224,160,.10); color:#9ff1c5; }

/* ── Score chip ── */
.score-chip {
  display:inline-flex; align-items:baseline; gap:6px;
  border-radius:12px; padding:11px 18px; margin-bottom:14px;
  backdrop-filter: blur(8px);
}
.score-chip .n { font-family:'Space Grotesk', sans-serif; font-size:1.8rem; font-weight:700; line-height:1; }
.score-chip .d { font-size:.72rem; font-weight:600; opacity:.75; text-transform:uppercase; letter-spacing:.08em; }

/* ── Stat block ── */
.stat-blk {
  background: linear-gradient(135deg, rgba(255,255,255,.045), rgba(255,255,255,.015));
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 16px; padding: 22px; text-align:center;
  backdrop-filter: blur(14px);
  box-shadow: 0 8px 24px -12px rgba(0,0,0,.5);
  transition: transform .25s, border-color .25s;
}
.stat-blk:hover { transform: translateY(-2px); border-color: rgba(34,211,238,.30); }
.stat-blk .n {
  font-family:'Space Grotesk', sans-serif;
  font-size:2.2rem; font-weight:700;
  background: linear-gradient(135deg, var(--ink-0), var(--cyan));
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.stat-blk .l {
  font-size:.62rem; font-weight:700; text-transform:uppercase;
  letter-spacing:.12em; color: var(--ink-2); margin-top:6px;
}

/* ── Rec rows ── */
.rec-row {
  border-radius:10px; padding:13px 16px; margin:7px 0;
  font-size:.84rem; font-weight:500; line-height:1.6;
  display:flex; gap:13px; align-items:flex-start;
  backdrop-filter: blur(8px);
}
.rec-row.crit { background:rgba(255,92,122,.10); border:1px solid rgba(255,92,122,.30); color:#ffc1cd; }
.rec-row.high { background:rgba(255,162,76,.10); border:1px solid rgba(255,162,76,.30); color:#ffd4a8; }
.rec-row.med  { background:rgba(255,216,77,.10); border:1px solid rgba(255,216,77,.30); color:#ffe999; }
.rec-row.info { background:rgba(91,124,255,.10); border:1px solid rgba(91,124,255,.30); color:#b9c5ff; }
.rec-row.def  { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.10); color: var(--ink-1); }
.rec-num {
  flex-shrink:0; width:24px; height:24px; border-radius:7px;
  background: linear-gradient(135deg, rgba(124,92,255,.30), rgba(34,211,238,.20));
  font-family:'Space Grotesk', sans-serif;
  font-size:.74rem; font-weight:700; color: var(--ink-0);
  display:flex; align-items:center; justify-content:center; margin-top:1px;
  border: 1px solid rgba(255,255,255,.08);
}

/* ── URL risk badge ── */
.url-badge {
  border-radius:14px; padding:20px; text-align:center;
  backdrop-filter: blur(10px);
}
.url-badge .n { font-family:'Space Grotesk', sans-serif; font-size:2.2rem; font-weight:700; }
.url-badge .l { font-size:.64rem; font-weight:700; text-transform:uppercase; letter-spacing:.11em; margin-top:6px; opacity:.85; }

/* ── Sidebar nav label ── */
.sb-section {
  font-size:.6rem; font-weight:700; text-transform:uppercase;
  letter-spacing:.14em; color: var(--ink-3); margin:18px 0 9px;
}

/* ── Hero ── */
.hero-wrap {
  background:
    radial-gradient(700px 320px at 90% 0%, rgba(124,92,255,.30), transparent 60%),
    radial-gradient(500px 300px at 0% 100%, rgba(34,211,238,.22), transparent 60%),
    linear-gradient(135deg, rgba(20,26,69,.85), rgba(12,16,48,.92));
  border: 1px solid rgba(255,255,255,.10);
  border-radius: 22px;
  padding: 58px 52px;
  position: relative; overflow: hidden;
  margin-bottom: 26px;
  backdrop-filter: blur(18px);
  box-shadow: 0 24px 60px -24px rgba(0,0,0,.7), inset 0 1px 0 rgba(255,255,255,.06);
}
.hero-wrap::after {
  content:''; position:absolute; right:-80px; top:-80px;
  width:360px; height:360px;
  background: radial-gradient(circle, rgba(236,72,153,.18) 0%, transparent 65%);
  pointer-events:none;
}
.hero-wrap * { position:relative; z-index:1; }
.hero-badge {
  display:inline-flex; align-items:center; gap:8px;
  background: rgba(124,92,255,.18);
  border: 1px solid rgba(124,92,255,.40);
  border-radius:999px; padding:6px 14px;
  font-size:.74rem; font-weight:600;
  color:#c4b5fd; margin-bottom:18px;
  backdrop-filter: blur(10px);
}
.hero-badge::before {
  content:''; width:6px; height:6px; border-radius:50%;
  background: var(--cyan); box-shadow:0 0 12px var(--cyan);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }
.hero-title {
  font-family:'Space Grotesk', sans-serif !important;
  font-size:3rem !important; font-weight:700 !important;
  letter-spacing:-1.2px !important; line-height:1.05 !important;
  margin-bottom:14px !important;
  background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 50%, #7dd3fc 100%);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; color: transparent !important;
}
.hero-sub {
  color: var(--ink-1) !important; font-size:1rem !important;
  max-width:560px; line-height:1.7; margin-bottom:26px;
}
.hero-tag {
  display:inline-block;
  background: rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.10);
  border-radius:8px; padding:5px 12px;
  font-size:.74rem; color: var(--ink-1); margin:3px;
  font-weight:500; transition: all .2s;
}
.hero-tag:hover { border-color: rgba(124,92,255,.40); color: var(--ink-0); }

/* ── Feature card ── */
.feat {
  background: linear-gradient(135deg, rgba(255,255,255,.045), rgba(255,255,255,.015));
  border:1px solid rgba(255,255,255,.08);
  border-radius:16px; padding:24px; height:100%;
  backdrop-filter: blur(14px);
  box-shadow: 0 8px 24px -12px rgba(0,0,0,.5);
  transition: transform .25s, border-color .25s;
}
.feat:hover { transform: translateY(-3px); border-color: rgba(124,92,255,.30); }
.feat-icon {
  font-size:1.6rem; margin-bottom:12px;
  display:inline-flex; width:44px; height:44px; border-radius:12px;
  align-items:center; justify-content:center;
  background: linear-gradient(135deg, rgba(124,92,255,.20), rgba(34,211,238,.12));
  border: 1px solid rgba(255,255,255,.08);
}
.feat-h {
  font-family:'Space Grotesk', sans-serif;
  font-size:1rem; font-weight:600; color: var(--ink-0); margin-bottom:8px;
}
.feat-p { font-size:.83rem; color: var(--ink-2); line-height:1.6; }

/* ── Sidebar logo ── */
.sb-logo {
  display:flex; align-items:center; gap:12px;
  padding-bottom:18px; border-bottom:1px solid rgba(255,255,255,.06);
  margin-bottom:18px;
}
.sb-logo-icon {
  width:40px; height:40px; border-radius:11px;
  background: linear-gradient(135deg, var(--violet), var(--cyan));
  display:flex; align-items:center; justify-content:center;
  font-size:1.15rem; flex-shrink:0;
  box-shadow: 0 4px 16px rgba(124,92,255,.5), inset 0 1px 0 rgba(255,255,255,.20);
}
.sb-logo-name {
  font-family:'Space Grotesk', sans-serif !important;
  font-size:1.1rem !important; font-weight:700 !important;
  color: var(--ink-0) !important; letter-spacing:-.3px;
}
.sb-logo-sub { font-size:.7rem !important; color: var(--ink-3) !important; margin-top:2px; }
</style>
""", unsafe_allow_html=True)

# ── Session ────────────────────────────────────────────────────────────────────
if 'report'   not in st.session_state: st.session_state.report   = None
if 'analyzer' not in st.session_state: st.session_state.analyzer = NeuroEMLAnalyzer()


# ── Colour helpers (Aurora palette) ────────────────────────────────────────────
_TIERS = {
    'critical': ('#ff5c7a', 'rgba(255,92,122,.10)',  'rgba(255,92,122,.35)',  'crit'),
    'high':     ('#ffa24c', 'rgba(255,162,76,.10)',  'rgba(255,162,76,.35)',  'high'),
    'medium':   ('#ffd84d', 'rgba(255,216,77,.10)',  'rgba(255,216,77,.35)',  'med'),
    'low':      ('#4ee0a0', 'rgba(78,224,160,.10)',  'rgba(78,224,160,.35)',  'low'),
    'safe':     ('#10d39e', 'rgba(16,211,158,.10)',  'rgba(16,211,158,.35)',  'low'),
}

def _tier(score):
    if score >= 80: return 'critical'
    if score >= 60: return 'high'
    if score >= 40: return 'medium'
    if score >= 20: return 'low'
    return 'safe'

def rc(score): return _TIERS[_tier(score)][0]
def rb(score): return _TIERS[_tier(score)][1]
def rd(score): return _TIERS[_tier(score)][2]
def rf(score): return _TIERS[_tier(score)][3]

def rlabel(score):
    return {'critical':'CRITICAL','high':'HIGH','medium':'MEDIUM','low':'LOW','safe':'SAFE'}[_tier(score)]

def ricon(score):
    return {'critical':'🚨','high':'⚠️','medium':'⚡','low':'✓','safe':'✅'}[_tier(score)]


# ── Chart builders ─────────────────────────────────────────────────────────────

def gauge(score):
    color = rc(score)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text':'Risk Score','font':{'size':13,'color':'#8b91c3','family':'Inter'}},
        number={'font':{'size':54,'color':color,'family':'Space Grotesk'}},
        domain={'x':[0,1],'y':[0,1]},
        gauge={
            'axis':{'range':[0,100],'tickfont':{'color':'#8b91c3','size':9},'tickcolor':'rgba(255,255,255,.10)'},
            'bar':{'color':color,'thickness':.24},
            'bgcolor':'rgba(255,255,255,.03)',
            'bordercolor':'rgba(255,255,255,.08)','borderwidth':1,
            'steps':[
                {'range':[0,20], 'color':'rgba(16,211,158,.18)'},
                {'range':[20,40],'color':'rgba(78,224,160,.18)'},
                {'range':[40,60],'color':'rgba(255,216,77,.18)'},
                {'range':[60,80],'color':'rgba(255,162,76,.18)'},
                {'range':[80,100],'color':'rgba(255,92,122,.20)'},
            ],
            'threshold':{'line':{'color':color,'width':3},'thickness':.85,'value':score},
        }
    ))
    fig.update_layout(
        height=300, margin=dict(l=28,r=28,t=56,b=8),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font={'family':'Inter','color':'#c7cbe8'},
    )
    return fig


def bar_chart(report):
    scores = {
        'Identity':   report.get('engines',{}).get('identity_engine',{}).get('risk_score',0),
        'Header Auth':report.get('engines',{}).get('header_engine',{}).get('auth_risk_score',0),
        'URLs':       report.get('engines',{}).get('url_engine',{}).get('overall_risk_score',0),
        'AI Profiler':report.get('ai_analysis',{}).get('profiler',{}).get('overall_suspicion_score',0),
        'AI Auditor': report.get('ai_analysis',{}).get('auditor',{}).get('technical_risk_score',0),
        'OSINT':      report.get('osint_enrichment',{}).get('osint_risk_score',0),
    }
    vals   = list(scores.values())
    labels = list(scores.keys())
    colors = [rc(v) for v in vals]

    fig = go.Figure(go.Bar(
        y=labels, x=vals, orientation='h',
        marker=dict(color=colors, line=dict(color='rgba(255,255,255,.08)',width=1)),
        text=[str(v) for v in vals], textposition='outside',
        textfont=dict(color='#c7cbe8',size=11,family='Space Grotesk'),
    ))
    fig.update_layout(
        title=dict(text='Engine Scores', font=dict(size=13,color='#8b91c3',family='Inter')),
        height=300, margin=dict(l=10,r=50,t=52,b=10),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[0,118],showgrid=True,gridcolor='rgba(255,255,255,.06)',
                   tickfont=dict(color='#8b91c3',size=9), zeroline=False),
        yaxis=dict(tickfont=dict(color='#c7cbe8',size=11,family='Inter')),
    )
    return fig


# ── Section renderers ──────────────────────────────────────────────────────────

def render_email_analysis(report):
    identity = report.get('engines',{}).get('identity_engine',{})
    auth     = report.get('engines',{}).get('header_engine',{}).get('authentication',{})

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="w-card"><div class="card-label">📬 Email Identity</div>', unsafe_allow_html=True)
        if identity:
            st.markdown(f"**From** `{identity.get('email_address','N/A')}`")
            st.markdown(f"**Name** {identity.get('display_name','N/A')}")
            st.markdown(f"**Domain** `{identity.get('domain','N/A')}`")
            if identity.get('homograph_check',{}).get('is_spoofing_attempt'):
                st.error("🚨 Spoofing Attempt")
                for ind in identity['homograph_check'].get('indicators',[]):
                    st.markdown(f'<div class="frow crit">• {ind}</div>', unsafe_allow_html=True)
            if identity.get('punycode_check',{}).get('is_suspicious'):
                st.error("🚨 Punycode / Homograph Attack")
                pc = identity['punycode_check']
                st.markdown(f'<div class="frow crit">Original: {pc.get("original","?")} → Decoded: {pc.get("decoded","?")}</div>',
                            unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="w-card"><div class="card-label">🔐 Authentication</div>', unsafe_allow_html=True)
        for proto, data in [('SPF', auth.get('spf',{})), ('DKIM', auth.get('dkim',{})), ('DMARC', auth.get('dmarc',{}))]:
            status = data.get('status','unknown')
            domain = data.get('domain','')
            detail = f" · {domain}" if domain else ""
            if status == 'pass':
                cls, dot = 'pass', 'pass'
            elif status in ('fail','none','softfail'):
                cls, dot = 'fail', 'fail'
            else:
                cls, dot = 'unknown', 'unknown'
            st.markdown(
                f'<div class="auth-pill {cls}">'
                f'<span class="auth-dot {dot}"></span>'
                f'<strong>{proto}</strong>&nbsp;{status.upper()}{detail}'
                f'</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Attachments
    attachments = report.get('parsing', {})
    if attachments and attachments.get('attachments_count', 0) > 0:
        st.info(f"📎 {attachments['attachments_count']} attachment(s) found")
    else:
        st.success("No attachments detected.")


def render_url_analysis(report):
    urls = report.get('engines',{}).get('url_engine',{}).get('urls',[])
    if not urls:
        st.info("No URLs found in this email.")
        return
    for url_data in urls:
        score = url_data.get('risk_score', 0)
        color = rc(score)
        bg    = rb(score)
        label = rlabel(score)
        short = url_data['url'][:68] + ('…' if len(url_data['url'])>68 else '')
        with st.expander(f"🔗  {short}"):
            col1, col2 = st.columns([3, 1], gap="large")
            with col1:
                st.code(url_data['url'], language=None)
                expanded = url_data.get('expanded',{})
                st.markdown(f"**Destination** `{expanded.get('final','Unknown')}`")
                st.markdown(f"**Redirects** {expanded.get('redirects',0)}")
                if expanded.get('redirect_chain'):
                    for step in expanded['redirect_chain']:
                        st.markdown(f'<div class="frow">→ {step}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(
                    f'<div class="url-badge" style="background:{bg};border:1.5px solid {rd(score)}">'
                    f'<div class="n" style="color:{color}">{score}</div>'
                    f'<div class="l" style="color:{color}">{label}</div>'
                    f'</div>', unsafe_allow_html=True)
                suspicious = url_data.get('suspicious_check',{})
                for ind in suspicious.get('suspicious_indicators',[]):
                    st.markdown(f'<div class="frow crit" style="font-size:.76rem;margin-top:8px">⚑ {ind}</div>',
                                unsafe_allow_html=True)


def render_ai_analysis(report):
    col1, col2 = st.columns(2, gap="large")

    with col1:
        profiler = report.get('ai_analysis',{}).get('profiler',{})
        st.markdown('<div class="w-card"><div class="card-label">🧠 AI Profiler — Psychological</div>', unsafe_allow_html=True)
        if profiler.get('error'):
            st.error(profiler['error'])
        else:
            score = profiler.get('overall_suspicion_score',0)
            st.markdown(
                f'<div class="score-chip" style="background:{rb(score)};border:1.5px solid {rd(score)}">'
                f'<span class="n" style="color:{rc(score)}">{score}</span>'
                f'<span class="d" style="color:{rc(score)}">/100 suspicion</span>'
                f'</div>', unsafe_allow_html=True)
            if profiler.get('summary'):
                st.markdown(f'<p style="margin-bottom:12px">{profiler["summary"]}</p>', unsafe_allow_html=True)
            tactics = profiler.get('tactics',{})
            if tactics:
                st.markdown('<div class="card-label" style="margin-top:10px">Detected Tactics</div>', unsafe_allow_html=True)
                for tactic, data in tactics.items():
                    if isinstance(data,dict) and data.get('score',0)>0:
                        with st.expander(f"{tactic.replace('_',' ').title()} · {data.get('score',0)}/100"):
                            for ind in data.get('indicators',[])[:3]:
                                st.markdown(f'<div class="frow high">• {ind}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        auditor = report.get('ai_analysis',{}).get('auditor',{})
        st.markdown('<div class="w-card"><div class="card-label">🔒 AI Auditor — Technical</div>', unsafe_allow_html=True)
        if auditor.get('error'):
            st.error(auditor['error'])
        else:
            score = auditor.get('technical_risk_score',0)
            st.markdown(
                f'<div class="score-chip" style="background:{rb(score)};border:1.5px solid {rd(score)}">'
                f'<span class="n" style="color:{rc(score)}">{score}</span>'
                f'<span class="d" style="color:{rc(score)}">/100 tech risk</span>'
                f'</div>', unsafe_allow_html=True)
            if auditor.get('recommendations'):
                st.markdown("**Recommendations**")
                st.markdown(f'<p style="margin-bottom:12px">{auditor["recommendations"]}</p>', unsafe_allow_html=True)
            for finding in auditor.get('critical_findings',[]):
                st.markdown(f'<div class="frow crit">⚑ {finding}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def render_osint(report):
    osint = report.get('osint_enrichment',{})
    col1, col2, col3 = st.columns(3)
    for col, lbl, val in zip([col1,col2,col3],[
        "Total IOCs","Flagged IOCs","OSINT Risk"],[
        osint.get('total_iocs',0), osint.get('flagged_iocs',0), osint.get('osint_risk_score',0)]):
        with col:
            st.markdown(f'<div class="stat-blk"><div class="n">{val}</div><div class="l">{lbl}</div></div>',
                        unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    high_risk = osint.get('high_risk_indicators',[])
    if high_risk:
        st.error("High Risk Indicators Found")
        for ind in high_risk:
            ioc_type = ind.get('type','?').upper()
            value    = ind.get('value','?')
            detail   = (f"Detected by {ind.get('detections',0)} engines" if ioc_type=='URL'
                        else f"Abuse Score: {ind.get('abuse_score',0)}" if ioc_type=='IP'
                        else value)
            st.markdown(
                f'<div class="frow crit"><strong>{ioc_type}</strong> — {detail}'
                f'<br><span style="font-size:.76rem;opacity:.7">{value}</span></div>',
                unsafe_allow_html=True)
    else:
        st.success("No high-risk IOCs detected.")


def render_recommendations(report):
    recs = report.get('recommendations',[])
    if not recs:
        st.info("No recommendations at this time.")
        return
    for idx, rec in enumerate(recs, 1):
        if   '🚨' in rec:              cls = 'crit'
        elif '⚠️' in rec or '🔴' in rec: cls = 'high'
        elif '⚡' in rec:              cls = 'med'
        elif 'ℹ' in rec or '🔵' in rec: cls = 'info'
        else:                           cls = 'def'
        st.markdown(
            f'<div class="rec-row {cls}">'
            f'<span class="rec-num">{idx}</span>'
            f'<span>{rec}</span>'
            f'</div>', unsafe_allow_html=True)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():

    # ── Session State Tracker for File Memory ──────────────────────────────
    if 'analyzed_file_key' not in st.session_state: 
        st.session_state.analyzed_file_key = None

    # ── Sidebar ────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div class="sb-logo">
          <div class="sb-logo-icon">🛡️</div>
          <div>
            <div class="sb-logo-name">NeuroEML</div>
            <div class="sb-logo-sub">Security Analysis</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sb-section">Upload</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "eml", type=['eml'], label_visibility="collapsed",
            help="Upload an .eml file for analysis")

        if uploaded_file is not None:
            # Create a unique fingerprint for this specific file
            current_file_key = f"{uploaded_file.name}_{uploaded_file.size}"
            
            # THE FIX: Only run analysis if this is a brand new file
            if st.session_state.analyzed_file_key != current_file_key:
                with st.spinner("Analyzing…"):
                    temp_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
                    with open(temp_path,'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    try:
                        # Run the heavy analysis
                        st.session_state.report = st.session_state.analyzer.analyze_email(temp_path)
                        # Lock it into memory so it doesn't run again!
                        st.session_state.analyzed_file_key = current_file_key
                        st.success("Analysis complete")
                    except Exception as e:
                        st.error(str(e))

        if st.session_state.report:
            st.markdown('<div class="sb-section">Export</div>', unsafe_allow_html=True)
            json_str = json.dumps(st.session_state.report, indent=2)
            st.download_button("📄  JSON Report", data=json_str,
                file_name=f"neuroeml_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json")
            osint = st.session_state.report.get('osint_enrichment',{})
            if osint.get('high_risk_indicators'):
                df = pd.DataFrame(osint['high_risk_indicators'])
                st.download_button("📊  IOCs CSV", data=df.to_csv(index=False),
                    file_name=f"iocs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv")

    # ── Main area ──────────────────────────────────────────────────────────
    if st.session_state.report is None:

        st.markdown("""
        <div class="hero-wrap">
          <div class="hero-badge">Email Threat Intelligence</div>
          <div class="hero-title">NeuroEML</div>
          <p class="hero-sub">
            Upload a <strong style="color:#e2e8f0">.eml</strong> file to run a full six-layer
            threat analysis — identity spoofing, header auth, URL inspection, AI profiling,
            and OSINT enrichment in one report.
          </p>
          <div>
            <span class="hero-tag">Identity Engine</span>
            <span class="hero-tag">SPF · DKIM · DMARC</span>
            <span class="hero-tag">URL Analysis</span>
            <span class="hero-tag">AI Profiler</span>
            <span class="hero-tag">AI Auditor</span>
            <span class="hero-tag">OSINT / VirusTotal</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        for col, icon, title, desc in zip([c1,c2,c3],
            ['🔍','🤖','🌐'],
            ['Six-Layer Analysis','AI-Driven Profiling','Live OSINT'],
            ['Every dimension of an email is inspected independently — identity, headers, links, content, and metadata.',
             'Psychological manipulation tactics and technical obfuscation detected using large language models.',
             'Domains, IPs, and URLs are enriched in real time against VirusTotal and AbuseIPDB.']):
            with col:
                st.markdown(f'<div class="feat"><div class="feat-icon">{icon}</div>'
                            f'<div class="feat-h">{title}</div>'
                            f'<div class="feat-p">{desc}</div></div>', unsafe_allow_html=True)

    else:
        report     = st.session_state.report
        risk_score = report.get('final_risk_score', 0)
        level      = rlabel(risk_score)
        icon       = ricon(risk_score)
        color      = rc(risk_score)
        timestamp  = report.get('metadata',{}).get('analysis_timestamp','')
        date_str   = timestamp.split('T')[0] if timestamp else '—'
        status     = report.get('metadata',{}).get('status','Unknown').upper()

        # ── Summary bar ────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="sum-bar">
          <div class="sum-cell score-cell">
            <div class="sum-score-num" style="color:{color}">{risk_score}</div>
            <div class="sum-score-lbl" style="color:{color}">Risk Score</div>
          </div>
          <div class="sum-sep"></div>
          <div class="sum-cell">
            <div class="sum-key">Risk Level</div>
            <div class="sum-val" style="color:{color}">{icon}&nbsp;{level}</div>
          </div>
          <div class="sum-sep"></div>
          <div class="sum-cell">
            <div class="sum-key">Status</div>
            <div class="sum-val">{status}</div>
          </div>
          <div class="sum-sep"></div>
          <div class="sum-cell">
            <div class="sum-key">Analyzed</div>
            <div class="sum-val" style="font-size:1.05rem;font-weight:500;color:#c7cbe8">{date_str}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Tab navigation ──────────────────────────────────────────────────
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Overview",
            "📧 Email",
            "🔗 URLs",
            "🧠 AI Analysis",
            "🌐 OSINT",
            "📋 Recommendations",
        ])

        with tab1:
            col1, col2 = st.columns(2, gap="large")
            with col1:
                st.plotly_chart(gauge(risk_score), use_container_width=True)
            with col2:
                st.plotly_chart(bar_chart(report), use_container_width=True)

        with tab2:
            render_email_analysis(report)

        with tab3:
            render_url_analysis(report)

        with tab4:
            render_ai_analysis(report)

        with tab5:
            render_osint(report)

        with tab6:
            st.markdown('<div class="w-card"><div class="card-label">📋 Security Recommendations</div>',
                        unsafe_allow_html=True)
            render_recommendations(report)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <p style="text-align:center;color:#5b6196;font-size:.72rem;padding:30px 0 4px;letter-spacing:.05em">
          NeuroEML v1.0 &nbsp;·&nbsp; Email Security Analysis Platform &nbsp;·&nbsp;
          Authorized security testing only
        </p>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()