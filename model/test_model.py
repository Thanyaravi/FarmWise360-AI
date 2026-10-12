
import torch

from config import ModelConfig
from transformer import FarmWiseTransformer


def main():
    torch.manual_seed(42)

    config = ModelConfig()
    model = FarmWiseTransformer(config)

    # Two sample sequences, each containing 16 tokens.
    input_ids = torch.randint(
        0, config.vocab_size, (2, 16)
    )

    logits = model(input_ids)

    parameter_count = sum(
        parameter.numel() for parameter in model.parameters()
    )

    print("FarmWise Transformer: TEST")
    print("Input shape:", tuple(input_ids.shape))
    print("Output shape:", tuple(logits.shape))
    print("Parameters:", f"{parameter_count:,}")
    print(
        "All parameters trainable:",
        all(p.requires_grad for p in model.parameters()),
    )

    assert logits.shape == (2, 16, config.vocab_size)
    assert torch.isfinite(logits).all()

    print("Forward-pass test: PASSED")


if __name__ == "__main__":
    main()
