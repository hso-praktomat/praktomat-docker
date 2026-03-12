FROM golang:1.26-alpine AS builder

RUN apk add --update --no-cache --force-overwrite git make 
WORKDIR /
RUN git clone https://codeberg.org/emersion/kimchi \
    && cd kimchi \
    && git checkout 39ccb6546be9e94d4ab95179268eaff4cb81f4fa

WORKDIR /kimchi
RUN make kimchi

FROM alpine:3

COPY --from=builder /kimchi/kimchi /usr/bin/kimchi
COPY kimchi.conf /kimchi.conf

USER nobody
WORKDIR /
EXPOSE 443
ENTRYPOINT ["/usr/bin/kimchi", "-config", "/kimchi.conf"]
