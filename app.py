import streamlit as st
import time
import json
import os
import re
import datetime
from typing import Dict, List, Tuple

# -------------------------------
# App config and constants
# -------------------------------
st.set_page_config(page_title="Emotional AI Companion", page_icon="💡", layout="wide")

DATA_DIR = "data"
JOURNAL_FILE = os.path.join(DATA_DIR, "journal.json")
MOOD_FILE = os.path.join(DATA_DIR, "mood.json")

EMOTIONS = ["happy", "sad", "angry", "stress", "excited", "lonely", "confused", "neutral"]

SAFE_REPLY = "Emotions can be layered and complex. I’m here to listen and help you take one small, helpful step."

REPLIES: Dict[str, str] = {
    "sad": "I hear you’re feeling low. It’s okay not to know the reason. Try a small step—like a short walk, writing how the morning went, or messaging someone you trust.",
    "angry": "That sounds frustrating. Your feelings are valid. Try a quick reset: slow breaths, a short break, and noting what triggered it.",
    "stress": "Stress can sneak up. Let’s lighten it: list 3 tasks, pick one tiny action, and set a 20‑minute focus timer.",
    "happy": "Love that energy. Want to capture this win? Save a note or set a small goal to keep the momentum.",
    "excited": "You sound pumped! Channel it—one action now, one later, one to share.",
    "lonely": "Feeling alone is tough. You’re not invisible here. Try a connection step: check‑in message, small online group, or 5‑minute gratitude note.",
    "confused": "Let’s find clarity. Share the options you’re considering. I’ll help you compare and pick one next step.",
    "neutral": "You seem steady. A tiny habit like a 2‑minute reset or a quick walk can keep things smooth."
}

# Soft crisis content detector (no diagnosing, just encourage human support)
CRISIS_PATTERNS = [
    r"\bi want to die\b", r"\bsuicide\b", r"\bkill myself\b", r"\bhurt myself\b",
    r"\bself harm\b", r"\bi hate myself\b"
]

# Profanity softening (basic)
PROFANITY = {"damn": "darn", "shit": "stuff", "fuck": "bleep", "fucking": "bleeping", "bitch": "person"}

# Keyword lexicon for fallback emotion detection
LEXICON: Dict[str, List[str]] = {
    "sad": ["sad", "down", "upset", "blue", "depressed", "cry", "unhappy"],
    "angry": ["angry", "mad", "furious", "rage", "annoyed", "irritated"],
    "stress": ["stress", "anxiety", "anxious", "worried", "overthinking", "pressure", "burnout"],
    "happy": ["happy", "joy", "glad", "smile", "grateful", "content"],
    "excited": ["excited", "hype", "thrilled", "pumped", "ecstatic"],
    "lonely": ["lonely", "alone", "isolated", "no one", "ignored"],
    "confused": ["confused", "lost", "unsure", "uncertain", "don’t know", "idk"],
    "neutral": ["okay", "fine", "normal", "meh"]
}

# Rate limiting per session (simple)
if "last_submit_ts" not in st.session_state:
    st.session_state.last_submit_ts = 0.0

# Mood store in session
if "moods" not in st.session_state:
    st.session_state.moods = []

# -------------------------------
# Utility functions
# -------------------------------
def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "w") as f:
            json.dump([], f)
    if not os.path.exists(MOOD_FILE):
        with open(MOOD_FILE, "w") as f:
            json.dump([], f)

def load_json(path: str) -> List[Dict]:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_json(path: str, data: List[Dict]) -> None:
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass  # never crash the app

def soften_profanity(text: str) -> str:
    def repl(match):
        w = match.group(0)
        lw = w.lower()
        return PROFANITY.get(lw, w)
    pattern = re.compile(r"\b(" + "|".join(map(re.escape, PROFANITY.keys())) + r")\b", re.IGNORECASE)
    return pattern.sub(repl, text)

def crisis_detect(text: str) -> bool:
    low = text.lower()
    return any(re.search(pat, low) for pat in CRISIS_PATTERNS)

def lexicon_emotion(text: str) -> str:
    low = text.lower()
    for emo, words in LEXICON.items():
        for w in words:
            if w in low:
                return emo
    return "neutral"

# -------------------------------
# Model loading with safe fallback
# -------------------------------
@st.cache_resource
def load_model_pipeline():
    try:
        from transformers import pipeline
        # Return-all-scores for more robust ranking
        model = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=True
        )
        return model
    except Exception:
        return None

MODEL = load_model_pipeline()

def detect_emotion(text: str) -> Tuple[str, Dict[str, float]]:
    # Try transformer first
    try:
        if MODEL:
            out = MODEL(text)[0]
            ranked = sorted(out, key=lambda x: x["score"], reverse=True)
            top = ranked[0]["label"]
            # Map labels to our set
            label_map = {
                "joy": "happy", "sadness": "sad", "anger": "angry", "fear": "stress",
                "surprise": "excited", "disgust": "angry", "neutral": "neutral"
            }
            emotion = label_map.get(top, "neutral")
            scores = {label_map.get(s["label"], s["label"]): float(round(s["score"], 4)) for s in ranked}
            return emotion, scores
    except Exception:
        pass
    # Fallback lexicon path (always available)
    emo = lexicon_emotion(text)
    return emo, {emo: 1.0}

def supportive_reply(emotion: str, text: str) -> str:
    base = REPLIES.get(emotion)
    if not base:
        return SAFE_REPLY
    if crisis_detect(text):
        return ("I’m really glad you told me. I’m not a professional, but you deserve real support from a trusted person. "
                "Please talk to a family member, friend, or a counselor. You don’t have to handle this alone.")
    return base

def summarize_text(text: str) -> Tuple[str, List[str]]:
    # Gentle summary: first sentence + simple insights
    sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]
    summary = sentences[0] if sentences else "A short reflective note."
    insights = []
    low = text.lower()
    if "morning" in low: insights.append("Morning mood signal")
    if any(k in low for k in ["tired", "sleep", "rest"]): insights.append("Energy/rest pattern")
    if any(k in low for k in ["alone", "lonely", "isolated"]): insights.append("Connection need")
    if any(k in low for k in ["study", "exam", "school", "college"]): insights.append("Study stress pattern")
    if any(k in low for k in ["work", "project", "deadline"]): insights.append("Workload pressure")
    return summary, insights or ["Try adding what felt hard or helpful."]

# -------------------------------
# Layout and UI
# -------------------------------
ensure_data_files()

# Header
st.markdown("""
<div style="padding:16px;border-radius:16px;background:linear-gradient(90deg,#0b0f17,#121826);
box-shadow: 0 0 24px rgba(124,252,255,0.15); border:1px solid rgba(255,255,255,0.08)">
  <h2 style="margin:0;color:#7cfcff">Emotional AI Companion</h2>
  <p style="margin:4px 0;color:#cfd8dc">Always here • Private • Non‑judgmental</p>
</div>
""", unsafe_allow_html=True)

col_chat, col_side = st.columns([3, 2])

with col_chat:
    st.subheader("Talk to me")
    user_input = st.text_area(
        "Share how you feel:",
        placeholder="e.g., I feel sadly from morning and I don’t know why.",
        height=120,
        help="Write freely. I’ll detect your emotion and respond supportively."
    )

    # Soft rate limiting: 1 request every 1.5 seconds
    now_ts = time.time()
    cooldown_ok = now_ts - st.session_state.last_submit_ts > 1.5

    cols = st.columns(3)
    with cols[0]:
        analyze_clicked = st.button("Analyze", type="primary", use_container_width=True)
    with cols[1]:
        save_journal_clicked = st.button("Save as journal", use_container_width=True)
    with cols[2]:
        clear_clicked = st.button("Clear", use_container_width=True)

    if clear_clicked:
        user_input = ""
        st.experimental_set_query_params()  # light reset

    if analyze_clicked:
        if not cooldown_ok:
            st.info("Just a sec… give me a moment between messages.")
        elif not user_input or len(user_input.strip()) < 3:
            st.warning("Tell me a little more so I can help.")
        else:
            st.session_state.last_submit_ts = now_ts
            with st.spinner("Understanding your feelings…"):
                safe_text = soften_profanity(user_input.strip())
                emo, scores = detect_emotion(safe_text)
                reply = supportive_reply(emo, safe_text)
                time.sleep(0.3)

            st.success(f"Detected emotion: {emo}")
            st.write(reply)

            # Save mood snapshot (session + file)
            snapshot = {
                "time": datetime.datetime.now().isoformat(timespec="minutes"),
                "emotion": emo
            }
            st.session_state.moods.append(snapshot)
            moods_file = load_json(MOOD_FILE)
            moods_file.append(snapshot)
            save_json(MOOD_FILE, moods_file)

            # Show scores if available
            with st.expander("Emotion confidence"):
                for k, v in scores.items():
                    st.progress(min(v, 1.0))
                    st.write(f"{k}: {v:.2f}")

    if save_journal_clicked:
        if not user_input or len(user_input.strip()) < 3:
            st.warning("Write a bit more to save a meaningful journal.")
        else:
            safe_text = soften_profanity(user_input.strip())
            summary, insights = summarize_text(safe_text)
            entry = {
                "time": datetime.datetime.now().isoformat(timespec="minutes"),
                "text": safe_text,
                "summary": summary,
                "insights": insights
            }
            journal = load_json(JOURNAL_FILE)
            journal.append(entry)
            save_json(JOURNAL_FILE, journal)
            st.success("Journal entry saved.")
            st.write("Summary:", summary)
            st.write("Insights:", ", ".join(insights))

with col_side:
    st.subheader("Mood history")
    moods_file = load_json(MOOD_FILE)
    if len(moods_file) == 0 and len(st.session_state.moods) == 0:
        st.caption("No moods yet. Analyze a feeling to start tracking.")
    else:
        # Aggregate per emotion
        counts: Dict[str, int] = {e: 0 for e in EMOTIONS}
        for m in moods_file[-200:]:
            counts[m.get("emotion", "neutral")] = counts.get(m.get("emotion", "neutral"), 0) + 1
        chart_data = {"emotion": [], "count": []}
        for e, c in counts.items():
            chart_data["emotion"].append(e)
            chart_data["count"].append(c)
        st.bar_chart(chart_data, x="emotion", y="count", height=220)

    st.subheader("Journaling")
    journal_list = load_json(JOURNAL_FILE)
    if not journal_list:
        st.caption("Your saved notes will appear here.")
    else:
        for j in journal_list[-5:][::-1]:
            with st.expander(f"{j['time']} • {j.get('summary','Note')}"):
                st.write(j.get("text", ""))
                st.write("Insights:", ", ".join(j.get("insights", [])))

st.divider()
st.caption("This app offers general emotional support and clarity. It is not medical advice or a replacement for professional help.")
