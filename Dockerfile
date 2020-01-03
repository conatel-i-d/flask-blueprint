FROM python:3.7

EXPOSE 80/tcp
EXPOSE 9191/tcp

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
  libatlas-base-dev \
  gfortran \
  nginx \
  supervisor

RUN pip3 install uswgi psycopg2

RUN useradd --no-create-home nginx
RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY nginx.conf /etc/nginx
COPY flask-nginx.conf /etc/nginx/conf.d/
COPY uswgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/usr/bin/supervisord"]

