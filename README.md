# Albert - Services Publics Plus

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

## CI/CD

Variables d'environnement nécessaires :

| key | type |
| --- | --- |
| CI_DEPLOY_USER | variable |
| CI_DEPLOY_USER_SSH_PRIVATE_KEY | variable |
| CI_API_IMAGE_TAG | variable |
| STAGING__ENV_FILE| file |
| PROD__ENV_FILE | file |
| STAGING__LLM_ROUTING_TABLE | file |
| PROD__LLM_ROUTING_TABLE | file |