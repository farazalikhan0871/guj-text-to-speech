import sys
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

import streamlit as st
import torch
import soundfile as sf
from transformers import AutoTokenizer, AutoModelForTextToWaveform

# -----------------------------------------------------
# LANGUAGE → HUGGINGFACE MODEL MAPPING
# -----------------------------------------------------
LANG_MODEL_MAP = {
    "Gujarati": "facebook/mms-tts-guj",
    "Hindi": "facebook/mms-tts-hin",
    "English": "facebook/mms-tts-eng",
    "Marathi": "facebook/mms-tts-mar",
    "Bengali": "facebook/mms-tts-ben",
    "Tamil": "facebook/mms-tts-tam",
    "Telugu": "facebook/mms-tts-tel",
    "Kannada": "facebook/mms-tts-kan",
    "Punjabi": "facebook/mms-tts-pan",
    "Malayalam": "facebook/mms-tts-mal"
}

# -----------------------------------------------------
# LOAD MODEL (cached by language)
# -----------------------------------------------------
@st.cache_resource
def load_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTextToWaveform.from_pretrained(model_name).to("cpu")
    return tokenizer, model


# -----------------------------------------------------
# BEAUTIFUL UI CSS
# -----------------------------------------------------
st.markdown("""
    <style>

        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        .header {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            padding: 40px 10px;
            border-radius: 0 0 25px 25px;
            text-align: center;
            color: white;
            margin-bottom: 35px;
        }

        .header h1 {
            font-size: 42px;
            font-weight: 700;
        }

        .header h3 {
            font-size: 18px;
            font-weight: 300;
            opacity: .9;
        }

        .glass-card {
            backdrop-filter: blur(12px);
            background: rgba(255, 255, 255, 0.4);
            padding: 25px;
            border-radius: 14px;
            max-width: 850px;
            margin: auto;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }

        .convert-btn button {
            background: linear-gradient(135deg, #ff512f 0%, #dd2476 100%) !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            margin-top: 10px;
            padding: 12px;
            border-radius: 10px !important;
            width: 100%;
        }

        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #777;
        }

    </style>
""", unsafe_allow_html=True)


# -----------------------------------------------------
# HEADER
# -----------------------------------------------------
st.markdown("""
    <div class="header">
        <h1>🎤 Multilingual Text → Speech Converter</h1>
        <h3>Convert text to natural speech in 10+ Indian languages</h3>
    </div>
""", unsafe_allow_html=True)


# -----------------------------------------------------
# MAIN CARD UI
# -----------------------------------------------------
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

# Language selector
language = st.selectbox(
    "🌐 Select Language:",
    list(LANG_MODEL_MAP.keys()),
    index=0
)

# User input text
text = st.text_area(
    f"✍ Enter {language} text:",
    placeholder="Type here...",
    height=180
)

# -----------------------------------------------------
# Convert Button
# -----------------------------------------------------
st.markdown("<div class='convert-btn'>", unsafe_allow_html=True)

if st.button("🔊 Convert to Speech"):
    if not text.strip():
        st.error("Please enter text!")
    else:
        try:
            model_id = LANG_MODEL_MAP[language]
            tokenizer, model = load_model(model_id)

            with st.spinner("🎧 Generating speech..."):
                
                # TOKENIZE
                inputs = tokenizer(text, return_tensors="pt")

                # 🔥🔥🔥 IMPORTANT FIX (for Marathi, Punjabi, Malayalam)
                inputs["input_ids"] = inputs["input_ids"].long()

                if "attention_mask" in inputs:
                    inputs["attention_mask"] = inputs["attention_mask"].long()
                # -------------------------------------------------------

                with torch.no_grad():
                    audio_tensor = model(**inputs).waveform

                audio = audio_tensor.squeeze().cpu().numpy()
                sr = model.config.sampling_rate

                sf.write("tts_output.wav", audio, sr)

            st.success("🎉 Speech generated successfully!")
            st.audio("tts_output.wav")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------
# FOOTER
# -----------------------------------------------------
st.markdown("""
    <div class="footer">
        Made with ❤️ Using Transformers & Streamlit
    </div>
""", unsafe_allow_html=True)
