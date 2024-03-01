FROM python:3.10-slim

ENV PYTHONPATH="$PYTHONPATH:/code/api"

RUN addgroup --gid 1100 albert && \
    adduser --uid 1001 --gid 1100 --home /code albert

WORKDIR /code
ADD . api
RUN pip install --no-cache-dir --upgrade -r ./api/requirements.txt

USER albert
