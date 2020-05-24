FROM python:3.7.3-alpine3.9 as dailycomicsbase
MAINTAINER jcoady9 jcoady927@gmail.com

FROM dailycomicsbase as packagesbuilder

RUN mkdir /install

WORKDIR /install

COPY requirements.txt /requirements.txt

RUN apk add --update --no-cache g++ libxslt-dev libxml2-dev && \  
  pip install --install-option="--prefix=/install" --no-cache-dir --trusted-host pypi.python.org -r /requirements.txt



FROM dailycomicsbase

# Please change this...
ENV DJANGO_COMICS_KEY itsasecrettoeverybody

ADD dailycomics-cron /etc/cron.d/dailycomics-cron

COPY --from=packagesbuilder /install /usr/local

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
