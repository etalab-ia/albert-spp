from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    return "ok"


@app.post("/{index_name}/_search")
async def search(index_name: str):
    data = []

    data = {
        "took": 30,
        "timed_out": False,
        "_shards": {"total": 5, "successful": 5, "skipped": 0, "failed": 0},
        "hits": {
            "total": {"value": 1000, "relation": "eq"},
            "max_score": 1.3862944,
            "hits": [
                {
                    "_index": index_name,
                    "_type": "_doc",
                    "_id": "1",
                    "_score": 1.3862944,
                    "_source": {
                        "id_experience": "some_id",
                        "titre": "Titre",
                        "description": "Description",
                        "reponse_structure_1": "Reponse Structure 1",
                    },
                },
            ],
        },
        "aggregations": {
            "categories": {
                "doc_count_error_upper_bound": 0,
                "sum_other_doc_count": 0,
                "buckets": [
                    {"key": "Programming", "doc_count": 2},
                    {"key": "Data Science", "doc_count": 1},
                ],
            }
        },
    }

    response = JSONResponse(data)
    response.headers["X-Elastic-Product"] = "Elasticsearch"
    return response
