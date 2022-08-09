FROM python:3.7-slim

ENV PORT=8000

WORKDIR /app
COPY templates /app/templates
COPY requirements.txt /app/requirements.txt
COPY repo.py /app/repo.py

EXPOSE $PORT

RUN pip install -r requirements.txt
ENTRYPOINT ["python", "repo.py"]
