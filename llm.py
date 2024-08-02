from pathlib import Path

from pyalbert.clients import LlmClient
from pyalbert.prompt import Prompter

from config import ALBERT_API_KEY, MODEL_NAME


def generate(query, model_name=MODEL_NAME, albert_api_key=ALBERT_API_KEY):
    # Build prompt
    prompter = Prompter(
        config={"sampling_params": {"temperature": 0.25, "max_tokens": 4096}},
        template=str(Path(__file__).resolve().parent / "templates/spp_fabrique_simple.jinja"),
        api_key=ALBERT_API_KEY,
    )
    messages = prompter.make_prompt(query=query)

    # Generate
    sampling_params = prompter.get_upstream_sampling_params()
    llm_client = LlmClient(model_name)
    result = llm_client.generate(messages, **sampling_params)
    answer = result.choices[0].message.content
    return answer.strip()
