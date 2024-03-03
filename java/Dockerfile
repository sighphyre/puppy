ARG TAG=main

FROM openjdk:11-jdk

RUN apt-get update && apt-get install -y git

RUN apt-get install -y maven

ARG GRADLE_VERSION=8.6
RUN wget https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip -P /tmp
RUN unzip -d /opt/gradle /tmp/gradle-${GRADLE_VERSION}-bin.zip
ENV GRADLE_HOME=/opt/gradle/gradle-${GRADLE_VERSION}
ENV PATH=${GRADLE_HOME}/bin:${PATH}

WORKDIR /usr/src/base/sdk

COPY ./unleash-client-java .
RUN git checkout $TAG
RUN mvn clean install -DskipTests

WORKDIR /usr/src/base/harness

COPY ./harness .

RUN ./gradlew build --no-daemon --refresh-dependencies

CMD ["./gradlew", "run", "--no-daemon", "-q"]