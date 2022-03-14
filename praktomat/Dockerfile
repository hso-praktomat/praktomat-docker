# syntax=docker/dockerfile:1
FROM ubuntu:bionic
EXPOSE 443/tcp

# Setup timezone
ENV TZ Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install system requirements
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -yq \
  apache2 \
  apache2-dev \
  libpq-dev \
  zlib1g-dev \
  libmysqlclient-dev \
  libsasl2-dev \
  libssl-dev \
  libffi-dev \
  swig \
  libapache2-mod-xsendfile \
  libapache2-mod-wsgi-py3 \
  openjdk-17-jdk \
  junit \
  junit4 \
  dejagnu \
  r-base \
  git-core \
  libldap2-dev \
  python3-setuptools \
  python3-psycopg2 \
  python3-virtualenv \
  python3-pip \
  sudo \
  && rm -rf /var/lib/apt/lists/*

# Install Gradle
ADD https://services.gradle.org/distributions/gradle-7.4-bin.zip /gradle.zip
RUN mkdir /opt/gradle
RUN unzip -d /opt/gradle /gradle.zip
RUN rm /gradle.zip
RUN chmod -R 775 /opt/gradle/gradle-7.4/bin
RUN ln -s /opt/gradle/gradle-7.4/bin/* /usr/local/bin

# Add users
RUN useradd -m praktomat && adduser praktomat sudo
RUN useradd -m tester && adduser tester sudo && adduser tester praktomat
COPY sudoers /etc/sudoers
RUN chmod 440 /etc/sudoers

USER praktomat
WORKDIR /home/praktomat
RUN git clone --recursive git://github.com/hannesbraun/Praktomat.git
RUN cd Praktomat && git checkout cda732c906426a4cadb5583f3385c5f3c767aee1
RUN sudo chown praktomat:tester Praktomat/src/checker/scripts/java
RUN sudo chown praktomat:tester Praktomat/src/checker/scripts/javac
RUN sudo chmod u+x,g+x,o-x Praktomat/src/checker/scripts/java
RUN sudo chmod u+x,g+x,o-x Praktomat/src/checker/scripts/javac

# Get wait-for-it.sh (used to wait for PostgreSQL to become available)
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/81b1373f17855a4dc21156cfe1694c31d7d1792e/wait-for-it.sh wait-for-it.sh
RUN sudo chmod 775 wait-for-it.sh

# Install Python requirements for Praktomat
RUN python3 -m pip install --upgrade pip && python3 -m pip install -U pip virtualenv setuptools wheel urllib3[secure]
RUN python3 -m pip install -r Praktomat/requirements.txt

# Setup our own Praktomat utils
RUN sudo -H python3 -m pip install pyyaml
RUN mkdir utils

# Set executable/search flag for directories (only) located inside of /home/praktomat/.local
# This is required for Apache in order to follow the symlinks to some files (referenced from static directory)
RUN chmod -R g+X .local

# Install Praktomat addons
ADD https://github.com/jplag/jplag/releases/download/v2.12.1-SNAPSHOT/jplag-2.12.1-SNAPSHOT-jar-with-dependencies.jar /opt/praktomat-addons/jplag.jar
ADD https://github.com/checkstyle/checkstyle/releases/download/checkstyle-8.14/checkstyle-8.14-all.jar /opt/praktomat-addons/checkstyle-8.14-all.jar
RUN sudo chown -R praktomat:praktomat /opt/praktomat-addons

# Copy config file
COPY local.py Praktomat/src/settings/local.py

# Setup required directories
RUN mkdir debug-data
RUN mkdir work-data
RUN mkdir test-data

# Configure Apache2
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
RUN sudo adduser www-data praktomat
RUN sudo a2enmod macro
COPY praktomat.wsgi Praktomat/wsgi/praktomat.wsgi
COPY apache_praktomat_wsgi.conf Praktomat/documentation/apache_praktomat_wsgi.conf
RUN printf "\nInclude /home/praktomat/Praktomat/documentation/apache_praktomat_wsgi.conf\n" | sudo tee -a /etc/apache2/apache2.conf

# Configure OpenLDAP
COPY CA17.pem /etc/ssl/certs/CA17.pem
RUN printf "\nTLS_CACERT    /etc/ssl/certs/CA17.pem\n" | sudo tee -a /etc/ldap/ldap.conf

# Initialize Praktomat
RUN COMPOSE_PROJECT_NAME="" PRAKTOMAT_NAME="" PRAKTOMAT_ADMIN="" PRAKTOMAT_DOMAIN="" python3 Praktomat/src/manage-local.py collectstatic --noinput --link

ENTRYPOINT ./wait-for-it.sh postgresql:5432 -- python3 Praktomat/src/manage-local.py migrate --noinput && sudo -E apache2ctl -DFOREGROUND
