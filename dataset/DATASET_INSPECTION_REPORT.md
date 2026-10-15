# FarmWise 360 AI Dataset Inspection Report

## 1. Purpose

This report describes the dataset inspection utility in `prepare_dataset.py`. The utility performs an initial inventory of plain-text documents so that files with enough text can be identified as candidates for later dataset processing.

It is an inspection step only: it does not clean, transform, classify, or otherwise prepare the document contents for model training.

## 2. Input and output

- **Input directory:** `dataset/raw/`, resolved relative to the script's location.
- **Files inspected:** Files matching `*.txt`, including files in nested subdirectories.
- **Output directory:** `dataset/metadata/`, created automatically if necessary.
- **Output report:** `dataset/metadata/inspection_report.json`.
- **Dependencies:** Python standard library (`pathlib` and `json`); no third-party packages are required.

Each document's path is recorded relative to `dataset/raw/` and uses forward slashes in the JSON report, making nested paths consistent across operating systems.

## 3. Inspection procedure

The utility:

1. Finds and sorts all matching text-file paths.
2. Reads each file as UTF-8, accepting and removing a UTF-8 byte-order mark when present.
3. Strips leading and trailing whitespace before measuring the text.
4. Marks a document as a **usable candidate** when the remaining text contains at least 100 characters.
5. Records a character count and candidate flag for successfully read files.
6. Records a read error for files that raise an operating-system or Unicode decoding error.
7. Writes an indented JSON summary and prints the main counts and report location.

The 100-character cutoff is a simple minimum-length screening rule. Passing it indicates only that a document is long enough to be considered; it does not establish that the content is relevant, accurate, non-duplicated, or suitable for training.

## 4. Report structure

The JSON report contains:

- `total_files`: Number of matching `.txt` paths discovered.
- `usable_candidates`: Number of successfully read files with at least 100 non-edge-whitespace characters.
- `empty_or_short_files`: Number of successfully read files below the cutoff.
- `documents`: Per-file records. Successful reads include `file`, `characters`, and `usable_candidate`; read failures include `file` and `error`.

Read failures are listed in `documents`, but they are not included in either `usable_candidates` or `empty_or_short_files`. The report does not currently include a separate error count.

## 5. Current dataset status

At the time this report was prepared, the `dataset` directory contained the inspection script and README, but no `dataset/raw/` files were present. Therefore, no real document inventory or candidate counts can be reported here. Run the utility after adding the source `.txt` files to generate those results.

From the repository root:

```powershell
python dataset\prepare_dataset.py
```

The generated summary will be saved to `dataset/metadata/inspection_report.json`.

## 6. Scope and limitations

- Only `.txt` files are inspected; other formats are ignored.
- The script counts Python string characters, not bytes, words, or tokens.
- Internal whitespace and punctuation count toward the 100-character threshold; only leading and trailing whitespace are excluded.
- The threshold does not assess agricultural relevance, language, quality, safety, duplication, or labeling.
- There is no separate summary count for unreadable files, although their paths and error messages are retained in the JSON.
- The script does not split documents, remove duplicates, normalize text, or produce model-ready training data.

## 7. Conclusion

`prepare_dataset.py` provides a lightweight first-pass inventory for text files in the FarmWise 360 AI dataset directory. It is useful for identifying empty or short documents and recording basic read errors before more substantive data validation and preparation. Its candidate flag should be treated as a length-based screening result, not as confirmation that a document is ready for model training.
