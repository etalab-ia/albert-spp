# Albert - Services Publics Plus

[[_TOC_]]

## Usage

1. Envoi du prompt au modèle

```sh
curl -XPOST  https://spp.etalab.gouv.fr/api/spp/anonymize  -H "Content-Type: application/json" \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"id":"123", "text":"Merci pour service"}'
```

2. Récupération de la réponse du modèle

```sh
curl -XPOST  https://spp.etalab.gouv.fr/api/spp/prod/run/ditp-get-data  -H "Content-Type: application/json" \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"id":"123"}'
```

## Déploiement

### Local

* Assurez vous de déployer une base de données Redis préalablement.

    Pour déployer rapidement une base de données Redis avec Docker :

    ```bash
    docker run --publish 6379:6379 --detach --name redis redis/redis-stack:7.4.0-v0
    ```

* Lancez l'API en remplacant dans la commande suivante les informations de connexion à la base de données Redis.

    ```bash
    MODELS_URLS=[\"http://localhost:8080\"] \
    MODEL_NAME="AgentPublic/fabrique-reference-2" \
    ENV=dev \
    REDIS_HOST=localhost \
    uvicorn app:app --proxy-headers --forwarded-allow-ips '*' --host 0.0.0.0 --port 8000 --reload
    ```

### Docker

```bash
docker compose up --detach
```

**Remarques**

* ⚠️ A des fins de développement cette API ne supporte qu'un seul modèle : [AgentPublic/fabrique-reference-2](https://huggingface.co/AgentPublic/fabrique-reference-2)
