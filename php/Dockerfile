# Specify the tag as a build argument
ARG TAG=main

# Use an official PHP runtime as a parent image
FROM php:8.2-cli

ENV COMPOSER_ALLOW_SUPERUSER 1

RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" \
    && php composer-setup.php --install-dir=/usr/local/bin --filename=composer \
    && php -r "unlink('composer-setup.php');"

# Install Git
RUN apt-get update && apt-get install -y git

# Set the working directory for the SDK
WORKDIR /usr/src/base/unleash-client-php

# Copy the PHP SDK directory
COPY ./unleash-client-php .

# Checkout the specific Git tag
RUN git checkout $TAG

# Install the PHP SDK
# (Adjust this step according to how your PHP SDK is installed,
# e.g., using Composer or other PHP package management tools)
# For example, if you use Composer:
# COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --prefer-dist

# Set the working directory for the harness
WORKDIR /usr/src/base/harness

# Copy the harness code
COPY ./harness/* .

# Command to run the PHP application
# (Adjust the command according to the entry point of your application)
CMD ["php", "main.php"]
