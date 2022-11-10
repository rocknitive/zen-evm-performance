FROM python:3.7

EXPOSE 8089

ENV HOST http://localhost:8282
ENV LOGFILE /output/locust-log.out

ENV LOCUST_TAG all
ENV CSV_PREFIX csv

ENV BENCHMARK_TIME 15
ENV SPAWN_RATE 10
ENV USER_COUNT 1200

RUN mkdir -p /data/
WORKDIR /data/

ADD requirements.txt /data/
RUN pip install -r requirements.txt

ADD locustfile.py /data/
ADD tx_out.json /data/
ADD token.json /data/
ADD wallets.json /data/

CMD locust -f locustfile.py \
    -H ${HOST} \
    -t ${BENCHMARK_TIME} \
    -r ${SPAWN_RATE} \
    -u ${USER_COUNT} \
    --headless \
    --tags ${LOCUST_TAG} \
    --autoquit 0 --autostart \
    --logfile ${LOGFILE}\
    --csv ${CSV_PREFIX}
