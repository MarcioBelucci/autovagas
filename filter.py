REGRAS_FILTRO = {
    "palavras_proibidas": [
        "senior", "sr", "tech lead", "principal", "presencial", "c++", "php"
    ],
    "pesos_tecnologias": {
        "python": 30,
        "javascript": 25,
        "typescript": 25,
        "react": 20,
        "sql": 15,
        "docker": 15,
        "fastapi": 20,
        "django": 20
    },
    "score_corte": 40  # Nota mínima para notificar
}

def avaliar_vaga(vaga):
    """
    Filtra termos proibidos e calcula o score de compatibilidade com base na stack.
    """
    texto_completo = f"{vaga.get('titulo', '')} {vaga.get('descricao', '')}".lower()
    
    # 1. Checagem de Hard Filter (Palavras Proibidas)
    for termo in REGRAS_FILTRO["palavras_proibidas"]:
        if termo in texto_completo:
            return {"aprovada": False, "score": 0, "matched": []}
            
    # 2. Cálculo de Score
    score = 0
    matched = []
    for tech, peso in REGRAS_FILTRO["pesos_tecnologias"].items():
        if tech in texto_completo:
            score += peso
            matched.append(tech)
            
    aprovada = score >= REGRAS_FILTRO["score_corte"]
    return {
        "aprovada": aprovada,
        "score": score,
        "matched": matched
    }