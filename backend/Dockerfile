FROM python:3.6.3-onbuild
MAINTAINER jussker "jussker_dev@126.com"

COPY docker-settings.py /usr/src/app/taiga-back/settings/local.py
COPY locale.gen /etc/locale.gen
COPY default.locale /etc/default/locale

RUN apt-get update  && apt-get autoremove -y && apt-get install locales -y
RUN locale-gen en_US.UTF-8 && dpkg-reconfigure locales

WORKDIR /usr/src/app/taiga-back

EXPOSE 8000

ENV POSTGRES_DB=taiga
ENV POSTGRES_HOST=postgresdb
ENV POSTGRES_USER=taiga
ENV POSTGRES_PASSWORD=taiga
ENV API_BASE_PROTOCOL=http
ENV API_BASE_DOMAIN=taigaback
ENV API_BASE_PORT=8000
ENV FRONT_BASE_PROTOCOL=http
ENV FRONT_BASE_DOMAIN=taigfront
ENV FRONT_BASE_PORT=9001
ENV MEDIA_URL=http://taigaback:8000/media/
ENV STATIC_URL=http://taigaback:8000/static/
ENV DEFAULT_FROM_EMAIL=no-replay@example.com
ENV EMAIL_USE_TLS=False
ENV EMAIL_HOST=mail.example.com
ENV EMAIL_PORT=25
ENV EMAIL_HOST_USER=example
ENV EMAIL_HOST_PASSWORD=example
ENV EMAIL_SUBJECT_PREFIX=no-replay

# Volume definition in docker-compose.yml instead of here, soon
VOLUME ["/usr/src/app/taiga-back/static","/usr/src/app/taiga-back/media"]

RUN locale -a

RUN (cd /usr/src/app/taiga-back/ && python /usr/src/app/taiga-back/manage.py collectstatic --noinput)

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
