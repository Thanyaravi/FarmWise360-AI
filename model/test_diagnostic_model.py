"""
Unit & Integration Test for FarmWise 360 AI Structured Diagnostic Architecture
Validates multi-head forward pass, tensor shapes, knowledge base retrieval,
and parameter constraints.
"""

import torch

from config import ModelConfig
from diagnostic_model import FarmWiseDiagnosticClassifier, CROPS, CONDITIONS, SEVERITIES
from knowledge_base import AgriculturalKnowledgeBase


def test_knowledge_base():
    kb = AgriculturalKnowledgeBase()

    crops = kb.list_supported_crops()
    assert "Tomato" in crops
    assert "Wheat" in crops

    # Test exact advisory retrieval
    advisory = kb.get_advisory("Tomato", "Early Blight")
    assert advisory is not None
    assert "Mancozeb" in advisory.treatment_chemical
    assert "Trichoderma" in advisory.treatment_organic

    # Test symptom search
    matches = kb.search_by_symptoms("yellow leaves brown target rings")
    assert len(matches) > 0
    assert matches[0].crop == "Tomato"

    print("Knowledge Base Tests: PASSED")


def test_diagnostic_classifier():
    torch.manual_seed(42)

    config = ModelConfig()
    model = FarmWiseDiagnosticClassifier(config)

    # Two sample sequences of 16 tokens each
    input_ids = torch.randint(0, config.vocab_size, (2, 16))

    outputs = model(input_ids)

    # Shape validation
    assert outputs["crop_logits"].shape == (2, len(CROPS))
    assert outputs["condition_logits"].shape == (2, len(CONDITIONS))
    assert outputs["severity_logits"].shape == (2, len(SEVERITIES))

    # Parameter count validation (must stay under 1M for lightweight edge deployment)
    parameter_count = sum(p.numel() for p in model.parameters())
    assert parameter_count < 1_000_000, f"Parameter count {parameter_count} exceeds 1M threshold"

    # End-to-end diagnosis test
    single_input = input_ids[:1]
    diagnosis_result = model.diagnose(single_input, symptom_text="dark spots on leaves with yellow halo")

    assert "diagnosis" in diagnosis_result
    assert "verified_advisory" in diagnosis_result
    assert diagnosis_result["verified_advisory"]["zero_hallucination_guarantee"] is True

    print("FarmWise Structured Diagnostic Model: TEST")
    print(f"Total Parameters: {parameter_count:,} (Sub-1M Verified)")
    print(f"Crop Logits Shape: {tuple(outputs['crop_logits'].shape)}")
    print(f"Condition Logits Shape: {tuple(outputs['condition_logits'].shape)}")
    print(f"Severity Logits Shape: {tuple(outputs['severity_logits'].shape)}")
    print(f"Sample Diagnosis Output:")
    print(f"  - Predicted Crop: {diagnosis_result['diagnosis']['crop']} (Conf: {diagnosis_result['diagnosis']['crop_confidence']})")
    print(f"  - Predicted Condition: {diagnosis_result['diagnosis']['condition']} (Conf: {diagnosis_result['diagnosis']['condition_confidence']})")
    print(f"  - Severity: {diagnosis_result['diagnosis']['severity']}")
    print(f"  - Chemical Control: {diagnosis_result['verified_advisory']['treatment_chemical'][:60]}...")
    print(f"  - Organic Control: {diagnosis_result['verified_advisory']['treatment_organic'][:60]}...")
    print("Forward-pass & Advisory Pipeline: PASSED")


def main():
    print("========================================")
    print("Testing FarmWise 360 AI Architecture V2")
    print("========================================")
    test_knowledge_base()
    test_diagnostic_classifier()
    print("========================================")
    print("All Architectural Tests PASSED!")
    print("========================================")


if __name__ == "__main__":
    main()
