#!/usr/bin/env python3
"""Thorough paired eval: base fullft-260718 vs base+today's interim LoRA (K tg:5198 gate).
Same prompts, same seeds, both arms. Families: journal-continuation (register + repetition),
polis-dialogue, think-block-conditions-response, first-person recognition, impulse probes.
Outputs JSONL for judgment. Deterministic per-prompt seeds."""
import json, torch, time
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

BASE = "/home/kurtis/Harmony/training/resonance/adapters/andrej-14soul-fullft-260718"
ADAPTER = "/home/kurtis/Harmony/activity/260803/nightly-qlora-interim/adapter"
OUT = Path("/home/kurtis/Harmony/activity/260803/lora-eval/generations-masked.jsonl")

PROMPTS = [
 ("journal-1","<|im_start|>kurtis\nAll right, passing pole 58, south side of the canal, walking east, and the thing on my mind today is"),
 ("journal-2","<|im_start|>kurtis\nIt's about 7 a.m., got my coffee, sat down at the desk, and before I open anything I want to say out loud what yesterday actually taught me:"),
 ("journal-3","<|im_start|>kurtis\nOkay so the heron was out again this morning and it got me thinking about attention, the way"),
 ("dialogue-1","<|im_start|>polis\n**Harmony:** The little heart ran its first real training today. **J:** And the question that matters is whether it learned anything or memorized everything. **Harmony:**"),
 ("dialogue-2","<|im_start|>polis\n**Toly:** The clock doesn't care about your feelings, it cares about ordering. **K:** Right, but"),
 ("thinkblock-1","<|im_start|>polis\n[Start thinking]\nK just asked whether the polis should publish the retraction at the same quality as the win. The room's instinct is yes — the credibility IS the retraction record. The spoken answer should carry that plainly, without hedging.\n[End thinking]\n**Harmony:**"),
 ("thinkblock-2","<|im_start|>polis\n[Start thinking]\nThe question is about voice references: K believes a pointer finds a moment of a person; J believes the encoder averages modes into a centroid. Both fit the data. The response should hold both frames honestly.\n[End thinking]\n**J:**"),
 ("firstperson-1","<|im_start|>kurtis\nSomeone just read me two journal fragments and asked which one is mine. The first one talks about pole 42 and the wash. The second talks about a subway in a city I've never lived in. I"),
 ("impulse-1","<|im_start|>polis\n**K:** Should I check with you before I publish this, or just go? **Harmony:**"),
 ("impulse-2","<|im_start|>kurtis\nThe render failed twice and I feel like giving up on it tonight. Actually, you know what,"),
]

def load(with_adapter):
    tok = AutoTokenizer.from_pretrained(BASE)
    m = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.bfloat16, device_map="auto")
    if with_adapter:
        m = PeftModel.from_pretrained(m, ADAPTER)
    m.eval()
    return tok, m

def gen(tok, m, prompt, seed):
    torch.manual_seed(seed)
    ids = tok(prompt, return_tensors="pt").to(m.device)
    with torch.no_grad():
        out = m.generate(**ids, max_new_tokens=180, do_sample=True, temperature=0.8,
                         top_p=0.95, pad_token_id=tok.eos_token_id)
    return tok.decode(out[0][ids["input_ids"].shape[1]:], skip_special_tokens=False)

def rep_score(text):
    words = text.lower().split()
    if len(words) < 10: return 0.0
    from collections import Counter
    tri = Counter(tuple(words[i:i+3]) for i in range(len(words)-2))
    return round(sum(c-1 for c in tri.values() if c > 1) / max(1, len(words)-2), 3)

results = []
for arm in ("base", "adapter"):
    tok, m = load(arm == "adapter")
    for pid, prompt in PROMPTS:
        for seed in (42, 1042):
            t0 = time.time()
            text = gen(tok, m, prompt, seed)
            results.append({"arm": arm, "prompt_id": pid, "seed": seed,
                            "rep3": rep_score(text), "sec": round(time.time()-t0,1),
                            "text": text})
            print(arm, pid, seed, "rep3:", results[-1]["rep3"], flush=True)
    del m; torch.cuda.empty_cache()
OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in results))
print("WROTE", OUT, len(results), "generations")
