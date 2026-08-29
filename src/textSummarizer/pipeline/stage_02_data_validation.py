from src.textSummarizer.config.configuration import ConfigurationManager
from src.textSummarizer.components.data_validation import Datavalidation
from src.textSummarizer.logging import logger


class DatavalidationTrainingPipeline:    
    def __init__(self) -> None:
        pass
        
    def main(self)  :  
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = Datavalidation(config=data_validation_config)
        data_validation.validate_all_files_exist()