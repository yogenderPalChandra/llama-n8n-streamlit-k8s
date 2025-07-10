# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/rag_pipeline/db

RUN chmod -R 777 /app/rag_pipeline/db

# Set environment variable to point to the Ollama service in your Kubernetes cluster
ENV OLLAMA_HOST=http://ollama-service.ollama.svc.cluster.local:8000

# Default command
CMD ["python", "main2.py"]
