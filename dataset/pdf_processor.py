"""
FarmWise 360 AI - Agricultural PDF and Text Manual Ingestion Processor
Parses extension bulletins, university manuals, and agronomic handbooks,
extracting semantically coherent chunks with document and page attribution.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import re

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


DATASET_DIR = Path(__file__).resolve().parent
RAW_DIR = DATASET_DIR / "raw"
PROCESSED_DIR = DATASET_DIR / "processed"
OUTPUT_CHUNKS_FILE = PROCESSED_DIR / "agricultural_knowledge_chunks.json"


def clean_text(text: str) -> str:
    """Normalize whitespace and strip unprintable characters."""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x20-\x7E\n]", " ", text)
    return text.strip()


def extract_from_txt(file_path: Path) -> List[Dict[str, Any]]:
    """Extract semantic paragraphs and sections from text files."""
    try:
        content = file_path.read_text(encoding="utf-8-sig")
    except Exception:
        content = file_path.read_text(encoding="latin-1", errors="ignore")

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", content) if len(p.strip()) >= 80]
    chunks = []

    for idx, para in enumerate(paragraphs, start=1):
        chunks.append({
            "source_file": file_path.name,
            "file_type": "text",
            "page_or_section": f"Section {idx}",
            "text": clean_text(para),
            "character_count": len(para),
        })

    return chunks


def extract_from_pdf(file_path: Path) -> List[Dict[str, Any]]:
    """Extract page-level text and semantic chunks from PDF documents."""
    if not PYPDF_AVAILABLE:
        print(f"[Warning] pypdf not available to process {file_path.name}")
        return []

    chunks = []
    try:
        reader = PdfReader(str(file_path))
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            cleaned = clean_text(page_text)

            if len(cleaned) < 50:
                continue

            # Split dense page text into paragraph-level chunks if long
            sub_chunks = [p.strip() for p in re.split(r"\n\s*\n+", page_text) if len(p.strip()) >= 80]
            if not sub_chunks:
                sub_chunks = [cleaned]

            for s_idx, chunk_text in enumerate(sub_chunks, start=1):
                chunks.append({
                    "source_file": file_path.name,
                    "file_type": "pdf",
                    "page_or_section": f"Page {page_num}",
                    "text": clean_text(chunk_text),
                    "character_count": len(chunk_text),
                })
    except Exception as e:
        print(f"[Error] Failed to read PDF {file_path.name}: {e}")

    return chunks


def process_all_documents(input_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Process all PDF and TXT files in the raw dataset directory."""
    target_dir = input_dir or RAW_DIR
    all_chunks = []

    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
        return []

    # Process all text files
    txt_files = list(target_dir.rglob("*.txt"))
    for tf in txt_files:
        chunks = extract_from_txt(tf)
        all_chunks.extend(chunks)

    # Process all PDF files
    pdf_files = list(target_dir.rglob("*.pdf"))
    for pf in pdf_files:
        chunks = extract_from_pdf(pf)
        all_chunks.extend(chunks)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_CHUNKS_FILE.write_text(
        json.dumps(all_chunks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("=" * 60)
    print("FarmWise 360 AI - Document Ingestion Report")
    print("=" * 60)
    print(f"Target Directory: {target_dir}")
    print(f"Text Files Processed: {len(txt_files)}")
    print(f"PDF Files Processed: {len(pdf_files)}")
    print(f"Total Knowledge Chunks Extracted: {len(all_chunks)}")
    print(f"Output File Saved: {OUTPUT_CHUNKS_FILE}")
    print("=" * 60)

    return all_chunks


if __name__ == "__main__":
    process_all_documents()
