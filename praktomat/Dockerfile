# syntax=docker/dockerfile:1
FROM ubuntu:bionic
EXPOSE 443/tcp

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

# Add users
RUN useradd -m praktomat && adduser praktomat sudo
RUN useradd -m tester && adduser tester sudo && adduser tester praktomat
COPY sudoers /etc/sudoers
RUN chmod 440 /etc/sudoers

USER praktomat
WORKDIR /home/praktomat
# Use an unmerged patch in order to make LDAP authentication work
RUN git clone --recursive git://github.com/hannesbraun/Praktomat.git
RUN cd Praktomat && git checkout 5b95e83dcb43b958f8cf99408c758781e5d42ef5
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

# Set executable/search flag for directories (only) located inside of /home/praktomat/.local
# This is required for Apache in order to follow the symlinks to some files (referenced from static directory)
RUN chmod -R g+X .local

# Install Praktomat addons
ADD https://github.com/jplag/jplag/releases/download/v2.12.1-SNAPSHOT/jplag-2.12.1-SNAPSHOT-jar-with-dependencies.jar /opt/praktomat-addons/jplag.jar
ADD https://github.com/checkstyle/checkstyle/releases/download/checkstyle-8.14/checkstyle-8.14-all.jar /opt/praktomat-addons/checkstyle-8.14-all.jar
RUN sudo chown -R praktomat:praktomat /opt/praktomat-addons

# Copy config file
ARG ID
ARG NAME
ARG DOMAIN
ARG ADMIN
COPY local.py Praktomat/src/settings/local.py
RUN sed -i -e "s/\${id}/$ID/" \
  -e "s/\${site_name}/$NAME/" \
  -e "s/\${domain}/$DOMAIN/" \
  -e "s/\${server_admin}/$ADMIN/" \
  Praktomat/src/settings/local.py

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
RUN sed -i -e "s/\${id}/$ID/" \
  -e "s/\${domain}/$DOMAIN/" \
  -e "s/\${server_admin}/$ADMIN/" \
  Praktomat/documentation/apache_praktomat_wsgi.conf
RUN printf "\nInclude /home/praktomat/Praktomat/documentation/apache_praktomat_wsgi.conf\n" | sudo tee -a /etc/apache2/apache2.conf

# Configure OpenLDAP
COPY CA17.pem /etc/ssl/certs/CA17.pem
RUN printf "\nTLS_CACERT    /etc/ssl/certs/CA17.pem\n" | sudo tee -a /etc/ldap/ldap.conf

# Initialize Praktomat
RUN python3 Praktomat/src/manage-local.py collectstatic --noinput --link

ENTRYPOINT ./wait-for-it.sh postgresql:5432 -- python3 Praktomat/src/manage-local.py migrate --noinput && sudo apache2ctl -DFOREGROUND
