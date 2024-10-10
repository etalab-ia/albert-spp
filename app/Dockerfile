FROM python:3.12-slim

RUN groupadd --gid 1100 albert
RUN useradd --home /home/albert --gid 1100 --uid 1100 albert 
USER albert

WORKDIR /home/albert
ADD ./pyproject.toml ./pyproject.toml
RUN pip install .
ADD ./app /home/albert/app
ENV PYTHONPATH="/home/albert/app:${PYTHONPATH}"
ENV PATH="/home/albert/.local/bin:${PATH}"