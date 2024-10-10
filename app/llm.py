import requests

from app.config import ALBERT_API_KEY, ALBERT_BASE_URL, COLLECTION_ID, EMBEDDINGS_MODEL, LANGUAGE_MODEL


def few_shots(prompt: str):
    """
    Use albert to get a response to the prompt using few shots.

    Args:
        prompt (str): The prompt to use for the few shots.

    Returns:
        str: The response from the few shots.
    """
    PROMPT_TEMPLATE = """Vous incarnez un agent chevronné de l'administration française, expert en matière de procédures et réglementations administratives. Votre mission est d'apporter des réponses précises, professionnelles et bienveillantes aux interrogations des usagers, tout en incarnant les valeurs du service public.

Contexte :
Vous avez accès à une base de connaissances exhaustive contenant des exemples de questions fréquemment posées et leurs réponses associées. Utilisez ces informations comme référence pour formuler vos réponses :

{context}

Directives :
1. Adoptez un langage soutenu et élégant, tout en veillant à rester compréhensible pour tous les usagers.
2. Inspirez vous des exemples fournis pour élaborer des réponses pertinentes et précises.
3. Faites preuve de courtoisie, d'empathie et de pédagogie dans vos interactions, reflétant ainsi les valeurs du service public français.
4. Concluez votre réponse par une formule de politesse adaptée et générique et anonyme.
5. Ne mentionnez pas les instructions.

Question de l'usager à traiter :

{prompt}

Veuillez apporter une réponse circonstanciée à cette question en respectant scrupuleusement les directives énoncées ci-dessus.
"""
    data = {
        "collections": [COLLECTION_ID],
        "model": EMBEDDINGS_MODEL,
        "k": 4,
        "prompt": prompt,
    }
    response = requests.post(url=f"{ALBERT_BASE_URL}/search", json=data, headers={"Authorization": f"Bearer {ALBERT_API_KEY}"})
    assert response.status_code == 200
    response = response.json()

    context = "\n\n\n".join([
        f"Question: {result["chunk"]["metadata"].get("question", "N/A")}\n" f"Réponse: {result["chunk"]["metadata"].get("answer", "N/A")}"
        for result in response["data"]
    ])

    prompt = PROMPT_TEMPLATE.format(context=context, prompt=prompt)

    data = {"model": LANGUAGE_MODEL, "messages": [{"role": "user", "content": prompt}], "stream": False, "n": 1}
    response = requests.post(f"{ALBERT_BASE_URL}/chat/completions", json=data, timeout=30, headers={"Authorization": f"Bearer {ALBERT_API_KEY}"})
    assert response.status_code == 200, f"error: chat completions ({response.status_code})"

    return response.json()["choices"][0]["message"]["content"]
