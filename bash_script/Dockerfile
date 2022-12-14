FROM kalilinux/kali-rolling:latest as build

WORKDIR /scripts

RUN mkdir -p /root/.config/haktools
RUN mkdir -p /root/.config/subfinder

COPY provider-config.yaml /root/.config/haktools
COPY haktrails-config.yml /root/.config/subfinder