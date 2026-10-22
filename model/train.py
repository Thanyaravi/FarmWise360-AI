
from pathlib import Path
import time

import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from tokenizers import Tokenizer

from config import ModelConfig
from transformer import FarmWiseTransformer


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "dataset"
TOKENIZER_PATH = DATA_DIR / "tokenized" / "farmwise_bpe_tokenizer.json"
CHECKPOINT_DIR = ROOT / "checkpoints"

BATCH_SIZE = 8
EPOCHS = 3
LEARNING_RATE = 3e-4
SEED = 42


class AgricultureDataset(Dataset):
    def __init__(self, csv_path, tokenizer, config):
        df = pd.read_csv(csv_path).fillna("")

        self.examples = []
        self.config = config

        bos_id = tokenizer.token_to_id("[BOS]")
        eos_id = tokenizer.token_to_id("[EOS]")

        if bos_id is None or eos_id is None:
            raise ValueError("BOS or EOS token is missing.")

        for _, row in df.iterrows():
            question = str(row["question"]).strip()
            answer = str(row["answer"]).strip()

            text = f"Question: {question}\nAnswer: {answer}"
            token_ids = tokenizer.encode(text).ids

            # Reserve room for BOS and EOS.
            token_ids = token_ids[:config.max_seq_len - 1]
            token_ids = [bos_id] + token_ids + [eos_id]

            self.examples.append(
                torch.tensor(token_ids, dtype=torch.long)
            )

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, index):
        return self.examples[index]


def make_collate_fn(pad_id):
    def collate(batch):
        inputs = [item[:-1] for item in batch]
        targets = [item[1:] for item in batch]

        max_len = max(len(item) for item in inputs)

        input_batch = torch.full(
            (len(batch), max_len), pad_id, dtype=torch.long
        )
        target_batch = torch.full(
            (len(batch), max_len), -100, dtype=torch.long
        )

        for i, (x, y) in enumerate(zip(inputs, targets)):
            input_batch[i, :len(x)] = x
            target_batch[i, :len(y)] = y

        return input_batch, target_batch

    return collate


def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    total_tokens = 0

    with torch.no_grad():
        for inputs, targets in loader:
            inputs = inputs.to(device)
            targets = targets.to(device)

            logits = model(inputs)

            loss_sum = nn.functional.cross_entropy(
                logits.reshape(-1, logits.size(-1)),
                targets.reshape(-1),
                ignore_index=-100,
                reduction="sum",
            )

            valid_tokens = (targets != -100).sum().item()
            total_loss += loss_sum.item()
            total_tokens += valid_tokens

    return total_loss / max(total_tokens, 1)


def main():
    torch.manual_seed(SEED)

    config = ModelConfig()
    config.validate()

    tokenizer = Tokenizer.from_file(str(TOKENIZER_PATH))
    pad_id = tokenizer.token_to_id("[PAD]")

    if pad_id is None:
        raise ValueError("PAD token is missing from the tokenizer.")

    train_data = AgricultureDataset(
        DATA_DIR / "splits" / "train.csv", tokenizer, config
    )
    val_data = AgricultureDataset(
        DATA_DIR / "splits" / "validation.csv", tokenizer, config
    )

    collate_fn = make_collate_fn(pad_id)

    train_loader = DataLoader(
        train_data,
        batch_size=BATCH_SIZE,
        shuffle=True,
        collate_fn=collate_fn,
    )
    val_loader = DataLoader(
        val_data,
        batch_size=BATCH_SIZE,
        shuffle=False,
        collate_fn=collate_fn,
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = FarmWiseTransformer(config).to(device)

    optimizer = torch.optim.AdamW(
        model.parameters(), lr=LEARNING_RATE
    )
    criterion = nn.CrossEntropyLoss(ignore_index=-100)

    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    best_val_loss = float("inf")

    print("FarmWise360 AI - Training from scratch")
    print("Device:", device)
    print("Training examples:", len(train_data))
    print("Validation examples:", len(val_data))
    print("Parameters:", f"{sum(p.numel() for p in model.parameters()):,}")
    print("Context length:", config.max_seq_len)

    start_time = time.time()

    for epoch in range(1, EPOCHS + 1):
        model.train()
        total_loss = 0.0
        total_tokens = 0

        for step, (inputs, targets) in enumerate(train_loader, start=1):
            inputs = inputs.to(device)
            targets = targets.to(device)

            optimizer.zero_grad(set_to_none=True)
            logits = model(inputs)

            loss = criterion(
                logits.reshape(-1, logits.size(-1)),
                targets.reshape(-1),
            )

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            valid_tokens = (targets != -100).sum().item()
            total_loss += loss.item() * valid_tokens
            total_tokens += valid_tokens

            if step % 500 == 0:
                print(
                    f"Epoch {epoch}/{EPOCHS} | "
                    f"Step {step}/{len(train_loader)} | "
                    f"Batch loss: {loss.item():.4f}"
                )

        train_loss = total_loss / max(total_tokens, 1)
        val_loss = evaluate(model, val_loader, criterion, device)

        print(
            f"\nEpoch {epoch}/{EPOCHS} | "
            f"Train loss: {train_loss:.4f} | "
            f"Validation loss: {val_loss:.4f}"
        )

        if val_loss < best_val_loss:
            best_val_loss = val_loss

            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "config": config.__dict__,
                    "epoch": epoch,
                    "train_loss": train_loss,
                    "validation_loss": val_loss,
                },
                CHECKPOINT_DIR / "farmwise_baseline.pt",
            )

            print("Best checkpoint saved.")

    elapsed = time.time() - start_time
    print(f"\nTraining finished in {elapsed / 60:.2f} minutes.")
    print("Best validation loss:", f"{best_val_loss:.4f}")
    print("Checkpoint:", CHECKPOINT_DIR / "farmwise_baseline.pt")


if __name__ == "__main__":
    main()
