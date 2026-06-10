import whisper
from pathlib import Path

model = whisper.load_model("small")
# Set dataset path and output file before running
input_dir = ""
output_file = ""

with open(output_file, "w") as fout:
    for flac in Path(input_dir).rglob("*.flac"):
        utt_id = flac.stem

        result = model.transcribe(
            str(flac),
            language="en",
            fp16=True
        )

        text = result["text"].strip()

        fout.write(f"{utt_id} {text}\n")
        fout.flush()

print("Done.")
