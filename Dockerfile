FROM debian:latest
MAINTAINER Kostas Stamatiou <kostas.stamatiou@digitalglobe.com>

RUN apt-get update && apt-get install -y \
    gdal-bin \
    git \
    python \
    python-setuptools \
    && rm -rf /var/lib/apt/lists/*

# Install protogen
ARG PROTOUSER
ARG PROTOPASSWORD
RUN git clone https://${PROTOUSER}:${PROTOPASSWORD}@github.com/digitalglobe/protogen && \
    cd protogen && \
    python setup.py install && \
    cd ..

ADD lulc.py /
