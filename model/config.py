
from dataclasses import dataclass

@dataclass
class ModelConfig:
    vocab_size: int = 1000
    max_seq_len: int = 128
    d_model: int = 128
    n_heads: int = 4
    n_layers: int = 4
    d_ff: int = 512
    dropout: float = 0.1

    def validate(self):
        assert self.vocab_size > 0
        assert self.max_seq_len > 0
        assert self.d_model % self.n_heads == 0
        assert self.n_layers > 0
        assert self.d_ff > 0
