"""
Generates vibrant, colorful PNG and vector SVG architectural block diagrams
with distinct color coding for each subsystem on a clean white background.
"""

import base64
import json
import urllib.request
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

DOCS_DIR = Path(r"d:\Internship\TIMES POINT\Farmwise360-AI\documentation")
DOWNLOADS_DIR = Path(r"D:\Downloads")
DOCS_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. Fetch Official Colorful Mermaid Diagram from Engine
# -------------------------------------------------------------
mermaid_code = """flowchart TD
    subgraph B1 ["🔷 BLOCK 1: INPUT & TOKENIZATION LAYER"]
        A["User Query / Field Symptoms<br>('Yellow target spots on tomato leaves')"] --> B["Tokenizer & Sequence Truncator<br>(max_seq_len = 128, vocab = 1000)"]
        B --> C["Embedding & Positional Encoding<br>(d_model = 128)"]
    end

    subgraph B2 ["🟣 BLOCK 2: LIGHTWEIGHT TRANSFORMER CORE (~937K Params)"]
        C --> D["Transformer Block 1<br>(4 Attention Heads + GELU MLP)"]
        D --> E["Transformer Block 2<br>(Pre-LayerNorm + Dropout 0.1)"]
        E --> F["Transformer Block 3<br>(Feedforward d_ff = 512)"]
        F --> G["Transformer Block 4<br>(Final LayerNorm)"]
        G --> H["Global Sequence Mean Pooling<br>(Vector representation: 1 x 128)"]
    end

    subgraph B3 ["🟠 BLOCK 3: MULTI-HEAD DIAGNOSTIC PROJECTION"]
        H --> I["Head A: Crop Classifier<br>(Linear: 128 -> 64 -> 6 classes)"]
        H --> J["Head B: Pathology Classifier<br>(Linear: 128 -> 64 -> 8 classes)"]
        H --> K["Head C: Severity Rating<br>(Linear: 128 -> 64 -> 4 classes)"]
        I --> L["Softmax & Confidence Calculator"]
        J --> L
        K --> L
    end

    subgraph B4 ["🟢 BLOCK 4: VERIFIED EDGE-RAG ADVISORY STORE"]
        L -->|Predicted Crop + Condition| M["Agricultural Knowledge Registry<br>(Certified In-Memory Database)"]
        M --> N["Active Chemical Ingredients & Dosages<br>(e.g., Mancozeb 75% WP @ 2.5g/L)"]
        M --> O["Organic & Biological Controls<br>(e.g., Trichoderma viride @ 5g/L)"]
        M --> P["Preventative Cultural Practices<br>(e.g., Crop rotation, Drip irrigation)"]
    end

    subgraph B5 ["🔴 BLOCK 5: API SERVING & DELIVERY"]
        N --> Q["Advisory Synthesis Engine<br>(Zero-Hallucination Guardrail)"]
        O --> Q
        P --> Q
        Q --> R["Structured JSON Advisory<br>(FastAPI /diagnose - 3.01 ms CPU)"]
    end

    %% Colorful Node Styling
    style B1 fill:#E0F2FE,stroke:#0284C7,stroke-width:2px,color:#0369A1
    style A fill:#FFFFFF,stroke:#0284C7,stroke-width:1.5px,color:#0F172A
    style B fill:#FFFFFF,stroke:#0284C7,stroke-width:1.5px,color:#0F172A
    style C fill:#FFFFFF,stroke:#0284C7,stroke-width:1.5px,color:#0F172A

    style B2 fill:#F3E8FF,stroke:#7C3AED,stroke-width:2px,color:#6D28D9
    style D fill:#FFFFFF,stroke:#7C3AED,stroke-width:1.5px,color:#0F172A
    style E fill:#FFFFFF,stroke:#7C3AED,stroke-width:1.5px,color:#0F172A
    style F fill:#FFFFFF,stroke:#7C3AED,stroke-width:1.5px,color:#0F172A
    style G fill:#FFFFFF,stroke:#7C3AED,stroke-width:1.5px,color:#0F172A
    style H fill:#EDE9FE,stroke:#6D28D9,stroke-width:2px,color:#4C1D95

    style B3 fill:#FEF3C7,stroke:#D97706,stroke-width:2px,color:#92400E
    style I fill:#FFFFFF,stroke:#D97706,stroke-width:1.5px,color:#0F172A
    style J fill:#FFFFFF,stroke:#D97706,stroke-width:1.5px,color:#0F172A
    style K fill:#FFFFFF,stroke:#D97706,stroke-width:1.5px,color:#0F172A
    style L fill:#FDE68A,stroke:#B45309,stroke-width:2px,color:#78350F

    style B4 fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#15803D
    style M fill:#FFFFFF,stroke:#16A34A,stroke-width:1.5px,color:#0F172A
    style N fill:#FFFFFF,stroke:#16A34A,stroke-width:1.5px,color:#0F172A
    style O fill:#FFFFFF,stroke:#16A34A,stroke-width:1.5px,color:#0F172A
    style P fill:#FFFFFF,stroke:#16A34A,stroke-width:1.5px,color:#0F172A

    style B5 fill:#FFE4E6,stroke:#E11D48,stroke-width:2px,color:#BE123C
    style Q fill:#FFFFFF,stroke:#E11D48,stroke-width:1.5px,color:#0F172A
    style R fill:#FECDD3,stroke:#BE123C,stroke-width:2px,color:#881337
"""

data = {
    "code": mermaid_code,
    "mermaid": {
        "theme": "default",
        "themeVariables": {
            "background": "#FFFFFF",
            "primaryColor": "#FFFFFF",
            "edgeLabelBackground": "#FFFFFF"
        }
    }
}
json_bytes = json.dumps(data).encode("utf-8")
b64_str = base64.urlsafe_b64encode(json_bytes).decode("ascii")

url_png = f"https://mermaid.ink/img/{b64_str}"
url_svg = f"https://mermaid.ink/svg/{b64_str}"

req_png = urllib.request.Request(url_png, headers={"User-Agent": "Mozilla/5.0"})
req_svg = urllib.request.Request(url_svg, headers={"User-Agent": "Mozilla/5.0"})

try:
    print("Downloading colorful Mermaid diagram (PNG & SVG)...")
    with urllib.request.urlopen(req_png, timeout=20) as resp:
        content = resp.read()
        (DOWNLOADS_DIR / "FarmWise360_Architecture_Colorful.png").write_bytes(content)
        (DOCS_DIR / "FarmWise360_Architecture_Colorful.png").write_bytes(content)
        print("Colorful PNG saved!")

    with urllib.request.urlopen(req_svg, timeout=20) as resp:
        content = resp.read()
        (DOWNLOADS_DIR / "FarmWise360_Architecture_Colorful.svg").write_bytes(content)
        (DOCS_DIR / "FarmWise360_Architecture_Colorful.svg").write_bytes(content)
        print("Colorful SVG saved!")
except Exception as e:
    print("Download note:", e)

# -------------------------------------------------------------
# 2. Also Generate Ultra-Crisp Colorful Matplotlib 300DPI Version
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 18), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
fig.patch.set_facecolor("#FFFFFF")

def draw_colorful_card(x, y, w, h, title, items, bg_color, border_color, title_color):
    card = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.8,rounding_size=1.2",
        edgecolor=border_color, facecolor=bg_color,
        linewidth=2.2, zorder=2
    )
    ax.add_patch(card)
    ax.text(x + w/2, y + h - 1.8, title, fontsize=11, fontweight="bold", ha="center", va="center", color=title_color)
    
    start_y = y + h - 4.2
    for i, item in enumerate(items):
        ax.text(x + 2.5, start_y - (i * 2.2), f"•  {item}", fontsize=9, ha="left", va="center", color="#1E293B")

def draw_flow_arrow(x1, y1, x2, y2, label=""):
    arrow = patches.FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=16,
        color="#475569", linewidth=2.0, zorder=3
    )
    ax.add_patch(arrow)
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2, label, fontsize=8, fontweight="bold", color="#B91C1C",
                bbox=dict(boxstyle="round,pad=0.25", fc="#FFFFFF", ec="#B91C1C", lw=1), ha="center", va="center", zorder=4)

# Block 1 - Blue
draw_colorful_card(10, 83, 80, 13, "BLOCK 1: INPUT & TOKENIZATION LAYER", [
    "User Query / Field Symptoms ('Yellow target spots on tomato leaves')",
    "Tokenizer & Sequence Truncator (max_seq_len = 128, vocab = 1000)",
    "Embedding & Positional Encoding (d_model = 128 continuous space)"
], "#E0F2FE", "#0284C7", "#0369A1")

draw_flow_arrow(50, 83, 50, 78)

# Block 2 - Purple
draw_colorful_card(10, 57, 80, 21, "BLOCK 2: LIGHTWEIGHT TRANSFORMER CORE (~937K Params)", [
    "Transformer Block 1 (4 Attention Heads + GELU MLP)",
    "Transformer Block 2 (Pre-LayerNorm + Dropout 0.1)",
    "Transformer Block 3 (Feedforward d_ff = 512)",
    "Transformer Block 4 (Final LayerNorm)",
    "Global Sequence Mean Pooling (Vector representation: 1 x 128)"
], "#F3E8FF", "#7C3AED", "#6D28D9")

draw_flow_arrow(50, 57, 50, 52)

# Block 3 - Orange (3 parallel heads)
card_w = 25
draw_colorful_card(10, 37, card_w, 15, "Head A: Crop", ["Tomato, Wheat", "Rice, Potato", "Cotton, Other", "Softmax Score"], "#FEF3C7", "#D97706", "#92400E")
draw_colorful_card(37.5, 37, card_w, 15, "Head B: Pathology", ["Early/Late Blight", "Leaf Rust, Blast", "Powdery Mildew", "Healthy Crop"], "#FEF3C7", "#D97706", "#92400E")
draw_colorful_card(65, 37, card_w, 15, "Head C: Severity", ["Low (Routine)", "Medium (Active)", "High (Urgent)", "Critical Alert"], "#FEF3C7", "#D97706", "#92400E")

draw_flow_arrow(22.5, 37, 35, 30)
draw_flow_arrow(50, 37, 50, 30, "Predicted (Crop, Disease, Severity)")
draw_flow_arrow(77.5, 37, 65, 30)

# Block 4 - Green
draw_colorful_card(10, 16, 80, 14, "BLOCK 4: VERIFIED EDGE-RAG ADVISORY STORE", [
    "Agricultural Knowledge Registry (Certified In-Memory Database)",
    "Chemical Control: Active ingredients (Mancozeb 75% WP @ 2.5g/L)",
    "Organic Control: Trichoderma viride @ 5g/L, Neem seed kernel extract (NSKE)",
    "Preventative Guidelines: 3-year crop rotation, drip irrigation practices"
], "#DCFCE7", "#16A34A", "#15803D")

draw_flow_arrow(50, 16, 50, 11)

# Block 5 - Red / Rose
draw_colorful_card(10, 1, 80, 10, "BLOCK 5: API SERVING & DELIVERY", [
    "Advisory Synthesis Engine (Zero-Hallucination Guardrail)",
    "Structured JSON Delivery (FastAPI /diagnose - 3.01 ms CPU execution)"
], "#FFE4E6", "#E11D48", "#BE123C")

plt.tight_layout()
plt.savefig(DOWNLOADS_DIR / "FarmWise360_Architecture_Colorful_CardView.png", dpi=300, bbox_inches="tight")
plt.savefig(DOCS_DIR / "FarmWise360_Architecture_Colorful_CardView.png", dpi=300, bbox_inches="tight")
plt.close()
print("CardView version saved!")

