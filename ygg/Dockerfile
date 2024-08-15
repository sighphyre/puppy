ARG TAG=main

FROM rust:1.80

RUN apt-get update && apt-get install -y git

WORKDIR /usr/src/base/yggdrasil

COPY ./yggdrasil .

RUN cargo build --release

WORKDIR /usr/src/base/harness

COPY ./harness .

RUN cargo build --release

WORKDIR /usr/src/base/harness/target/release

CMD ["./harness"]