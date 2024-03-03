ARG TAG=main

FROM python:3.9

RUN apt-get update && apt-get install -y git

WORKDIR /usr/src/base/sdk

COPY ./unleash-client-python .

RUN git checkout $TAG
RUN pip install setuptools wheel setuptools_scm
RUN pip install .

WORKDIR /usr/src/base/harness

COPY ./harness/* .

CMD ["python", "main.py"]
