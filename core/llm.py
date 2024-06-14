from pyalbert.clients import LlmClient
from pyalbert.prompt import get_prompter

from config import LLM_DEFAULT_MODEL


def generate(query, model_name=LLM_DEFAULT_MODEL):
    # Build prompt
    prompter = get_prompter(model_name, mode="simple")
    prompt = prompter.make_prompt(query=query)

    # Generate
    llm_client = LlmClient(model_name)
    answer = llm_client.generate(prompt)
    return answer
