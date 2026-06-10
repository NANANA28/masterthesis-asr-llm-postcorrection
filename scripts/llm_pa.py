from openai import OpenAI
from pathlib import Path
import time


client = OpenAI()


INPUT_DIR = Path("")


OUTPUT_DIR = Path("")


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


PROMPT_TEMPLATE = """
Correct the following ASR transcript.

Output only the corrected transcript text.

Transcript:
{chunk_text}
"""

for transcript_dir in INPUT_DIR.iterdir():

    if not transcript_dir.is_dir():
        continue

    transcript_id = transcript_dir.name

    print(f"\nProcessing transcript: {transcript_id}")


    output_subdir = OUTPUT_DIR / transcript_id
    output_subdir.mkdir(parents=True, exist_ok=True)

    
    chunk_files = sorted(transcript_dir.glob("*.txt"))

    for chunk_file in chunk_files:

        output_file = output_subdir / chunk_file.name

       
        if output_file.exists():
            print(f"Skipping existing: {chunk_file.name}")
            continue

        print(f"Correcting: {chunk_file.name}")

        
        with open(chunk_file, "r", encoding="utf-8") as f:
            chunk_text = f.read()

        
        prompt = PROMPT_TEMPLATE.format(chunk_text=chunk_text)

        try:
            # 调用 GPT-4o-mini
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            corrected_text = response.choices[0].message.content.strip()

            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(corrected_text)

            print(f"Saved: {output_file}")

            
            time.sleep(1)

        except Exception as e:
            print(f"Error processing {chunk_file.name}: {e}")

print("\nAll done.")

