FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install uv \
    && uv pip install --system --no-cache -r requirements.txt \
    && pip uninstall -y uv

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]