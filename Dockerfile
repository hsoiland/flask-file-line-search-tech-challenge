FROM python:3.10-slim as base

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app/ /app/

RUN mkdir /app/test-files

# For local dev purposes
# COPY test-files /app/test-files
WORKDIR /app

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0",  "--port=8279" ]

