import os
# import ssl
import werkzeug.serving as serving
from rucio.web.rest.flaskapi.v1.main import application


app_key = '/etc/grid-security/hostkey.pem'
app_key_password = None
app_cert = '/etc/grid-security/hostcert.pem'

ssl_context = serving.load_ssl_context(cert_file=app_cert, pkey_file=app_key)

def initialize_flask_server_debugger_if_needed():
    if os.getenv("DEBUGGER") == "True":
        if serving.is_running_from_reloader():
            import debugpy
            debugpy.listen(("0.0.0.0", 5679))
            print("⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳", flush=True)
            debugpy.wait_for_client()
            print("🎉 VS Code debugger attached, enjoy debugging 🎉", flush=True)
        else:
            print("Socket already in use")

# ssl_context = ssl.create_default_context()
# ssl_context.load_cert_chain(certfile=app_cert, keyfile=app_key, password=app_key_password)
# application.config
initialize_flask_server_debugger_if_needed()

# if __name__ == '__main__':
#     initialize_flask_server_debugger_if_needed()
#     application.run(ssl_context=ssl_context, debug=True, host='0.0.0.0', port=443, use_debugger=True)
