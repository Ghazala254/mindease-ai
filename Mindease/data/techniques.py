import random

CBT_TECHNIQUES = {
    "job_stress": [
        "**Time Blocking:** Schedule specific deep-work hours and hard stop-times. Write them down and honor them.",
        "**Cognitive Restructuring:** When you think 'I will fail', ask: What is the actual evidence? What would I tell a trusted friend?",
        "**The 2-Minute Rule:** Tasks under 2 minutes -- do them immediately. Eliminate the small pile that creates background anxiety.",
        "**Work-Life Boundary:** Set one specific time each evening after which you absolutely will not check any work messages.",
        "**Values Reconnection:** Write three sentences about why your work matters to you. Reconnect with the deeper purpose.",
    ],
    "family_stress": [
        "**'I' Statements:** Instead of 'You always do this', say 'I feel hurt when this happens.' Less defensive, more honest.",
        "**Scheduled Conversations:** Set a specific calm time for difficult family discussions. Never mid-argument.",
        "**Boundary Declaration:** Write one boundary you need this week. Practice the exact words you will use.",
        "**Validation First:** Before defending yourself, say 'I hear you. This sounds really hard.' It disarms conflict.",
        "**Self-Compassion Practice:** You cannot give from an empty vessel. Caring for yourself is not selfishness.",
    ],
    "financial_stress": [
        "**Worry Window:** Give yourself exactly 15 minutes each day to worry about finances. Outside that window, redirect firmly.",
        "**Three Action Steps:** Write three small, realistic financial actions you can take this week. Control what you can.",
        "**Non-Financial Gratitude:** List five things you have right now that money genuinely cannot buy.",
        "**5-Year Perspective:** Ask yourself -- in five years, will this specific moment define who I am?",
        "**Information Seeking:** Financial anxiety grows in darkness. Research one resource, option, or advisor today.",
    ],
    "health_stress": [
        "**Body Scan Relaxation:** Lie down. Starting at your toes, notice tension in each body part. Consciously release it.",
        "**Sleep Ritual:** No screens 30 minutes before bed. Your brain needs a clear signal that the day is finished.",
        "**Micro-Exercise:** Even a 10-minute walk outside lowers cortisol measurably. Start with just 10 minutes.",
        "**Hydration Check:** Stress is amplified by dehydration. Drink one full glass of water right now.",
        "**Medical Permission:** You are allowed to seek help. Asking a doctor is a sign of strength, not weakness.",
    ],
    "relationship_stress": [
        "**Active Listening Practice:** In your next conversation, listen to understand -- not to respond. Notice the difference.",
        "**Needs Clarification:** Write down what you actually need from this relationship. Have you clearly communicated it?",
        "**Acceptance vs. Change:** Identify what you can influence and what you must accept. Stop pouring energy into the unmovable.",
        "**Connection Investment:** Reach out to one person who gives you energy today. Just one message or call.",
        "**Grief Permission:** If a relationship has ended or damaged you, you are allowed to grieve that loss fully.",
    ],
    "academic_stress": [
        "**Pomodoro Technique:** Study for 25 focused minutes, then take a 5-minute break. Repeat four times, then a longer break.",
        "**Completion Over Perfection:** A completed assignment at 80% is worth far more than a perfect one never submitted.",
        "**Study Group:** Connect with two peers. Teaching material to others is the fastest way to understand it yourself.",
        "**Progress Journaling:** Each evening, write one thing you actually learned or accomplished that day. No matter how small.",
        "**Future Self Visualization:** Close your eyes. See yourself having successfully passed. Feel that relief. Use it as fuel.",
    ],
    "general_stress": [
        "**Box Breathing:** Inhale 4 counts, hold 4, exhale 4, hold 4. Repeat four times. Do it right now, in this moment.",
        "**Body Scan:** Starting at your toes, slowly move awareness through your body and release every area of tension.",
        "**Stream of Consciousness Journaling:** Write for 5 minutes without stopping. No editing. Just empty your mind onto the page.",
        "**Behavioral Activation:** Choose one enjoyable activity. Schedule it for today. Do not wait until you feel ready.",
        "**5-4-3-2-1 Grounding:** Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
        "**Progressive Muscle Relaxation:** Tense each muscle group for 5 seconds, then completely release. Begin with your fists.",
        "**Self-Compassion Statement:** Write one kind thing you would say to a dear friend in your situation. Now say it to yourself.",
        "**Nature Exposure:** Even 10 minutes outside in natural light can measurably lower your body's cortisol levels.",
        "**Digital Detox Hour:** One hour each day with no phone, no screen. Observe how your nervous system responds.",
        "**Gratitude Anchor:** Write three specific things from today, however small, that were not entirely terrible.",
    ],
    "anxiety_depression": [
        "**Thought Defusion:** When an anxious thought arrives, say 'I am noticing that I am having the thought that...' Distance yourself from it.",
        "**Opposite Action:** Depression says stay in bed. The evidence says move your body. Do the opposite of what depression tells you.",
        "**Worry Postponement:** When worry arrives, write it down and tell yourself 'I will address this at 5pm.' Return to the present.",
        "**Behavioral Activation:** Depression thrives in inactivity. Choose one small activity and do it, even if you feel nothing.",
        "**Professional Support:** What you are experiencing is real and it deserves real professional care. Reaching out is a brave act.",
    ],
}

def get_cbt_tip(category="general_stress"):
    tips = CBT_TECHNIQUES.get(category, CBT_TECHNIQUES["general_stress"])
    return random.choice(tips)