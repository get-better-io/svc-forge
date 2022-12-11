k8s_yaml(kustomize('kubernetes/tilt'))

k8s_resource(
  objects=['{{ service }}:namespace'],
  new_name='namespace'
)

local_resource(
    name='config', resource_deps=['namespace'],
    cmd='kubectx docker-desktop && kubectl -n {{ service }} create configmap config --from-file config/ --dry-run=client -o yaml | kubectl apply -f -'
)

local_resource(
    name='secret', resource_deps=['namespace'],
    cmd='kubectx docker-desktop && kubectl -n {{ service }} create secret generic secret --from-file secret/ --dry-run=client -o yaml | kubectl apply -f -'
)
