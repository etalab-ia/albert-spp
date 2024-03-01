from config import LLM_DEFAULT_MODEL
from core.legacy import get_prompter, get_llm_client

def generate(query, model_name=LLM_DEFAULT_MODEL):
    # Build prompt
    prompter = get_prompter(model_name, mode="simple")
    prompt = prompter.make_prompt(query=query)

    # Generate
    llm_client = get_llm_client(model_name)
    answer = llm_client.generate(prompt)
    return answer
