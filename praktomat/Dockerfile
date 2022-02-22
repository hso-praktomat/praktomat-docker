# syntax=docker/dockerfile:1
FROM ubuntu:bionic
EXPOSE 8000/tcp

# Install system requirements
RUN apt-get update
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install -yq apache2 apache2-dev libpq-dev zlib1g-dev libmysqlclient-dev libsasl2-dev libssl-dev libffi-dev swig libapache2-mod-xsendfile libapache2-mod-wsgi-py3 openjdk-8-jdk junit junit4 dejagnu r-base git-core python3-setuptools python3-psycopg2 python3-virtualenv python3-pip sudo

# Add users
RUN useradd -m praktomat && adduser praktomat sudo
RUN useradd -m tester && adduser tester sudo && adduser tester praktomat
COPY sudoers /etc/sudoers
RUN chmod 440 /etc/sudoers

USER praktomat
WORKDIR /home/praktomat
RUN git clone --recursive git://github.com/KITPraktomatTeam/Praktomat.git && cd Praktomat && git checkout 0279d68967eb32b4716240eb8844abba4ec8ecfa
RUN sudo chown praktomat:tester Praktomat/src/checker/scripts/java
RUN sudo chown praktomat:tester Praktomat/src/checker/scripts/javac
RUN sudo chmod u+x,g+x,o-x Praktomat/src/checker/scripts/java
RUN sudo chmod u+x,g+x,o-x Praktomat/src/checker/scripts/javac

# Get wait-for-it.sh (used to wait for PostgreSQL to become available)
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/81b1373f17855a4dc21156cfe1694c31d7d1792e/wait-for-it.sh wait-for-it.sh
RUN sudo chmod 775 wait-for-it.sh

# Install Python requirements
RUN python3 -m pip install --upgrade pip && python3 -m pip install -U pip virtualenv setuptools wheel urllib3[secure]
RUN python3 -m pip install -r Praktomat/requirements.txt

# Install Praktomat addons
ADD https://github.com/jplag/jplag/releases/download/v2.12.1-SNAPSHOT/jplag-2.12.1-SNAPSHOT-jar-with-dependencies.jar /opt/praktomat-addons/jplag.jar
ADD https://github.com/checkstyle/checkstyle/releases/download/checkstyle-8.14/checkstyle-8.14-all.jar /opt/praktomat-addons/checkstyle-8.14-all.jar
RUN sudo chown -R praktomat:praktomat /opt/praktomat-addons

# Copy config files
COPY local.py Praktomat/src/settings/local.py
COPY apache_praktomat_wsgi.conf Praktomat/documentation/apache_praktomat_wsgi.conf
RUN printf "\nInclude /home/praktomat/Praktomat/documentation/apache_praktomat_wsgi.conf\nUse Praktomat hso /home/praktomat/\n" | sudo tee -a /etc/apache2/apache2.conf && sudo a2enmod macro

# Setup required directories
RUN mkdir debug-data
RUN mkdir work-data
RUN mkdir test-data

# Initialize Praktomat
RUN python3 Praktomat/src/manage-local.py collectstatic --noinput --link

ENTRYPOINT ./wait-for-it.sh postgresql:5432 -- python3 Praktomat/src/manage-local.py migrate --noinput && python3 Praktomat/src/manage-local.py runserver --insecure 0.0.0.0:8000
