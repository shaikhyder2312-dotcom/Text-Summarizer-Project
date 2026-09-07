from dataclasses import dataclass
from pathlib import Path


@dataclass
class SummarizerConfig:
    root_dir: Path
    abstractive_model_name: str
    abstractive_max_input_length: int
    abstractive_max_new_tokens: int
    abstractive_num_beams: int
    abstractive_no_repeat_ngram_size: int
    abstractive_min_input_words: int
    extractive_model_name: str
    extractive_top_n_sentences: int