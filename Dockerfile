FROM tarantool/tarantool:3.1.1

WORKDIR /opt/tarantool

# Устанавливаем Python и необходимые инструменты
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# Копируем requirements.txt, если он есть, и устанавливаем зависимости
COPY requirements.txt /opt/tarantool/requirements.txt
RUN pip3 install -r /opt/tarantool/requirements.txt

# Копируем setup.sh в контейнер
COPY setup.sh /opt/tarantool/setup.sh

# Копируем app.py в контейнер
COPY app.py /opt/tarantool/app.py

USER root
RUN chmod +x /opt/tarantool/setup.sh

EXPOSE 8001
# Выполняем setup.sh при старте контейнера
CMD ["bash", "-c", "./setup.sh && tail -f /dev/null"]
