import streamlit as st
from groq import Groq
import base64
import tempfile
import os
import datetime

# --- Local imports ---
from backend.utils       import init_session, detect_stress_category
from backend.groq_client import chat
from backend.report      import generate_report_data, create_pdf
from data.techniques     import get_cbt_tip
from frontend.styles     import inject_css

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MindEase AI -- Stress Relief Companion",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()
init_session()

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:18px 0 8px;'>
        <div style='font-size:2.4rem;'>🧘</div>
        <div style='font-family:"Instrument Serif",serif; font-size:1.4rem; color:#4f9d8f; font-weight:400; margin:8px 0 3px; letter-spacing:0.01em;'>MindEase AI</div>
        <div style='color:#6b7a92; font-size:0.76rem; letter-spacing:0.07em; text-transform:uppercase;'>Stress Relief Companion</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    api_key = st.text_input("🔑 Groq API Key", type="password", placeholder="gsk_...")
    lang    = st.selectbox("🌐 Language", ["English", "Roman Urdu"])

    st.divider()

    if st.session_state["stress_category"]:
        cat_display = st.session_state["stress_category"].replace("_", " ").title()
        st.markdown(f'<div style="color:#4f9d8f;font-size:0.8rem;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;margin-bottom:6px;">📍 Focus: {cat_display}</div>', unsafe_allow_html=True)

    q    = st.session_state["q_count"]
    prog = min(q / 12, 1.0)
    st.markdown(f'<div style="color:#6b7a92;font-size:0.78rem;margin-bottom:6px;">Session Progress -- {q} of 12 exchanges</div>', unsafe_allow_html=True)
    st.progress(prog)

    st.divider()

    if st.button("📄 Generate PDF Report"):
        if not api_key or not st.session_state["messages"]:
            st.error("Please add your API key and have an active conversation first.")
        else:
            with st.spinner("Analyzing your session and generating report..."):
                try:
                    client_temp = Groq(api_key=api_key)
                    data = generate_report_data(client_temp)
                    if data:
                        st.session_state["report_data"] = data
                        st.success("Report ready! Scroll down to view.")
                    else:
                        st.error("Report generation failed. Please continue the conversation a bit longer.")
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.button("🔄 Reset Session"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    st.divider()

    cat = st.session_state.get("stress_category", "general_stress")
    tip = get_cbt_tip(cat)
    st.markdown(f"""
    <div class='info-card'>
        <div class='card-title'>💡 Technique For You</div>
        <div style='color:#b0bdd0; font-size:0.82rem; line-height:1.75;'>{tip}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-card'>
        <div class='card-title'>⚠️ Remember</div>
        <div style='color:#8896b3; font-size:0.78rem; line-height:1.7;'>
        MindEase is a supportive companion, not a medical tool. If you are in crisis, please contact a mental health professional immediately.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# STOP IF NO KEY
# -----------------------------------------------------------------------------
if not api_key:
    st.markdown("""
    <div class='hero'>
        <h1>🧘 MindEase AI</h1>
        <p>Your personal stress relief and mental wellness companion. Tell me what is weighing on you.</p>
    </div>
    """, unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="info-card"><div class="card-title">🤖 AI-Powered</div><div style="color:#8896b3;font-size:0.85rem;">Deep psychological conversations powered by LLaMA-3 via Groq -- completely free.</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="info-card"><div class="card-title">📷 Emotion AI</div><div style="color:#8896b3;font-size:0.85rem;">Analyzes your facial expression via camera to better understand your emotional state.</div></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="info-card"><div class="card-title">📄 PDF Reports</div><div style="color:#8896b3;font-size:0.85rem;">Generates a complete personalized wellness report with actionable recommendations.</div></div>', unsafe_allow_html=True)
    st.info("👈 Enter your free Groq API key in the sidebar to begin. Get one in 60 seconds at **console.groq.com**")
    st.stop()

client = Groq(api_key=api_key)

# -----------------------------------------------------------------------------
# MAIN LAYOUT
# -----------------------------------------------------------------------------
st.markdown("""
<div class='hero'>
    <h1>MindEase <span>AI</span></h1>
    <p>Tell me what is troubling you -- I am here to listen, understand, and help you find relief.</p>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 2.2])

# -----------------------------------------------------------------------------
# LEFT COLUMN
# -----------------------------------------------------------------------------
with col_left:
    st.markdown('<div class="card-title">📷 Emotion Scanner</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#6b7a92;font-size:0.8rem;margin-bottom:8px;">Capture your expression so I can better understand how you feel</div>', unsafe_allow_html=True)

    camera_img = st.camera_input("Take photo", label_visibility="collapsed")

    if camera_img:
        b64 = base64.b64encode(camera_img.getvalue()).decode('utf-8')
        try:
            vision_msgs = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this facial expression. Reply with EXACTLY ONE WORD from this list only: HAPPY SAD ANGRY FEAR NEUTRAL SURPRISE DISGUST. Nothing else."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]
            }]
            with st.spinner("Reading your expression..."):
                vres = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=vision_msgs,
                    temperature=0.05,
                    max_tokens=10
                )
            emo = vres.choices[0].message.content.strip().upper()
            emo = ''.join(c for c in emo if c.isalpha())
            valid_emotions = ["HAPPY", "SAD", "ANGRY", "FEAR", "NEUTRAL", "SURPRISE", "DISGUST"]
            if emo not in valid_emotions:
                emo = "NEUTRAL"
            st.session_state["emotion_log"].append(emo)
            emotion_styles = {
                "HAPPY":    ("#10b981", "😊", "You seem happy. That is wonderful."),
                "SAD":      ("#3b82f6", "😢", "I can see sadness in your expression. I am here."),
                "ANGRY":    ("#ef4444", "😠", "Your expression shows anger. It is valid to feel this way."),
                "FEAR":     ("#f59e0b", "😨", "I notice fear in your expression. You are safe here."),
                "NEUTRAL":  ("#6366f1", "😐", "Your expression appears neutral. Take your time."),
                "SURPRISE": ("#8b5cf6", "😲", "You look surprised. That is interesting."),
                "DISGUST":  ("#64748b", "🤢", "I can see discomfort in your expression."),
            }
            color, emoji, note = emotion_styles.get(emo, ("#6366f1", "😐", ""))
            st.markdown(f"""
            <div style='background:{color}18;border:1px solid {color}55;border-radius:14px;padding:14px;text-align:center;margin-top:8px;'>
                <div style='font-size:2rem;'>{emoji}</div>
                <div style='color:{color};font-weight:800;font-size:1rem;letter-spacing:0.06em;margin-top:6px;'>{emo}</div>
                <div style='color:#8896b3;font-size:0.75rem;margin-top:4px;'>{note}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Emotion scan unavailable: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">🎙️ Voice Input</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#6b7a92;font-size:0.8rem;margin-bottom:6px;">Record your response -- I will transcribe it automatically</div>', unsafe_allow_html=True)
    audio = st.audio_input("Record", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-card'>
        <div class='card-title'>🌬️ Breathe With Me</div>
        <div style='color:#6b7a92;font-size:0.79rem;margin-bottom:4px;'>Inhale 4s &nbsp;·&nbsp; Hold 4s &nbsp;·&nbsp; Exhale 4s</div>
        <div class='breathe-wrap'><div class='circle'></div></div>
        <div style='color:#6b7a92;font-size:0.74rem;text-align:center;'>Follow the circle with your breath</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-card'>
        <div class='card-title'>⚓ Grounding: 5-4-3-2-1</div>
        <div style='color:#b0bdd0;font-size:0.83rem;line-height:2.1;'>
            <span style='color:#4f9d8f;font-weight:700;'>5</span>&nbsp; things you can <b>see</b><br>
            <span style='color:#4f9d8f;font-weight:700;'>4</span>&nbsp; things you can <b>touch</b><br>
            <span style='color:#4f9d8f;font-weight:700;'>3</span>&nbsp; things you can <b>hear</b><br>
            <span style='color:#4f9d8f;font-weight:700;'>2</span>&nbsp; things you can <b>smell</b><br>
            <span style='color:#4f9d8f;font-weight:700;'>1</span>&nbsp; thing you can <b>taste</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# RIGHT COLUMN — CHAT (messages upar, input neeche) ✅
# -----------------------------------------------------------------------------
with col_right:
    st.markdown('<div class="card-title">💬 Therapy Session</div>', unsafe_allow_html=True)

    # Opening message
    if not st.session_state["messages"]:
        if lang == "Roman Urdu":
            opener = "Assalam o Alaikum! Main MindEase hun -- aapka personal stress relief companion. Main yahan aapki baat sunne aur madad karne ke liye hun. Pehle mujhe batayein -- aap ka naam kya hai aur aaj aap kaisa mehsoos kar rahe hain?"
        else:
            opener = "Hello! I am MindEase -- your personal stress relief companion. I am here to listen without judgment and genuinely help you feel better. To start, could you tell me your name and how you are feeling today?"
        st.session_state["messages"].append({"role": "assistant", "content": opener})

    # ✅ Chat messages UPAR — scrollable container
    chat_container = st.container(height=480)
    with chat_container:
        for msg in st.session_state["messages"]:
            role   = msg["role"]
            avatar = "🧘" if role == "assistant" else "🙋"
            with st.chat_message(role, avatar=avatar):
                st.write(msg["content"])

    # Handle voice
    transcribed_from_voice = None
    if audio and audio != st.session_state["last_audio"]:
        st.session_state["last_audio"] = audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio.getvalue())
            tmp_path = tmp.name
        try:
            with open(tmp_path, "rb") as f:
                trans = client.audio.transcriptions.create(
                    file=(tmp_path, f.read()),
                    model="whisper-large-v3"
                )
            transcribed_from_voice = trans.text
        except Exception as e:
            st.error(f"Voice transcription error: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    # ✅ Chat input NEECHE
    placeholder = "Share what is on your mind..." if lang == "English" else "Apni baat yahan likhein..."
    user_input = st.chat_input(placeholder)

    if transcribed_from_voice:
        user_input = transcribed_from_voice

    if user_input and user_input.strip():
        user_text = user_input.strip()

        st.session_state["messages"].append({"role": "user", "content": user_text})
        st.session_state["q_count"] += 1

        if not st.session_state["stress_category"]:
            all_user_text = " ".join(m["content"] for m in st.session_state["messages"] if m["role"] == "user")
            detected = detect_stress_category(all_user_text)
            if detected != "general_stress":
                st.session_state["stress_category"] = detected

        with st.spinner(""):
            try:
                reply = chat(client, lang, user_text)
                st.session_state["messages"].append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")

        st.rerun()

# -----------------------------------------------------------------------------
# REPORT SECTION
# -----------------------------------------------------------------------------
if st.session_state["report_data"]:
    data = st.session_state["report_data"]
    st.divider()
    st.markdown('<div style="font-family:\'Instrument Serif\',serif;font-size:1.7rem;color:#e8edf5;margin-bottom:20px;font-weight:400;">Wellness Report</div>', unsafe_allow_html=True)

    def stress_color(v):
        if v >= 70: return "#f87171"
        if v >= 40: return "#fbbf24"
        return "#4ade80"

    def well_color(v):
        if v >= 70: return "#4ade80"
        if v >= 40: return "#fbbf24"
        return "#f87171"

    sv = data.get('stress_level', 0)
    av = data.get('anxiety_level', 0)
    wv = data.get('wellbeing', 0)

    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:{stress_color(sv)};">{sv}%</div><div class="metric-lbl">Stress Level</div></div>', unsafe_allow_html=True)
    with mc2:
        st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:{stress_color(av)};">{av}%</div><div class="metric-lbl">Anxiety Level</div></div>', unsafe_allow_html=True)
    with mc3:
        st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:{well_color(wv)};">{wv}%</div><div class="metric-lbl">Wellbeing Score</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    rc1, rc2 = st.columns(2)
    with rc1:
        st.markdown("**📋 Clinical Summary**")
        st.info(data.get("summary", ""))
        st.markdown("**💪 Your Strengths**")
        for s in data.get("strengths", []):
            st.markdown(f"✅ {s}")
    with rc2:
        st.markdown("**🎯 Personalized Recommendations**")
        for r in data.get("recommendations", []):
            st.markdown(f"• {r}")
        daily = data.get("daily_plan", {})
        if daily:
            st.markdown("**🌅 Daily Wellness Plan**")
            for period, act in daily.items():
                st.markdown(f"**{period.capitalize()}:** {act}")

    st.markdown("<br>", unsafe_allow_html=True)
    pdf_bytes = create_pdf(data)
    st.download_button(
        label="⬇️ Download Full PDF Report",
        data=pdf_bytes,
        file_name=f"MindEase_Wellness_Report_{datetime.date.today()}.pdf",
        mime="application/pdf",
    )

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.divider()
st.markdown(
    '<div style="text-align:center;color:#3d4a5c;font-size:0.74rem;padding:10px 0;letter-spacing:0.04em;">'
    'MindEase AI &nbsp;·&nbsp; Powered by Groq + LLaMA-3 &nbsp;·&nbsp; Not a substitute for professional mental health care'
    '</div>',
    unsafe_allow_html=True
)