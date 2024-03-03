ARG TAG=main

FROM ruby:3.1

RUN apt-get update && apt-get install -y git

WORKDIR /usr/src/base/sdk

COPY ./unleash-client-ruby .

RUN git checkout $TAG
RUN bundle install
RUN gem build unleash-client.gemspec
RUN gem install ./unleash-5.0.0.gem

WORKDIR /usr/src/base/harness

COPY ./runner/* .

CMD ["ruby", "main.rb"]