FROM python:3.7.3-alpine3.9
MAINTAINER jcoady9 jcoady927@gmail.com

# Please change this...
ENV DJANGO_COMICS_KEY itsasecrettoeverybody

WORKDIR /dailycomicsproject

COPY . /dailycomicsproject

ADD dailycomics-cron /etc/cron.d/dailycomics-cron

# Install dependencies
RUN apk add --update --no-cache g++ libxslt-dev libxml2-dev tzdata && \
  pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt && \
  cp /usr/share/zoneinfo/America/Chicago /etc/localtime && \
  echo "America/Chicago" > /etc/timezone && \
  apk del tzdata g++ && \
  chmod 0644 /etc/cron.d/dailycomics-cron && \
  crontab /etc/cron.d/dailycomics-cron && \
  mkdir /var/dailycomics && \
  python manage.py migrate

VOLUME ["/var/dailycomics"]

EXPOSE 8000

CMD ["sh", "-c", "crond -b -l 2 && gunicorn dailycomicsproject.wsgi:application --bind 0.0.0.0:8000 --workers 1 "]
