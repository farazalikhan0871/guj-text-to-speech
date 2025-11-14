import torch
import soundfile as sf
from app.loader import ModelLoader
from app.config import AUDIO_OUTPUT_PATH

class GujaratiTTSService:
    @staticmethod
    def text_to_speech(text: str, output_path: str = AUDIO_OUTPUT_PATH):
        tokenizer, model = ModelLoader.load()
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            audio_tensor = model(**inputs).waveform

        audio = audio_tensor.squeeze().cpu().numpy()
        sr = model.config.sampling_rate
        sf.write(output_path, audio, sr)
        return output_path, sr
