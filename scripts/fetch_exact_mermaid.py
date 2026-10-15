import base64
import json
import urllib.request
from pathlib import Path

DOCS_DIR = Path(r"d:\Internship\TIMES POINT\Farmwise360-AI\documentation")
DOWNLOADS_DIR = Path(r"D:\Downloads")

mermaid_code = """flowchart TD
    subgraph BLOCK1 ["BLOCK 1: INPUT and TOKENIZATION LAYER"]
        A["User Query / Field Symptoms<br>('Yellow target spots on tomato leaves')"] --> B["Tokenizer and Sequence Truncator<br>(max_seq_len = 128, vocab = 1000)"]
        B --> C["Embedding and Positional Encoding<br>(d_model = 128)"]
    end

    subgraph BLOCK2 ["BLOCK 2: LIGHTWEIGHT TRANSFORMER CORE (~937K Params)"]
        C --> D["Transformer Block 1<br>(4 Attention Heads + GELU MLP)"]
        D --> E["Transformer Block 2<br>(Pre-LayerNorm + Dropout 0.1)"]
        E --> F["Transformer Block 3<br>(Feedforward d_ff = 512)"]
        F --> G["Transformer Block 4<br>(Final LayerNorm)"]
        G --> H["Global Sequence Mean Pooling<br>(Vector representation: 1 x 128)"]
    end

    subgraph BLOCK3 ["BLOCK 3: MULTI-HEAD DIAGNOSTIC PROJECTION"]
        H --> I["Head A: Crop Classifier<br>(Linear: 128 -> 64 -> 6 classes)"]
        H --> J["Head B: Pathology Classifier<br>(Linear: 128 -> 64 -> 8 classes)"]
        H --> K["Head C: Severity Rating<br>(Linear: 128 -> 64 -> 4 classes)"]
        I --> L["Softmax and Confidence Calculator"]
        J --> L
        K --> L
    end

    subgraph BLOCK4 ["BLOCK 4: VERIFIED EDGE-RAG ADVISORY STORE"]
        L -->|Predicted Crop + Condition| M["Agricultural Knowledge Registry<br>(Certified In-Memory Database)"]
        M --> N["Active Chemical Ingredients and Dosages<br>(e.g., Mancozeb 75% WP @ 2.5g/L)"]
        M --> O["Organic and Biological Controls<br>(e.g., Trichoderma viride @ 5g/L)"]
        M --> P["Preventative Cultural Practices<br>(e.g., Crop rotation, Drip irrigation)"]
    end

    subgraph BLOCK5 ["BLOCK 5: API SERVING and DELIVERY"]
        N --> Q["Advisory Synthesis Engine<br>(Zero-Hallucination Guardrail)"]
        O --> Q
        P --> Q
        Q --> R["Structured JSON Advisory<br>(FastAPI /diagnose - 3.01 ms CPU)"]
    end
"""

data = {
    "code": mermaid_code,
    "mermaid": {"theme": "dark"}
}
json_bytes = json.dumps(data).encode("utf-8")
b64_str = base64.urlsafe_b64encode(json_bytes).decode("ascii")

url_png = f"https://mermaid.ink/img/{b64_str}"
url_svg = f"https://mermaid.ink/svg/{b64_str}"

req_png = urllib.request.Request(url_png, headers={"User-Agent": "Mozilla/5.0"})
req_svg = urllib.request.Request(url_svg, headers={"User-Agent": "Mozilla/5.0"})

try:
    print("Fetching exact dark theme render from Mermaid Engine...")
    with urllib.request.urlopen(req_png, timeout=20) as resp:
        content = resp.read()
        (DOWNLOADS_DIR / "FarmWise360_Exact_Mermaid_Dark.png").write_bytes(content)
        (DOCS_DIR / "FarmWise360_Exact_Mermaid_Dark.png").write_bytes(content)
        print("Exact Dark PNG downloaded!")

    with urllib.request.urlopen(req_svg, timeout=20) as resp:
        content = resp.read()
        (DOWNLOADS_DIR / "FarmWise360_Exact_Mermaid_Dark.svg").write_bytes(content)
        (DOCS_DIR / "FarmWise360_Exact_Mermaid_Dark.svg").write_bytes(content)
        print("Exact Dark SVG downloaded!")
except Exception as e:
    print("Fetch note:", e)

