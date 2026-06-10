from pathlib import Path

# =========================================================
# INPUT / OUTPUT
# =========================================================

INPUT_DIR = Path(
    ""
)

OUTPUT_DIR = Path(
    ""
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =========================================================
# FIND TRANSCRIPT FOLDERS
# =========================================================

transcript_dirs = sorted([
    d for d in INPUT_DIR.iterdir()
    if d.is_dir()
    and d.name != "merged_outputs"
])

print(f"Found {len(transcript_dirs)} transcript folders")

# =========================================================
# MAIN LOOP
# =========================================================

for transcript_dir in transcript_dirs:

    transcript_id = transcript_dir.name

    print(f"\nProcessing: {transcript_id}")

    chunk_files = sorted(
        transcript_dir.glob("*.txt")
    )

    merged_chunks = []

    # -----------------------------------------------------
    # READ CHUNKS
    # -----------------------------------------------------

    for chunk_file in chunk_files:

        with open(
            chunk_file,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read().strip()

            # remove accidental newlines
            text = " ".join(text.split())

            merged_chunks.append(text)

    # -----------------------------------------------------
    # MERGE
    # -----------------------------------------------------

    final_text = " ".join(merged_chunks)

    # remove duplicated spaces
    final_text = " ".join(final_text.split())

    # -----------------------------------------------------
    # ADD UTTERANCE ID
    # -----------------------------------------------------

    final_output = f"{transcript_id} {final_text}"

    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    output_path = OUTPUT_DIR / f"{transcript_id}.txt"

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(final_output + "\n")

    print(f"Saved: {output_path}")

# =========================================================
# FINISHED
# =========================================================

print("\nALL DONE")