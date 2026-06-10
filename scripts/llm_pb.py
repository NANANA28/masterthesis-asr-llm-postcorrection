import os
from openai import OpenAI

# =========================================================
# CONFIG
# =========================================================



# Input chunk directory
INPUT_ROOT = ""

# Output directory
OUTPUT_ROOT = ""

# Model
MODEL_NAME = "gpt-4o-mini"

# =========================================================
# OPENAI CLIENT
# =========================================================

client = OpenAI()

# =========================================================
# CREATE OUTPUT DIR
# =========================================================

os.makedirs(OUTPUT_ROOT, exist_ok=True)

# =========================================================
# PROMPT TEMPLATE
# =========================================================

PROMPT_TEMPLATE = """
You are a reliable ASR post-correction system.

Your task is to correct ASR transcription errors while preserving the original wording and meaning as much as possible.

Step 1:
First determine whether the transcript contains obvious ASR recognition errors.

- If the transcript is already correct or understandable,
return it unchanged.

- Only modify words that are very likely to be ASR errors.

Step 2:
When making corrections:

- Keep edits minimal and conservative.
- Preserve the original sentence structure.
- Do NOT paraphrase.
- Do NOT summarize.
- Do NOT invent content.


VERY IMPORTANT:
- Output ONLY the corrected transcript.
- The output must contain exactly ONE continuous line.
- Do not insert line breaks.
- Do not use bullet points.
- Do not add explanations or labels.

Transcript:
{chunk_text}
"""

# =========================================================
# PROCESS ALL TRANSCRIPTS
# =========================================================

transcript_dirs = sorted([
    d for d in os.listdir(INPUT_ROOT)
    if os.path.isdir(os.path.join(INPUT_ROOT, d))
])

print(f"Found {len(transcript_dirs)} transcript folders.\n")

# =========================================================
# MAIN LOOP
# =========================================================

for transcript_id in transcript_dirs:

    transcript_input_dir = os.path.join(
        INPUT_ROOT,
        transcript_id
    )

    transcript_output_dir = os.path.join(
        OUTPUT_ROOT,
        transcript_id
    )

    os.makedirs(
        transcript_output_dir,
        exist_ok=True
    )

    # -----------------------------------------------------
    # GET CHUNK FILES
    # -----------------------------------------------------

    chunk_files = sorted([
        f for f in os.listdir(transcript_input_dir)
        if f.endswith(".txt")
    ])

    print(f"\nProcessing {transcript_id}")
    print(f"Chunks: {len(chunk_files)}")

    # -----------------------------------------------------
    # PROCESS EACH CHUNK
    # -----------------------------------------------------

    for chunk_file in chunk_files:

        chunk_path = os.path.join(
            transcript_input_dir,
            chunk_file
        )

        # -------------------------------------------------
        # LOAD CHUNK TEXT
        # -------------------------------------------------

        with open(chunk_path, "r", encoding="utf-8") as f:
            chunk_text = f.read().strip()

        # -------------------------------------------------
        # BUILD PROMPT
        # -------------------------------------------------

        prompt = PROMPT_TEMPLATE.format(
            chunk_text=chunk_text
        )

        # -------------------------------------------------
        # API CALL
        # -------------------------------------------------

        try:

            response = client.chat.completions.create(
                model=MODEL_NAME,
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a careful ASR correction assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            corrected_text = response.choices[0].message.content.strip()

            # -------------------------------------------------
            # CLEAN OUTPUT
            # -------------------------------------------------

            corrected_text = corrected_text.replace("\n", " ")
            corrected_text = " ".join(corrected_text.split())

            # -------------------------------------------------
            # SAVE OUTPUT
            # -------------------------------------------------

            output_path = os.path.join(
                transcript_output_dir,
                chunk_file
            )

            with open(output_path, "w", encoding="utf-8") as out_f:
                out_f.write(corrected_text)

            print(f"Saved: {chunk_file}")

        except Exception as e:

            print(f"ERROR in {chunk_file}")
            print(e)

# =========================================================
# FINISHED
# =========================================================

print("\nALL TRANSCRIPTS FINISHED.")