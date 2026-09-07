from src.textSummarizer.pipeline.prediction_pipeline import PredictionPipeline
from src.textSummarizer.logging import logger


STAGE_NAME = "Prediction Pipeline"

try:

    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")

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

    print("\nExtractive Summary:")
    print(result["extractive_summary"])

    print("\nAbstractive Summary:")
    print(result["abstractive_summary"])

    logger.info(
        f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x"
    )

except Exception as e:

    logger.exception(e)
    raise e