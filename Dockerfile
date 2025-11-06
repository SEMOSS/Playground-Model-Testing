FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync

# Copy source code
COPY src/ ./src/
COPY server_src/ ./server_src/
COPY server.py ./

# Expose FastAPI port
EXPOSE 8888

# Run FastAPI server
CMD ["uv", "run", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8888"]
