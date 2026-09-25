FROM golang:1.27-alpine AS builder

RUN apk add --update --no-cache --force-overwrite git make 
WORKDIR /
RUN git clone https://codeberg.org/emersion/kimchi \
    && cd kimchi \
    && git checkout a1aadc0bccd25612c366ea5d24b634cc39206bee

WORKDIR /kimchi
RUN make kimchi

FROM alpine:3

COPY --from=builder /kimchi/kimchi /usr/bin/kimchi
COPY kimchi.conf /kimchi.conf

USER nobody
WORKDIR /
EXPOSE 443
ENTRYPOINT ["/usr/bin/kimchi", "-config", "/kimchi.conf"]
