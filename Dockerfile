# =========================
# Stage 1: Build React frontend
# =========================
FROM node:22-alpine AS frontend-build

WORKDIR /frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


# =========================
# Stage 2: FastAPI backend
# =========================
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

COPY requirements-prod.txt .

# Install CPU-only PyTorch
RUN pip install --no-cache-dir \
    torch==2.12.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining dependencies
RUN pip install --no-cache-dir -r requirements-prod.txt

# Install spaCy English model
RUN python -m spacy download en_core_web_lg

COPY . .

# Copy React production build
COPY --from=frontend-build /frontend/dist /app/frontend/dist

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]