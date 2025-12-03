# Use official Python base image
FROM python:3.9

# Set working directory inside container
WORKDIR /app

# Copy everything from current folder to container
COPY . .

# Install dependencies (FastAPI, Uvicorn, etc.)
RUN pip install fastapi uvicorn[standard]

# Expose port 8000 for the API
EXPOSE 8000

# Run FastAPI app (from backend/main.py)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
