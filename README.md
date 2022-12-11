# {{ service }}

# Requirements

- A Mac (Linux will work too but you're on your own)
- make (I think comes with xcode, git, etc)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [kubectx](https://formulae.brew.sh/formula/kubectx)
- [kustomize](https://formulae.brew.sh/formula/kustomize)
- [Tilt](https://docs.tilt.dev/install.html)

# Install

To install as a module, list in requirements.txt as:

```
git+ssh://git@github.com.com/get-better-io/{{ service }}.git@0.1.0#egg={{ service }}
```

# Development

If you make changes to `api/lib/{{ service }}.py` make sure you bump the version in `VERSION`.

After merging to main, update locally and type `make tag` and that'll tag with the new version.

## Actions

Make sure you've installed:

Also make sure you have https://github.com/gaf3/tilt-mysql and https://github.com/gaf3/tilt-prometheus up and running.

- `make up` - Fires up Tilt (run locally in Kuberentes). Hit space to open the dashboard in a browser
  - In the browser, if any micorservices (blocks) fail (turn red/yellow) click the refresh in the block
- `make down` - Removes everything locally from Kuberentes
- `make setup` - Verifies that this repo can be installeeld as a module by other services
- `make tag` - Tags this repo because you're absolutely sure this is perfect and will work
- `make untag` - Undoes the taggin you just did because you totally screwed something up

## Directories / Files

- `Makefile` - File that provides all the `make` commands
- `Tiltfile` - Deploys to the locally Kubernetes environment
- `kubernetes/` - Service Kubernetes files
  - `base/` - Base kustomization for the service to deploy to production
    - `namespace.yaml` - Namespace file
    - `kustomization.yaml` - Collates the above
  - `tilt/` - Tilt kustomization for the service to deploy locally
    - `kustomization.yaml` - Collates the base and microservice tilt kustomizations
- `.vscode/` - Settings for vscode local development and debugging
  - `lauch.json` - Debugger information for each microservice
- `secret/` - Directory used to create local secrets (.gitignore'd)
  - `mysql.json` - Connection informatioin for tilt-mysql
- `config/` - Directory used to create local config (.gitignore'd)
- `setup.py` - Makes this repo installable as `pip install git@github.com.com:get-better-io/{{ service }}.git` to access these Models via this API
