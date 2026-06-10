import pandas as pd
import os
import shutil

# =========================================
# PATHS
# =========================================
# Set input/output paths before running
METADATA_PATH = "region_metadata.csv"

RAW_DIR = ""

OUTPUT_DIR = ""

# =========================================
# LOAD METADATA
# =========================================

df = pd.read_csv(METADATA_PATH)

fileid_to_region = dict(
    zip(df["File ID"].astype(str), df["Region"])
)

regions = sorted(df["Region"].dropna().unique())

# =========================================
# CREATE whisper_raw DIRS
# =========================================

for region in regions:

    os.makedirs(
        os.path.join(OUTPUT_DIR, region, "whisper_raw"),
        exist_ok=True
    )

# =========================================
# COPY RAW FILES
# =========================================

raw_files = os.listdir(RAW_DIR)

for filename in raw_files:

    if not filename.endswith(".txt"):
        continue

    file_id = filename[:-4]

    region = fileid_to_region.get(file_id)

    if region:

        src_path = os.path.join(RAW_DIR, filename)

        dst_path = os.path.join(
            OUTPUT_DIR,
            region,
            "whisper_raw",
            filename
        )

        shutil.copy(src_path, dst_path)

    else:
        print(f"[RAW] region not found: {file_id}")

print("\nWhisper raw transcripts have been categorized by region")
