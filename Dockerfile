FROM python:3.6

RUN pip install locustio==0.14.6 ujson

EXPOSE 8089

ENV HOST http://localhost:8282

RUN mkdir -p /data/
WORKDIR /data/
ADD locustfile.py /data/
ADD tx_out.json /data/
ADD token.json /data/
ADD wallets.json /data/

CMD locust -f locustfile.py --host=${HOST} -t 45 -r 150 -c 10000 --no-web
