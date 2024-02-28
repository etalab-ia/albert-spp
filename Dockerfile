FROM python:3.10-slim

ENV PYTHONPATH="$PYTHONPATH:/code/api"

WORKDIR /code
ADD . api
RUN pip install --no-cache-dir --upgrade -r ./api/requirements.txt

CMD ["uvicorn", "api.app:app", "--proxy-headers", "--root-path", "/", "--forwarded-allow-ips='*'", "--host", "0.0.0.0", "--port", "8000", "--reload"]
