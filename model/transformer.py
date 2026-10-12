
import torch
import torch.nn as nn

from config import ModelConfig


class TransformerBlock(nn.Module):
    def __init__(self, config):
        super().__init__()

        self.norm1 = nn.LayerNorm(config.d_model)
        self.attention = nn.MultiheadAttention(
            embed_dim=config.d_model,
            num_heads=config.n_heads,
            dropout=config.dropout,
            batch_first=True,
        )

        self.norm2 = nn.LayerNorm(config.d_model)

        self.feed_forward = nn.Sequential(
            nn.Linear(config.d_model, config.d_ff),
            nn.GELU(),
            nn.Linear(config.d_ff, config.d_model),
        )

        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x):
        seq_len = x.size(1)

        # Prevent each token from attending to future tokens.
        causal_mask = torch.triu(
            torch.ones(
                seq_len, seq_len,
                dtype=torch.bool,
                device=x.device,
            ),
            diagonal=1,
        )

        normalized = self.norm1(x)

        attention_output, _ = self.attention(
            normalized,
            normalized,
            normalized,
            attn_mask=causal_mask,
            need_weights=False,
        )

        x = x + self.dropout(attention_output)
        x = x + self.dropout(self.feed_forward(self.norm2(x)))

        return x


class FarmWiseTransformer(nn.Module):
    def __init__(self, config):
        super().__init__()

        config.validate()
        self.config = config

        self.token_embedding = nn.Embedding(
            config.vocab_size, config.d_model
        )

        self.position_embedding = nn.Embedding(
            config.max_seq_len, config.d_model
        )

        self.blocks = nn.ModuleList(
            [TransformerBlock(config) for _ in range(config.n_layers)]
        )

        self.final_norm = nn.LayerNorm(config.d_model)

        self.lm_head = nn.Linear(
            config.d_model, config.vocab_size, bias=False
        )

        # Share input and output token embeddings.
        self.lm_head.weight = self.token_embedding.weight

    def forward(self, input_ids):
        batch_size, seq_len = input_ids.shape

        if seq_len > self.config.max_seq_len:
            raise ValueError("Input exceeds max_seq_len")

        positions = torch.arange(
            seq_len, device=input_ids.device
        ).unsqueeze(0)

        x = (
            self.token_embedding(input_ids)
            + self.position_embedding(positions)
        )

        for block in self.blocks:
            x = block(x)

        x = self.final_norm(x)

        return self.lm_head(x)
