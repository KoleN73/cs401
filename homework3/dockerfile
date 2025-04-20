FROM python:3.10-slim
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && \
    pip install pytest

CMD ["python", "analyze_data.py", "data.json"]