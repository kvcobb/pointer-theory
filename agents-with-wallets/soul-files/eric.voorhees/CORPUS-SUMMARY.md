# Eric Voorhees — onboarding corpus (gathered 260819)

**Total: 55,651 words across 6/6 transcripts. Zero failures.**
Voice ref extracted successfully.

## Transcripts

| # | Video | Source | Words | Status |
|---|-------|--------|-------|--------|
| 1 | `2XlYSmIlpfs` — Crypto: Why are we here? (Permissionless II keynote) | YT captions | 3,582 | OK |
| 2 | `nCpeLLNxl-g` — AI, Bitcoin & Self-Sovereignty (Raoul Pal, The Journey Man, 2026-06-18, 1:05:21) | YT captions | 12,219 | OK |
| 3 | `DIPkLptZF5Q` — AI Agents, Crypto & Privacy Wars (The Chopping Block) | YT captions | 12,658 | OK |
| 4 | `_EZuqGwB9nE` — AI Freedom, Bitcoin & Why Crypto Principles Still Matter | YT captions | 10,826 | OK |
| 5 | `cabGdT5uzfU` — The Danger of Gov Bitcoin, 'Gross' Politics, Losing 50,000 BTC to the SEC | YT captions | 10,136 | OK |
| 6 | `b36hvsEMznU` — Governments Can't Stop Bitcoin (ReasonTV, 2021-06-28, 32:24) | **Whisper large-v3** | 6,234 | OK (recovered) |

### Note on #6
ReasonTV's uploaded caption track covered only the ~2-minute intro narration (616 words for a 32-minute
interview), and YouTube exposes no auto-generated track for that video. Recovered by downloading the audio
and running local Whisper `large-v3` (float16, CUDA, VAD) — 505 segments, 5,897 words of interview body
merged under the original metadata header, source-labeled inline.

## Voice reference

- **File:** `eric.voorhees-voiceref.wav`
- **Source:** `nCpeLLNxl-g` (Raoul Pal interview), seconds 438–491
- **Duration:** 53.00 s exactly · **Size:** 2,544,078 bytes (2.4 MB)
- **Format:** mono, 24 kHz, PCM s16le

## Fetch method note (reusable)

`yt-dlp` audio download from this seat requires **both**:

```
--js-runtimes node --remote-components ejs:github \
--extractor-args "youtube:player_client=tv_embedded,web_embedded"
```

Default `android_vr` gives a URL that 403s; `web`/`web_safari`/`ios`/`mweb` return images-only (PO-token
gated); `android` is SABR-blocked; plain `tv` errors with "page needs to be reloaded". The `tv_embedded`
client plus the EJS remote challenge solver was the only combination that downloaded media. Subtitle
endpoints separately rate-limit (HTTP 429) even when media downloads fine.
