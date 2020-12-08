FROM alpine:3.11

ENV PYTHON_VERSION=3.8.2-r1
ENV APP_PORT 8080
ENV BUTTERROBOT_VERSION 0.0.3
ENV EXTRA_DEPENDENCIES ""
ENV APP_PATH /etc/butterrobot

COPY bin/start-server.sh /usr/local/bin/start-server
RUN apk --update add curl python3-dev==${PYTHON_VERSION} gcc musl-dev libffi-dev openssl-dev && \
    pip3 install butterrobot==${BUTTERROBOT_VERSION} ${EXTRA_DEPENDENCIES} && \
    mkdir ${APP_PATH} && \
    chown -R 1000:1000 ${APP_PATH}

USER 1000

CMD ["/usr/local/bin/start-server"]
