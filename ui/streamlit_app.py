import sys
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

import streamlit as st
from app.tts_service import GujaratiTTSService
from app.utils import validate_text

# -----------------------------------------
# BEAUTIFUL CUSTOM CSS (Glassmorphism UI)
# -----------------------------------------
st.markdown("""
    <style>

        /* Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 40px 10px;
            border-radius: 0 0 25px 25px;
            text-align: center;
            color: white;
            margin-bottom: 35px;
            box-shadow: 0px 8px 18px rgba(0,0,0,0.15);
        }

        .header h1 {
            font-size: 40px;
            font-weight: 700;
            margin: 0;
        }

        .header h3 {
            font-size: 18px;
            font-weight: 400;
            opacity: 0.9;
            margin-top: 6px;
        }

        .glass-card {
            backdrop-filter: blur(12px);
            background: rgba(255, 255, 255, 0.55);
            border-radius: 18px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            max-width: 850px;
            margin: auto;
        }

        .convert-btn button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            padding: 12px;
            font-size: 20px !important;
            border-radius: 12px !important;
            width: 100%;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }

        .convert-btn button:hover {
            transform: scale(1.03);
            box-shadow: 0px 8px 18px rgba(118, 75, 162, 0.3);
        }

        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #666;
        }

    </style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER SECTION
# -------------------------
st.markdown("""
    <div class="header">
        <h1>🎤 Gujarati Text → Speech</h1>
        <h3>Convert any Gujarati text into crystal-clear speech in seconds</h3>
    </div>
""", unsafe_allow_html=True)

# -------------------------
# BODY CARD
# -------------------------
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

text = st.text_area(
    "✨ Enter Gujarati text:",
    placeholder="ઉદાહરણ: નમસ્તે! આજે તમારો દિવસ કેમ ગયો?",
    height=180
)

# -------------------------
# GENERATE BUTTON
# -------------------------
st.markdown("<div class='convert-btn'>", unsafe_allow_html=True)

if st.button("🔊 Convert to Speech"):
    try:
        validate_text(text)

        with st.spinner("🎧 Transforming text into speech…"):
            filepath, _ = GujaratiTTSService.text_to_speech(text)

        st.success("✅ Speech generated successfully!")
        st.audio(filepath)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)

# Close card
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# FOOTER
# -------------------------
st.markdown("""
    <div class="footer">
        Made with ❤️ by Gujarati AI | Powered by Streamlit & HuggingFace
    </div>
""", unsafe_allow_html=True)
