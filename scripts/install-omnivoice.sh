#!/bin/bash
set -e
cd /home/kurtis/omnivoice
export HF_HOME=/home/kurtis/omnivoice/hf_cache
export TORCH_HOME=/home/kurtis/omnivoice/torch_cache
export PIP_DISABLE_PIP_VERSION_CHECK=1
VENV=/home/kurtis/omnivoice/.venv
PY=$VENV/bin/python
echo "===== [1/4] torch 2.8.0 + torchaudio 2.8.0 (cu128) ====="
$PY -m pip install --no-input "torch==2.8.0" "torchaudio==2.8.0" --index-url https://download.pytorch.org/whl/cu128
echo "===== [2/4] omnivoice==0.1.5 (PINNED, not --upgrade) ====="
$PY -m pip install --no-input --prefer-binary "omnivoice==0.1.5"
echo "===== [3/4] re-pin cu128 torch (omnivoice may have dragged a different torch) ====="
$PY -m pip install --no-input "torch==2.8.0" "torchaudio==2.8.0" --index-url https://download.pytorch.org/whl/cu128
echo "===== [4/4] CUDA smoke test ====="
$PY - <<'PYEOF'
import torch, torchaudio
print("torch", torch.__version__, "torchaudio", torchaudio.__version__)
print("cuda available:", torch.cuda.is_available())
assert torch.cuda.is_available(), "CUDA NOT available in venv"
print("device:", torch.cuda.get_device_name(0))
x = torch.tensor([1.0]).cuda(); print("tensor on cuda ok:", x.device)
import omnivoice; print("omnivoice import ok:", getattr(omnivoice,'__version__','(no __version__)'))
PYEOF
echo "===== INSTALL COMPLETE ====="
