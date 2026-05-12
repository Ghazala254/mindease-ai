import streamlit as st
import datetime

def detect_stress_category(text: str) -> str:
    text_lower = text.lower()
    keywords = {
        "job_stress":          ["job", "work", "boss", "office", "career", "salary", "colleague", "deadline", "manager", "fired", "resign"],
        "family_stress":       ["family", "parent", "mother", "father", "wife", "husband", "children", "sibling", "home", "marriage"],
        "financial_stress":    ["money", "debt", "loan", "bill", "rent", "broke", "financial", "afford"],
        "health_stress":       ["sick", "illness", "hospital", "doctor", "pain", "disease", "health", "sleep", "tired"],
        "relationship_stress": ["relationship", "friend", "love", "breakup", "lonely", "betrayal", "trust", "partner"],
        "academic_stress":     ["study", "exam", "school", "college", "university", "grade", "teacher"],
        "anxiety_depression":  ["anxiety", "depress", "hopeless", "numb", "panic", "worthless"],
    }
    scores = {cat: 0 for cat in keywords}
    for cat, words in keywords.items():
        for word in words:
            if word in text_lower:
                scores[cat] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general_stress"

def init_session():
    defaults = {
        "messages":        [],
        "q_count":         0,
        "report_data":     None,
        "last_audio":      None,
        "emotion_log":     [],
        "stress_category": None,
        "phase":           "start",
        "session_start":   datetime.datetime.now().isoformat(),
        "user_name":       "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v