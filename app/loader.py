import torch
from transformers import AutoTokenizer, AutoModelForTextToWaveform
from app.config import MODEL_ID

class ModelLoader:
    _tokenizer = None
    _model = None

    @staticmethod
    def load():
        if ModelLoader._tokenizer is None or ModelLoader._model is None:
            tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
            model = AutoModelForTextToWaveform.from_pretrained(MODEL_ID).to("cpu")
            ModelLoader._tokenizer = tokenizer
            ModelLoader._model = model
        return ModelLoader._tokenizer, ModelLoader._model
