FROM python:3.11-slim

WORKDIR /app

COPY requirement.txt requirement.txt

RUN pip install --no-cache-dir -r requirement.txt

COPY .env .env

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]