FROM python:3.10-slim

ENV PYTHONPATH="$PYTHONPATH:/code/api"

RUN addgroup -S albert -g 1100 && \
    adduser -S albert  -u 1001 -G  --h /code

WORKDIR /code
ADD . api
RUN pip install --no-cache-dir --upgrade -r ./api/requirements.txt

USER albert
