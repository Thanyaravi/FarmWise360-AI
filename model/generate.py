
from pathlib import Path

import torch
from tokenizers import Tokenizer

from config import ModelConfig
from transformer import FarmWiseTransformer


ROOT = Path(__file__).resolve().parent.parent

TOKENIZER_PATH = (
    ROOT / "dataset" / "tokenized" / "farmwise_bpe_tokenizer.json"
)
CHECKPOINT_PATH = (
    ROOT / "checkpoints" / "farmwise_baseline.pt"
)


def generate_answer(model, tokenizer, question, device, max_new_tokens=80):
    bos_id = tokenizer.token_to_id("[BOS]")
    eos_id = tokenizer.token_to_id("[EOS]")

    prompt = f"Question: {question.strip()}\nAnswer:"
    prompt_ids = tokenizer.encode(prompt).ids
    input_ids = torch.tensor(
        [[bos_id] + prompt_ids], dtype=torch.long, device=device
    )

    model.eval()

    with torch.no_grad():
        for _ in range(max_new_tokens):
            # Keep the most recent tokens within the context window.
            context = input_ids[:, -model.config.max_seq_len:]
            logits = model(context)
            next_token_logits = logits[:, -1, :]

            # Greedy decoding: choose the highest-scoring next token.
            next_token = torch.argmax(
                next_token_logits, dim=-1, keepdim=True
            )

            token_id = next_token.item()

            if token_id == eos_id:
                break

            input_ids = torch.cat([input_ids, next_token], dim=1)

    generated_ids = input_ids[0].tolist()
    decoded = tokenizer.decode(generated_ids, skip_special_tokens=True)

    if "Answer:" in decoded:
        return decoded.rsplit("Answer:", 1)[-1].strip()

    return decoded


def main():
    if not CHECKPOINT_PATH.exists():
        raise FileNotFoundError(
            f"Checkpoint not found: {CHECKPOINT_PATH}"
        )

    torch.manual_seed(42)
    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    checkpoint = torch.load(
        CHECKPOINT_PATH, map_location=device, weights_only=True
    )

    config = ModelConfig(**checkpoint["config"])
    model = FarmWiseTransformer(config).to(device)
    model.load_state_dict(checkpoint["model_state_dict"])

    tokenizer = Tokenizer.from_file(str(TOKENIZER_PATH))

    print("FarmWise360 AI - Generation Test")
    print("Device:", device)
    print("Checkpoint epoch:", checkpoint["epoch"])
    print("Validation loss:", checkpoint["validation_loss"])
    print("\nType 'exit' to stop.")

    while True:
        question = input("\nAgricultural question: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        answer = generate_answer(
            model, tokenizer, question, device
        )
        print("\nGenerated answer:", answer)


if __name__ == "__main__":
    main()
