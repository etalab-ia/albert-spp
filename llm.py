from pathlib import Path

from pyalbert.clients import LlmClient
from pyalbert.prompt import Prompter

from config import MODEL_NAME


def generate(query, model=MODEL_NAME):
    # Build prompt
    system_prompt = "Tu es un générateur de réponse automatique à une expérience utilisateur. Tu parles un français courtois."
    prompter = Prompter(
        config={
            "sampling_params": {"temperature": 0.25, "max_tokens": 4096},
            "default": {"limit": 5},
        },
        template=str(Path(__file__).resolve().parent / "templates/spp_fewshots.jinja"),
    )
    messages = prompter.make_prompt(query=query, system_prompt=system_prompt)

    # Generate
    sampling_params = prompter.get_upstream_sampling_params()
    llm_client = LlmClient(model)
    result = llm_client.generate(messages, **sampling_params)
    answer = result.choices[0].message.content
    return answer.strip()
