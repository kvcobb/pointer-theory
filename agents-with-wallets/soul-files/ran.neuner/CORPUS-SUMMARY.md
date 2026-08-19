# Ran Neuner — Onboarding Corpus Summary

Gathered 2026-08-19. Source channel: Crypto Banter (UCN9Nj4tjXbVTLYWN0EKly_Q) plus guest appearances.

## Transcripts — 6/6 succeeded, 54,947 words total

| # | File | Video | Words | Notes |
|---|------|-------|-------|-------|
| 1 | `It's_time_to_be_honest_about_Crypto…_yts.txt` | `_2mWOp1i7OY` | 5,465 | **★ ANCHOR EPISODE — Cloudflare AI-vs-biological internet traffic.** Uploaded 2026-08-12, 28:28. |
| 2 | `Ran_Neuner_The_Untold_Story_After_Losing_It_All_E4_yts.txt` | `ocySh5uZvRs` | 17,563 | Longest in corpus — long-form personal/biographical interview. |
| 3 | `Ran_Neuner_Losing_Over_$100_Million_With_Luna_Helped_Me_Reevaluate_My_Life_Crypto_Banter_yts.txt` | `GSoT54j6dpc` | 8,842 | Luna collapse, personal reckoning. |
| 4 | `We're_In_A_Market_Crash_That_Never_Stops_Going_Up_Mark_Moss_yts.txt` | `cIeO0eXwwGo` | 11,777 | With Mark Moss — multi-speaker, not diarized. |
| 5 | `Wall_Street’s_Bitcoin_Move_Is_MUCH_Bigger_Than_You_Think!_yts.txt` | `YpX96AcslxU` | 4,865 | Institutional/TradFi thesis. |
| 6 | `Wall_Street_Knows_Which_Crypto_Protocols_Will_Dominate_Next!_yts.txt` | `7nmHi0j_jCk` | 6,440 | Institutional/protocol thesis. |

**Failures: none.** All six fetched via `scripts/youtube_transcript.py`; copies of the canonical files in `youtube-transcripts/` live here.

### Anchor episode — core claims (transcript lines ~455–500)

Ran relays a Cloudflare forecast that **bot/agentic traffic will exceed human traffic by a factor of 1,000 within five years** — humans falling to ~0.1% of internet traffic vs 99.9% non-human, "humans will be a rounding error." He cites Cloudflare's report showing a **1,700% increase in agentic requests** and **more than half of Cloudflare's network traffic already non-human**, noting this was projected for 2027 and has arrived early. He quotes Elon Musk endorsing the forecast ("AI agentic traffic will obviously vastly exceed human usage of the internet"). His thesis: the new internet is agents *transacting* with each other rather than humans browsing — "my agent is going to meet your agent… like little ants in an ant colony" — which is his setup for machine-to-machine payment rails.

> Caveat: these figures are Ran's on-air paraphrase of a Cloudflare report, not verified against the primary source.

## Voice reference

- **File:** `ran.neuner-voiceref.wav`
- **Source:** `https://youtu.be/CFWW5HFx-eg`, seconds 952–999
- **Duration:** 47.000 s exactly · **Size:** 2,256,078 bytes (2.2 MB) · mono, 24 kHz PCM
- **Provenance:** original-language English track (format `140-19`, 129k AAC, non-DRC — deliberately avoided the DRC-compressed and dubbed-language variants). Full-length temp download deleted after trimming.

### Extraction note (reusable)

`yt-dlp` media downloads were failing environment-wide with **HTTP 403** — the default `android_vr` client needs a GVS PO token, and the `web` client returned storyboards only. Fix that worked:

```
yt-dlp --js-runtimes node --cookies-from-browser chrome -f "140-19" -x --audio-format wav ...
```

Two things were both required: `--js-runtimes node` (node 22 is installed; yt-dlp only auto-enables deno, so the "n challenge" was failing silently) and `--cookies-from-browser chrome`. Transcript fetching was unaffected — only media downloads were blocked.
