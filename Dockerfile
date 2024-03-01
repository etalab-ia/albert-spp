FROM python:3.10-slim

ENV PYTHONPATH="$PYTHONPATH:/code/api"

WORKDIR /code
ADD . api
RUN pip install --no-cache-dir --upgrade -r ./api/requirements.txt
