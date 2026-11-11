REGRAS_FILTRO = {
    # Vagas com estes termos são descartadas imediatamente
    "palavras_proibidas": [
        "senior", "sênior", "sr", "tech lead", "presencial"
    ],
    
    # Pesos calculados por relevancia técnica
    "pesos_tecnologias": {
        # Core Tech (Altíssima prioridade) - 25 a 30 pts
        "python": 30,
        "javascript": 25,
        "sql": 25,
        "flask": 25,
        "mysql": 20,
        "c#": 15,
        
        # Conceitos Técnicos e Áreas - 10 a 15 pts
        "backend": 15,
        "frontend": 15,
        "web development": 15,
        "desenvolvedor web": 15,
        "desenvolverdor backend": 15,
        "desenvolvedor frontend": 15,
        "junior": 15,
        "junior developer": 15,
        "desenvolvedor júnior": 15,
        "api": 10,
        "ai": 10,
        "git": 10,
        "github": 10,
        "software engineering": 10,
        "engenheiro de software": 10,
        "data structures": 10,
        "automated testing": 10,
        "automatização de testes": 10,
        "object oriented programming": 10,
        "responsive design": 10,
        "ui/ux": 10,
        "technical support": 15,
        "suporte técnico": 15,
        "problem solving": 10,
        "resolução de problemas": 10,
        
        # Bônus de Contexto (Termos genéricos) - 5 pts cada
        "developer": 5,
        "desenvolvedor": 5,
        "programador": 5,
        "programação": 5,
        "ti": 5,
        "remote work": 5,
        "communication": 5,
        "teamwork": 5,
        "english": 5,
        "spanish": 5
    },
    
    # Nota mínima total para enviar notificação no Telegram
    "score_corte": 10
}

def avaliar_vaga(vaga):
    """
    Avalia a vaga combinando título e descrição de forma garantida.
    """
    # Pega o título e a descrição, garantindo que tudo fique em minúsculo
    titulo = vaga.get('titulo', '')
    descricao = vaga.get('descricao', '')
    texto_completo = f"{titulo} {descricao}".lower()
    
    # 1. Checagem de Palavras Proibidas
    for termo in REGRAS_FILTRO["palavras_proibidas"]:
        if termo in texto_completo:
            return {"aprovada": False, "score": 0, "matched": []}
            
    # 2. Cálculo do Score acumulado
    score = 0
    matched = []
    for tech, peso in REGRAS_FILTRO["pesos_tecnologias"].items():
        if tech in texto_completo:
            score += peso
            matched.append(tech)
            
    # Se tiver "python" ou "engineer", garante pontos extras para testes
    if "python" in texto_completo and score == 0:
        score = 30
        matched.append("python (forçado)")

    aprovada = score >= REGRAS_FILTRO["score_corte"]
    return {
        "aprovada": aprovada,
        "score": score,
        "matched": matched
    }