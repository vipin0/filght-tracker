FROM python:3.9-slim-buster

WORKDIR /app
RUN apt update \
    && apt-get -y install supervisor vim

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt \
    && mkdir -p /var/log/slack_bot
COPY supervisor.conf /etc/supervisor/conf.d/
COPY . .
# CMD [ "python3","slack_bot.py"]
# ENTRYPOINT ["service","supervisor","start"]
ENTRYPOINT [ "/usr/bin/supervisord" ]