import streamlit as st

def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap');
:root {
    --bg:        #0a0d12;
    --surface:   #0f1318;
    --card:      #161b23;
    --card2:     #1c2330;
    --card-hover:#1e2535;
    --accent:    #4f9d8f;
    --accent-lt: #62b8a8;
    --accent-dim: rgba(79,157,143,0.12);
    --gold:      #c9a96e;
    --gold-dim:  rgba(201,169,110,0.10);
    --text:      #e8edf5;
    --text-soft: #b0bdd0;
    --muted:     #6b7a92;
    --border:    rgba(255,255,255,0.07);
    --border-accent: rgba(79,157,143,0.22);
    --green:  #52c87a;
    --red:    #e06c6c;
    --amber:  #d4a847;
}
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: var(--bg);
    color: var(--text);
}
.stApp { background: var(--bg); }
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
.stButton > button {
    background: transparent !important;
    color: var(--accent-lt) !important;
    border: 1px solid var(--border-accent) !important;
    border-radius: 8px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
    letter-spacing: 0.03em !important;
    padding: 9px 18px !important;
    width: 100%;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: var(--accent-dim) !important;
    border-color: var(--accent-lt) !important;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--border-accent) !important;
    box-shadow: 0 0 0 2px var(--accent-dim) !important;
}
[data-testid="stChatMessage"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    margin-bottom: 8px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.25) !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    border-left: 2px solid var(--accent) !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: var(--card2) !important;
    border-left: 2px solid var(--gold) !important;
}
[data-testid="stChatMessage"] p {
    color: var(--text-soft) !important;
    font-size: 0.93rem !important;
    line-height: 1.75 !important;
    margin: 0 !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: var(--accent-dim) !important;
    border: 1px solid var(--border-accent) !important;
    border-radius: 50% !important;
}
[data-testid="stChatMessageAvatarUser"] {
    background: var(--gold-dim) !important;
    border: 1px solid rgba(201,169,110,0.25) !important;
    border-radius: 50% !important;
}
[data-testid="stChatInput"] textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 12px 16px !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--border-accent) !important;
    box-shadow: 0 0 0 2px var(--accent-dim) !important;
}
[data-testid="stChatInput"] {
    background: var(--surface) !important;
    padding: 10px 0 !important;
}
[data-testid="stChatInput"] button {
    background: var(--accent) !important;
    border-radius: 8px !important;
    border: none !important;
    color: #fff !important;
}
[data-testid="stChatInput"] button:hover { background: var(--accent-lt) !important; }
.stProgress > div > div {
    background: linear-gradient(90deg, var(--accent), var(--gold)) !important;
    border-radius: 4px !important;
}
.stProgress > div {
    background: var(--card2) !important;
    border-radius: 4px !important;
}
.breathe-wrap { text-align: center; padding: 10px 0; }
.circle {
    width: 64px; height: 64px;
    border-radius: 50%;
    background: radial-gradient(circle, var(--accent-lt), #1a4a44);
    margin: 12px auto;
    animation: breathe 8s infinite ease-in-out;
    box-shadow: 0 0 24px rgba(79,157,143,0.3);
}
@keyframes breathe {
    0%   { transform: scale(0.55); opacity: 0.35; }
    40%  { transform: scale(1.18); opacity: 1; }
    50%  { transform: scale(1.18); opacity: 1; }
    100% { transform: scale(0.55); opacity: 0.35; }
}
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--card2); border-radius: 2px; }
.hero { padding: 4px 0 20px; }
.hero h1 {
    font-family: 'Instrument Serif', serif;
    font-size: 2.3rem;
    color: var(--text);
    margin: 0;
    font-weight: 400;
    letter-spacing: -0.01em;
}
.hero h1 span { color: var(--accent-lt); }
.hero p { color: var(--muted); font-size: 0.88rem; margin: 6px 0 0; }
.info-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 12px;
}
.card-title {
    color: var(--accent-lt);
    font-weight: 600;
    font-size: 0.76rem;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.metric-box {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 16px;
    text-align: center;
}
.metric-val {
    font-size: 2.1rem;
    font-weight: 700;
    font-family: 'Instrument Serif', serif;
}
.metric-lbl {
    color: var(--muted);
    font-size: 0.75rem;
    margin-top: 5px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
hr { border-color: var(--border) !important; }
.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)