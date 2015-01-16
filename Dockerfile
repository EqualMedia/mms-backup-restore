FROM state/mongodb:2.6.7

ENV LANG en_US.UTF-8

RUN yum install -y python3-pip; \
    pip-python3 install requests

ADD fetch_snapshot.py /opt/fetch_snapshot.py
ADD restore.sh /opt/restore.sh

VOLUME /data
WORKDIR /data

CMD /opt/restore.sh
