import os
import re

# =========================================================
# CONFIG
# =========================================================

# Root directory containing all regions
INPUT_ROOT = ""

# Output directory for chunked files
OUTPUT_ROOT = ""

# Region names
REGIONS = [
    "African",
    "Asian",
    "English",
    "Germanic",
    "Other_Romance",
    "Slavic",
    "Spanish_Portuguese"
]

# Chunk size settings
MAX_WORDS = 550
MIN_WORDS = 350

# Create output root
os.makedirs(OUTPUT_ROOT, exist_ok=True)

# =========================================================
# FUNCTION 1
# Remove utterance ID at beginning
# =========================================================

def remove_utterance_id(text):

    """
    Example:

    Input:
    4453225 Hello everyone welcome...

    Output:
    Hello everyone welcome...
    """

    parts = text.strip().split(" ", 1)

    if len(parts) == 2:

        first_part = parts[0]

        # remove numeric utterance ID
        if first_part.isdigit():

            return parts[1]

    return text


# =========================================================
# FUNCTION 2
# Split transcript into paragraph-like units
# =========================================================

def split_into_paragraphs(text):

    """
    Split using punctuation + capital letter.

    Example:
    "Thank you. Good afternoon everyone."

    ->
    [
        "Thank you.",
        "Good afternoon everyone."
    ]
    """

    paragraphs = re.split(
        r'(?<=[\.\?\!])\s+(?=[A-Z])',
        text
    )

    return [
        p.strip()
        for p in paragraphs
        if p.strip()
    ]


# =========================================================
# FUNCTION 3
# Dynamic chunking
# =========================================================

def chunk_paragraphs(
    paragraphs,
    max_words=550,
    min_words=350
):

    chunks = []

    current_chunk = []
    current_word_count = 0

    for para in paragraphs:

        para_word_count = len(para.split())

        # ---------------------------------------------
        # Start new chunk if current chunk large enough
        # ---------------------------------------------

        if (
            current_word_count + para_word_count > max_words
            and current_word_count >= min_words
        ):

            chunks.append(
                " ".join(current_chunk)
            )

            current_chunk = [para]
            current_word_count = para_word_count

        else:

            current_chunk.append(para)
            current_word_count += para_word_count

    # ---------------------------------------------
    # Save final chunk
    # ---------------------------------------------

    if current_chunk:

        chunks.append(
            " ".join(current_chunk)
        )

    return chunks


# =========================================================
# MAIN LOOP
# =========================================================

for region in REGIONS:

    print("\n" + "=" * 60)
    print(f"PROCESSING REGION: {region}")
    print("=" * 60)

    # -----------------------------------------------------
    # INPUT whisper_raw folder
    # -----------------------------------------------------

    input_dir = os.path.join(
        INPUT_ROOT,
        region,
        "whisper_raw"
    )

    # Skip if missing
    if not os.path.exists(input_dir):

        print(f"Missing: {input_dir}")
        continue

    # -----------------------------------------------------
    # GET TXT FILES
    # -----------------------------------------------------

    txt_files = sorted([
        f for f in os.listdir(input_dir)
        if f.endswith(".txt")
    ])

    print(f"Found {len(txt_files)} files")

    # -----------------------------------------------------
    # PROCESS EACH FILE
    # -----------------------------------------------------

    for filename in txt_files:

        filepath = os.path.join(
            input_dir,
            filename
        )

        # -------------------------------------------------
        # LOAD TRANSCRIPT
        # -------------------------------------------------

        with open(filepath, "r", encoding="utf-8") as f:

            raw_text = f.read().strip()

        # -------------------------------------------------
        # REMOVE UTTERANCE ID
        # -------------------------------------------------

        raw_text = remove_utterance_id(raw_text)

        # -------------------------------------------------
        # SPLIT INTO PARAGRAPHS
        # -------------------------------------------------

        paragraphs = split_into_paragraphs(raw_text)

        # -------------------------------------------------
        # CREATE CHUNKS
        # -------------------------------------------------

        chunks = chunk_paragraphs(
            paragraphs,
            max_words=MAX_WORDS,
            min_words=MIN_WORDS
        )

        # -------------------------------------------------
        # OUTPUT DIRECTORY
        # -------------------------------------------------

        base_name = os.path.splitext(filename)[0]

        transcript_output_dir = os.path.join(
            OUTPUT_ROOT,
            region,
            base_name
        )

        os.makedirs(
            transcript_output_dir,
            exist_ok=True
        )

        # -------------------------------------------------
        # SAVE CHUNKS
        # -------------------------------------------------

        for idx, chunk in enumerate(chunks, start=1):

            chunk_filename = f"{base_name}_chunk{idx:02d}.txt"

            chunk_path = os.path.join(
                transcript_output_dir,
                chunk_filename
            )

            with open(chunk_path, "w", encoding="utf-8") as out_f:

                out_f.write(chunk)

        print(
            f"{filename} -> {len(chunks)} chunks"
        )

# =========================================================
# FINISHED
# =========================================================

print("\nALL REGIONS FINISHED.")
