Place a hostcert.pem and a hostkey.pem that should be used for the development VM.
Also place a ca-bundle.pem containing the certificate chain that verifies the hostcert.pem

If you are developing on a CERN VM, you can generate host certificates from https://cern.ch/ca
The CERN CA bundle available at:
https://github.com/CMSTrackerDPG/cernrequests/blob/master/cernrequests/cern-cacert.pem
or
https://linuxsoft.cern.ch/cern/centos/7/cern/x86_64/repoview/CERN-CA-certs.html 
