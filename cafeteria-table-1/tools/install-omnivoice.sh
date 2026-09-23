#!/usr/bin/env bash
# Portable OmniVoice setup for this folder. Creates ./.venv next to tools/, installs the exact package versions the
# original render used, downloads the EXACT model revision it used, and serves FROM THAT LOCAL SNAPSHOT (so a later
# upstream model update can't silently change the voices). Needs Python 3.10+, an NVIDIA GPU with CUDA 12.8-compatible
# drivers, and ffmpeg. The model download is several GB.
#
#   bash tools/install-omnivoice.sh          # install + download the pinned model snapshot
#   bash tools/install-omnivoice.sh serve    # start the server on 127.0.0.1:8810 (leave running; Ctrl-C to stop)
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$HERE/.venv"
REV="c5fdb5ccb189668d56333f77ba2629f4cd7535f4"     # k2-fsa/OmniVoice revision used for the original render
export HF_HOME="${HF_HOME:-$HERE/.hf_cache}"
if [ "${1:-}" = "serve" ]; then
  SNAP="$(cat "$VENV/omnivoice-model-path")"
  [ -d "$SNAP" ] || { echo "pinned snapshot missing; run the install step first"; exit 1; }
  export OMNIVOICE_MODEL="$SNAP"                    # the server loads from this local path, not the mutable hub name
  export OMNIVOICE_REGISTRY="$HERE/.no-registry.json" # absent on purpose: render_audio.py sends every ref inline
  echo "serving OmniVoice from $SNAP (revision $REV)"
  exec "$VENV/bin/python" "$HERE/tools/omnivoice-server.py"
fi
python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install "torch==2.8.0" "torchaudio==2.8.0" --index-url https://download.pytorch.org/whl/cu128
"$VENV/bin/python" -m pip install "omnivoice==0.1.5" "fastapi==0.136.3" "uvicorn==0.48.0" soundfile numpy pydantic huggingface_hub
"$VENV/bin/python" -m pip install "torch==2.8.0" "torchaudio==2.8.0" --index-url https://download.pytorch.org/whl/cu128   # re-pin
"$VENV/bin/python" -c "import torch, omnivoice; assert torch.cuda.is_available(), 'CUDA not available'; print('ok', torch.__version__)"
"$VENV/bin/python" - "$REV" "$VENV/omnivoice-model-path" <<'PY'
import sys
from huggingface_hub import snapshot_download
p = snapshot_download("k2-fsa/OmniVoice", revision=sys.argv[1])
open(sys.argv[2], "w").write(p); print("pinned model snapshot:", p)
PY
echo "Installed. Start the server with: bash tools/install-omnivoice.sh serve"
