# FarmWise 360 AI 🌱

A lightweight Generative AI transformer architecture and intelligence system optimized for smart farming and agricultural decision-making.

---

## Overview

FarmWise 360 AI is an end-to-end smart agriculture platform powered by a lightweight custom Generative AI Transformer architecture (~937K parameters) designed for fast, efficient execution on commodity hardware and edge devices without requiring heavy dedicated GPUs.

### Key Highlights
- **Sub-1M Parameter Architecture:** Engineered for minimal memory footprint and fast inference.
- **CPU & Edge Optimized:** Validated and benchmarked on CPU runtimes with PyTorch 2.x.
- **Modular Design:** Clear separation across model architectures, datasets, experiments, backend services, and admin tooling.
- **Reproducible Environments:** Cross-device Conda environment specifications included for seamless team collaboration.

---

## Repository Structure

```text
FarmWise360-AI/
├── admin-panel/        # Management dashboard and monitoring UI
├── backend/            # API services and integration logic
├── dataset/            # Agricultural datasets and data loading pipelines
├── documentation/      # Technical architecture and API documentation
├── environment/        # Conda environment YAML and requirements specifications
├── experiments/        # Model training, fine-tuning, and evaluation notebooks
├── model/              # Core Transformer model implementation
│   ├── config.py       # Model hyperparameter configuration
│   ├── transformer.py  # Custom multi-head attention transformer architecture
│   └── test_model.py   # Forward-pass verification and shape validation
├── requirements.txt    # Top-level Python dependency specification
└── README.md           # Project documentation
```

---

## Model Architecture Specifications

| Hyperparameter | Value | Description |
| :--- | :--- | :--- |
| **Vocabulary Size** | `1,000` | Token vocabulary |
| **Max Sequence Length** | `128` | Maximum sequence window |
| **Embedding Dimension ($d_{model}$)** | `128` | Hidden representation dimension |
| **Attention Heads ($n_{heads}$)** | `4` | Multi-head self-attention heads |
| **Transformer Layers** | `4` | Stacked transformer encoder blocks |
| **Feedforward Dimension ($d_{ff}$)** | `512` | Intermediate MLP projection size |
| **Dropout** | `0.1` | Regularization dropout probability |
| **Total Parameters** | **937,728** | Ultra-lightweight footprint |

---

## Quick Start & Verification

### 1. Environment Setup (Recommended)
Create and activate the matching Conda environment using the exported specification:

```bash
conda env create -f environment/genai-environment.yml
conda activate genai
```

Or install via pip with Python 3.12:

```bash
pip install -r requirements.txt
```

### 2. Run the Verification Test
Execute the forward-pass validation test to verify that the model compiles and runs cleanly:

```bash
python model/test_model.py
```

Expected output:
```text
FarmWise Transformer: TEST
Input shape: (2, 16)
Output shape: (2, 16, 1000)
Parameters: 937,728
All parameters trainable: True
Forward-pass test: PASSED
```

---

## License
MIT License

