FROM tarantool/tarantool:3.1.1

WORKDIR /opt/tarantool

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

COPY requirements.txt /opt/tarantool/requirements.txt
RUN pip3 install -r /opt/tarantool/requirements.txt

COPY setup.sh /opt/tarantool/setup.sh

COPY app.py /opt/tarantool/app.py

USER root
RUN chmod +x /opt/tarantool/setup.sh

EXPOSE 8001

CMD ["bash", "-c", "./setup.sh && tail -f /dev/null"]
