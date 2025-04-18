FROM python:3.9-slim

WORKDIR /app

# Install system dependencies required for TensorFlow, OpenCV, and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    wget \
    curl \
    libopenblas-dev \
    python3-dev \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for better TensorFlow performance
ENV PYTHONUNBUFFERED=1
ENV TF_ENABLE_ONEDNN_OPTS=0
ENV TF_CPP_MIN_LOG_LEVEL=2
ENV PYTHONPATH=/app
ENV PIP_NO_CACHE_DIR=1
ENV KERAS_BACKEND=tensorflow

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python packages with error checking and version control
RUN pip install --no-cache-dir --upgrade pip && \
    # Install core dependencies first
    pip install --no-cache-dir fastapi==0.103.1 uvicorn==0.23.2 pydantic==2.3.0 && \
    # Install database dependencies
    pip install --no-cache-dir sqlalchemy==2.0.20 psycopg2-binary==2.9.7 && \
    # Install authentication dependencies
    pip install --no-cache-dir python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 && \
    # Install utility dependencies
    pip install --no-cache-dir python-dotenv==1.0.0 python-multipart==0.0.6 email-validator==2.2.0 && \
    # Install ML dependencies in specific order
    pip install --no-cache-dir numpy==1.23.5 && \
    pip install --no-cache-dir scipy==1.10.1 && \
    pip install --no-cache-dir tensorflow==2.12.0 && \
    pip install --no-cache-dir keras==2.12.0 && \
    pip install --no-cache-dir pillow==10.0.1 && \
    pip install --no-cache-dir opencv-python==4.8.0.76 && \
    # Install LLM dependencies
    pip install --no-cache-dir torch==2.0.1 && \
    pip install --no-cache-dir torchvision==0.15.2 && \
    pip install --no-cache-dir transformers==4.33.3 && \
    pip install --no-cache-dir accelerate==0.23.0 && \
    pip install --no-cache-dir timm==0.9.2 && \
    # Install OpenAI package
    pip install --no-cache-dir openai==1.74.0 && \
    # Pre-download MiDaS model
    python -c "import torch; torch.hub.load('intel-isl/MiDaS', 'DPT_Large')" && \
    # Install development dependencies
    pip install --no-cache-dir pytest==7.4.2 httpx==0.25.0 gunicorn==21.2.0 && \
    # Install pandas for data loading
    pip install --no-cache-dir pandas==2.0.3 && \
    # Verify installations
    python -c "import tensorflow as tf; print(f'TensorFlow version: {tf.__version__}')" && \
    python -c "import numpy as np; print(f'NumPy version: {np.__version__}')" && \
    python -c "import keras; print(f'Keras version: {keras.__version__}')" && \
    python -c "import cv2; print(f'OpenCV version: {cv2.__version__}')" && \
    python -c "import torchvision; print(f'torchvision version: {torchvision.__version__}')" && \
    python -c "import timm; print(f'timm version: {timm.__version__}')" && \
    python -c "import openai; print(f'OpenAI version: {openai.__version__}')"

# Pre-download MiDaS model
RUN python -c "import torch; torch.hub.load('intel-isl/MiDaS', 'DPT_Large'); print('MiDaS model downloaded successfully')"

# Copy the rest of the application
COPY . .

# Make sure the models directory exists and has correct permissions
RUN mkdir -p /app/models && \
    chmod -R 755 /app/models

# Create a healthcheck script
RUN echo '#!/bin/bash\n\
python -c "import tensorflow as tf; import numpy as np; import keras; import cv2; import torchvision; import timm; import openai; print(\"All ML dependencies working correctly\")"' > /app/healthcheck.sh && \
    chmod +x /app/healthcheck.sh

# Expose the port the app runs on
EXPOSE 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD /app/healthcheck.sh

# Command to run the application with error handling
CMD ["sh", "-c", "\
    echo 'Starting application...' && \
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload"] 