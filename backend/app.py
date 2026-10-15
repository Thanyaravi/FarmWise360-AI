"""
FarmWise 360 AI - Edge Inference Backend API
Serves structured agricultural diagnostic predictions and verified treatment advisories.
"""

from typing import List, Optional
import sys
from pathlib import Path
import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Standard package imports resolved by VS Code and Python
from model.config import ModelConfig
from model.diagnostic_model import FarmWiseDiagnosticClassifier
from model.knowledge_base import AgriculturalKnowledgeBase


app = FastAPI(
    title="FarmWise 360 AI - Edge Diagnostic Engine",
    description="Zero-hallucination lightweight agricultural diagnostic & advisory API.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model and knowledge base state
config = ModelConfig()
knowledge_base = AgriculturalKnowledgeBase()
model = FarmWiseDiagnosticClassifier(config, knowledge_base=knowledge_base)
model.eval()


class DiagnosisRequest(BaseModel):
    symptoms: str = Field(..., description="Description of crop symptoms (e.g., 'brown target spots on lower tomato leaves')")
    input_ids: Optional[List[int]] = Field(None, description="Optional pre-tokenized token IDs (length <= 128)")


class SearchRequest(BaseModel):
    query: str = Field(..., description="Query terms to search verified agronomic advisories")


@app.get("/")
def root():
    return {
        "service": "FarmWise 360 AI Diagnostic API",
        "version": "2.0.0",
        "architecture": "Structured Edge-RAG & Multi-Head Transformer",
        "zero_hallucination": True,
        "docs_url": "/docs",
    }


@app.get("/health")
def health_check():
    param_count = sum(p.numel() for p in model.parameters())
    return {
        "status": "healthy",
        "device": "CPU / Edge",
        "parameters": param_count,
        "sub_1m_compliant": param_count < 1_000_000,
        "supported_crops": len(knowledge_base.list_supported_crops()),
    }


@app.get("/crops")
def list_supported_crops():
    crops = knowledge_base.list_supported_crops()
    data = {}
    for crop in crops:
        data[crop] = knowledge_base.list_supported_conditions(crop)
    return {"crops": data}


@app.post("/diagnose")
def diagnose_crop_issue(request: DiagnosisRequest):
    if not request.symptoms.strip():
        raise HTTPException(status_code=400, detail="Symptoms description cannot be empty.")

    # If input token IDs are supplied, validate length; otherwise generate simple hash-based tokens
    if request.input_ids:
        token_ids = request.input_ids[:config.max_seq_len]
    else:
        # Simple deterministic tokenization for edge testing
        tokens = [abs(hash(word)) % config.vocab_size for word in request.symptoms.split()]
        token_ids = tokens[:config.max_seq_len] or [0]

    input_tensor = torch.tensor([token_ids], dtype=torch.long)

    try:
        result = model.diagnose(input_tensor, symptom_text=request.symptoms)
        result["input_symptoms"] = request.symptoms
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnostic error: {str(e)}")


@app.post("/advisory/search")
def search_advisory(request: SearchRequest):
    matches = knowledge_base.search_by_symptoms(request.query)
    results = []
    for match in matches:
        results.append({
            "crop": match.crop,
            "condition": match.condition,
            "severity": match.severity,
            "chemical_treatment": match.treatment_chemical,
            "organic_treatment": match.treatment_organic,
            "prevention": match.prevention,
        })
    return {"query": request.query, "matches_found": len(results), "advisories": results}


if __name__ == "__main__":
    print("=" * 60)
    print("Starting FarmWise 360 AI Diagnostic API Server")
    print("Access API Docs at: http://127.0.0.1:8000/docs")
    print("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=8000)

