REGRAS_FILTRO = {
    # Vagas com estes termos são descartadas imediatamente
    "palavras_proibidas": [
        "senior", "sr", "tech lead", "", "presencial", "c++", "php"
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
        "git": 10,
        "github": 10,
        "software engineering": 10,
        "software architecture": 10,
        "data structures": 10,
        "automated testing": 10,
        "object oriented programming": 10,
        "responsive design": 10,
        "ui/ux": 10,
        "technical support": 15,  # Alinhado com Springboard/suporte acadêmico
        "problem solving": 10,
        
        # Bônus de Contexto (Termos genéricos) - 5 pts cada
        "developer": 5,
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
    Filtra termos proibidos, valida se é recente (<= 7 dias) e calcula o score.
    """
    texto_data = vaga.get('texto_data', '')
    
    # Filtro de Recência: Se explicitamente disser que tem mais de 7 dias / semanas / meses, descarta
    termos_antigos = ["semanas atrás", "2 semanas", "3 semanas", "mês", "meses", "há 8 dias", "há 9 dias"]
    for termo in termos_antigos:
        if termo in texto_data:
            return {"aprovada": False, "score": 0, "matched": []}

    texto_completo = f"{vaga.get('titulo', '')} {vaga.get('descricao', '')}".lower()
    
    # 1. Checagem de Hard Filter (Palavras Proibidas)
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
            
    aprovada = score >= REGRAS_FILTRO["score_corte"]
    return {
        "aprovada": aprovada,
        "score": score,
        "matched": matched
    }