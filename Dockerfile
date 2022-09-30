FROM python:3.6

RUN pip install locustio==0.14.6 ujson web3

EXPOSE 8089

ARG FILE_POSTFIX

ENV HOST http://localhost:8282
ENV LOCSUTFILE locustfile-${FILE_POSTFIX}.py

RUN mkdir -p /data/
WORKDIR /data/
ADD locustfile-${FILE_POSTFIX}.py /data/
ADD tx_out.json /data/
ADD token.json /data/
ADD wallets.json /data/
ADD env.json /data/

CMD locust -f ${LOCSUTFILE} --host=${HOST} -t 60 -r 300 -c 12000 --no-web
