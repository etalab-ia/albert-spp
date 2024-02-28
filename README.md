# Albert - Services publics plus

[[_TOC_]]

## Déploiement

### Build

```bash
export CI_REGISTRY_IMAGE=myregistry
export CI_API_IMAGE=1.0.0
docker build --rm --tag ${CI_REGISTRY_IMAGE}/api:${CI_API_IMAGE_TAG} --file ./Dockerfile .
```

### Run

```bash
bash deploy.sh -r llm_routing_table.example.json -f .env.example
```