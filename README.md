# rucio-vscode-dev-env

This repository provides a development environment setup for working with the Rucio codebase using Visual Studio Code.

## Setup Instructions

1. **Clone the Repository**  
   Clone this repository into the `.vscode` folder inside the [Rucio codebase](https://github.com/rucio/rucio):
   ```bash
   git clone https://github.com/<your-repo>/rucio-vscode-dev-env .vscode
   ```

2. **Prepare Certificates**  
   Obtain the host certificates and the CA certificate chain for your development server. Place the following files in the `certs` directory:
   - `hostkey.pem`
   - `hostcert.pem`
   - `ca-bundle.pem`

3. **Update `rucio.cfg`**  
   Edit the `rucio.cfg` file in the Rucio source code to include the `urls` option in the `[webui]` section. Specify the host where you will run WebUI 2.0 (e.g., `http://localhost:3000` for local development):
   ```ini
   [webui]
   urls = http://localhost:3000
   ```

4. **Modify `docker-compose.yml`**  
   Update the `docker-compose.yml` file in this repository. Change the `RUCIO_HOST` environment variable for the `rucio-dev` container to match the hostname of your remote development VM:
   ```yaml
   environment:
     RUCIO_HOST: <your-remote-vm-hostname>
   ```

## Additional Resources

For detailed setup and usage instructions, refer to the [official documentation](https://rucio.github.io/documentation/developer/setting_up_vscode_dev_env).

