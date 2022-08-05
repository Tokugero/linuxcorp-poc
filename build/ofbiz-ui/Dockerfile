# https://github.com/sandeepkose/OFBiz-Docker/blob/master/Dockerfile
# OpenJdk IMAGE


FROM openjdk:8-jdk-alpine as build

ENV OFBIZ_VERSION="18.12.05"

RUN apk update && apk upgrade && apk add \
        wget \
        unzip && \
    wget -O ofbiz.zip https://dlcdn.apache.org/ofbiz/apache-ofbiz-${OFBIZ_VERSION}.zip && \
    unzip ofbiz.zip -d ofbiz

FROM openjdk:8-jdk-alpine

# Install necessary packages and desirable debug tools
RUN apk update && \
    apk upgrade && \
    apk add git \
        bash \
        subversion \
        mysql-client

COPY --from=build ofbiz/ /usr/local/apache-ofbiz/

WORKDIR /root/

#TODO: Add startup script for https://tecadmin.net/steps-to-install-apache-ofbiz-on-linux-system/