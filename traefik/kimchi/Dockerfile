FROM golang:1.25-alpine AS builder

RUN apk add --update --no-cache --force-overwrite git make 
WORKDIR /
RUN git clone https://codeberg.org/emersion/kimchi \
    && cd kimchi \
    && git checkout e503b13cdcafcc8633c3cc2878c2b3af04dcdf97

WORKDIR /kimchi
RUN make kimchi

FROM alpine:3

COPY --from=builder /kimchi/kimchi /usr/bin/kimchi
COPY kimchi.conf /kimchi.conf

USER nobody
WORKDIR /
EXPOSE 443
ENTRYPOINT ["/usr/bin/kimchi", "-config", "/kimchi.conf"]
