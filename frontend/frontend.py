# Gradio UI (Speaker + Viewer tabs)


"""
| Tab             | Purpose                                                    |
| --------------- | ---------------------------------------------------------- |
| Speaker Tab     | Mic recording → Send audio chunks to FastAPI /transcribe |
| Viewer Tab*     | WebSocket listener → Live real-time caption display        |

"""

import gradio as gr
import requests
import asyncio
import websockets
import threading
import time
import wave
import sounddevice as sd
import soundfile as sf
import numpy as np
import io
import os
import csv
from datetime import datetime
from threading import Event

# ---------------- Configuration ---------------- #
BACKEND_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws"
CSV_PATH = "saved_captions/database.csv"

# ---------------- Captions Memory ---------------- #
live_captions = ""

# ---------------- Save Captions ---------------- #
def save_caption_to_csv(caption_text: str) -> str:
    if not caption_text.strip():
        return "❌ Nothing to save."

    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    header_needed = not os.path.isfile(CSV_PATH)

    try:
        with open(CSV_PATH, "a", newline="") as f:
            writer = csv.writer(f)
            if header_needed:
                writer.writerow(["timestamp", "caption"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), caption_text])
        return "✅ Saved to database.csv"
    except Exception as e:
        return f"⚠️ Error: {e}"

# ---------------- Speaker Tab ---------------- #
def create_speaker_tab():
    with gr.Blocks() as speaker_tab:
        status = gr.Textbox(label="Status", value="Ready", interactive=False)
        start_btn = gr.Button("Start Streaming")
        stop_btn = gr.Button("Stop Streaming", interactive=False)

        stop_event = Event()
        audio_thread = gr.State(value=None)

        def start_streaming():
            stop_event.clear()
            return "Streaming...", gr.update(interactive=False), gr.update(interactive=True)

        def stop_streaming():
            stop_event.set()
            return "Stopped", gr.update(interactive=True), gr.update(interactive=False)

        def audio_capture_loop():
            SAMPLE_RATE = 16000
            CHANNELS = 1
            DURATION = 2  # seconds per chunk
            print("Audio streaming started")
            try:
                while not stop_event.is_set():
                    audio_data = sd.rec(
                        int(DURATION * SAMPLE_RATE),
                        samplerate=SAMPLE_RATE,
                        channels=CHANNELS,
                        dtype='float32'
                    )
                    sd.wait()
                    wav_buffer = io.BytesIO()
                    sf.write(wav_buffer, audio_data, SAMPLE_RATE, format='WAV', subtype='PCM_16')
                    wav_data = wav_buffer.getvalue()
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/stream",
                            data=wav_data,
                            headers={"Content-Type": "audio/wav"}
                        )
                        if response.status_code != 200:
                            print(f"Backend error: {response.text}")
                    except Exception as e:
                        print(f"Network error: {e}")
                    time.sleep(0.1)
            except Exception as e:
                print(f"Audio capture error: {e}")
            finally:
                print("Audio streaming stopped")

        def toggle_streaming(thread_ref):
            thread = threading.Thread(target=audio_capture_loop, daemon=True)
            thread.start()
            return thread

        start_btn.click(fn=start_streaming, inputs=[], outputs=[status, start_btn, stop_btn])\
                 .then(fn=toggle_streaming, inputs=[audio_thread], outputs=[audio_thread])

        stop_btn.click(fn=stop_streaming, inputs=[], outputs=[status, start_btn, stop_btn])

    return speaker_tab

# ---------------- Viewer Tab ---------------- #

async def websocket_listener():
    global live_captions
    try:
        async with websockets.connect(WS_URL) as websocket:
            async for message in websocket:
                # Directly use the message without adding another timestamp
                live_captions += message + "\n"
                time.sleep(0.1)
    except Exception as e:
        live_captions += f"\n[WebSocket error: {e}]\n"

def start_websocket_listener():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_listener())

def launch_websocket_listener():
    thread = threading.Thread(target=start_websocket_listener, daemon=True)
    thread.start()

def get_live_captions():
    return live_captions

def clear_live_captions():
    global live_captions
    live_captions = ""
    return ""

def create_viewer_tab():
    with gr.Blocks() as viewer_tab:
        caption_box = gr.Textbox(label="Live Captions", lines=20)
        save_btn = gr.Button("💾 Save current captions")
        clear_btn = gr.Button("🧹 Clear captions")
        save_status = gr.Textbox(label="Save status", interactive=False)

        timer = gr.Timer(value=1.0)
        timer.tick(lambda: get_live_captions(), outputs=caption_box)

        save_btn.click(fn=save_caption_to_csv, inputs=caption_box, outputs=save_status)
        clear_btn.click(fn=clear_live_captions, outputs=caption_box)

    return viewer_tab

# ---------------- Launch App ---------------- #
launch_websocket_listener()

speaker_tab = create_speaker_tab()
viewer_tab = create_viewer_tab()

app = gr.TabbedInterface(
    interface_list=[speaker_tab, viewer_tab],
    tab_names=["🎙️ Speaker", "📺 Viewer"]
)

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)
