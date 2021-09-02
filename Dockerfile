FROM python:3.9
ENV ELK_HOST="" \
    ELK_PORT="" \
    PYTHOPYTHONUNBUFFERED=1
COPY requirements.txt /tmp/
EXPOSE 8000
RUN apt-get update && \
    apt-get install -y apache2 apache2-dev && \
    pip3 install --default-timeout=100 -r tmp/requirements.txt && \
    mkdir cip && mkdir /static && \
WORKDIR ./cip
COPY . .
CMD /bin/bash -c 'python3 manage.py collectstatic --no-input && python3 manage.py runmodwsgi --setup-only --host 0.0.0.0 --user www-data --group www-data --server-root=/etc/mod_wsgi-express-8000 --log-to-terminal && /etc/mod_wsgi-express-8000/apachectl -D FOREGROUND'