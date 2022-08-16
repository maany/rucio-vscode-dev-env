import os
from rucio.web.ui.flask.main import application
from flask.helpers import send_from_directory
from flask import request, Response
import requests
import werkzeug.serving as serving
import ssl
import OpenSSL

host = os.getenv("RUCIO_HOST")


class PeerCertWSGIRequestHandler(serving.WSGIRequestHandler):
    """
    We subclass this class so that we can gain access to the connection
    property. self.connection is the underlying client socket. When a TLS
    connection is established, the underlying socket is an instance of
    SSLSocket, which in turn exposes the getpeercert() method.

    The output from that method is what we want to make available elsewhere
    in the application.
    """

    def make_environ(self):
        """
        The superclass method develops the environ hash that eventually
        forms part of the Flask request object.

        We allow the superclass method to run first, then we insert the
        peer certificate into the hash. That exposes it to us later in
        the request variable that Flask provides
        """
        environ = super(PeerCertWSGIRequestHandler, self).make_environ()
        x509_binary = self.connection.getpeercert(True)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, x509_binary)
        environ['peercert'] = x509
        environ['SSL_CLIENT_VERIFY'] = "SUCCESS"
        environ['SSL_CLIENT_S_DN'] = str(x509.get_subject()).split(" ")[2][1:-2]
        return environ


@application.route('/proxy/<path:path>')
def proxy(path):
    url = request.url.replace(request.host_url, f'https://{host}:443').replace('proxy', '')
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        verify=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response


@application.route('/authproxy/<path:path>')
def authproxy(path):
    url = request.url.replace(request.host_url, f'https:{host}:443').replace('authproxy', '')
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        verify=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response


@application.route('/static/<path>')
def serve_static(path):
    return send_from_directory('/opt/rucio/lib/rucio/web/ui/static', path)


@application.route('/media/<path:path>')
def serve_media(path):
    return send_from_directory('/opt/rucio/lib/rucio/web/ui/media', path)


# to establish an SSL socket we need the private key and certificate that
# we want to serve to users.
# app_key_password here is None, because the key isn't password protected,
# but if yours is protected here's where you place it.
app_key = '/etc/grid-security/hostkey.pem'
app_key_password = None
app_cert = '/etc/grid-security/hostcert.pem'

# in order to verify client certificates we need the certificate of the
# CA that issued the client's certificate. In this example I have a
# single certificate, but this could also be a bundle file.
# There is a /etc/grod-security/client-ca-bundle.pem available.
# If you install a client certificate from the CA bundled in this configuration, then use that CA
# If you use your CERN grid user ceritificate, then use ca-bundle.pem
ca_cert_chain = '/etc/grid-security/ca-bundle.pem'

# create_default_context establishes a new SSLContext object that
# aligns with the purpose we provide as an argument. Here we provide
# Purpose.CLIENT_AUTH, so the SSLContext is set up to handle validation
# of client certificates.
ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH,
                                         cafile=ca_cert_chain)

# load in the certificate and private key for our server to provide to clients.
# force the client to provide a certificate.
ssl_context.load_cert_chain(certfile=app_cert, keyfile=app_key, password=app_key_password)
ssl_context.verify_mode = ssl.CERT_REQUIRED


def initialize_flask_server_debugger_if_needed():
    if os.getenv("DEBUGGER") == "True":
        if serving.is_running_from_reloader():
            import debugpy
            debugpy.listen(("0.0.0.0", 5678))
            print("⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳", flush=True)
            debugpy.wait_for_client()
            print("🎉 VS Code debugger attached, enjoy debugging 🎉", flush=True)
        else:
            print("Socket already in use")


initialize_flask_server_debugger_if_needed()
# if __name__ == '__main__':
#     initialize_flask_server_debugger_if_needed()
#     application.run(ssl_context=ssl_context, request_handler=PeerCertWSGIRequestHandler)
