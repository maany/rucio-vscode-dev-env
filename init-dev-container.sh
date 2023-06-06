#!/bin/bash
echo "************ Setting up ntp ****************"
echo "********************************************"
systemctl start ntpd
systemctl enable ntpd
systemctl status ntpd
ntpdate -u -s 0.centos.pool.ntp.org 1.centos.pool.ntp.org 2.centos.pool.ntp.org
systemctl restart ntpd
timedatectl set-timezone Europe/Paris
timedatectl
echo "Done!"
echo "" 

echo "************* Copying Rucio Config ******************"
echo "*****************************************************"
cp etc/rse-accounts.cfg.template etc/rse-accounts.cfg
echo "Done!"
echo "" 

echo "************* Initialize Rucio ******************"
echo "*************************************************"
tools/run_tests_docker.sh -ir
echo "Done!"
echo ""

echo "************* Disable httpd ******************"
echo "**********************************************"
pkill httpd
echo "Done!"
echo ""

echo "************* Apply Debug Configuration ***********"
echo "***************************************************"
sed -i "s@^rucio_host = .*@rucio_host = https://$RUCIO_HOST:443@g" /opt/rucio/etc/rucio.cfg
sed -i "s@^auth_host = .*@auth_host = https://$RUCIO_HOST:443@g" /opt/rucio/etc/rucio.cfg
echo "Done!"
echo "" 

echo "************* Setup Client Certs ******************"
echo "***************************************************"

cp /etc/grid-security/hostcert.pem /etc/grid-security/hostcert.pem.orig
cp /etc/grid-security/hostcert.pem /etc/grid-security/hostcert.pem.orig
cp /etc/grid-security/hostcert.pem.cern.ca /etc/grid-security/hostcert.pem
cp /etc/grid-security/hostkey.pem.cern.ca /etc/grid-security/hostkey.pem

echo "export X509_CERT_DIR=/etc/grid-security/ca-bundle.pem" >> ~/.bashrc
echo "Done!"
echo ""

echo "************* Setup Rucio Client ******************"
echo "***************************************************"

sed -i "s@^ca_cert.*@ca_cert = /etc/grid-security/ca-bundle.pem@" /opt/rucio/etc/rucio.cfg
echo "Done!"
echo ""

echo "************* Setup WebUI ******************"
echo "***************************************************"

echo "[webui]" >> /opt/rucio/etc/rucio.cfg
echo "urls = http://localhost:3000" >> /opt/rucio/etc/rucio.cfg

echo "Done!"
echo ""

echo "Initialization is now Complete! Happy Debugging \m/"