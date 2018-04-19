FROM python:3.5-jessie

RUN pip install locustio ujson

EXPOSE 8089

ENV HOST http://localhost:8282

RUN mkdir -p /data/
WORKDIR /data/
ADD locustfile.py /data/
ADD tx_out.json /data/

CMD locust --host=${HOST}
