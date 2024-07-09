ARG TAG=main

FROM node:16

RUN apt-get update && apt-get install -y git

WORKDIR /usr/src/base/sdk/unleash-client-node

COPY ./unleash-client-node .

RUN yarn link

WORKDIR /usr/src/base/sdk

RUN git checkout $TAG
RUN yarn install
RUN yarn build
RUN yarn link

WORKDIR /usr/src/base/harness

COPY ./harness/* .

RUN yarn link unleash-client

CMD ["node", "index.js"]
