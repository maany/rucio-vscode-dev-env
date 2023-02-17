# rucio-vscode-dev-env
- Clone this repo in the `.vscode` folder inside the [rucio codebase](https://github.com/rucio/rucio)
- Get the host certificates and the CA certificate chain for your development server and place them in the `certs` directory (hostkey.pem, hostcert.pem, ca-bundle.pem)
- Edit the `rucio.cfg` in the rucio source code to add the `urls` option in the `webui` section, specifying the host where you would host WebUI 2.0 ( http://localhost:3000 for local development)
- Edit the `docker-compose.yml` in this repo and change the `RUCIO_HOST` environment variable for the `rucio-dev` container to the hostname of the remote development VM.



