# Albert - Services Publics Plus

[[_TOC_]]

## Déploiement

### Local

* Assurez vous de déployer une base de données Redis préalablement.

    Pour déployer rapidement une base de données Redis avec Docker :

    ```bash
    docker run --publish 6000:6379 --detach --name redis redis:7.2.4 redis-server --save 20 1 --loglevel warning --requirepass mypassword
    ```

* Lancez l'API en remplacant dans la commande suivante les informations de connexion à la base de données Redis.

    ```bash
    REDIS_HOST=localhost \
    REDIS_PORT=6000 \
    REDIS_PASSWORD=mypassword \
    LLM_TABLE="" \
    uvicorn app:app --proxy-headers --root-path / --forwarded-allow-ips '*' --host 0.0.0.0 --port 8000 --reload
    ```

    Si la variable d'environnement `DEV` n'est pas passée, elle prend la valeur "dev" par défaut. Vous pouvez passer en header (clef: Autorization) de vos requêtes n'importe quel token.

    La variable `LLM_TABLE` doit être une string qui prend la forme d'une liste de tuple python comme ceçi : `'[("model_name"), ("model_url")]'`. Il est possible de fournir la liste de plusieurs modèles déployés à l'API.

    > **⚠️ Attention à des fins de développement cette API ne supporte qu'une entrée de modèle et un seul modèle : [AgentPublic/fabrique-reference-2](https://huggingface.co/AgentPublic/fabrique-reference-2)**

### Docker

#### Build

```bash
export CI_REGISTRY_IMAGE=myregistry
export CI_API_IMAGE_TAG=1.0.0
docker build --rm --tag ${CI_REGISTRY_IMAGE}/api:${CI_API_IMAGE_TAG} --file ./Dockerfile .
```

### Run

```bash
bash deploy.sh -r llm_routing_table.example.json -f .env.example
```

### CI/CD (docker)

Variables d'environnement nécessaires :

| key | type | value |
| --- | --- | --- |
| CI_DEPLOY_USER | variable | compte utilisateur sur les VM de déploiement |
| CI_DEPLOY_USER_SSH_PRIVATE_KEY | variable | clef SSH privée du compte utilisateur |
| CI_API_IMAGE_TAG | variable | version de l'image API qui est build (ex: 1.0.0) |
| STAGING__ENV_FILE | file | (1) |
| PROD__ENV_FILE | file | (1) |
| STAGING__LLM_ROUTING_TABLE | file | (2) |
| PROD__LLM_ROUTING_TABLE | file | (2) |
| API_KEYS | file | (3) |

**(1)** Les fichiers `STAGING__ENV_FILE` et `PROD__ENV_FILE` doivent contenir les variables d'environnements suivantes :

| key | value |
| --- | --- |
| ENV | staging ou prod |
| CI_DEPLOY_HOST | IP ou DNS de la vm de déployement |![alt text](image.png)
| REDIS_PASSWORD | mot de passe de base de données Redis |


**(2)** Les fichiers `STAGING__LLM_ROUTING_TABLE` et `PROD__LLM_ROUTING_TABLE` doivent être sur le modèle du fichier [llm_routing_table.example.json](./llm_routing_table.example.json). **Ce fichier json doit pour chaque clef indiqué un modèle de LLM déployé. Le fichier de déploiement [deploy.sh](./deploy.sh) va déployé une API pour chaque valeur de l'attribut *api_port* unique mentionné.**

> **⚠️ Attention à des fins de développement cette API ne supporte qu'une entrée de modèle et un seul modèle : [AgentPublic/fabrique-reference-2](https://huggingface.co/AgentPublic/fabrique-reference-2)**

**(3)** Le fichier `API_KEYS` doit être sur le modèle du fichier [api_keys.example.json](./api_keys.example.json).
