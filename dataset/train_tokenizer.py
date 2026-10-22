
from pathlib import Path
import pandas as pd
from tokenizers import Tokenizer, models, trainers
from tokenizers import pre_tokenizers, decoders

BASE_DIR = Path(__file__).resolve().parent
TRAIN_FILE = BASE_DIR / "splits" / "train.csv"
OUTPUT_DIR = BASE_DIR / "tokenized"

VOCAB_SIZE = 4000


def main():
    if not TRAIN_FILE.exists():
        raise FileNotFoundError(f"Missing training file: {TRAIN_FILE}")

    df = pd.read_csv(TRAIN_FILE).fillna("")

    texts = []
    for _, row in df.iterrows():
        question = str(row["question"]).strip()
        answer = str(row["answer"]).strip()

        if question and answer:
            texts.append(
                f"Question: {question}\nAnswer: {answer}"
            )

    tokenizer = Tokenizer(models.BPE(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(
        add_prefix_space=False
    )
    tokenizer.decoder = decoders.ByteLevel()

    trainer = trainers.BpeTrainer(
        vocab_size=VOCAB_SIZE,
        min_frequency=2,
        special_tokens=["[PAD]", "[UNK]", "[BOS]", "[EOS]"],
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
    )

    tokenizer.train_from_iterator(texts, trainer=trainer)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / "farmwise_bpe_tokenizer.json"
    tokenizer.save(str(output_file))

    print("TOKENIZER TRAINING COMPLETE")
    print("----------------------------")
    print("Training examples:", len(texts))
    print("Requested vocabulary:", VOCAB_SIZE)
    print("Actual vocabulary:", tokenizer.get_vocab_size())
    print("Tokenizer saved to:", output_file)

    sample_text = texts[0]
    encoded = tokenizer.encode(sample_text)

    print("\nSample text:", sample_text[:200])
    print("Token count:", len(encoded.ids))
    print("Token IDs:", encoded.ids[:40])
    print("Decoded text:", tokenizer.decode(encoded.ids)[:200])


if __name__ == "__main__":
    main()
