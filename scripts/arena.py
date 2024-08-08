import os
import json
import re

os.environ["API_URL"] = "https://franceservices.dev.etalab.gouv.fr"
os.environ["ELASTIC_HOST"] = "albert.bdd.001.etalab.gouv.fr"
os.environ["ELASTIC_PORT"] = "39200"
os.environ["ELASTIC_PASSWORD"] = "Zva5yiiiHfqVPYupDw7HEXVMyMpYUMSd"

import numpy as np
import pandas as pd
from openai import OpenAI

# ============================
# !pip instal pyalbert==0.7.3
# ============================
from pyalbert.clients import LlmClient
from pyalbert.prompt import Prompter, get_prompter
from pyalbert import set_llm_table


# Set model locations
# --
albert_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjMyMDQzOTksImlhdCI6MTcyMzExNzk5OSwic3ViIjoiNTUifQ.RKEbALq0ulAleoEAK-rUSKPpcQSfKX7MESzIGTmR9NA"
jeanzay_api_key = "multivac-FQ1cWX4DpshdhkXY2m"

LLM_TABLE = [
        #{"model": "AgentPublic/fabrique-reference-2", "url": "http://albert.gpu.001.etalab.gouv.fr:8001/v1", "token": albert_api_key, "legacy":True, "prompt_format":"llama2-chat", "template":"spp_fabrique_simple.jinja"},
        {"model": "AgentPublic/llama3-instruct-8b", "url": "http://albert.gpu.005.etalab.gouv.fr:8001/v1", "token": albert_api_key, "template":"spp_fewshots.jinja"},
        #{"model": "meta-llama/Meta-Llama-3.1-8B-Instruct", "url": "http://llama38b.multivacplatform.org/v1/", "token": jeanzay_api_key, "alias"},

    ]
# We just need or to point the embedding model
set_llm_table([
        {"model": "BAAI/bge-m3", "url": "http://albert.gpu.005.etalab.gouv.fr:8001" },
])

# Load test data
# --
file_path = '_data/export-expa-c-riences.json'
df = pd.read_json(file_path)

# Filter the df on the given attributes
domains = ["MSA", "CNAV"]
df = df[df['intitule_typologie_1'].isin(domains)]

# Randomly sample 10 items from the DataFrame
small_df = df.sample(n=12, random_state=1)  # random_state is optional for reproducibility
del df


# Just for pedogical purpose
def legacy_generate(messages, model=None, base_url=None, api_key=None, **sampling_params):
    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        **sampling_params
    )

    return completion

#system_prompt = "Tu es un générateur de réponse automatique à une expérience utilisateur. Tu réponds directement, sans explications."
system_prompt = "Tu es un générateur de réponse automatique à une expérience utilisateur. Tu parles un français courtois."
spp_sampling_params = {
    "temperature": 0.25,
    "max_tokens": 4096,
}

results = []
for i, item in small_df.iterrows():
    query = item["description"]
    row = {
        "query": query,
        "reponse_SPP": item["reponse_structure_1"],
        "institution": item["intitule_typologie_1"],
    }
    for model_ in LLM_TABLE:
        llm_client = LlmClient(model_["model"], base_url=model_["url"], api_key=model_["token"])
        model_name = model_["model"].split("/")[-1]

        # Build the prompt/messages
        # --
        config = {
            "do_encode_prompt": model_.get("legacy", False),
            "prompt_format": model_.get("prompt_format"),
            "sampling_params": spp_sampling_params,
            "default": {"limit":5}
        }
        prompter = Prompter(config=config, template=model_.get("template"))
        prompt = prompter.make_prompt(query=query, system_prompt=system_prompt)

        # Gnerate the answer
        # --
        sampling_params = prompter.get_upstream_sampling_params() # eventual sampling param defined in the prompter config/mode
        try:
            result = llm_client.generate(prompt, **sampling_params)
            # Stricly equivalent here to:
            #result = legacy_generate(prompt, model=model_["model"], base_url=model_["url"], api_key=model_["token"], **sampling_params)
        except:
            result = llm_client.generate(prompt, **sampling_params)

        # Remove artefact from the answer
        answer = result.choices[0].message.content
        answer = re.sub(r'^<[^>]+>|<[^>]+>$', '', answer.strip("\n \"'#`"))
        if answer.startswith("Réponse :"):
            answer = answer[len("Réponse :"):]
        model_name = model_.get("alias", model_name)
        row[f"answser_{model_name}"] = answer.strip()
        print(".", end="", flush=True)

    results.append(row)

df = pd.DataFrame(results)
df.to_csv('spp_arena.csv', index=False)

