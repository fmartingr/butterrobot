FROM alpine:3.11

ENV PYTHON_VERSION=3.8.2-r0
ENV APP_PORT 8080
ENV BUTTERROBOT_VERSION 0.0.2
ENV EXTRA_DEPENDENCIES ""

COPY bin/start-server.sh /usr/local/bin/start-server
RUN apk --update add python3-dev==${PYTHON_VERSION} gcc musl-dev libffi-dev openssl-dev && \
    pip3 install butterrobot==${BUTTERROBOT_VERSION} ${EXTRA_DEPENDENCIES}

USER 1000

CMD ["/usr/local/bin/start-server"]
