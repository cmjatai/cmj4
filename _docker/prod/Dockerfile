FROM python:3.12.7-bookworm

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND noninteractive

ENV BUILD_PACKAGES apt-utils apt-file libpq-dev graphviz-dev build-essential pkg-config \
                   python3-dev libxml2-dev libjpeg-dev libssl-dev libffi-dev libxslt1-dev \
                   libcairo2-dev software-properties-common python3-setuptools python3-pip \
                   procps nmap

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends $BUILD_PACKAGES

ENV RUN1_PACKAGES git graphviz python3-lxml python3-magic postgresql-client  \
                 poppler-utils curl jq bash vim python3-venv tzdata nodejs nginx
RUN apt-get install -y --no-install-recommends $RUN1_PACKAGES

ENV RUN2_PACKAGES fontconfig fonts-liberation openjdk-17-jdk-headless
RUN apt-get install -y --no-install-recommends $RUN2_PACKAGES

ENV RUN3_PACKAGES tesseract-ocr tesseract-ocr-por ghostscript python3-psycopg
RUN apt-get install -y --no-install-recommends $RUN3_PACKAGES

ENV LIBRE_PACKAGES libreoffice \
                    libreoffice-writer \
                    ure \
                    libreoffice-java-common \
                    libreoffice-core \
                    libreoffice-common \
                    fonts-opensymbol \
                    hyphen-pt-br \
                    fonts-dejavu \
                    fonts-dejavu-core \
                    fonts-dejavu-extra \
                    fonts-droid-fallback \
                    fonts-dustin \
                    fonts-f500 \
                    fonts-fanwood \
                    fonts-freefont-ttf \
                    fonts-lmodern \
                    fonts-lyx \
                    fonts-sil-gentium \
                    fonts-texgyre \
                    fonts-tlwg-purisa
RUN apt-get install -y -q $LIBRE_PACKAGES

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - &&\
    apt-get install -y nodejs

RUN fc-cache -fv && \
    pip3 install --no-cache-dir --upgrade pip setuptools

RUN rm -f /etc/nginx/conf.d/* && \
    rm -f /etc/nginx/sites-enabled/*
    #&& \
    #SUDO_FORCE_REMOVE=yes apt-get purge -y --auto-remove $BUILD_PACKAGES && \
    #apt-get -y autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN adduser --home=/opt/libreoffice --disabled-password --gecos "" --shell=/bin/bash libreoffice
ADD libreoffice_entrypoint.sh /opt/libreoffice/libreoffice_entrypoint.sh
RUN chmod +x /opt/libreoffice/libreoffice_entrypoint.sh

RUN mkdir -p /var/cmjatai/cmj4/run
RUN mkdir -p /var/cmjatai/cmj4/logs/celery
RUN mkdir -p /var/cmjatai/cmj_data
RUN mkdir -p /var/cmjatai/cmj_media
RUN mkdir -p /var/cmjatai/BD_POSTGRESQL

WORKDIR /var/cmjatai/cmj4/

ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip3 install poetry
COPY po* $HOME
COPY py* $HOME
RUN poetry install

ADD _docker     /var/cmjatai/cmj4/_docker
ADD _frontend   /var/cmjatai/cmj4/_frontend
ADD _templates  /var/cmjatai/cmj4/_templates

ADD cmj4        /var/cmjatai/cmj4/cmj4
ADD solr        /var/cmjatai/cmj4/solr

COPY .env $HOME
COPY manage.py $HOME
COPY package-lock.json $HOME
COPY package.json $HOME
COPY vite.config.js $HOME

RUN npm install
RUN npm run build

RUN python3 manage.py collectstatic --noinput --clear --settings=cmj4.settings.fake
RUN rm -rf /var/cmjatai/cmj4/db.sqlite3

#COPY key_cert.pfx $HOME

COPY _docker/prod/start.sh $HOME
COPY _docker/prod/wait-for-pg.sh $HOME
COPY _docker/prod/wait-for-solr.sh $HOME
COPY _docker/prod/start_gunicorn.sh $HOME
COPY _docker/prod/start_daphne.sh $HOME
COPY _docker/prod/solr_cli.py $HOME

COPY _docker/prod/nginx/cmj4_docker.conf /etc/nginx/conf.d/.
COPY _docker/prod/nginx/nginx_docker.conf /etc/nginx/nginx.conf

RUN chmod +x /var/cmjatai/cmj4/start.sh && \
    chmod +x /var/cmjatai/cmj4/start_gunicorn.sh && \
    chmod +x /var/cmjatai/cmj4/start_daphne.sh && \
    chmod +x /var/cmjatai/cmj4/wait-for-solr.sh && \
    chmod +x /var/cmjatai/cmj4/wait-for-pg.sh


# Debian não possui usuário 'nginx' necessário para o Debian
RUN useradd -r -u 1002 --no-create-home -g root nginx

USER nginx

ENV DEBIAN_FRONTEND teletype

EXPOSE 80/tcp 443/tcp

VOLUME ["/var/cmjatai/cmj4/data", "/var/cmjatai/cmj_media", "/var/cmjatai/cmj4/logs"]

CMD ["/var/cmjatai/cmj4/start.sh"]
