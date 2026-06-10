import numpy as np

from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# PATHS
# =========================================================

REF_DIR = Path(
    ""
)

HYP_FILE = Path(
    ""
)

OUT_FILE = Path(
    ""
)

OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# =========================================================
# LOAD MODEL
# =========================================================

print("Loading embedding model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# =========================================================
# LOAD HYP INTO DICT
# =========================================================

print("Loading hypothesis file...")

hyp_map = {}

with open(HYP_FILE, "r", encoding="utf-8") as f:

    for line in f:

        line = line.strip()

        if not line:
            continue

        parts = line.split(maxsplit=1)

        if len(parts) < 2:
            continue

        utt_id = parts[0]
        text = parts[1]

        hyp_map[utt_id] = text

print(f"Loaded hypothesis transcripts: {len(hyp_map)}")

# =========================================================
# REF FILES
# =========================================================

ref_files = sorted(REF_DIR.glob("*.txt"))

scores = []

matched = 0
missing = 0

# =========================================================
# PROCESS
# =========================================================

for i, ref_file in enumerate(ref_files):

    utt_id = ref_file.stem

    # -----------------------------------------------------
    # CHECK HYP EXISTS
    # -----------------------------------------------------

    if utt_id not in hyp_map:
        missing += 1
        continue

    # -----------------------------------------------------
    # LOAD REF
    # -----------------------------------------------------

    with open(ref_file, "r", encoding="utf-8") as f:
        ref_raw = f.read().strip()

    ref_parts = ref_raw.split(maxsplit=1)

    if len(ref_parts) < 2:
        continue

    ref_text = ref_parts[1]

    # -----------------------------------------------------
    # LOAD HYP
    # -----------------------------------------------------

    hyp_text = hyp_map[utt_id]

    # -----------------------------------------------------
    # SKIP EMPTY
    # -----------------------------------------------------

    if len(ref_text) == 0 or len(hyp_text) == 0:
        continue

    # -----------------------------------------------------
    # EMBEDDINGS
    # -----------------------------------------------------

    ref_emb = model.encode([ref_text])[0]
    hyp_emb = model.encode([hyp_text])[0]

    # -----------------------------------------------------
    # COSINE SIMILARITY
    # -----------------------------------------------------

    sim = cosine_similarity(
        [ref_emb],
        [hyp_emb]
    )[0][0]

    scores.append(sim)

    matched += 1

    print(f"{utt_id}: {sim:.4f}")

# =========================================================
# RESULTS
# =========================================================

avg_score = np.mean(scores)

report = f"""
================================================
LLM PROMPTA MINIMAL - SEMANTIC SIMILARITY
================================================

Reference transcripts : {len(ref_files)}
Matched transcripts   : {matched}
Missing transcripts   : {missing}

------------------------------------------------

Average cosine similarity: {avg_score:.4f}

================================================
"""

# =========================================================
# SAVE
# =========================================================

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(report)

# =========================================================
# PRINT
# =========================================================

print(report)

print(f"Saved to: {OUT_FILE}")