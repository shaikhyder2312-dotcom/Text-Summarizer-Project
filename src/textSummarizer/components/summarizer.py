
import torch
import spacy
import pytextrank

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from src.textSummarizer.logging import logger


class Summarizer:

    def __init__(self, config):
        self.config = config

        logger.info("Initializing Summarizer")

        logger.info(
            f"Abstractive model: {self.config.abstractive_model_name}"
        )

        logger.info(
            f"Extractive model: {self.config.extractive_model_name}"
        )

        # -----------------------------
        # Device
        # -----------------------------
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        logger.info(f"Using device: {self.device}")

        # -----------------------------
        # Load DistilBART Tokenizer
        # -----------------------------
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.abstractive_model_name
        )

        # -----------------------------
        # Load DistilBART Model
        # -----------------------------
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.config.abstractive_model_name
        )

        self.model = self.model.to(self.device)
        self.model.eval()

        logger.info("Base DistilBART model loaded successfully")
        logger.info(
            f"DistilBART model is running on {self.device}"
        )

        # -----------------------------
        # PyTextRank
        # -----------------------------
        self.nlp = spacy.load(
            self.config.extractive_model_name
        )

        self.nlp.add_pipe("textrank")

        logger.info("PyTextRank initialized successfully")

    # =========================================================
    # Extractive Summarization
    # =========================================================
    def extractive_summary(self, text: str):

        doc = self.nlp(text)

        sentences = []

        for sentence in doc._.textrank.summary(
            limit_phrases=0,
            limit_sentences=self.config.extractive_top_n_sentences
        ):
            sentences.append(sentence.text)

        return " ".join(sentences)

    # =========================================================
    # Generate summary for a single chunk
    # =========================================================
    def _generate_summary(self, text: str):

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            max_length=self.config.abstractive_max_input_length,
            truncation=True
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.config.abstractive_max_new_tokens,
                num_beams=self.config.abstractive_num_beams,
                no_repeat_ngram_size=self.config.abstractive_no_repeat_ngram_size,
                early_stopping=True
            )

        return self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        ).strip()

    # =========================================================
    # Split text into token-safe chunks
    # =========================================================
    def _split_into_chunks(self, text: str):

        # Keep some safety margin below the model's maximum
        # input length.
        chunk_size = min(
            self.config.abstractive_max_input_length,
            384
        )

        # Use slightly overlapping chunks so information near
        # chunk boundaries is less likely to be lost.
        overlap = 32

        tokens = self.tokenizer.encode(
            text,
            add_special_tokens=False
        )

        chunks = []

        start = 0

        while start < len(tokens):

            end = min(
                start + chunk_size,
                len(tokens)
            )

            chunk_tokens = tokens[start:end]

            chunk_text = self.tokenizer.decode(
                chunk_tokens,
                skip_special_tokens=True
            )

            if chunk_text.strip():
                chunks.append(chunk_text)

            if end >= len(tokens):
                break

            start = end - overlap

        logger.info(
            f"Long text split into {len(chunks)} chunks"
        )

        return chunks

    # =========================================================
    # Abstractive Summarization
    # =========================================================
    def abstractive_summary(self, text: str):

        if not text or not text.strip():
            return ""

        text = text.strip()

        # -----------------------------------------------------
        # Very short text protection
        # -----------------------------------------------------
        words = text.split()

        if len(words) < 5:
            logger.info(
                "Input is too short for summarization. "
                "Returning original text."
            )
            return text

        # -----------------------------------------------------
        # Count actual tokenizer tokens
        # -----------------------------------------------------
        token_count = len(
            self.tokenizer.encode(
                text,
                add_special_tokens=True
            )
        )

        logger.info(
            f"Input token count: {token_count}"
        )

        # -----------------------------------------------------
        # Short/normal text
        # -----------------------------------------------------
        if token_count <= self.config.abstractive_max_input_length:

            logger.info(
                "Input fits model context. Using direct summarization."
            )

            return self._generate_summary(text)

        # -----------------------------------------------------
        # Long text
        # -----------------------------------------------------
        logger.info(
            "Input exceeds model context. Using chunked summarization."
        )

        chunks = self._split_into_chunks(text)

        chunk_summaries = []

        for index, chunk in enumerate(chunks, start=1):

            logger.info(
                f"Summarizing chunk {index}/{len(chunks)}"
            )

            summary = self._generate_summary(chunk)

            if summary:
                chunk_summaries.append(summary)

        # -----------------------------------------------------
        # Combine chunk summaries
        # -----------------------------------------------------
        combined_summary = " ".join(chunk_summaries)

        if not combined_summary:
            return ""

        combined_token_count = len(
            self.tokenizer.encode(
                combined_summary,
                add_special_tokens=True
            )
        )

        logger.info(
            f"Combined summary token count: {combined_token_count}"
        )

        # -----------------------------------------------------
        # If combined summary fits, return it
        # -----------------------------------------------------
        if combined_token_count <= self.config.abstractive_max_input_length:

            return combined_summary

        # -----------------------------------------------------
        # Final compression pass
        # -----------------------------------------------------
        logger.info(
            "Combined summary is still long. Running final compression."
        )

        return self._generate_summary(
            combined_summary
        )

