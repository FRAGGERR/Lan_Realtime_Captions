# FastAPI server (HTTP + WebSocket endpoints)

"""
This server handles audio transcription and real-time caption broadcasting
using FastAPI and WebSockets. It allows a Gradio frontend to connect and receive
real-time captions from audio files uploaded by users.
"""
from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi import Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio
import datetime
import time
from transcriber import transcribe_audio
from buffer import CaptionBuffer

app = FastAPI()


# Allow Gradio frontend to connect (CORS setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For LAN, it's fine. Later restrict this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


# Global variables
clients: List[WebSocket] = [] 
caption_buffer = CaptionBuffer(duration_seconds=300)  # 5 minutes buffer 
 
@app.get("/")
def root():
    return {"message": "Welcome to the Audio Transcription Server!"}


@app.post("/transcribe") 
async def transcribe_endpoint(audio_file: UploadFile = File(...)): 
    audio_bytes = await audio_file.read() 
    text = transcribe_audio(audio_bytes) 

    # Timestamped entry
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    caption_entry = {"timestamp": timestamp, "text": text} 

    # Update buffer
    caption_buffer.add_caption(caption_entry) 

    # Broadcast to WebSocket clients
    await broadcast_caption(caption_entry)

    return {"caption": text}

# Newly added code : -->
@app.post("/stream")
async def stream_audio(audio_chunk: bytes = Body(...)):
    try:
        start_time = time.time()
        text = transcribe_audio(audio_chunk)
        
        # Timestamped entry
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caption_entry = {"timestamp": timestamp, "text": text}
        
        # Update buffer
        caption_buffer.add_caption(caption_entry)
        
        # Broadcast to WebSocket clients
        await broadcast_caption(caption_entry)
        
        print(f"Transcription time: {time.time() - start_time:.2f}s")
        return {"caption": text}
    except Exception as e:
        print(f"Stream processing error: {e}")
        return {"error": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        # Send last 5 minutes of history upon new connection
        for caption in caption_buffer.get_captions():
            await websocket.send_text(f"[{caption['timestamp']}] {caption['text']}")

        # Keep connection alive
        while True:
            await asyncio.sleep(10)  # Prevent disconnect due to inactivity

    except Exception as e:
        print(f"WebSocket connection error: {e}")

    finally:
        clients.remove(websocket)
        await websocket.close()


async def broadcast_caption(caption_entry):
    disconnected_clients = []

    for client in clients:
        try:
            message = f"[{caption_entry['timestamp']}] {caption_entry['text']}"
            await client.send_text(message)
        except Exception as e:
            print(f"Failed to send to client: {e}")
            disconnected_clients.append(client)

    # Clean up disconnected clients
    for client in disconnected_clients:
        clients.remove(client)