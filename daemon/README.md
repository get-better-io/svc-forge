
# {{ service }}-{{ daemon }}

## Actions

- `cd {{ daemon }}` - Enter this microservice
- `make dep` - Pull dependencies from {{ api }} (do this first)
- `make build` - Build a local image to use
- `make test` - Run tests
- `make debug` - Run tests with step through debugging. Will pause until the '{{ daemon }}' debugger is started.
- `make shell` - Fire up a shell for deeper testing / debugging
  - `$test test.test_service` - Test only the `test/test_service.py` file
  - `$test test.test_service.TestHealth` - Test only the `test/test_service.py` `TestHealth` class
  - `$test test.test_service.TestHealth.test_get` - Test only the `test/test_service.py` `TestHealth.test_get` method
  - `$debug test.test_service` - Debug only the `test/test_service.py` file
  - `$debug test.test_service.TestHealth` - Debug only the `test/test_service.py` `TestHealth` class
  - `$debug test.test_service.TestHealth.test_get` - Debug only the `test/test_service.py` `TestHealth.test_get` method
  - Make sure you fire up the debugger for those above
- `make lint`- Run the linter (uses `.pylintc`)

## Directories / Files

- `Makefile` - File that provides all the `make` commands
- `Dockerfile` - File that builds the Docker image
- `requirements.txt` - Put all your standard Python libs here
- `.pylintrc` - L:inting definitions. Change to suit your needs.
- `bin/` - Executables
  - `daemon.py` - Runs the {{ daemon }}
- `kubernetes/` - Kubernetes files
  - `base/` - Base files, what's deploy to the actual cluster
    - `daemon.yaml` - Deployment and Service for {{ daemon }}
    - `prometheus.yaml` - Prometheus Monitors
    - `kustomization.yaml` - Collates the above to form base
  - `tilt/` - Tilt files, what's deploy to your local machine
    - `daemon.yaml` - Deployment and Service for {{ daemon }} overriden for debugging
    - `kustomization.yaml` - Collates the above to form tilt
- `lib/` - Main code
  - `service.py` - Main {{ daemon }} codes, etc.
- `test/` - Main code
  - `test_service.py` - Test {{ daemon }} code, etc. Change to match your service changes
