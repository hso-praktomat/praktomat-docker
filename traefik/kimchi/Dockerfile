FROM golang:1.22-alpine as builder

RUN apk add --update --no-cache --force-overwrite git make 
WORKDIR /
RUN git clone https://git.sr.ht/~emersion/kimchi \
    && cd kimchi \
    && git checkout 4b663f91b4bc7bb1a7d8257a436ef4c552f7875b

WORKDIR /kimchi
RUN make kimchi

FROM alpine:3

COPY --from=builder /kimchi/kimchi /usr/bin/kimchi
COPY kimchi.conf /kimchi.conf

USER nobody
WORKDIR /
EXPOSE 443
ENTRYPOINT ["/usr/bin/kimchi", "-config", "/kimchi.conf"]
