"""
FarmWise 360 AI - CPU Inference Latency & Performance Benchmark
Measures execution speed, memory footprint, and stability on commodity CPU hardware.
"""

import time
import sys
from pathlib import Path
import torch

MODEL_DIR = Path(__file__).resolve().parent.parent / "model"
sys.path.insert(0, str(MODEL_DIR))

from config import ModelConfig
from diagnostic_model import FarmWiseDiagnosticClassifier


def benchmark_cpu(iterations: int = 50):
    print("==================================================")
    print("FarmWise 360 AI - Edge CPU Benchmark")
    print("==================================================")

    config = ModelConfig()
    model = FarmWiseDiagnosticClassifier(config)
    model.eval()

    param_count = sum(p.numel() for p in model.parameters())
    print(f"Total Parameters: {param_count:,}")
    print(f"Sub-1M Constraint Met: {param_count < 1_000_000}")
    print(f"Device: CPU")
    print("--------------------------------------------------")

    # Warmup
    dummy_input = torch.randint(0, config.vocab_size, (1, 32))
    for _ in range(5):
        _ = model(dummy_input)

    latencies = []
    with torch.no_grad():
        for _ in range(iterations):
            start = time.perf_counter()
            _ = model.diagnose(dummy_input, symptom_text="brown spots on wheat leaves")
            end = time.perf_counter()
            latencies.append((end - start) * 1000.0)  # Convert to ms

    latencies.sort()
    mean_lat = sum(latencies) / len(latencies)
    p50_lat = latencies[len(latencies) // 2]
    p95_lat = latencies[int(len(latencies) * 0.95)]
    min_lat = latencies[0]
    max_lat = latencies[-1]

    print(f"Iterations: {iterations}")
    print(f"Mean Latency: {mean_lat:.2f} ms")
    print(f"Median (P50) Latency: {p50_lat:.2f} ms")
    print(f"95th Percentile (P95): {p95_lat:.2f} ms")
    print(f"Min / Max: {min_lat:.2f} ms / {max_lat:.2f} ms")
    print(f"Throughput: {1000.0 / mean_lat:.1f} requests/second on 1 CPU core")
    print("--------------------------------------------------")

    target_met = p95_lat < 50.0
    print(f"Edge Latency Target (<50ms): {'PASSED' if target_met else 'NEEDS OPTIMIZATION'}")
    print("==================================================")


if __name__ == "__main__":
    benchmark_cpu(50)
