import json
from pathlib import Path
from collections import defaultdict

# ============================================================
# PATHS
# ============================================================

# REF entities
REF_ENTITY_JSON = (
    ""
)

#  LLM hyp file
HYP_FILE = (
    ""
    
)

# OUTPUT
OUTPUT_JSON = (
    ""
)

# ============================================================
# LOAD REF ENTITIES
# ============================================================

with open(REF_ENTITY_JSON, "r", encoding="utf-8") as f:
    ref_entities = json.load(f)

# ============================================================
# LOAD HYP FILE
# ============================================================

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
        text = parts[1].lower().strip()

        hyp_map[utt_id] = " ".join(text.split())

print(f"Loaded hypothesis transcripts: {len(hyp_map)}")

# ============================================================
# STATISTICS
# ============================================================

total_entities = 0
matched_entities = 0

matched_by_type = defaultdict(int)
total_by_type = defaultdict(int)

missed_examples = []

# ============================================================
# MAIN LOOP
# ============================================================

for filename, entities in ref_entities.items():

    # remove .txt
    utt_id = Path(filename).stem

    # skip if missing
    if utt_id not in hyp_map:
        print(f"[Missing hyp] {utt_id}")
        continue

    hyp_text = hyp_map[utt_id]

    # --------------------------------------------------------
    # CHECK EACH ENTITY
    # --------------------------------------------------------

    for ent in entities:

        entity_text = ent["text"].lower().strip()
        entity_label = ent["label"]

        total_entities += 1
        total_by_type[entity_label] += 1

        # exact substring matching
        if entity_text in hyp_text:

            matched_entities += 1
            matched_by_type[entity_label] += 1

        else:

            missed_examples.append({
                "file": utt_id,
                "entity": entity_text,
                "label": entity_label
            })

# ============================================================
# RESULTS
# ============================================================

entity_recall = (
    matched_entities / total_entities
    if total_entities > 0 else 0
)

neer = 1 - entity_recall

report = f"""
============================================================
ENTITY PRESERVATION RESULTS
============================================================

Total REF entities: {total_entities}
Matched entities: {matched_entities}

Entity Recall: {entity_recall:.4f}
NEER: {neer:.4f}

============================================================
PER ENTITY TYPE
============================================================
"""

print(report)

# ============================================================
# PER TYPE
# ============================================================

for label in sorted(total_by_type.keys()):

    total = total_by_type[label]
    matched = matched_by_type[label]

    recall = matched / total if total > 0 else 0
    neer_type = 1 - recall

    print(f"{label}:")
    print(f"  Total: {total}")
    print(f"  Recall: {recall:.4f}")
    print(f"  NEER: {neer_type:.4f}")

# ============================================================
# SAVE MISSED ENTITIES
# ============================================================

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(missed_examples, f, indent=2, ensure_ascii=False)

print("\n============================================================")
print("Sample Missed Entities")
print("============================================================")

for ex in missed_examples[:30]:
    print(f'{ex["file"]} --> {ex["entity"]} ({ex["label"]})')

print(f"\nSaved missed entities to:")
print(OUTPUT_JSON)