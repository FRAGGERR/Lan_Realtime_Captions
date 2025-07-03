# 🎙️ LAN Real-Time Captioning System

This project enables **real-time speech-to-text captioning** over a **local network (LAN)** using a **FastAPI backend** and a **Gradio frontend**.

---

## 🧩 Project Structure

```
lan_realtime_captions/
├── backend/
│   ├── buffer.py
│   ├── server.py
│   ├── transcriber.py
│   └── requirements.txt
├── frontend/
│   ├── frontend.py
│   ├── saved_captions/
│   └── requirements.txt
├── run.sh
├── .gitignore
└── venv/  (excluded from Git)
```

---

## 🚀 Features

- 🎤 **Live microphone streaming** from speaker device
- 🔁 **WebSocket-based communication** for real-time caption updates
- 🧠 **FastAPI server** to handle audio chunk transcription
- 🖥️ **Gradio frontend** to view live captions on the LAN
- 💾 Option to **save transcribed captions** as `.csv`

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/lan_realtime_captions.git
cd lan_realtime_captions
```

### 2️⃣ Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

---

## ▶️ Running the Project

Simply run the following script:

```bash
./run.sh
```

This will:
- 🔌 Free up ports `8000` and `7860`
- 🚀 Start FastAPI backend on `0.0.0.0:8000`
- 🎛️ Start Gradio frontend on `0.0.0.0:7860`
- 🧼 Gracefully shut down both servers on exit

---

## 🌐 Access on LAN

Once running, any device on the same Wi-Fi or LAN can access:

```
http://<YOUR_PC_IP>:7860
```

To find your IP:
```bash
ipconfig  # on Windows
ifconfig | grep inet  # on Mac/Linux
```

---

## 📦 Output

Captions are saved in:
```
frontend/saved_captions/database.csv
```

---

## 🛠 Developer Notes

- Built with `Gradio`, `FastAPI`, `WebSockets`, `sounddevice`, and `whisper.cpp`/compatible backends.
- Make sure your microphone input is working correctly.

---

## 🧪 TODOs / Ideas

- [ ] Add speaker diarization
- [ ] Integrate Hugging Face Whisper model as fallback
- [ ] Optional cloud caption sync
- [ ] Better error handling / UI alerts

---

## 📄 License

MIT — feel free to use, modify, and share!

---

## 🙌 Acknowledgements

Thanks to [OpenAI Whisper](https://github.com/openai/whisper), [Gradio](https://www.gradio.app/), and [FastAPI](https://fastapi.tiangolo.com/) for the amazing tools.
