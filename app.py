from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.textSummarizer.pipeline.prediction_pipeline import PredictionPipeline


app = FastAPI(
    title="Text Summarization API",
    description="Extractive and Abstractive Text Summarization API",
    version="1.0.0"
)

app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return FileResponse("frontend/dist/index.html")


@app.post("/summarize")
def summarize(request: TextRequest):

    result = pipeline.predict(request.text)

    return result