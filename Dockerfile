## Base Image
FROM docker.io/rucio/rucio-dev:py3 as base

## install debugpy
FROM base as debug
RUN python3 -m pip install debugpy pyOpenSSL

## Copy debug utils
COPY utils /opt/rucio/debug_utils

## enable python2
RUN rm /usr/bin/python && ln -fs /usr/bin/python2 /usr/bin/python

## install utils
RUN yum install -y wget net-tools iproute openssh openssh-server openssh-clients openssl-libs tcpdump telnet ntp ntpupdate

## enable python3
RUN rm /usr/bin/python && ln -fs /usr/bin/python3 /usr/bin/python

## expose debug port
EXPOSE 5678

## Copy CA and Certificates
COPY certs/hostcert.pem /etc/grid-security/hostcert.pem.cern.ca
COPY certs/hostkey.pem /etc/grid-security/hostkey.pem.cern.ca
COPY certs/ca-bundle.pem /etc/grid-security/ca-bundle.pem

## Copy CA chain used for issuing client certificates
COPY client-ca/intermediate/certs/ca-chain.cert.pem /etc/grid-security/client-ca-bundle.pem

## Set environment variables
ENV LC_ALL="en_US.utf-8" 
ENV FLASK_ENV="development"
ENV FLASK_DEBUG=1
ENV PYTHONPATH="$PYTHONPATH:/opt/rucio/lib:/opt/rucio/debug_utils"
ENV CA_BUNDLE="/etc/grid-security/ca-bundle.pem"
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

## Copy init script
COPY init-dev-container.sh /opt/rucio/etc/

## init system inside the container ##
ENV container docker
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]



#### Debug Image: WebUI ####
