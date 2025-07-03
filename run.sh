#!/usr/bin/env bash
set -euo pipefail

# ───────────────────────── CONFIG ────────────────────────── #
BACKEND_PORT=8000
FRONTEND_PORT=7860
BACKEND_HOST="0.0.0.0"   # listen on LAN
VENV_DIR="venv"          # adjust if you keep your venv elsewhere
# ─────────────────────────────────────────────────────────── #

# ---------- helper: free a TCP port (macOS / Linux) ----------
free_port () {
  local PORT=$1
  # lsof prints the PIDs; xargs -r (or --no-run-if-empty) kills only if we found any.
  if lsof -ti tcp:"$PORT" >/dev/null 2>&1; then
    echo "⚠️  Port $PORT in use — killing old process(es)…"
    lsof -ti tcp:"$PORT" | xargs -r kill -9
    # Give the OS a moment to release TIME_WAIT sockets
    sleep 1
  fi
}

echo "🧹  Reclaiming ports $BACKEND_PORT & $FRONTEND_PORT"
free_port "$BACKEND_PORT"
free_port "$FRONTEND_PORT"

# ---------- activate venv ----------
if [[ -d "$VENV_DIR" ]]; then
  source "$VENV_DIR/bin/activate"
else
  echo "❌  Virtual environment not found ($VENV_DIR). Aborting."
  exit 1
fi

# ---------- start backend ----------
echo "🚀  Starting FastAPI backend on $BACKEND_HOST:$BACKEND_PORT …"
cd backend
uvicorn server:app --host "$BACKEND_HOST" --port "$BACKEND_PORT" --reload &
BACKEND_PID=$!
cd ..

# optional: give backend a head‑start
sleep 2

# ---------- start frontend ----------
echo "🎛️  Starting Gradio frontend on port $FRONTEND_PORT …"
export GRADIO_SERVER_PORT="$FRONTEND_PORT"
export GRADIO_SERVER_NAME="0.0.0.0"       # make it reachable on LAN
cd frontend
python frontend.py &
FRONTEND_PID=$!
cd ..

# ---------- cleanup on exit ----------
cleanup () {
  echo -e "\n🛑  Caught signal – shutting everything down…"
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
  wait 2>/dev/null || true
  type deactivate &>/dev/null && deactivate
  echo "✅  All stopped."
}
trap cleanup INT TERM EXIT

# ---------- hand over control ----------
wait

 
# ./run.sh 