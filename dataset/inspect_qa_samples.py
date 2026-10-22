
from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).resolve().parent / "raw"

datasets = [
    {
        "filename": "agriculture_qa_cleaned.csv",
        "question": "question",
        "answer": "answer",
    },
    {
        "filename": "agriculture_crop_disease_cleaned.csv",
        "question": "Question",
        "answer": "Answer",
    },
]

for item in datasets:
    matches = list(RAW_DIR.rglob(item["filename"]))

    if not matches:
        print(f"\nFile not found: {item['filename']}")
        continue

    df = pd.read_csv(matches[0])
    question_col = item["question"]
    answer_col = item["answer"]

    df[question_col] = df[question_col].fillna("").astype(str).str.strip()
    df[answer_col] = df[answer_col].fillna("").astype(str).str.strip()

    q_lengths = df[question_col].str.split().str.len()
    a_lengths = df[answer_col].str.split().str.len()

    print("\n" + "=" * 60)
    print(item["filename"])
    print("=" * 60)
    print("Records:", len(df))
    print("\nQuestion word counts:")
    print(q_lengths.describe())
    print("\nAnswer word counts:")
    print(a_lengths.describe())

    for index, row in df.head(3).iterrows():
        print(f"\nSample {index + 1}")
        print("Question:", row[question_col][:500])
        print("Answer:", row[answer_col][:800])
