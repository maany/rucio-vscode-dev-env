## Base Image
FROM docker.io/rucio/rucio-dev:latest-alma9 as base

## install debugpy
FROM base as debug
RUN python3 -m pip install debugpy pyOpenSSL

## Copy debug utils
COPY utils /opt/rucio/debug_utils

## install utils
RUN yum install -y wget net-tools iproute openssh openssh-server openssh-clients openssl-libs tcpdump telnet ntpsec procps

## expose debug port
EXPOSE 5678

## Copy CA and Certificates
COPY certs/rucio_ca.pem /etc/grid-security/certificates/5fca1cb1.0
COPY certs/hostcert_rucio.pem /etc/grid-security/hostcert.pem
COPY certs/hostcert_rucio.key.pem /etc/grid-security/hostkey.pem
COPY certs/hostcert.pem /etc/grid-security/hostcert.pem.cern.ca
COPY certs/hostkey.pem /etc/grid-security/hostkey.pem.cern.ca
COPY certs/ca-bundle.pem /etc/grid-security/ca-bundle.pem

## Copy CA chain used for issuing client certificates
# COPY client-ca/intermediate/certs/ca-chain.cert.pem /etc/grid-security/client-ca-bundle.pem

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

ENV RUCIO_POLICY_PACKAGE="atlas_rucio_policy_package"

## Copy init script
COPY init-dev-container.sh /opt/rucio/etc/

## init system inside the container ##
ENV container docker

CMD ["sleep", "infinity"]
