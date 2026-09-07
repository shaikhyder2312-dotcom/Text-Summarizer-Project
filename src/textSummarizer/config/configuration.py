from src.textSummarizer.constants import *
from src.textSummarizer.utils.common import read_yaml, create_directories
from src.textSummarizer.entity import SummarizerConfig


class ConfigurationManager:

    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH
    ):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_summarizer_config(self) -> SummarizerConfig:

        config = self.config.summarizer
        params = self.params.summarizer
        

        create_directories([config.root_dir])

        summarizer_config = SummarizerConfig(
            root_dir=config.root_dir,
            abstractive_model_name=params.abstractive.model_name,
            abstractive_max_input_length=params.abstractive.max_input_length,
            abstractive_max_new_tokens=params.abstractive.max_new_tokens,
            abstractive_num_beams=params.abstractive.num_beams,
            abstractive_no_repeat_ngram_size=params.abstractive.no_repeat_ngram_size,
            abstractive_min_input_words=params.abstractive.min_input_words,
            extractive_model_name=params.extractive.model_name,
            extractive_top_n_sentences=params.extractive.top_n_sentences
        )

        return summarizer_config