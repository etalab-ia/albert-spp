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

    Si la variable d'environnment `LLM_TABLE` n'est pas passée, elle prend la valeur `'[("AgentPublic/fabrique-reference-2", "http://127.0.0.1:8081")]'`. Ce qui suppose qu'un LLM est déployé en local sur le port 8081. La variable `LLM_TABLE` doit être une string qui prend la forme d'une liste de tuple python comme ceci : `'[("model_name"), ("model_url")]'`. Il est possible de fournir la liste de plusieurs modèles déployés à l'API.

    > **⚠️ Attention à des fins de développement cette API ne supporte qu'une entrée de modèle et un seul modèle : [AgentPublic/fabrique-reference-2](https://huggingface.co/AgentPublic/fabrique-reference-2)**

### Docker

#### Build

```bash
export CI_REGISTRY_IMAGE=myregistry
export CI_API_IMAGE_TAG=1.0.0
docker build --rm --tag ${CI_REGISTRY_IMAGE}/api:${CI_API_IMAGE_TAG} --file ./Dockerfile .
```

#### Run

```bash
docker compose --env-file .env.example up --detach
```

### CI/CD (docker)

Variables d'environnement nécessaires :

| key | type | value |
| --- | --- | --- |
| CI_DEPLOY_USER | variable | compte utilisateur sur les VM de déploiement |
| CI_DEPLOY_USER_SSH_PRIVATE_KEY | variable | clef SSH privée du compte utilisateur |
| CI_API_IMAGE_TAG | variable | version de l'image API qui est build (ex: 1.0.0) |
| CI_VLLM_IMAGE_TAG | variable | |
| CI_DEPLOY_GROUP_USER | var | |
| CI_DEPLOY_GROUP_TOKEN | var | |
| STAGING__ENV_FILE | file | (1) |
| PROD__ENV_FILE | file | (1) |
| API_KEYS | file | (2) |

**(1)** Les fichiers `STAGING__ENV_FILE` et `PROD__ENV_FILE` doivent contenir les variables d'environnements suivantes :

| key | value |
| --- | --- |
| ENV | *staging* ou *prod* |
| CI_DEPLOY_HOST | IP ou DNS de la vm de déploiement |
| REDIS_PASSWORD | mot de passe de base de données Redis |
| LLM_TABLE | table des modèles auquel l'API (3) |
| API_PORT | port de l'API |
| API_ROOT_PATH | |
| VLLM_HF_REPO_ID | |
| VLLM_TENSOR_PARALLEL_SIZE | |
| VLLM_GPU_MEMORY_UTILIZATION | |
| MODELS_CACHE_DIR | *AgentPublic/fabrique-reference-2* (4) | 

**(2)** Le fichier `API_KEYS` doit être sur le modèle du fichier [api_keys.example.json](./api_keys.example.json).

**(3)** Les modèles doivent être déployer séparer de ce repository. Pour déployer un modèle rendez-vous sur le repository [albert-backend](https://gitlab.com/etalab-datalab/llm/albert-backend).

**(4)** ⚠️ A des fins de développement cette API ne supporte qu'un seul modèle : [AgentPublic/fabrique-reference-2](https://huggingface.co/AgentPublic/fabrique-reference-2)