import whisper
import numpy as np
from pydub import AudioSegment
import io

# Load Whisper model (small.en recommended for performance on CPU)
model = whisper.load_model("small.en")

def transcribe_audio(file_bytes: bytes) -> str:
    try:
        # Convert incoming bytes to AudioSegment
        audio = AudioSegment.from_file(io.BytesIO(file_bytes))
        audio = audio.set_channels(1).set_frame_rate(16000)
        
        # Convert audio to numpy array
        audio_np = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0
        
        # Whisper expects numpy arrays in float32
        result = model.transcribe(audio_np, fp16=False)  # Disable fp16 for CPU compatibility
        
        return result['text'].strip()

    except Exception as e:
        print(f"Transcription error: {e}")
        return "[ERROR: Could not transcribe audio]"
