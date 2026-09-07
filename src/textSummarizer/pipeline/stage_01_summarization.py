from src.textSummarizer.config.configuration import ConfigurationManager
from src.textSummarizer.components.summarizer import Summarizer
from src.textSummarizer.logging import logger


class SummarizationPipeline:

    def __init__(self):
        pass

    def main(self):

        config = ConfigurationManager()

        summarizer_config = config.get_summarizer_config()

        summarizer = Summarizer(config=summarizer_config)

        logger.info("Summarizer initialized successfully")

        # Test input
        text = """
        Amazon Web Services is a cloud computing platform that provides
        services such as EC2, S3, RDS, Lambda, and VPC. EC2 allows users
        to run virtual servers in the cloud. S3 provides scalable object
        storage, while RDS makes it easier to manage relational databases.
        AWS also provides networking services such as VPC, load balancers,
        and Route 53.
        """

        # Extractive summary
        extractive = summarizer.extractive_summary(text)

        logger.info(f"Extractive Summary: {extractive}")

        # Abstractive summary
        abstractive = summarizer.abstractive_summary(text)

        logger.info(f"Abstractive Summary: {abstractive}")