FROM python:3.7.2-alpine3.7

ENV LANG C.UTF-8

RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
        git \
        nodejs && \
    npm config set unsafe-perm true && \
    npm install codefresh -g

COPY script/pipeline_creator.py /pipeline_creator.py

ENTRYPOINT ["python", "/pipeline_creator.py"]
