import streamlit as st
import datetime
import json
from fpdf import FPDF

def generate_report_data(client):
    prompt = """Analyze this mental wellness conversation carefully. Return ONLY valid JSON with no extra text before or after:
{"stress_level": 0, "anxiety_level": 0, "wellbeing": 0, "primary_category": "", "summary": "", "recommendations": ["", "", "", "", ""], "strengths": ["", ""], "daily_plan": {"morning": "", "afternoon": "", "evening": ""}}
Rules: stress_level, anxiety_level, wellbeing are integers 0-100. summary is 3 sentences. recommendations has 5 specific actionable tips. strengths has 2 genuine strengths found in conversation."""

    msgs = [{"role": "system", "content": prompt}]
    for m in st.session_state["messages"][-20:]:
        msgs.append({"role": m["role"], "content": m["content"]})

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=msgs,
        temperature=0.05,
        max_tokens=700,
    )
    raw = res.choices[0].message.content
    try:
        start = raw.index('{')
        end   = raw.rindex('}') + 1
        return json.loads(raw[start:end])
    except Exception:
        return None

def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_fill_color(15, 22, 41)
    pdf.rect(0, 0, 210, 38, 'F')
    pdf.set_font("Helvetica", 'B', 22)
    pdf.set_text_color(139, 124, 248)
    pdf.set_xy(10, 7)
    pdf.cell(190, 12, "MindEase AI", align='C')
    pdf.set_font("Helvetica", '', 11)
    pdf.set_text_color(160, 170, 210)
    pdf.set_xy(10, 21)
    pdf.cell(190, 9, "Stress & Wellness Assessment Report", align='C')
    pdf.ln(28)
    pdf.set_font("Helvetica", '', 9)
    pdf.set_text_color(110, 120, 150)
    cat_display = data.get('primary_category', '').replace('_', ' ').title()
    pdf.cell(0, 6, f"Generated: {datetime.datetime.now().strftime('%d %B %Y  %I:%M %p')}   |   Primary Stress Area: {cat_display}", ln=True)
    pdf.ln(6)

    def score_box(label, score, r, g, b):
        pdf.set_fill_color(r, g, b)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(58, 20, f"{label}\n{score}%", border=0, ln=0, align='C', fill=True)
        pdf.cell(5, 20, '', ln=0)

    score_box("Stress Level",  data.get('stress_level', 0),  124, 106, 247)
    score_box("Anxiety Level", data.get('anxiety_level', 0),  45, 212, 191)
    score_box("Wellbeing",     data.get('wellbeing', 0),       74, 222, 128)
    pdf.ln(26)

    def section_header(text, r, g, b):
        pdf.ln(4)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.set_text_color(r, g, b)
        pdf.cell(0, 9, text, ln=True)
        pdf.set_font("Helvetica", '', 10)
        pdf.set_text_color(55, 55, 75)

    section_header("Clinical Summary", 139, 124, 248)
    pdf.multi_cell(0, 7, data.get('summary', ''))
    section_header("Personalized Recommendations", 45, 212, 191)
    for r in data.get('recommendations', []):
        pdf.set_x(15)
        pdf.cell(5, 7, chr(149))
        pdf.multi_cell(0, 7, f" {r}")
    section_header("Your Identified Strengths", 74, 222, 128)
    for s in data.get('strengths', []):
        pdf.set_x(15)
        pdf.cell(5, 7, chr(149))
        pdf.multi_cell(0, 7, f" {s}")
    daily = data.get('daily_plan', {})
    if daily:
        section_header("Your Daily Wellness Plan", 251, 191, 36)
        for period, activity in daily.items():
            pdf.set_font("Helvetica", 'B', 10)
            pdf.set_text_color(80, 90, 110)
            pdf.cell(28, 7, f"{period.capitalize()}:", ln=0)
            pdf.set_font("Helvetica", '', 10)
            pdf.set_text_color(55, 55, 75)
            pdf.multi_cell(0, 7, activity)
    pdf.set_y(-16)
    pdf.set_font("Helvetica", 'I', 8)
    pdf.set_text_color(130, 140, 160)
    pdf.cell(0, 8, "This report is for informational purposes only and does not replace professional mental health care.", align='C')
    return bytes(pdf.output())