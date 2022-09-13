FROM python:3.9-slim

WORKDIR /app

ADD ./ ./

RUN apt update && \
    # dependencies for `WeasyPrint`
    apt install -y libpango1.0-dev libcairo2-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    # TODO maybe this could be dealt with using multi-stage builds
    pip install -r requirements.dev.txt

VOLUME /app
VOLUME /data

ENTRYPOINT ["/app/toc.py"]
