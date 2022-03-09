FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive
ENV TZ Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update
RUN apt-get install -y wget
COPY install-tivoli /tmp/install-tivoli
RUN bash /tmp/install-tivoli
