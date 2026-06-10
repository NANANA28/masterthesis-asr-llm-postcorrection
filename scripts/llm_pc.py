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
# PROMPT TEMPLATE (FINAL PROMPT C)
# =========================================================

PROMPT_TEMPLATE = """
You are a conservative ASR post-correction system.

Correct only obvious ASR recognition errors.

If the transcript is already correct or understandable,
keep it unchanged.

Keep edits minimal and conservative.

Only modify words that are very likely to be ASR errors.

Do NOT rewrite the transcript into polished written English.

Do NOT paraphrase.

Do NOT summarize.

Do NOT invent content.


Output ONLY the corrected transcript.

Output ONLY the corrected transcript.
The output must contain exactly ONE continuous line.
Do not insert line breaks.
Do not use bullet points.
Do not add explanations or labels.

Keep the same plain transcript style as the corrected examples above.

========================================================
EXAMPLES
========================================================

Example 1

ASR:
In fact, the European from-bosis disposal and the Japanese business disposal you have previously.

Corrected:
In fact the European Thrombosis Disposal and the Japanese Business Disposal here previously

--------------------------------------------------------

Example 2

ASR:
Now those sales were the biggest driver of the growth if you take them out that 29% constant exchange rate, 1.7% constant exchange rate growth.

Corrected:
Now those sales were the biggest driver of the growth If you take them out that 29% constant exchange rate was 7% constant exchange rate growth

--------------------------------------------------------

Example 3

ASR:
However, just for noting as we move forward in the presentation, those sales are low to margin,

Corrected:
However just for noting as we move forward in the presentation those sales are low to no margin

--------------------------------------------------------

Example 4

ASR:
Moving on to the normalized EBIT dial on, this is quite a busy table

Corrected:
Moving onto the normalized EBITDA line this is quite a busy table

--------------------------------------------------------

Example 5

ASR:
the targeted initiatives they've commenced in FY2021 will continue into FY2022.

Corrected:
the targeted initiatives that commenced in FY 2021 will continue into FY 2022

--------------------------------------------------------

Example 6

ASR:
the man that will step into the shoes of Group 2 financial officer, Mr. Sean Cattisario. 

Corrected:
the man that will step into the shoes of Group Chief Financial Officer Mr Sean Capazorio

--------------------------------------------------------

Example 7

ASR:
he was in a company that we acquired in 1999, FA Dragos.

Corrected:
he was in a company that we acquired in 1999 SA Druggists

--------------------------------------------------------

Example 8

ASR:
we've had zero fertility

Corrected:
we've had zero fatalities

========================================================
NOW CORRECT THE FOLLOWING TRANSCRIPT
========================================================

ASR:
{chunk_text}

Corrected:
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
                        "content": "You are a careful and conservative ASR correction assistant."
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