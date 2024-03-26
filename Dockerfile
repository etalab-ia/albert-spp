FROM python:3.10-slim

RUN addgroup --gid 1100 albert && \
    adduser --uid 1001 --gid 1100 --home /code albert

WORKDIR /code

# add requirements.txt before the rest of the code to cache the pip install
ADD ./requirements.txt /code/api/requirements.txt
RUN pip install --no-cache-dir -r /code/api/requirements.txt

# add the rest of the code
ENV PYTHONPATH="$PYTHONPATH:/code/api"
ADD . /code/api

USER albert
