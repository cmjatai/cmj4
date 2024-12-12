FROM leandrojatai/building_foundation:0001

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND noninteractive

RUN mkdir -p /var/cmjatai/cmj4/run
RUN mkdir -p /var/cmjatai/cmj4/logs/celery
RUN mkdir -p /var/cmjatai/cmj_data
RUN mkdir -p /var/cmjatai/cmj_media
RUN mkdir -p /var/cmjatai/BD_POSTGRESQL

WORKDIR /var/cmjatai/cmj4/

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
