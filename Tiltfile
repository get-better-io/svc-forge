k8s_yaml(kustomize('kubernetes/tilt'))

local_resource(
    name='config', deps=["config/"],
    cmd='kubectl --context docker-desktop -n {{ service }} create configmap config --from-file config/ --dry-run=client -o yaml | kubectl --context docker-desktop apply -f -'
)

local_resource(
    name='secret',
    cmd='kubectl --context docker-desktop -n {{ service }} create secret generic secret --from-file secret/ --dry-run=client -o yaml | kubectl --context docker-desktop apply -f -'
)

# {{ api }}

docker_build('{{ service }}-{{ api }}', './{{ api }}')

k8s_resource('{{ api }}', port_forwards=['{{ api_port }}:80', '{{ api_debug_port }}:5678'], resource_deps=['redis'])

docker_build('{{ service }}-{{ daemon }}', './{{ daemon }}')

k8s_resource('{{ daemon }}', port_forwards=['26738:5678'], resource_deps=['redis'])

docker_build('{{ service }}-{{ gui }}', './{{ gui }}')


k8s_resource('{{ gui }}', port_forwards=['{{ gui_port }}:80'], resource_deps=['{{ api }}'])

docker_build('{{ service }}-{{ cron }}', './{{ cron }}')





k8s_resource('redis', port_forwards=['26770:5678'])
