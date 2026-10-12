
from pathlib import Path
import json

PROJECT_DIR = Path(__file__).resolve().parent
RAW_DIR = PROJECT_DIR / "raw"
METADATA_DIR = PROJECT_DIR / "metadata"
REPORT_FILE = METADATA_DIR / "inspection_report.json"

MIN_CHARACTERS = 100


def inspect_dataset():
    files = sorted(RAW_DIR.rglob("*.txt"))

    report = {
        "total_files": len(files),
        "usable_candidates": 0,
        "empty_or_short_files": 0,
        "documents": []
    }

    for file_path in files:
        try:
            text = file_path.read_text(encoding="utf-8-sig")
            character_count = len(text.strip())
            usable = character_count >= MIN_CHARACTERS

            report["documents"].append({
                "file": file_path.relative_to(RAW_DIR).as_posix(),
                "characters": character_count,
                "usable_candidate": usable
            })

            if usable:
                report["usable_candidates"] += 1
            else:
                report["empty_or_short_files"] += 1

        except (OSError, UnicodeError) as error:
            report["documents"].append({
                "file": file_path.relative_to(RAW_DIR).as_posix(),
                "error": str(error)
            })

    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("FarmWise 360 Dataset Inspection")
    print("--------------------------------")
    print("Text files found:", report["total_files"])
    print("Usable candidates:", report["usable_candidates"])
    print("Empty or short files:", report["empty_or_short_files"])
    print("Report saved to:", REPORT_FILE)


if __name__ == "__main__":
    inspect_dataset()