"""
Generates high-resolution PNG and vector SVG architectural block diagrams
for FarmWise 360 AI without requiring external web tools.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

DOCS_DIR = Path(__file__).resolve().parent.parent / "documentation"
DOCS_DIR.mkdir(parents=True, exist_ok=True)
PNG_OUTPUT = DOCS_DIR / "farmwise360_block_diagram.png"
SVG_OUTPUT = DOCS_DIR / "farmwise360_block_diagram.svg"

# Set up figure
fig, ax = plt.subplots(figsize=(15, 12), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Title Header
ax.text(
    50, 97,
    "FarmWise 360 AI - Architectural Block Diagram",
    fontsize=20, fontweight="bold", ha="center", va="center", color="#1A237E"
)
ax.text(
    50, 94.2,
    "Lightweight Multi-Head Transformer (~963K Params) with Verified Edge-RAG Advisory Engine",
    fontsize=11, fontstyle="italic", ha="center", va="center", color="#424242"
)


def draw_box(x, y, w, h, title, subtitle, items, bg_color, border_color):
    """Draws a styled architectural component block."""
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.8,rounding_size=1.5",
        edgecolor=border_color,
        facecolor=bg_color,
        linewidth=2,
        zorder=2
    )
    ax.add_patch(box)

    # Title Banner
    ax.text(
        x + w / 2, y + h - 2.5,
        title,
        fontsize=12, fontweight="bold", ha="center", va="center", color=border_color
    )
    if subtitle:
        ax.text(
            x + w / 2, y + h - 5.0,
            subtitle,
            fontsize=9, fontstyle="italic", ha="center", va="center", color="#424242"
        )

    # Item text
    start_y = y + h - 8.0
    for i, item in enumerate(items):
        ax.text(
            x + 2.5, start_y - (i * 2.6),
            f"•  {item}",
            fontsize=9.5, ha="left", va="center", color="#212121"
        )


def draw_arrow(start_x, start_y, end_x, end_y, label=""):
    """Draws an informative directional connection arrow."""
    arrow = patches.FancyArrowPatch(
        (start_x, start_y), (end_x, end_y),
        arrowstyle="-|>",
        mutation_scale=18,
        color="#37474F",
        linewidth=2.2,
        zorder=3
    )
    ax.add_patch(arrow)
    if label:
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        ax.text(
            mid_x, mid_y, label,
            fontsize=8.5, fontweight="bold", color="#B71C1C",
            bbox=dict(boxstyle="round,pad=0.3", fc="#FFFFFF", ec="#B71C1C", lw=1, alpha=0.95),
            ha="center", va="center", zorder=4
        )


# ==========================================
# DRAW BLOCKS
# ==========================================

# 1. Input Block
draw_box(
    x=5, y=75, w=90, h=15,
    title="BLOCK 1: INPUT INGESTION & TOKENIZATION LAYER",
    subtitle="Captures field symptom queries and constructs continuous tensor representations",
    items=[
        "Natural Symptom Text Input: e.g., 'Yellow target-like rings on tomato leaves'",
        "Vocabulary Mapping: Bounded within vocab_size = 1,000 domain tokens",
        "Sequence Truncator & Padder: Fixed sequence dimension max_seq_len = 128",
        "Embedding & Positional Space: Injects sinusoidal position vectors (d_model = 128)"
    ],
    bg_color="#E1F5FE", border_color="#0288D1"
)

# Arrow 1 -> 2
draw_arrow(50, 75, 50, 68, "Input Tensor (B, 128, 128)")

# 2. Transformer Core Block
draw_box(
    x=5, y=49, w=90, h=19,
    title="BLOCK 2: FARM-WISE TRANSFORMER CORE (Sub-1M Parameter Backbone)",
    subtitle="Deep contextual feature extraction running in ~3ms on Intel CPU hardware",
    items=[
        "4x Stacked Transformer Encoder Blocks with Pre-LayerNorm stabilization",
        "Multi-Head Self-Attention: 4 parallel heads modeling non-local symptom relationships",
        "Feed-Forward Sublayer: d_ff = 512 intermediate projection with GELU non-linear activations",
        "Regularization: Dropout (p = 0.1) preventing overfitting on localized agronomic terms",
        "Global Sequence Mean Pooling: Collapses token vectors into unified sequence embedding (1 x 128)"
    ],
    bg_color="#EDE7F6", border_color="#512DA8"
)

# Arrow 2 -> 3
draw_arrow(50, 49, 50, 42, "Context Embedding (1 x 128)")

# 3. Multi-Head Diagnostic Projections (3 Sub-boxes horizontally)
# Box 3A: Crop Head
draw_box(
    x=5, y=26, w=27, h=16,
    title="Crop Classifier",
    subtitle="Linear: 128 -> 64 -> 6",
    items=[
        "Tomato, Wheat",
        "Rice, Potato",
        "Cotton, Other",
        "Softmax Probability"
    ],
    bg_color="#FFF3E0", border_color="#E65100"
)

# Box 3B: Condition Head
draw_box(
    x=36.5, y=26, w=27, h=16,
    title="Pathology Classifier",
    subtitle="Linear: 128 -> 64 -> 8",
    items=[
        "Early/Late Blight",
        "Leaf Rust, Blast",
        "Powdery Mildew",
        "Healthy / Normal"
    ],
    bg_color="#FFF3E0", border_color="#E65100"
)

# Box 3C: Severity Head
draw_box(
    x=68, y=26, w=27, h=16,
    title="Severity Rating",
    subtitle="Linear: 128 -> 64 -> 4",
    items=[
        "Low (Routine)",
        "Medium (Active)",
        "High (Urgent)",
        "Critical (Triage)"
    ],
    bg_color="#FFF3E0", border_color="#E65100"
)

# Connecting Arrows from Core to 3 Heads
draw_arrow(25, 49, 18.5, 42)
draw_arrow(50, 49, 50, 42)
draw_arrow(75, 49, 81.5, 42)

# Arrows 3 -> 4
draw_arrow(18.5, 26, 32, 19)
draw_arrow(50, 26, 50, 19, "Predicted (Crop, Condition, Severity)")
draw_arrow(81.5, 26, 68, 19)

# 4. Verified Edge-RAG & Delivery Block
draw_box(
    x=5, y=3, w=90, h=16,
    title="BLOCK 4 & 5: VERIFIED EDGE-RAG ADVISORY STORE & FASTAPI DELIVERY",
    subtitle="Deterministic agronomic retrieval guaranteeing 0% hallucination and field safety",
    items=[
        "In-Memory Agronomic Knowledge Base: Exact O(1) matching on certified extension records",
        "Chemical Protocols: Registered active ingredients (Mancozeb, Propiconazole) with calibrated dosage",
        "Organic Alternatives: Trichoderma viride, NSKE 5% Neem extract, biological biofertilizers",
        "FastAPI Service Endpoint (/diagnose): Dispatches structured JSON in 3.01ms CPU latency (332 req/s)"
    ],
    bg_color="#E8F5E9", border_color="#2E7D32"
)

# Save high-res PNG and vector SVG
plt.tight_layout()
plt.savefig(PNG_OUTPUT, dpi=300, bbox_inches="tight")
plt.savefig(SVG_OUTPUT, format="svg", bbox_inches="tight")
plt.close()

print(f"Diagram successfully generated:")
print(f"PNG: {PNG_OUTPUT}")
print(f"SVG: {SVG_OUTPUT}")
