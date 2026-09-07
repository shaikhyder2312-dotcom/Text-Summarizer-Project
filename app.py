from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.textSummarizer.pipeline.prediction_pipeline import PredictionPipeline


app = FastAPI(
    title="Text Summarization API",
    description="Extractive and Abstractive Text Summarization API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load the models once when the application starts
pipeline = PredictionPipeline()


class TextRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "message": "Text Summarization API is running"
    }


@app.post("/summarize")
def summarize(request: TextRequest):

    result = pipeline.predict(request.text)

    return result