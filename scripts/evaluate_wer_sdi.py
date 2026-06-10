from pathlib import Path
from jiwer import process_words

# ==========================================
# PATHS
# ==========================================
ref_dir = Path("")
hyp_dir = Path("")

out_file = Path("")
out_file.parent.mkdir(parents=True, exist_ok=True)

# ==========================================
# LOAD FILES
# ==========================================
ref_files = sorted(ref_dir.glob("*.txt"))

matched = 0
missing = 0

refs = []
hyps = []

ref_utts = 0
hyp_utts = 0

for ref_file in ref_files:
    hyp_file = hyp_dir / ref_file.name

    # count ref utterances
    with open(ref_file, "r", encoding="utf8") as f:
        ref_lines = [x.strip() for x in f if x.strip()]
    ref_utts += len(ref_lines)

    if not hyp_file.exists():
        missing += len(ref_lines)
        continue

    with open(hyp_file, "r", encoding="utf8") as f:
        hyp_lines = [x.strip() for x in f if x.strip()]
    hyp_utts += len(hyp_lines)

    # map utt_id -> text
    ref_map = {}
    hyp_map = {}

    for line in ref_lines:
        parts = line.split(maxsplit=1)
        utt_id = parts[0]
        text = parts[1] if len(parts) > 1 else ""
        ref_map[utt_id] = text

    for line in hyp_lines:
        parts = line.split(maxsplit=1)
        utt_id = parts[0]
        text = parts[1] if len(parts) > 1 else ""
        hyp_map[utt_id] = text

    # matched utts
    common_ids = sorted(set(ref_map.keys()) & set(hyp_map.keys()))

    matched += len(common_ids)

    for utt_id in common_ids:
        refs.append(ref_map[utt_id])
        hyps.append(hyp_map[utt_id])

# ==========================================
# SCORE
# ==========================================
result = process_words(refs, hyps)

S = result.substitutions
I = result.insertions
D = result.deletions
H = result.hits
N = S + D + H

wer = (S + I + D) / N * 100 if N else 0
s_rate = S / N * 100 if N else 0
i_rate = I / N * 100 if N else 0
d_rate = D / N * 100 if N else 0

# ==========================================
# OUTPUT
# ==========================================
report = f"""
==================================================
Whisper Normalized Evaluation
==================================================
Reference utterances : {ref_utts}
Hypothesis utterances: {hyp_utts}
Matched utterances   : {matched}
Missing in raw       : {missing}
--------------------------------------------------
WER               : {wer:.2f}%

Substitutions (S) : {S}
Insertions    (I) : {I}
Deletions     (D) : {D}
Hits              : {H}

Reference words N : {N}
--------------------------------------------------
S Rate            : {s_rate:.2f}%
I Rate            : {i_rate:.2f}%
D Rate            : {d_rate:.2f}%
==================================================
"""

with open(out_file, "w", encoding="utf8") as f:
    f.write(report)

print(report)
print(f"Saved to: {out_file}")
