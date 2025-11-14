from fastapi import FastAPI
from pydantic import BaseModel
from app.tts_service import GujaratiTTSService

app = FastAPI(title="Gujarati TTS API")

class TTSRequest(BaseModel):
    text: str

@app.post("/tts")
def tts_endpoint(req: TTSRequest):
    try:
        filepath, sr = GujaratiTTSService.text_to_speech(req.text)
        return {"status": "success", "file": filepath, "sampling_rate": sr}
    except Exception as e:
        return {"status": "error", "message": str(e)}
