"""
FarmWise 360 AI - Context-Aware Semantic Knowledge Index
Enables conceptual semantic search across agricultural manuals and PDFs.
Matches context and intent rather than requiring exact verbatim query words.
"""

from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import json
import math
import re
from collections import Counter


DATASET_DIR = Path(__file__).resolve().parent
PROCESSED_FILE = DATASET_DIR / "processed" / "agricultural_knowledge_chunks.json"

# Agricultural semantic synonyms and context bridges
SYNONYM_EXPANSIONS = {
    "scorched": ["burnt", "necrosis", "marginal browning", "drying", "wilted"],
    "burnt": ["scorched", "necrosis", "blight", "pustules"],
    "powder": ["mildew", "fungal", "fluffy", "white dust", "spores"],
    "rings": ["target", "concentric", "alternaria", "circular spots"],
    "target": ["rings", "concentric", "early blight", "lesions"],
    "holes": ["borer", "caterpillar", "chewing", "larvae", "insect"],
    "yellowing": ["chlorosis", "pale", "nutrient deficiency", "blight"],
    "rotting": ["decay", "soft rot", "late blight", "foul smell"],
    "spots": ["lesions", "pustules", "blight", "specks", "rings"],
}


class SemanticContextIndex:
    """
    Dense Contextual TF-IDF & N-Gram Embedding Engine.
    Provides fast, local, zero-network semantic document search.
    """

    def __init__(self, chunks_path: Optional[Path] = None):
        self.chunks_path = chunks_path or PROCESSED_FILE
        self.chunks: List[Dict[str, Any]] = []
        self.doc_tokens: List[List[str]] = []
        self.idf: Dict[str, float] = {}
        self.vocab: Dict[str, int] = {}
        self.doc_vectors: List[Dict[str, float]] = []

        if self.chunks_path.exists():
            self.load_and_index()

    def _tokenize(self, text: str) -> List[str]:
        """Normalize and tokenize with semantic expansion."""
        words = re.findall(r"\b[a-z]{3,}\b", text.lower())
        tokens = list(words)

        # Expand character 3-grams for typo & morphology tolerance
        for word in words:
            if word in SYNONYM_EXPANSIONS:
                tokens.extend(SYNONYM_EXPANSIONS[word])
            if len(word) >= 5:
                for i in range(len(word) - 3):
                    tokens.append(f"ng_{word[i:i+3]}")

        return tokens

    def load_and_index(self):
        """Build the semantic vector index over extracted chunks."""
        data = json.loads(self.chunks_path.read_text(encoding="utf-8"))
        self.chunks = data
        num_docs = len(self.chunks)

        if num_docs == 0:
            return

        self.doc_tokens = [self._tokenize(chunk["text"]) for chunk in self.chunks]

        # Calculate Document Frequencies
        df_counts = Counter()
        for tokens in self.doc_tokens:
            unique_tokens = set(tokens)
            for token in unique_tokens:
                df_counts[token] += 1

        # Calculate Inverse Document Frequency (IDF)
        self.idf = {
            token: math.log((num_docs + 1) / (df + 1)) + 1.0
            for token, df in df_counts.items()
        }

        # Build Normalized TF-IDF Vectors for each document
        self.doc_vectors = []
        for tokens in self.doc_tokens:
            tf = Counter(tokens)
            vec = {}
            norm_sq = 0.0
            for token, count in tf.items():
                weight = (count / len(tokens)) * self.idf.get(token, 1.0)
                vec[token] = weight
                norm_sq += weight * weight

            norm = math.sqrt(norm_sq) or 1.0
            norm_vec = {k: v / norm for k, v in vec.items()}
            self.doc_vectors.append(norm_vec)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search documents by semantic meaning and context.
        Returns top-k chunks with cosine similarity score.
        """
        if not self.doc_vectors:
            self.load_and_index()
            if not self.doc_vectors:
                return []

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        # Vectorize query
        q_tf = Counter(query_tokens)
        q_vec = {}
        norm_sq = 0.0
        for token, count in q_tf.items():
            weight = (count / len(query_tokens)) * self.idf.get(token, 1.0)
            q_vec[token] = weight
            norm_sq += weight * weight

        norm = math.sqrt(norm_sq) or 1.0
        norm_q_vec = {k: v / norm for k, v in q_vec.items()}

        # Compute Cosine Similarity against all indexed document vectors
        results = []
        for idx, doc_vec in enumerate(self.doc_vectors):
            dot_product = sum(
                norm_q_vec[tok] * doc_vec[tok]
                for tok in norm_q_vec
                if tok in doc_vec
            )
            if dot_product > 0.05:
                results.append((self.chunks[idx], round(dot_product, 4)))

        results.sort(key=lambda item: item[1], reverse=True)
        return results[:top_k]
