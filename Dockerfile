# syntax=docker/dockerfile:1
FROM ubuntu:bionic
EXPOSE 8000/tcp

RUN apt-get update
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install -yq postgresql apache2 libpq-dev zlib1g-dev libmysqlclient-dev libsasl2-dev libssl-dev swig libapache2-mod-xsendfile libapache2-mod-wsgi-py3 openjdk-8-jdk junit junit4 dejagnu r-base git-core python3-setuptools python3-psycopg2 python3-virtualenv python3-pip sudo
RUN useradd -m praktomat && adduser praktomat sudo
COPY sudoers /etc/sudoers
RUN chmod 440 /etc/sudoers

USER postgres
RUN /etc/init.d/postgresql start && createuser -DRS praktomat && createdb -O praktomat praktomat_default

USER praktomat
WORKDIR /home/praktomat
RUN pip3 install --upgrade pip && pip3 install -U pip virtualenv setuptools wheel urllib3[secure]
RUN git clone --recursive git://github.com/KITPraktomatTeam/Praktomat.git
RUN pip3 install -r Praktomat/requirements.txt
COPY local.py Praktomat/src/settings/local.py
ADD https://github.com/jplag/jplag/releases/download/v2.12.1-SNAPSHOT/jplag-2.12.1-SNAPSHOT-jar-with-dependencies.jar /srv/praktomat/contrib/jplag.jar
ADD https://github.com/checkstyle/checkstyle/releases/download/checkstyle-5.8/checkstyle-5.8-all.jar /srv/praktomat/contrib/checkstyle.jar
RUN sudo /etc/init.d/postgresql start && mkdir PraktomatSupport && python3 Praktomat/src/manage-local.py collectstatic --noinput --link && python3 Praktomat/src/manage-local.py migrate --noinput

ENTRYPOINT sudo /etc/init.d/postgresql start && python3 Praktomat/src/manage-local.py runserver --insecure 0.0.0.0:8000
