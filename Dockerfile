FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim AS builder
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY ant_api ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]