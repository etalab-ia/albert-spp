from pyalbert.clients import LlmClient
from pyalbert.prompt import get_prompter

from config import LLM_DEFAULT_MODEL


def generate(query, model_name=LLM_DEFAULT_MODEL):
    # Build prompt
    prompter = get_prompter(model_name, mode="simple")
    messages = prompter.make_prompt(query=query)

    # Generate
    sampling_params = prompter.get_upstream_sampling_params()
    llm_client = LlmClient(model_name)
    result = llm_client.generate(messages, **sampling_params)
    answer = result.choices[0].message.content
    return answer.strip()
