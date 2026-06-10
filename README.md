# Master Thesis: ASR Error Correction Using Large Language Models under the 1-best Hypothesis Setting

This repository contains the code, prompts, and metadata used in the master's thesis:
## Overview

This study investigates the effectiveness of LLMs for ASR post-correction under the 1-best hypothesis setting.

Experiments were conducted on:

- LibriSpeech test-clean
- LibriSpeech test-other
- Earnings-22

The ASR system used in this study is Whisper-small, and GPT-4o mini is employed as the post-correction model.

Evaluation metrics include:

- Word Error Rate (WER)
- Substitution / Deletion / Insertion (SDI) statistics
- Named Entity Error Rate (NEER)
- Semantic Similarity

## Experiments

Three experimental settings were used in this study.

### 1. ASR and LLM Post-Correction Across Different Speech Conditions

This experiment was conducted on:

- LibriSpeech test-clean
- LibriSpeech test-other
- the full Earnings-22 dataset

Dataset sources:

**LibriSpeech**
https://www.openslr.org/12

**Earnings-22**
https://github.com/revdotcom/speech-datasets/tree/main/earnings22

---

### 2. Prompting Strategy Experiments

The prompting strategy experiments were conducted on the official Earnings-22 subset-10 split provided by the Earnings-22 benchmark.

Dataset source:

**Earnings-22**
https://github.com/revdotcom/speech-datasets/tree/main/earnings22

---

### 3. Accent-Region Experiments

The accent-region experiments were conducted on the full Earnings-22 dataset.

Speaker samples were grouped into seven regional accent categories following the Earnings-22 benchmark:

- African
- Asian
- English
- Germanic
- Other Romance
- Slavic
- Spanish/Portuguese

The regional grouping process is documented in:

```text
metadata/Earnings22/
├── region_metadata.csv
├── region_categorization.py
└── region_sample_ids.txt
```


---
## Research Objectives

This repository supports the experiments presented in the master's thesis on LLM-based ASR post-correction.

The study investigates:

1. Whether LLM can improve ASR outputs under the 1-best hypothesis setting, particularly in realistic and domain-diverse scenarios.
2. How post-correction performance varies across different speech conditions.
3. How different prompting strategies affect correction performance.
4. Whether post-correction effectiveness varies across regional accent groups in Earnings-22.
---
## Repository Structure

```text
metadata/
├── Earnings22/
│   ├── data_information.txt
│   ├── region_categorization.py
│   ├── region_metadata.csv
│   └── region_sample_ids.txt
│
└── Librispeech/
    └── data_information.txt

prompts/
├── prompt_a.txt
├── prompt_b.txt
└── prompt_c.txt

scripts/
├── whisper.py                # Whisper-small transcription
├── chunking.py               # Transcript chunking for GPT-4o mini
├── normalization.py          # Whisper text normalization
├── llm_pa.py                 # Prompt A (unconstrained)
├── llm_pb.py                 # Prompt B (constrained zero-shot)
├── llm_pc.py                 # Prompt C (constrained few-shot)
├── merge_chunks.py           # Merge corrected chunks
├── extract_ref_entities.py   # Reference entity extraction
├── evaluate_wer_sdi.py       # WER and SDI evaluation
├── evaluate_neer.py          # NEER evaluation
└── evaluate_similarity.py    # Semantic similarity evaluation

requirements.txt
README.md
---
## Data Availability

This repository does not include:

- LibriSpeech audio files
- Earnings-22 audio files
- Whisper outputs
- GPT-4o mini outputs





