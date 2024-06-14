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

```bash
docker build --rm --tag albert/spp/api:latest --file ./Dockerfile .
docker compose up --detach
```

**Remarques**

* Le fichier `API_KEYS` doit être sur le modèle du fichier [api_keys.example.json](./api_keys.example.json).

* Le modèle doit être déployé à l'aide de ce repository [albert-backend](https://gitlab.com/etalab-datalab/llm/albert-backend).

* ⚠️ A des fins de développement cette API ne supporte qu'un seul modèle : [AgentPublic/fabrique-reference-2](https://huggingface.co/AgentPublic/fabrique-reference-2)