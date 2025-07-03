Sure! Here's a complete `README.md` for your **LAN Real-Time Captions** project, written in Markdown:

```markdown
# 🎤 LAN Real-Time Captions

A lightweight, fast, and offline-ready real-time speech-to-text captioning system over LAN using **Gradio**, **FastAPI**, and **Faster-Whisper**. Built for local environments, workshops, classrooms, or meetings — where accurate and fast transcriptions are needed without internet dependency.

---

## 🚀 Features

- 🎙️ **Speaker Interface** to capture audio and stream it for real-time transcription
- 📺 **Viewer Interface** to display captions live via WebSocket
- ⚡ Uses [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) for fast and efficient transcription
- 💾 Save and 📂 Clear caption logs to a local CSV file
- 🌐 Runs on LAN — no cloud, no API keys, full privacy

---

## 🧱 Project Structure

```

lan\_realtime\_captions/
│
├── backend/
│   ├── buffer.py              # Caption buffer manager
│   ├── server.py              # FastAPI server + WebSocket broadcaster
│   ├── transcriber.py         # Audio transcription using Faster-Whisper
│   └── requirements.txt       # Backend dependencies
│
├── frontend/
│   ├── frontend.py            # Gradio UI: Speaker & Viewer
│   ├── saved\_captions/
│   │   └── database.csv       # Auto-generated CSV of saved captions
│   └── requirements.txt       # Frontend dependencies
│
├── venv/                      # Python virtual environment (gitignored)
├── run.sh                     # Script to start both frontend and backend
└── README.md                  # You're here 📄

````

---

## ⚙️ Installation & Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/lan_realtime_captions.git
cd lan_realtime_captions
````

### 2. Create & activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

> 💡 **Note:** This uses `faster-whisper`, which supports CPU and GPU (optional).

### 4. Run the app

```bash
./run.sh
```

* Backend (FastAPI): [http://localhost:8000](http://localhost:8000)
* Frontend (Gradio): [http://localhost:7860](http://localhost:7860)

---

## 📦 Backend API

* `POST /stream` → Accepts 2-sec audio chunks, returns transcribed text
* `GET /` → Returns welcome message
* `POST /transcribe` → (Optional) Accepts full audio files
* `WS /ws` → WebSocket broadcasting live captions to connected clients

---

## 🖥️ UI Walkthrough

### 🎙️ Speaker Tab

* Start/Stop streaming microphone audio
* Sends 2-second chunks to the backend
* Backend returns transcriptions and broadcasts them to viewers

### 📺 Viewer Tab

* Displays captions in real-time
* Save current session captions to CSV
* Clear live captions

---

## 🧠 Model Info

* Model used: `small.en` (244 MB) by default
* Can be changed in `transcriber.py` via `MODEL_NAME = "base.en"` or others
* Runs on **CPU** or **CUDA GPU** (auto-configurable)

---

## 📁 Output

Saved captions are stored in:

```
frontend/saved_captions/database.csv
```

With format:

```csv
timestamp,caption
2025-07-03 22:15:12,"Hello everyone, welcome to the session..."
```

---

## 🛠️ TODO / Ideas

* Add language selector for multi-lingual support
* Allow saving .txt or .srt format
* Improve noise filtering for better accuracy
* Add client authentication for viewer tab

---

## 📄 License

MIT License © 2025 Hardik Chhipa

---

## 🙏 Acknowledgements

* [Gradio](https://www.gradio.app/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Faster-Whisper](https://github.com/guillaumekln/faster-whisper)
* [pydub](https://github.com/jiaaro/pydub)

```

Let me know if you'd like me to automatically insert your GitHub repo link in this `README.md`.
```
