
from pathlib import Path
import json
import pandas as pd
from tokenizers import Tokenizer

BASE_DIR = Path(__file__).resolve().parent

TRAIN_FILE = BASE_DIR / "splits" / "train.csv"
VAL_FILE = BASE_DIR / "splits" / "validation.csv"
TEST_FILE = BASE_DIR / "splits" / "test.csv"

TOKENIZER_FILE = (
    BASE_DIR / "tokenized" / "farmwise_bpe_tokenizer.json"
)


def main():
    tokenizer = Tokenizer.from_file(str(TOKENIZER_FILE))

    files = {
        "train": TRAIN_FILE,
        "validation": VAL_FILE,
        "test": TEST_FILE,
    }

    results = {}

    for split, path in files.items():
        df = pd.read_csv(path).fillna("")
        lengths = []

        for _, row in df.iterrows():
            text = (
                f"Question: {str(row['question']).strip()}\n"
                f"Answer: {str(row['answer']).strip()}"
            )

            if text.strip():
                lengths.append(
                    len(tokenizer.encode(text).ids)
                )

        series = pd.Series(lengths)

        results[split] = {
            "examples": len(lengths),
            "total_tokens": int(series.sum()),
            "mean_tokens": round(series.mean(), 2),
            "median_tokens": int(series.median()),
            "p90_tokens": int(series.quantile(0.90)),
            "p95_tokens": int(series.quantile(0.95)),
            "p99_tokens": int(series.quantile(0.99)),
            "maximum_tokens": int(series.max()),
        }

        print(f"\n{split.upper()}")
        print("-" * 30)

        for key, value in results[split].items():
            print(f"{key}: {value}")

    output = BASE_DIR / "metadata" / "token_length_report.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8"
    )

    print("\nReport saved to:", output)


if __name__ == "__main__":
    main()
