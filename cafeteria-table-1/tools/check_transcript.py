#!/usr/bin/env python3
"""Check a generated cafeteria-table transcript before rendering it.

    python tools/check_transcript.py TRANSCRIPT.md --model "Claude Opus 5.5"

PASS only if:
  - every non-empty line is exactly one turn, "LABEL: text", with LABEL from voices.json (or an unvoiced "STAGE:" line);
  - no line contains a second speaker label inside it (e.g. "... JOSCHA-OPUS: ...");
  - every speaker in voices.json speaks at least once;
  - the first spoken line belongs to the FIRST speaker listed in voices.json (Kurtis's seat; rename-safe) and its
    disclosure contains the word "echo" AND the model name you pass with --model.
Importable: check(path, model) -> dict.
"""
import argparse, json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent

def check(path, model, text=None, voices=None):
    """text/voices: pass already-frozen inputs (render_audio does) so the check runs on exactly what gets rendered."""
    model = (model or "").strip()
    if len(model) < 2: raise ValueError("--model must name the model (e.g. 'Claude Opus 5.5'); empty or 1-char is not allowed")
    voices = voices if voices is not None else json.loads((HERE / "voices.json").read_text())["voices"]
    labels = list(voices); opener = labels[0]
    lines = [l for l in (text if text is not None else Path(path).read_text()).splitlines() if l.strip()]
    lab = lambda l: l.split(":", 1)[0]
    bad = [l[:80] for l in lines if not (l.startswith("STAGE: ") or (re.match(r"^[A-Z][A-Z0-9-]*: \S", l) and lab(l) in labels))]
    emb = re.compile(r"\b(" + "|".join(map(re.escape, labels + ["STAGE"])) + r"):")
    embedded = [l[:80] for l in lines if emb.search(l.split(":", 1)[1] if ":" in l else l)]
    spoken = [l for l in lines if lab(l) in labels]
    first = spoken[0] if spoken else ""
    disclosure = first.startswith(opener + ":") and "echo" in first.lower() and model.lower() in first.lower()
    res = {"turns": len(spoken), "words": sum(len(l.split()) for l in spoken), "bad_lines": bad[:5], "embedded_labels": embedded[:5],
           "missing_speakers": sorted(set(labels) - {lab(l) for l in spoken}), "opener": opener, "model": model,
           "opening_disclosure_ok": disclosure}
    res["PASS"] = not bad and not embedded and not res["missing_speakers"] and disclosure
    return res

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("transcript"); ap.add_argument("--model", required=True, help='the model that generated it, as named in its disclosure, e.g. "Claude Opus 5.5"')
    a = ap.parse_args()
    try: r = check(a.transcript, a.model)
    except ValueError as e: sys.exit(str(e))
    print(json.dumps(r, indent=1)); sys.exit(0 if r["PASS"] else 1)
