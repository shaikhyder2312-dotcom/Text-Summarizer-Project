from src.textSummarizer.config.configuration import ConfigurationManager
from src.textSummarizer.components.summarizer import Summarizer


class PredictionPipeline:

    def __init__(self):

        config = ConfigurationManager()

        summarizer_config = config.get_summarizer_config()

        self.summarizer = Summarizer(
            config=summarizer_config
        )

    def predict(self, text: str):

        extractive_summary = self.summarizer.extractive_summary(text)

        abstractive_summary = self.summarizer.abstractive_summary(text)

        return {
            "extractive_summary": extractive_summary,
            "abstractive_summary": abstractive_summary
        }
        
if __name__ == "__main__":

    pipeline = PredictionPipeline()

    text = """
    Amazon Web Services is a cloud computing platform that provides
    services such as EC2, S3, RDS, Lambda, and VPC. EC2 allows users
    to run virtual servers in the cloud. S3 provides scalable object
    storage, while RDS makes it easier to manage relational databases.
    AWS also provides networking services such as VPC, load balancers,
    and Route 53.
    """

    result = pipeline.predict(text)

    print("Extractive Summary:")
    print(result["extractive_summary"])

    print("\nAbstractive Summary:")
    print(result["abstractive_summary"])