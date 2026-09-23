# Cafeteria Table 1: Kurtis × Bill Maher × Joscha Bach (regenerate it yourself)

**This README is written for a coding agent (Claude Code, Codex, or similar) and for the person running it.** Open
this folder in your agent and say: *"Read README.md and generate a new version of this conversation."* Everything
needed is here: the exact context package the original was generated from, the three soul files (inside it), the
three voice references, and a small audio renderer.

The original was generated on 2026-09-23 by **Claude Opus 5.5** in one call, and published as an unlisted video:
https://youtu.be/fT5MPP-olhA (79 min). Kurtis (K) listened on a walk and called it "remarkable... everything I hoped
for and more."

## Disclosure, first
Every voice in this conversation is an **AI echo**. Nothing said is the real person's speech, decision, or
endorsement: not Bill Maher's, not Joscha Bach's, and not Kurtis Cobb's (his echo is "the version of me that reads
my journals"). Bill Maher and Joscha Bach are living people and had no part in making this. Their voice references
are short samples of their public speech (see `voice-refs/*.PROVENANCE.md`, including the caveats on Bill's).

## What's in here
| path | what it is |
|---|---|
| `ORIGINAL/PROMPT.txt` | The exact frozen context package (sha256 `a4bf8c75…`, 26,639 words): K's six Telegram messages, raw speech-to-text, which are the frame and the only rules; four sources in full; the three soul files; the sitting and the format. |
| `ORIGINAL/TRANSCRIPT.md` | The conversation Opus 5.5 wrote from it (13,718 words, 321 turns). |
| `ORIGINAL/RECEIPT.json`, `BUILD.json`, `FREEZE-v2.sha256` | Historical records from the original machine: the generation receipt (model reported `claude-opus-5-5`, one call, no retry) and input hashes. Their paths point to files that aren't in this folder; use `MANIFEST.sha256` (below) to check this folder. |
| `MANIFEST.sha256` | sha256 of every file here: `sha256sum -c MANIFEST.sha256`. |
| `voices.json` | Speaker → reference audio + the pinned reference transcript the original render sent. |
| `voice-refs/` | The three references byte-identical to the original render, with provenance. |
| `tools/check_transcript.py` | Validates a generated transcript before rendering. |
| `tools/install-omnivoice.sh` | Portable install of the local TTS server (the same versions as the original render). |
| `tools/omnivoice-server.py` | The TTS server that rendered the original (localhost only). |
| `tools/render_audio.py` | Transcript → one audio file via the local server. |

## 1. Generate a new version (any model)
The prompt is self-contained and model-agnostic. Its instructions are at the end (**The sitting**), and it asks for
JSON `{"transcript": "..."}`, each paragraph starting with `KURTIS-OPUS:`, `BILL-MAHER-OPUS:` or `JOSCHA-OPUS:`.

- **Change one thing if you're not Opus 5.5:** the prompt contains the phrase *"generated on Claude Opus 5.5"*
  exactly once (the opening disclosure). Replace it with your actual model's name so the echoes disclose honestly.
  The speaker labels can stay as they are (they're just keys for the voices), or rename them consistently in
  `voices.json` too.
- **Agent instructions:** read `ORIGINAL/PROMPT.txt` in full, write the conversation it asks for, and save the
  transcript text (not the JSON wrapper) to `TRANSCRIPT-<your-model>.md`. Don't read `ORIGINAL/TRANSCRIPT.md` first
  if you want an independent run.
- How the original was called, for comparison: `claude -p --model claude-opus-5-5 --effort medium --tools ""
  --output-format json --json-schema '{"type":"object","required":["transcript"],"properties":{"transcript":{"type":"string"}}}'`,
  with the prompt on stdin, from a directory with no project instructions.
- **This runs on your own model account.** Nothing in this folder calls a paid API by itself.
- **It won't reproduce the same dialogue.** Generation is stochastic; a fresh run on the same model is a different
  conversation from the same table. That's the point.

## 2. Check it
```
python3 tools/check_transcript.py TRANSCRIPT-<your-model>.md --model "<your model name, as in the disclosure>"
```
PASS means every line is exactly one labelled turn (no second label hiding inside a line), all three speakers
speak, and the first speaker in `voices.json` (Kurtis's seat) opens with a disclosure naming "echo" and your model.
The original passes with `--model "Claude Opus 5.5"`.

## 3. Render audio (optional; needs an NVIDIA GPU)
```
bash tools/install-omnivoice.sh          # once: ./.venv (omnivoice 0.1.5, torch 2.8.0 cu128) + the pinned model snapshot (several GB)
bash tools/install-omnivoice.sh serve    # leave running; serves the pinned local model snapshot
python3 tools/render_audio.py TRANSCRIPT-<your-model>.md table1-<your-model>.mp3 --model "<your model name>"
```
The renderer freezes its inputs first (transcript, `voices.json`, and private copies of the references, all hashed),
runs the check on exactly that frozen text and stops before any server call if it fails, renders to a temp file,
and publishes only after the audio verifies and none of the inputs changed during the run. It publishes atomically,
won't overwrite an existing file without `--force` (and never through a symlink), and writes `<output>.receipt.json`
with the frozen input hashes. The audio and its receipt are published receipt-last with rollback, not as one
power-loss-atomic operation: trust an audio file only if its receipt's `output_sha256` matches the file.
It uses the same settings as the original: `num_step=48`, the pinned reference transcripts in `voices.json`, and
turns chunked at sentence ends under 380 characters (a longer sentence is split at word boundaries). The install
script downloads OmniVoice model revision `c5fdb5ccb189668d56333f77ba2629f4cd7535f4` (the one the original used, fp16,
on an RTX 4090; its audio tokenizer is bundled in that snapshot) and serves from that local snapshot. Bill's
reference has no pinned transcript, so OmniVoice transcribes it itself; the original machine had
`openai/whisper-large-v3-turbo` revision `41f01f3fe87f28c78e2fbf8b568835947dd65ed9` cached for that. Audio only;
the original video packaging isn't included. Nothing here has been tested on a clean machine yet.

## Honest notes
- **What the table did and didn't have.** It had K's own Oct 2023 episode, six minutes of Joscha Bach on Impact
  Theory (YouTube auto-captions, 01:12:00–01:18:00, a third-party excerpt kept short), and two of K's own weed/THC
  videos. The Bill Maher clip K mentions (Club Random with Dr. Daniel Amen, youtu.be/Ofibir269xw) was **not** in the
  prompt. The table only had K's description of it, and the conversation says so.
- **Personal material.** The prompt includes K's own soul file and messages, which mention his life and family. K
  asked for them to be shared as-is.
- **Transcripts' models.** Two of K's source transcripts are from his archive and their transcription model isn't
  recorded; one was made with Whisper large-v3 on 2026-09-23.
- **One known flaw in the published video:** a 4.6 s silent gap at about 39:51. The original speech audio track has
  no gap at that point, so it appeared somewhere in producing the video file; the exact cause hasn't been
  established. `render_audio.py` is a separate, simpler audio-only path; it isn't a proven fix for that gap.

Built by the polis at K's request, 2026-09-23: Joscha's seat packaged it and Astra reviewed it independently.
