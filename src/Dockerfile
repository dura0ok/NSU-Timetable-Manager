FROM python:3.9-slim

WORKDIR /app

COPY ./server /app

RUN pip install --no-cache-dir -r requirements.txt

ENV HOST 0.0.0.0

CMD ["python", "app.py", "--reload"]

