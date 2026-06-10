import os
import json
import spacy
from collections import Counter

# =========================
# CONFIG
# =========================

INPUT_DIR = ""
OUTPUT_JSON = ""

KEEP_LABELS = {"ORG", "PERSON", "GPE"}

# keep important short finance/location entities
SHORT_WHITELIST = {
    "us", "uk", "eu",
    "gm", "bp", "ibm"
}

BAD_PHRASES = [
    "good morning",
    "thank you",
    "operator",
    "qa session",
]

SPECIAL_CHARS = ["%", "$", "¢"]

# =========================
# LOAD MODEL
# =========================

print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")

# =========================
# STORAGE
# =========================

all_entities = {}
label_counter = Counter()

# anomaly tracking
anomaly_examples = {
    "too_short": [],
    "repeated_words": [],
    "special_chars": [],
    "bad_phrase": [],
}

total_raw_entities = 0
total_kept_entities = 0

# =========================
# PROCESS FILES
# =========================

txt_files = sorted([
    f for f in os.listdir(INPUT_DIR)
    if f.endswith(".txt")
])

print(f"Found {len(txt_files)} txt files.\n")

for idx, filename in enumerate(txt_files):

    filepath = os.path.join(INPUT_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read().strip()

    doc = nlp(text)

    cleaned_entities = []

    for ent in doc.ents:

        total_raw_entities += 1

        entity_text = ent.text.lower().strip()
        label = ent.label_

        # -------------------------
        # FILTER 1: label filtering
        # -------------------------
        if label not in KEEP_LABELS:
            continue

        # -------------------------
        # FILTER 2: too short
        # keep important short entities
        # -------------------------
        if len(entity_text) <= 2 and entity_text not in SHORT_WHITELIST:
            anomaly_examples["too_short"].append(entity_text)
            continue

        # -------------------------
        # FILTER 3: special chars
        # -------------------------
        if any(ch in entity_text for ch in SPECIAL_CHARS):
            anomaly_examples["special_chars"].append(entity_text)
            continue

        # -------------------------
        # FILTER 4: repeated words
        # -------------------------
        words = entity_text.split()

        if len(words) >= 2 and len(set(words)) < len(words):
            anomaly_examples["repeated_words"].append(entity_text)
            continue

        # -------------------------
        # FILTER 5: bad phrases
        # -------------------------
        if any(bp in entity_text for bp in BAD_PHRASES):
            anomaly_examples["bad_phrase"].append(entity_text)
            continue

        # -------------------------
        # KEEP ENTITY
        # -------------------------
        cleaned_entities.append({
            "text": entity_text,
            "label": label
        })

        label_counter[label] += 1
        total_kept_entities += 1

    all_entities[filename] = cleaned_entities

    # progress display
    if (idx + 1) % 10 == 0:
        print(f"Processed {idx+1}/{len(txt_files)} files")

# =========================
# SAVE JSON
# =========================

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(all_entities, f, indent=2, ensure_ascii=False)

# =========================
# SUMMARY
# =========================

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)

print(f"Processed files: {len(txt_files)}")
print(f"Raw entities found: {total_raw_entities}")
print(f"Cleaned entities kept: {total_kept_entities}")

print("\nEntity type distribution:")
for label, count in label_counter.most_common():
    print(f"{label}: {count}")

# =========================
# ANOMALY REPORT
# =========================

print("\n" + "=" * 60)
print("ANOMALY REPORT")
print("=" * 60)

for category, items in anomaly_examples.items():

    unique_items = list(set(items))

    print(f"\n[{category}]")
    print(f"Count removed: {len(items)}")

    if unique_items:
        print("Examples:")
        for ex in unique_items[:15]:
            print(f"  - {ex}")
    else:
        print("  None")

print("\nSaved cleaned entities to:")
print(OUTPUT_JSON)