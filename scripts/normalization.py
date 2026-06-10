
from whisper.normalizers import EnglishTextNormalizer

normalizer = EnglishTextNormalizer()


files = [
    ("INPUT_REF.txt", "OUTPUT_REF_NORM.txt"),
    ("INPUT_HYP.txt", "OUTPUT_HYP_NORM.txt")
]

for input_file, output_file in files:

    output_lines = []

    with open(input_file, "r", encoding="utf8") as f:

        for line in f:
            line = line.strip()

            if not line:
                continue

            parts = line.split(maxsplit=1)

            utt_id = parts[0]
            text = parts[1] if len(parts) > 1 else ""

            norm_text = normalizer(text).strip()

            if norm_text:
                output_lines.append(f"{utt_id} {norm_text}")
            else:
                output_lines.append(f"{utt_id}")

    with open(output_file, "w", encoding="utf8") as f_out:
        f_out.write("\n".join(output_lines) + "\n")

    print(f"Done: {input_file}")

print("All normalization finished.")


