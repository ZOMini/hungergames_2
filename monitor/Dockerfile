FROM python:3.11-slim
WORKDIR /monitor
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
COPY . .
# CMD ["gunicorn", "wsgi_app:app", "--bind", "0.0.0.0:5000", "--reload"]
