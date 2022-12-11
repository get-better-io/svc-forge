
# {{ service }}-{{ gui }}

## Actions

- `cd {{ gui }}` - Enter this microservice (do this first)
- `make build` - Build a local image to use (do this third)
- `make shell` - Fire up a shell for deeper testing / debugging

## Directories / Files

- `Makefile` - File that provides all the `make` commands
- `Dockerfile` - File that builds the Docker image
- `kubernetes/` - Kubernetes files
  - `base/` - Base files, what's deploy to the actual cluster
    - `gui.yaml` - Deployment and Service for {{ gui }}
    - `prometheus.yaml` - Prometheus Monitors
    - `kustomization.yaml` - Collates the above to form base
  - `tilt/` - Tilt files, what's deploy to your local machine
    - `gui.yaml` - Deployment and Service for {{ gui }} overriden for debugging
    - `kustomization.yaml` - Collates the above to form tilt
- `nginx/` - Nginx configuration
  - `nginx.conf` - OVerall config for nginx
  - `default.conf` - Reverse proxy to talk to {{ api }}
- `www/` - Main code
  - `css/service.css` - Put customizations here
  - `js/relations.js` - Main Relations Controller.
  - `js/service.js` - Custom Controllers. This is were you changes go for new models
  - `index.html` - Only page loaded directly by the browser
  - `header.html` - Partial template for the header for all pages
  - `footer.html` - Partial template for the footer of all pages
  - `form.html` - Psrtial tempalte for all the pages with fields (create, retrieve, update)
  - `html.html` - Home template
  - `fields.html` - Sub template for for all the pages with fields (create, retrieve, update)
  - `create.html` - Create tempalte for all models
  - `retrieve.html` - Retrieve template for all models
  - `list.html`- List template for all models
