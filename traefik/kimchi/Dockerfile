FROM golang:1.24-alpine AS builder

RUN apk add --update --no-cache --force-overwrite git make 
WORKDIR /
RUN git clone https://codeberg.org/emersion/kimchi \
    && cd kimchi \
    && git checkout 63ffe933897eadaceb4b502a4ee7570b8f84f40e

WORKDIR /kimchi
RUN make kimchi

FROM alpine:3

COPY --from=builder /kimchi/kimchi /usr/bin/kimchi
COPY kimchi.conf /kimchi.conf

USER nobody
WORKDIR /
EXPOSE 443
ENTRYPOINT ["/usr/bin/kimchi", "-config", "/kimchi.conf"]
