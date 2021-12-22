FROM python:3.7.3-alpine3.9 as dailycomicsbase
MAINTAINER jcoady9 jcoady927@gmail.com

# Please change this...
ENV DJANGO_COMICS_KEY itsasecrettoeverybody

COPY . /dailycomicsproject

WORKDIR /dailycomicsproject

# Install dependencies
RUN apk add --update --no-cache tzdata && \
  cp /usr/share/zoneinfo/America/Chicago /etc/localtime && \
  echo "America/Chicago" > /etc/timezone && \
  apk del tzdata && \
  chmod 0644 /etc/cron.d/dailycomics-cron && \
  crontab /etc/cron.d/dailycomics-cron && \
  mkdir /var/dailycomics && \
  python manage.py migrate

VOLUME ["/var/dailycomics"]

EXPOSE 8000

CMD ["sh", "-c", "crond -b -l 2 && gunicorn dailycomicsproject.wsgi:application --bind 0.0.0.0:8000 --workers 1 "]
