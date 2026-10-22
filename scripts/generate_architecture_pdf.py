# -*- coding: utf-8 -*-
"""
FarmWise360 AI -- Master-Slave Architecture Document Generator
Generates a detailed landscape-format PDF with block diagrams and flowcharts.
Output: documentation/FarmWise360_System_Architecture.pdf
"""

import os
import sys
import io

# Force UTF-8 output on Windows so print() doesn't crash on special chars
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import KeepTogether

# ─── Output path ────────────────────────────────────────────────────────────
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "documentation")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PDF = os.path.join(OUT_DIR, "FarmWise360_System_Architecture.pdf")

PAGE = landscape(A4)   # 841.89 x 595.28 points
MARGIN = 1.5 * cm

# ─── Colour palette ─────────────────────────────────────────────────────────
GREEN_DARK   = "#1B5E20"
GREEN_MID    = "#2E7D32"
GREEN_LIGHT  = "#66BB6A"
GREEN_PALE   = "#E8F5E9"
BLUE_DARK    = "#0D47A1"
BLUE_MID     = "#1565C0"
BLUE_LIGHT   = "#42A5F5"
BLUE_PALE    = "#E3F2FD"
ORANGE_DARK  = "#E65100"
ORANGE_MID   = "#F57C00"
ORANGE_LIGHT = "#FFA726"
ORANGE_PALE  = "#FFF3E0"
PURPLE_DARK  = "#4A148C"
PURPLE_MID   = "#6A1B9A"
PURPLE_LIGHT = "#AB47BC"
PURPLE_PALE  = "#F3E5F5"
RED_DARK     = "#B71C1C"
RED_MID      = "#C62828"
RED_LIGHT    = "#EF5350"
RED_PALE     = "#FFEBEE"
GREY_DARK    = "#212121"
GREY_MID     = "#424242"
GREY_LIGHT   = "#9E9E9E"
WHITE        = "#FFFFFF"
YELLOW_PALE  = "#FFFDE7"


# ════════════════════════════════════════════════════════════════════════════
# HELPER — save matplotlib figure to ReportLab Image flowable
# ════════════════════════════════════════════════════════════════════════════
def fig_to_image(fig, width_cm=23, height_cm=13):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return Image(buf, width=width_cm * cm, height=height_cm * cm)


# ════════════════════════════════════════════════════════════════════════════
# DIAGRAM 1 — High-Level System Overview
# ════════════════════════════════════════════════════════════════════════════
def draw_overview():
    fig, ax = plt.subplots(figsize=(22, 9))
    fig.patch.set_facecolor(GREEN_PALE)
    ax.set_facecolor(GREEN_PALE)
    ax.set_xlim(0, 22); ax.set_ylim(0, 9)
    ax.axis("off")

    def box(x, y, w, h, fc, ec, label, sublabel="", fontsize=11, radius=0.4):
        patch = FancyBboxPatch((x, y), w, h,
                               boxstyle=f"round,pad=0.05,rounding_size={radius}",
                               fc=fc, ec=ec, lw=2, zorder=3)
        ax.add_patch(patch)
        cy = y + h / 2
        ax.text(x + w / 2, cy + (0.18 if sublabel else 0), label,
                ha="center", va="center", fontsize=fontsize,
                fontweight="bold", color=WHITE, zorder=4,
                wrap=True)
        if sublabel:
            ax.text(x + w / 2, cy - 0.32, sublabel,
                    ha="center", va="center", fontsize=8,
                    color=WHITE, alpha=0.9, zorder=4)

    def arrow(x1, y1, x2, y2, col="#333333", label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2,
                                   connectionstyle="arc3,rad=0"),
                    zorder=5)
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my + 0.22, label, ha="center", va="bottom",
                    fontsize=8, color=col, fontstyle="italic", zorder=6)

    # ── Farmer ──────────────────────────────────────────────
    box(0.4, 3.5, 2.8, 2.0, GREEN_MID, GREEN_DARK,
        " FARMER", "Asks a question\nin any language", fontsize=10)

    # ── Slave Model ─────────────────────────────────────────
    box(4.0, 2.5, 4.2, 4.0, BLUE_MID, BLUE_DARK,
        " SLAVE MODEL", "(On-Device, Offline)", fontsize=11)
    # Internal steps inside slave
    for i, (lbl, yy) in enumerate([
        ("① NLP  —  Read & Clean Text", 5.8),
        ("② NLU  —  Understand Meaning", 5.0),
        ("③ Neural Net  —  Find Answer", 4.2),
        ("④ Safety Check  —  Filter", 3.4),
    ]):
        ax.text(4.2, yy, lbl, fontsize=7.5, color=WHITE, zorder=5,
                va="center")

    # ── Knowledge Base ─────────────────────────────────────
    box(4.0, 0.4, 4.2, 1.6, GREEN_DARK, GREEN_MID,
        " KNOWLEDGE BASE", "Verified PDF & Text Files", fontsize=9.5)

    # ── Decision Diamond ────────────────────────────────────
    diamond_x, diamond_y = 9.8, 4.3
    d = 1.0
    diamond = plt.Polygon(
        [[diamond_x, diamond_y + d],
         [diamond_x + d * 1.5, diamond_y],
         [diamond_x, diamond_y - d],
         [diamond_x - d * 1.5, diamond_y]],
        fc=ORANGE_MID, ec=ORANGE_DARK, lw=2, zorder=3)
    ax.add_patch(diamond)
    ax.text(diamond_x, diamond_y, "HIGH\nCONFIDENCE?",
            ha="center", va="center", fontsize=8,
            fontweight="bold", color=WHITE, zorder=4)

    # ── Master Model ────────────────────────────────────────
    box(12.5, 2.5, 4.2, 4.0, PURPLE_MID, PURPLE_DARK,
        " MASTER MODEL", "(Cloud, Online)", fontsize=11)
    for i, (lbl, yy) in enumerate([
        ("① Deep Reasoning Engine", 5.8),
        ("② Human Expert Validation", 5.0),
        ("③ Trusted Answer Generation", 4.2),
        ("④ Teach Slave (Distillation)", 3.4),
    ]):
        ax.text(12.7, yy, lbl, fontsize=7.5, color=WHITE, zorder=5,
                va="center")

    # ── Response Back to Farmer ─────────────────────────────
    box(17.5, 3.5, 3.8, 2.0, GREEN_MID, GREEN_DARK,
        "[OK] ANSWER", "Delivered to Farmer", fontsize=10)

    # ── Arrows ──────────────────────────────────────────────
    arrow(3.2, 4.5, 4.0, 4.5, BLUE_DARK, "Question")
    arrow(4.2, 0.4, 4.2, 2.5, GREEN_DARK, "Lookup")      # KB → Slave bottom
    arrow(8.2, 4.5, 9.0, 4.5, ORANGE_DARK, "Result")     # Slave → Diamond
    # YES path → Answer
    ax.annotate("", xy=(17.5, 4.5), xytext=(11.3, 4.3),
                arrowprops=dict(arrowstyle="-|>", color=GREEN_MID, lw=2.2), zorder=5)
    ax.text(14.3, 4.7, "YES → Direct Answer", ha="center", fontsize=8,
            color=GREEN_MID, fontstyle="italic", zorder=6)
    # NO path → Master
    ax.annotate("", xy=(12.5, 4.5), xytext=(11.3, 4.3),
                arrowprops=dict(arrowstyle="-|>", color=PURPLE_MID, lw=2.2), zorder=5)
    ax.text(11.9, 4.0, "NO → Escalate", ha="center", fontsize=8,
            color=PURPLE_MID, fontstyle="italic", zorder=6)
    # Master → Answer
    arrow(16.7, 4.5, 17.5, 4.5, PURPLE_DARK, "Verified Answer")
    # Master → Slave (distill)
    ax.annotate("", xy=(8.2, 3.0), xytext=(12.5, 3.0),
                arrowprops=dict(arrowstyle="-|>", color=GREEN_LIGHT, lw=1.8,
                                linestyle="dashed"), zorder=5)
    ax.text(10.4, 3.2, "Learns & Improves", ha="center", fontsize=8,
            color=GREEN_DARK, fontstyle="italic", zorder=6)

    ax.set_title("FarmWise360 AI — Complete System Overview",
                 fontsize=16, fontweight="bold", color=GREEN_DARK, pad=10)
    return fig


# ════════════════════════════════════════════════════════════════════════════
# DIAGRAM 2 — Slave Model Detailed Pipeline
# ════════════════════════════════════════════════════════════════════════════
def draw_slave_pipeline():
    fig, ax = plt.subplots(figsize=(22, 9))
    fig.patch.set_facecolor(BLUE_PALE)
    ax.set_facecolor(BLUE_PALE)
    ax.set_xlim(0, 22); ax.set_ylim(0, 9)
    ax.axis("off")

    def stage(x, y, w, h, fc, ec, title, bullets, fontsize=9):
        patch = FancyBboxPatch((x, y), w, h,
                               boxstyle="round,pad=0.05,rounding_size=0.3",
                               fc=fc, ec=ec, lw=2.2, zorder=3)
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h - 0.42, title,
                ha="center", va="center", fontsize=fontsize + 1,
                fontweight="bold", color=WHITE, zorder=4)
        for i, b in enumerate(bullets):
            ax.text(x + 0.2, y + h - 0.9 - i * 0.52, f"• {b}",
                    ha="left", va="center", fontsize=7.5,
                    color=WHITE, zorder=4)

    def arr(x1, y, x2, col="#333"):
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.5), zorder=5)

    # Stage 0: Input
    stage(0.3, 2.5, 2.5, 4.0, GREEN_MID, GREEN_DARK,
          "[IN] INPUT",
          ["Farmer types question", "Voice / Photo input",
           "Any local language", "No internet needed"])
    arr(2.8, 4.5, 3.5, GREEN_DARK)

    # Stage 1: NLP
    stage(3.5, 2.5, 3.5, 4.0, BLUE_MID, BLUE_DARK,
          "🔤 NLP LAYER",
          ["Remove noise & symbols", "Fix spelling mistakes",
           "Break into words/tokens", "Detect language",
           "Normalize text"])
    arr(7.0, 4.5, 7.8, BLUE_DARK)

    # Stage 2: NLU
    stage(7.8, 2.5, 3.5, 4.0, PURPLE_MID, PURPLE_DARK,
          "[IDEA] NLU LAYER",
          ["Understand what is meant", "Find crop & disease names",
           "Map synonyms to standard", "Extract intent & urgency",
           "Score relevance to KB"])
    arr(11.3, 4.5, 12.1, PURPLE_DARK)

    # Stage 3: Neural Net
    stage(12.1, 2.5, 3.5, 4.0, ORANGE_MID, ORANGE_DARK,
          " NEURAL NET",
          ["Match to known patterns", "Rank best answers",
           "Generate confidence %", "< 1 M params (tiny!)",
           "Runs in 3 ms on CPU"])
    arr(15.6, 4.5, 16.4, ORANGE_DARK)

    # Stage 4: Safety
    stage(16.4, 2.5, 3.5, 4.0, RED_MID, RED_DARK,
          "[SAFE] SAFETY GATE",
          ["Block harmful chemicals", "Verify dosage limits",
           "Add legal disclaimer", "PHI/residue check",
           "Never guess — use docs"])
    arr(19.9, 4.5, 20.5, RED_DARK)

    # Stage 5: Output
    stage(20.0, 3.2, 1.8, 2.6, GREEN_DARK, GREEN_MID,
          "[OK] OUT",
          ["Clear answer", "Safe advice"])

    # Knowledge Base floating below
    kb = FancyBboxPatch((7.0, 0.3), 5.5, 1.5,
                        boxstyle="round,pad=0.05,rounding_size=0.3",
                        fc=GREEN_DARK, ec=GREEN_MID, lw=2, zorder=3)
    ax.add_patch(kb)
    ax.text(9.75, 1.05, " VERIFIED KNOWLEDGE BASE  (PDF + TXT files)",
            ha="center", va="center", fontsize=9.5,
            fontweight="bold", color=WHITE, zorder=4)
    # KB feeds NLU and Neural Net
    ax.annotate("", xy=(9.55, 2.5), xytext=(9.55, 1.8),
                arrowprops=dict(arrowstyle="-|>", color=GREEN_MID, lw=2), zorder=5)
    ax.text(9.55, 2.15, "Semantic Lookup", ha="center", fontsize=7.5,
            color=GREEN_DARK, fontstyle="italic")

    ax.set_title("SLAVE MODEL — Step-by-Step Pipeline  (On-Device · Offline · < 1M Parameters)",
                 fontsize=14, fontweight="bold", color=BLUE_DARK, pad=10)
    return fig


# ════════════════════════════════════════════════════════════════════════════
# DIAGRAM 3 — Master Model Pipeline
# ════════════════════════════════════════════════════════════════════════════
def draw_master_pipeline():
    fig, ax = plt.subplots(figsize=(22, 9))
    fig.patch.set_facecolor(PURPLE_PALE)
    ax.set_facecolor(PURPLE_PALE)
    ax.set_xlim(0, 22); ax.set_ylim(0, 9)
    ax.axis("off")

    def box(x, y, w, h, fc, ec, title, sub="", fontsize=10):
        p = FancyBboxPatch((x, y), w, h,
                           boxstyle="round,pad=0.05,rounding_size=0.35",
                           fc=fc, ec=ec, lw=2.2, zorder=3)
        ax.add_patch(p)
        cy = y + h / 2
        ax.text(x + w / 2, cy + (0.22 if sub else 0), title,
                ha="center", va="center", fontsize=fontsize,
                fontweight="bold", color=WHITE, zorder=4)
        if sub:
            ax.text(x + w / 2, cy - 0.38, sub,
                    ha="center", va="center", fontsize=7.8,
                    color=WHITE, alpha=0.92, zorder=4)

    def arr(x1, y1, x2, y2, col, lab="", rad=0):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2,
                                   connectionstyle=f"arc3,rad={rad}"), zorder=5)
        if lab:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my + 0.25, lab, ha="center", fontsize=8,
                    color=col, fontstyle="italic", zorder=6)

    # Trigger
    box(0.3, 3.7, 2.8, 1.6, RED_MID, RED_DARK,
        "[!] ESCALATION", "Slave confidence < 70%", fontsize=9.5)
    arr(3.1, 4.5, 4.0, 4.5, RED_DARK, "Trigger")

    # Queue
    box(4.0, 3.7, 2.8, 1.6, ORANGE_MID, ORANGE_DARK,
        "[Q] QUEUE", "Batch Offline Requests", fontsize=9.5)
    arr(6.8, 4.5, 7.7, 4.5, ORANGE_DARK, "When online")

    # Deep Reasoning
    box(7.7, 2.8, 3.5, 3.4, PURPLE_MID, PURPLE_DARK,
        " DEEP REASONING", "Large LLM Engine\n(billions of params)", fontsize=10)
    arr(11.2, 4.5, 12.1, 4.5, PURPLE_DARK, "Draft answer")

    # Human Expert
    box(12.1, 3.0, 3.5, 3.0, BLUE_MID, BLUE_DARK,
        "👩‍🔬 HUMAN EXPERT", "Agronomist validates\nbefore sending", fontsize=10)
    arr(15.6, 4.5, 16.5, 4.5, BLUE_DARK, "Approved ✓")

    # Final Answer
    box(16.5, 3.7, 2.8, 1.6, GREEN_MID, GREEN_DARK,
        "[OK] FINAL ANSWER", "Sent to Farmer", fontsize=9.5)
    arr(19.3, 4.5, 20.1, 4.5, GREEN_DARK)

    # Feedback
    box(20.1, 3.7, 1.7, 1.6, GREEN_DARK, GREEN_MID,
        "[LOOP] FEED", "Back to Slave", fontsize=8.5)

    # Distillation loop (curved arrow back)
    ax.annotate("", xy=(5.5, 7.5), xytext=(20.9, 5.3),
                arrowprops=dict(arrowstyle="-|>", color=GREEN_LIGHT, lw=2,
                                linestyle="dashed",
                                connectionstyle="arc3,rad=0.4"), zorder=5)
    ax.text(13, 7.8, "[TEACH]  KNOWLEDGE DISTILLATION  —  Master teaches Slave new skills",
            ha="center", fontsize=10, fontweight="bold",
            color=GREEN_DARK, zorder=6)

    # Safety Note
    note = FancyBboxPatch((0.3, 0.3), 21.4, 1.5,
                          boxstyle="round,pad=0.05,rounding_size=0.3",
                          fc=RED_PALE, ec=RED_MID, lw=2, zorder=3)
    ax.add_patch(note)
    ax.text(11.0, 1.05,
            "[SAFE]  SAFETY LOCK:  No answer leaves the Master without Human Expert sign-off.  "
            "Chemical doses are NEVER generated — only copied from verified documents.",
            ha="center", va="center", fontsize=9.5,
            color=RED_DARK, fontweight="bold", zorder=4)

    ax.set_title("MASTER MODEL — Deep Reasoning & Distillation Pipeline  (Cloud · Human-in-the-Loop)",
                 fontsize=14, fontweight="bold", color=PURPLE_DARK, pad=10)
    return fig


# ════════════════════════════════════════════════════════════════════════════
# DIAGRAM 4 — Data Processing Pipeline
# ════════════════════════════════════════════════════════════════════════════
def draw_data_pipeline():
    fig, ax = plt.subplots(figsize=(22, 9))
    fig.patch.set_facecolor(ORANGE_PALE)
    ax.set_facecolor(ORANGE_PALE)
    ax.set_xlim(0, 22); ax.set_ylim(0, 9)
    ax.axis("off")

    def step(x, y, w, h, fc, ec, num, title, desc, fontsize=9):
        p = FancyBboxPatch((x, y), w, h,
                           boxstyle="round,pad=0.05,rounding_size=0.35",
                           fc=fc, ec=ec, lw=2.2, zorder=3)
        ax.add_patch(p)
        ax.text(x + 0.35, y + h - 0.45, num,
                ha="center", va="center", fontsize=15,
                fontweight="bold", color=WHITE, zorder=4, alpha=0.4)
        ax.text(x + w/2 + 0.1, y + h - 0.45, title,
                ha="center", va="center", fontsize=fontsize+1,
                fontweight="bold", color=WHITE, zorder=4)
        for i, d in enumerate(desc):
            ax.text(x + 0.2, y + h - 0.85 - i*0.52, f"• {d}",
                    ha="left", va="center", fontsize=7.5,
                    color=WHITE, alpha=0.95, zorder=4)

    def arr(x1, y, x2, col):
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.5), zorder=5)

    # Raw Sources
    step(0.3, 2.0, 2.8, 5.0, GREEN_DARK, GREEN_MID,
         "①", "RAW DATA",
         ["PDF research papers", "TXT advisory files",
          "Government guidelines", "Farmer field notes",
          "Crop handbooks"])
    arr(3.1, 4.5, 4.0, GREEN_DARK)

    # NLP Cleaning
    step(4.0, 2.0, 3.2, 5.0, BLUE_MID, BLUE_DARK,
         "②", "NLP CLEANING",
         ["Extract text from PDFs", "Remove headers/footers",
          "Fix encoding issues", "Lowercase + normalize",
          "Language detection"])
    arr(7.2, 4.5, 8.0, BLUE_DARK)

    # NLU Chunking
    step(8.0, 2.0, 3.2, 5.0, PURPLE_MID, PURPLE_DARK,
         "③", "NLU CHUNKING",
         ["Split into bite-size chunks", "Tag crop & disease",
          "Mark chemical names", "Assign confidence score",
          "Store with metadata"])
    arr(11.2, 4.5, 12.0, PURPLE_DARK)

    # Semantic Index
    step(12.0, 2.0, 3.2, 5.0, ORANGE_MID, ORANGE_DARK,
         "④", "SEMANTIC INDEX",
         ["TF-IDF keyword scores", "N-gram phrase matching",
          "Synonym expansion", "Instant lookup (no DB)",
          "Pure Python, offline"])
    arr(15.2, 4.5, 16.0, ORANGE_DARK)

    # Neural Query Match
    step(16.0, 2.0, 3.2, 5.0, RED_MID, RED_DARK,
         "⑤", "NEURAL MATCH",
         ["Query embedding created", "Find top-K closest chunks",
          "Rank by relevance score", "Return best answer",
          "< 3 ms on CPU"])
    arr(19.2, 4.5, 20.1, RED_DARK)

    # Output
    step(20.1, 3.2, 1.7, 2.6, GREEN_MID, GREEN_DARK,
         "✓", "READY",
         ["Knowledge", "Base live"])

    ax.set_title("DATA PROCESSING PIPELINE  —  How Raw Documents Become Instant Answers",
                 fontsize=14, fontweight="bold", color=ORANGE_DARK, pad=10)
    return fig


# ════════════════════════════════════════════════════════════════════════════
# DIAGRAM 5 — Safety & Legal Framework
# ════════════════════════════════════════════════════════════════════════════
def draw_safety_framework():
    fig, ax = plt.subplots(figsize=(22, 9))
    fig.patch.set_facecolor(RED_PALE)
    ax.set_facecolor(RED_PALE)
    ax.set_xlim(0, 22); ax.set_ylim(0, 9)
    ax.axis("off")

    def gate(x, y, w, h, fc, ec, icon, title, checks):
        p = FancyBboxPatch((x, y), w, h,
                           boxstyle="round,pad=0.05,rounding_size=0.35",
                           fc=fc, ec=ec, lw=2.5, zorder=3)
        ax.add_patch(p)
        ax.text(x + w/2, y + h - 0.4, icon,
                ha="center", va="center", fontsize=14, zorder=4)
        ax.text(x + w/2, y + h - 0.9, title,
                ha="center", va="center", fontsize=10,
                fontweight="bold", color=WHITE, zorder=4)
        for i, c in enumerate(checks):
            ax.text(x + 0.25, y + h - 1.45 - i * 0.55, f"✔ {c}",
                    ha="left", va="center", fontsize=8,
                    color=WHITE, zorder=4)

    def arr(x1, y, x2, col, label=""):
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.5), zorder=5)
        if label:
            ax.text((x1+x2)/2, y+0.25, label, ha="center",
                    fontsize=8, color=col, fontstyle="italic")

    # Input
    p = FancyBboxPatch((0.3, 3.8), 2.2, 1.4,
                       boxstyle="round,pad=0.05,rounding_size=0.3",
                       fc=ORANGE_MID, ec=ORANGE_DARK, lw=2, zorder=3)
    ax.add_patch(p)
    ax.text(1.4, 4.5, " AI Draft\nAnswer",
            ha="center", va="center", fontsize=9,
            fontweight="bold", color=WHITE, zorder=4)
    arr(2.5, 4.5, 3.3, ORANGE_DARK)

    # Gate 1
    gate(3.3, 1.5, 4.0, 5.5, RED_MID, RED_DARK,
         "[BAN]", "GATE 1\nBanned Chemicals",
         ["Cross-check vs.\nprohibited list",
          "Block if banned", "Flag for expert"])
    arr(7.3, 4.5, 8.1, RED_DARK)

    # Gate 2
    gate(8.1, 1.5, 4.0, 5.5, ORANGE_MID, ORANGE_DARK,
         "[LAB]", "GATE 2\nDosage Calibration",
         ["Verify dose range", "Copy exact from doc",
          "Never auto-generate"])
    arr(12.1, 4.5, 12.9, ORANGE_DARK)

    # Gate 3
    gate(12.9, 1.5, 4.0, 5.5, PURPLE_MID, PURPLE_DARK,
         "[PHI]", "GATE 3\nPHI / Residue Check",
         ["Pre-Harvest Interval ok?",
          "Soil residue safe?",
          "Export regulation ok?"])
    arr(16.9, 4.5, 17.7, PURPLE_DARK)

    # Gate 4
    gate(17.7, 1.5, 3.5, 5.5, BLUE_MID, BLUE_DARK,
         "[LAW]", "GATE 4\nLegal Disclaimer",
         ["Add usage caveat",
          "Recommend expert",
          "Log for audit trail"])
    arr(21.2, 4.5, 21.5, BLUE_DARK)

    ax.text(21.7, 4.5, "[OK]", fontsize=18, ha="center", va="center", zorder=5)

    # Reject path
    ax.text(5.3, 0.9, "[X] REJECT", ha="center", fontsize=10,
            fontweight="bold", color=RED_DARK, zorder=5)
    ax.annotate("", xy=(5.3, 1.5), xytext=(5.3, 0.9),
                arrowprops=dict(arrowstyle="<|-", color=RED_DARK, lw=1.8), zorder=5)

    ax.set_title("SAFETY & LEGAL FRAMEWORK  —  4 Gates Every Answer Must Pass",
                 fontsize=14, fontweight="bold", color=RED_DARK, pad=10)
    return fig


# ════════════════════════════════════════════════════════════════════════════
# PDF BUILDER
# ════════════════════════════════════════════════════════════════════════════
def build_pdf():
    doc = SimpleDocTemplate(
        OUT_PDF,
        pagesize=PAGE,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="FarmWise360 AI System Architecture",
        author="FarmWise360 Team — TIMES POINT",
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=28, leading=34, spaceAfter=6,
        textColor=colors.HexColor(GREEN_DARK),
        alignment=TA_CENTER,
    )
    h1 = ParagraphStyle(
        "H1", parent=styles["Heading1"],
        fontSize=18, leading=22, spaceBefore=10, spaceAfter=4,
        textColor=colors.HexColor(BLUE_DARK),
        alignment=TA_CENTER,
    )
    h2 = ParagraphStyle(
        "H2", parent=styles["Heading2"],
        fontSize=13, leading=16, spaceBefore=6, spaceAfter=3,
        textColor=colors.HexColor(GREEN_DARK),
    )
    body = ParagraphStyle(
        "Body", parent=styles["Normal"],
        fontSize=10, leading=14, spaceAfter=4,
        textColor=colors.HexColor(GREY_DARK),
        alignment=TA_JUSTIFY,
    )
    note_style = ParagraphStyle(
        "Note", parent=styles["Normal"],
        fontSize=9, leading=13, spaceAfter=3,
        textColor=colors.HexColor(BLUE_DARK),
        leftIndent=10,
    )

    def section_header(text, color=GREEN_DARK):
        return [
            HRFlowable(width="100%", thickness=2,
                       color=colors.HexColor(color)),
            Paragraph(text, h1),
            HRFlowable(width="100%", thickness=1,
                       color=colors.HexColor(color), spaceAfter=6),
        ]

    story = []

    # ── COVER PAGE ───────────────────────────────────────────────────────
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph("🌱 FarmWise360 AI", title_style))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Complete System Architecture", ParagraphStyle(
        "Sub", parent=styles["Title"], fontSize=20, leading=26,
        textColor=colors.HexColor(BLUE_MID), alignment=TA_CENTER)))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Master Model · Slave Model · NLP · NLU · Neural Networks",
                            ParagraphStyle("TagLine", parent=styles["Normal"],
                                           fontSize=12, leading=16, alignment=TA_CENTER,
                                           textColor=colors.HexColor(GREY_MID))))
    story.append(Spacer(1, 0.6 * cm))

    # Cover summary table
    cover_data = [
        ["Project", "FarmWise360 AI — Smart Agricultural Advisory"],
        ["Team", "Thanya Ravi  &  Vachan Gowda V  ·  TIMES POINT"],
        ["Version", "v2.0  —  Master-Slave Architecture"],
        ["Date", "October 2026"],
        ["Stack", "NLP + NLU + Neural Networks  (< 1M params offline)"],
        ["Philosophy", "Vast Knowledge · Tiny Size · Zero Hallucination · Always Safe"],
    ]
    cover_table = Table(cover_data, colWidths=[5*cm, 20*cm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor(GREEN_DARK)),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor(GREEN_PALE)),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor(GREY_DARK)),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ROWBACKGROUND", (1, 0), (1, -1),
         [colors.HexColor(GREEN_PALE), colors.white] * 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(GREEN_MID)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "This document explains — in plain language — how FarmWise360 AI works "
        "from the moment a farmer asks a question to the moment a safe, verified "
        "answer reaches their phone. No jargon. No shortcuts. Just clear diagrams "
        "and honest explanations.",
        ParagraphStyle("Intro", parent=body, fontSize=11, leading=16,
                       alignment=TA_CENTER,
                       textColor=colors.HexColor(GREEN_DARK))))
    story.append(PageBreak())

    # ── TABLE OF CONTENTS ────────────────────────────────────────────────
    story += section_header("[LIST]  Table of Contents")
    toc_data = [
        ["Page", "Section", "What it covers"],
        ["3", "System Overview", "The big picture — how everything connects"],
        ["4", "Slave Model Pipeline", "Step-by-step: how offline device answers"],
        ["5", "Master Model Pipeline", "Deep reasoning + human validation in cloud"],
        ["6", "Data Processing Pipeline", "How PDFs & TXT files become instant answers"],
        ["7", "Safety & Legal Framework", "4 gates every answer must pass"],
        ["8", "Key Design Decisions", "Why we built it this way"],
    ]
    toc_table = Table(toc_data, colWidths=[2*cm, 8*cm, 15*cm])
    toc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(GREEN_DARK)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUND", (0, 1), (-1, -1),
         [colors.HexColor(GREEN_PALE), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(GREEN_MID)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # ── PAGE 1 — OVERVIEW ────────────────────────────────────────────────
    story += section_header("🌐  Section 1 — System Overview: The Big Picture", GREEN_DARK)
    story.append(Paragraph(
        "Think of FarmWise360 like a two-doctor clinic. The <b>Slave Model</b> is "
        "the <b>local doctor</b> who sits in the village — always available, no "
        "internet needed, answers common questions in seconds. When the question is "
        "too complex, it calls the <b>Master Model</b> — the <b>specialist doctor</b> "
        "in the city who does deep research and also has a human expert double-check "
        "the answer before it's sent. The specialist then teaches the local doctor "
        "so it keeps getting smarter.", body))
    story.append(Spacer(1, 0.3 * cm))
    story.append(fig_to_image(draw_overview(), width_cm=24, height_cm=12))
    story.append(PageBreak())

    # ── PAGE 2 — SLAVE PIPELINE ──────────────────────────────────────────
    story += section_header("  Section 2 — Slave Model: Step-by-Step Pipeline", BLUE_DARK)
    story.append(Paragraph(
        "The Slave Model runs <b>entirely on the farmer's device — no internet required</b>. "
        "It is tiny (under 1 million parameters) yet powerful enough to handle 332 "
        "questions per second with a 3 ms response time. Here is every step:", body))
    story.append(Spacer(1, 0.3 * cm))
    story.append(fig_to_image(draw_slave_pipeline(), width_cm=24, height_cm=12))
    story.append(Spacer(1, 0.3 * cm))

    steps_data = [
        ["Step", "Layer", "What happens in plain language"],
        ["①", "NLP — Natural Language Processing",
         "Reads the farmer's raw text, fixes typos, removes punctuation noise, "
         "identifies the language, and breaks it into clean word pieces (tokens)."],
        ["②", "NLU — Natural Language Understanding",
         "Goes deeper than words — figures out WHAT the farmer means. Maps "
         "colloquial names ('yellowing leaf') to scientific terms, extracts the "
         "crop name, disease hint, and urgency level."],
        ["③", "Neural Network",
         "Matches the understood question against learned patterns from the "
         "Knowledge Base. Produces a confidence score (0-100 %). Under 1M params, "
         "runs in 3 ms on a basic CPU — no GPU needed."],
        ["④", "Safety Gate",
         "Every answer passes through a filter that blocks banned chemicals, "
         "verifies dosages against verified documents, and adds a legal disclaimer. "
         "Zero guessing allowed."],
    ]
    steps_table = Table(steps_data, colWidths=[1.5*cm, 6*cm, 17.5*cm])
    steps_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(BLUE_DARK)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUND", (0, 1), (-1, -1),
         [colors.HexColor(BLUE_PALE), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(BLUE_MID)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(steps_table)
    story.append(PageBreak())

    # ── PAGE 3 — MASTER PIPELINE ─────────────────────────────────────────
    story += section_header("  Section 3 — Master Model: Deep Reasoning in the Cloud", PURPLE_DARK)
    story.append(Paragraph(
        "When the Slave Model is not sure (confidence below 70 %), it queues the "
        "question for the <b>Master Model in the cloud</b>. The Master uses a large, "
        "powerful AI engine and — critically — always has a <b>human agricultural "
        "expert validate the answer</b> before it reaches the farmer. No answer from "
        "the Master is automatic.", body))
    story.append(Spacer(1, 0.3 * cm))
    story.append(fig_to_image(draw_master_pipeline(), width_cm=24, height_cm=11))
    story.append(Spacer(1, 0.3 * cm))

    master_data = [
        ["Step", "What happens"],
        ["Escalation Trigger", "Slave confidence < 70% → question is queued, farmer gets 'checking with expert' message"],
        ["Offline Queue", "Questions are stored locally and synced when internet is available — no data is lost"],
        ["Deep Reasoning", "Large language model (billions of params) analyses the question with full agricultural context"],
        ["Human Expert Review", "A certified agronomist reads the AI draft and approves, edits, or rejects it"],
        ["Answer Delivery", "Only after expert sign-off does the verified answer reach the farmer"],
        ["Knowledge Distillation", "The Master's new knowledge is compressed and taught back to the Slave so it improves over time"],
    ]
    master_table = Table(master_data, colWidths=[5*cm, 20*cm])
    master_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(PURPLE_DARK)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUND", (0, 1), (-1, -1),
         [colors.HexColor(PURPLE_PALE), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(PURPLE_MID)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(master_table)
    story.append(PageBreak())

    # ── PAGE 4 — DATA PIPELINE ───────────────────────────────────────────
    story += section_header("  Section 4 — Data Processing: PDF → Instant Answers", ORANGE_DARK)
    story.append(Paragraph(
        "FarmWise360 is built on <b>real documents — PDFs, government guidelines, "
        "research papers, and advisory texts</b> — not on noisy, unverified CSV "
        "datasets. Here is how raw documents are turned into the fast, accurate "
        "Knowledge Base that powers every answer:", body))
    story.append(Spacer(1, 0.3 * cm))
    story.append(fig_to_image(draw_data_pipeline(), width_cm=24, height_cm=11))
    story.append(Spacer(1, 0.3 * cm))

    data_pipeline_data = [
        ["Stage", "Tool / Method", "Plain-language explanation"],
        ["① Collect", "PDF + TXT files", "Trusted sources only: ICAR, TNAU, state agriculture departments, peer-reviewed papers"],
        ["② NLP Clean", "pypdf + regex + langdetect", "Text is extracted from PDFs, headers/footers removed, language detected, and text normalised"],
        ["③ NLU Chunk", "Sentence splitter + crop tagger", "Long documents are cut into small, meaningful paragraphs each tagged with crop, disease, and chemical metadata"],
        ["④ Index", "TF-IDF + N-gram + synonyms", "Each chunk gets a relevance score. Synonyms are expanded so 'yellowing' also matches 'chlorosis'. No external database needed"],
        ["⑤ Match", "Neural embedding lookup", "When a question arrives, the Neural Net finds the top-matching chunks in under 3 ms and assembles the answer"],
    ]
    dp_table = Table(data_pipeline_data, colWidths=[2.5*cm, 5*cm, 17.5*cm])
    dp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(ORANGE_DARK)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUND", (0, 1), (-1, -1),
         [colors.HexColor(ORANGE_PALE), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(ORANGE_MID)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(dp_table)
    story.append(PageBreak())

    # ── PAGE 5 — SAFETY ──────────────────────────────────────────────────
    story += section_header("[SAFE]  Section 5 — Safety & Legal Framework: 4 Non-Negotiable Gates", RED_DARK)
    story.append(Paragraph(
        "Every single answer — whether from Slave or Master — must pass through "
        "<b>4 safety gates</b> before reaching the farmer. These gates are "
        "<b>non-negotiable and cannot be bypassed</b>. This protects farmers, "
        "protects the environment, and protects the company legally.", body))
    story.append(Spacer(1, 0.3 * cm))
    story.append(fig_to_image(draw_safety_framework(), width_cm=24, height_cm=10))
    story.append(Spacer(1, 0.3 * cm))

    safety_data = [
        ["Gate", "Name", "What it does", "What happens if it fails"],
        ["1", "Banned Chemical Filter",
         "Every chemical name in the answer is checked against the national list of "
         "banned / restricted pesticides.",
         "Answer is BLOCKED. Farmer is told to consult local authority."],
        ["2", "Dosage Calibration",
         "Dosages are NEVER generated by the AI. They are copied verbatim from the "
         "verified source document and checked against safe range limits.",
         "Dosage is removed. Only qualitative advice is given."],
        ["3", "PHI / Residue Check",
         "Pre-Harvest Interval (PHI) and soil residue rules are verified so the "
         "farmer's produce does not violate food safety or export standards.",
         "Additional waiting period is added to the advice."],
        ["4", "Legal Disclaimer",
         "Every answer includes a standard disclaimer recommending the farmer also "
         "consult a local agronomist. All queries are logged for audit.",
         "Answer is not sent without disclaimer attached."],
    ]
    safety_table = Table(safety_data, colWidths=[1.5*cm, 5*cm, 10*cm, 8.5*cm])
    safety_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(RED_DARK)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUND", (0, 1), (-1, -1),
         [colors.HexColor(RED_PALE), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(RED_MID)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(safety_table)
    story.append(PageBreak())

    # ── PAGE 6 — KEY DECISIONS ────────────────────────────────────────────
    story += section_header("[IDEA]  Section 6 — Key Design Decisions: Why We Built It This Way", GREEN_DARK)
    decisions = [
        ("Why NLP + NLU + Neural Networks?",
         "NLP cleans the language, NLU understands the meaning, and the Neural Network "
         "finds the best answer. These three layers together give us accuracy without "
         "requiring a huge, expensive model."),
        ("Why PDF and TXT files instead of spreadsheet datasets?",
         "Government guidelines and research papers in PDF/TXT format are already "
         "trusted, structured, and widely available in agriculture. They contain "
         "more reliable information than auto-generated CSV rows and are free to use."),
        ("Why is the Slave Model under 1 million parameters?",
         "A small model fits on a basic Android phone, runs without internet, consumes "
         "very little battery, and still responds in 3 ms. Farmers in remote areas "
         "benefit the most from this tiny-but-smart design."),
        ("Why is there always a human in the loop for the Master?",
         "Agriculture advice can affect a farmer's livelihood and health. No AI — "
         "however advanced — should send chemical recommendations without a certified "
         "expert confirming them. The human gate is mandatory, always."),
        ("Why does the Master teach the Slave (Knowledge Distillation)?",
         "Every time the Master solves a hard case, that knowledge is compressed and "
         "added to the Slave. This means the Slave gets smarter with every deployment "
         "cycle without becoming bigger or slower — vast knowledge, tiny size."),
        ("How does zero-hallucination work in practice?",
         "All dosages and chemical names are stored verbatim in the verified Knowledge "
         "Base. The model is NOT allowed to generate these — it can only look them up. "
         "This is enforced at the Safety Gate level, not just as a rule."),
    ]
    for title, text in decisions:
        story.append(Paragraph(f"<b>▶ {title}</b>", h2))
        story.append(Paragraph(text, body))
        story.append(Spacer(1, 0.2 * cm))

    # Final performance box
    perf_data = [
        ["Metric", "Slave Model", "Master Model"],
        ["Parameters", "< 1 Million", "Billions (cloud)"],
        ["Response Time", "3 ms (CPU)", "5–30 seconds (cloud + human review)"],
        ["Internet Required?", "No — fully offline", "Yes — escalation path only"],
        ["Human in the Loop?", "No (direct answer)", "Yes — mandatory"],
        ["Use Case", "Common, known questions", "Complex, rare, or high-risk queries"],
    ]
    perf_table = Table(perf_data, colWidths=[6*cm, 9*cm, 10*cm])
    perf_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(GREEN_DARK)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUND", (0, 1), (-1, -1),
         [colors.HexColor(GREEN_PALE), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(GREEN_MID)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (1, 1), (1, -1), colors.HexColor(BLUE_PALE)),
        ("BACKGROUND", (2, 1), (2, -1), colors.HexColor(PURPLE_PALE)),
    ]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("<b>Performance at a Glance</b>", h2))
    story.append(perf_table)
    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor(GREEN_DARK)))
    story.append(Paragraph(
        "FarmWise360 AI  ·  TIMES POINT  ·  v2.0  ·  October 2026  ·  "
        "Confidential — Internal Architecture Document",
        ParagraphStyle("Footer", parent=body, fontSize=8,
                       alignment=TA_CENTER,
                       textColor=colors.HexColor(GREY_LIGHT))))

    doc.build(story)
    print(f"\n[OK]  PDF generated successfully!\n📄  {OUT_PDF}\n")
    return OUT_PDF


if __name__ == "__main__":
    path = build_pdf()
    # Copy to Downloads for easy access
    import shutil, pathlib
    downloads = pathlib.Path.home() / "Downloads" / "FarmWise360_System_Architecture.pdf"
    shutil.copy(path, downloads)
    print(f"[IN]  Also copied to: {downloads}")
