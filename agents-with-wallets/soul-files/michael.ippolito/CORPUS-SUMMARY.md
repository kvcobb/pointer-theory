# Michael Ippolito ("Mippo") — Onboarding Corpus

Gathered 2026-08-19. Source tool: `scripts/youtube_transcript.py` (transcripts land in
`/home/kurtis/Harmony/youtube-transcripts/` by default; copies placed here).

## Transcripts — 6 of 6 succeeded, 0 failures

| # | File | Video | Date | Dur | Words |
|---|------|-------|------|-----|-------|
| 1 | `The_Blockworks_Origin_Story_Michael_&_Jason_yts.txt` | gP9Z13AH6s8 — *The Blockworks Origin Story* (Empire) | 2023-08-09 | 1:32:00 | 17,805 |
| 2 | `Investor_Relations_in_the_Onchain_Era_DAS_NYC_2026_Day_1_Main_yts.txt` | 18NlF8jHK1w — *Investor Relations in the Onchain Era*, DAS NYC 2026 (Blockworks) | 2026-03-24 | 20:25 | 3,571 |
| 3 | `Blockworks_Acquires_Messari_yts.txt` | DcxBot9_u5c — *Blockworks Acquires Messari* (Blockworks) | 2026-06-12 | 29:10 | 6,090 |
| 4 | `[LIVE]_A_Conversation_with_Michael_Ippolito_yts.txt` | QwEaAwfiF_s — *[LIVE] A Conversation with Michael Ippolito* (Bankless) | 2024-02-17 | 1:16:45 | 15,824 |
| 5 | `Michael_Ippolito_and_Jason_Yanowitz_Founders_of_Blockworks_World-Class_Web3_Media_EP_#56_yts.txt` | 33uxZ2MTFmY — *Frictionless EP #56* (Logan Jastremski) | 2023-02-06 | 1:12:05 | 13,913 |
| 6 | `How_Will_Solana_Fare_Amidst_Greater_Competition_From_Ethereum_and_Hyperliquid_yts.txt` | sjVJc7pPkcI — *How Will Solana Fare…* (Unchained, w/ Tushar Jain) | 2026-02-27 | 1:23:14 | 14,727 |

**Total: 71,930 words** across ~6h 13m of source audio. Word counts include the ~15-line
metadata/description header each file carries.

Note: files 1, 3, 5 are multi-speaker with co-founder Jason Yanowitz; file 6 is with Tushar Jain;
file 4 is with Bankless's David Hoffman. None are diarized — speaker attribution to Mippo
specifically will need a diarization pass before voice/register work.

## Voice reference

`michael.ippolito-voiceref.wav` — **extracted successfully.**

- Source: QwEaAwfiF_s (Bankless), seconds 1988–2044
- Duration: 56.000 s exactly · 2,688,078 bytes (2.6 MB)
- Format: mono, 24 kHz, 16-bit PCM WAV
- **Not yet ear-checked.** Source is a two-person livestream, so this range should be verified as
  clean solo Mippo speech (no Hoffman overlap) before it is treated as canonical — per
  `feedback-voice-ref-transfers-one-voice-not-range` (a ref latches to the dominant/leading timbre)
  and `feedback-voice-ref-register-must-match-room`.

### Download note (worth keeping)

Plain `yt-dlp -x` failed on this video with `HTTP Error 403: Forbidden` across every player client
(`web`/`ios`/`mweb`/`tv`/`web_safari` returned images-only or DRM; `android_vr` surfaced audio
formats but 403'd on the actual fetch, both native and via ffmpeg `--download-sections`). Two
things were required together:

```
yt-dlp --js-runtimes node --cookies-from-browser chrome -f 140 -o out.m4a "<url>"
```

- `--js-runtimes node` — yt-dlp 2026.07.04 only auto-enables deno; node 22 is installed and solves
  the n-challenge fine, it just has to be named explicitly.
- `--cookies-from-browser chrome` — the PO-token/SABR enforcement is what produces the 403; local
  Chrome cookies clear it.

Trim was done afterward with `ffmpeg -ss 1988 -to 2044 -ac 1 -ar 24000`. Temp full-length audio
(71 MB m4a) was deleted.

## Flagged: DC crypto-regulation source

No transcript in this set is a dedicated DC/Capitol-Hill regulation news episode. The closest, and
the one to use for a regulation-themed follow-up piece:

**`Blockworks_Acquires_Messari_yts.txt`** (2026-06-12) — most recent of the six and by far the
densest on regulatory language (17 keyword hits vs. 4 or fewer in every other file). Mippo argues
the industry's transition out of being an *"outsider, unregulated kind of industry"*, works through
*"do we need to be regulated? do we not need to be regulated?"*, and lands on standardized
**disclosures** as the trust layer connecting issuers, investors, exchanges, **regulators**, and AI
agents. That is his live position on the regulatory turn, stated in his own voice.

Secondary: **`Investor_Relations_in_the_Onchain_Era_DAS_NYC_2026_Day_1_Main_yts.txt`**
(2026-03-24) — same disclosure/IR-regime thesis, solo-Mippo panel, and therefore also the best
candidate source for an *additional* clean voice ref.

If a genuine DC-news segment is wanted, it is not in this batch and a seventh URL will be needed.
