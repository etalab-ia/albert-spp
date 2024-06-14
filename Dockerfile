FROM python:3.10-slim

RUN addgroup --gid 1101 albert && \
    adduser --uid 1100 --gid 1101 --home /code albert

WORKDIR /code

# add requirements.txt before the rest of the code to cache the pip install
ADD ./pyproject.toml /code/api/pyproject.toml
RUN pip install --no-cache-dir /code/api/.

# add the rest of the code
ENV PYTHONPATH="$PYTHONPATH:/code/api"
ADD . /code/api

USER albert
