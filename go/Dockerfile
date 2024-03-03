FROM golang:1.22

WORKDIR /usr/src/sdk

COPY ./unleash-client-go .

WORKDIR /usr/src/harness

COPY ./harness/* .

RUN go build main.go

CMD ["./main"]