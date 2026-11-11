import re
import unicodedata

REGRAS_FILTRO = {
    "palavras_proibidas": ["senior", "sr", "tech lead", "presencial", "c++", "php"],
    "pesos_tecnologias": {
        "python": 30, "javascript": 25, "sql": 25, "flask": 25, "mysql": 20,
        "c#": 15, "backend": 15, "frontend": 15, "web development": 15,
        "desenvolvedor web": 15, "desenvolvedor backend": 15,
        "desenvolvedor frontend": 15, "junior": 15, "junior developer": 15,
        "api": 10, "ai": 10, "git": 10, "github": 10,
        "software engineering": 10, "engenheiro de software": 10,
        "data structures": 10, "automated testing": 10,
        "automatizacao de testes": 10, "object oriented programming": 10,
        "responsive design": 10, "ui/ux": 10, "technical support": 15,
        "suporte tecnico": 15, "problem solving": 10,
        "resolucao de problemas": 10, "developer": 5, "desenvolvedor": 5,
        "programador": 5, "programacao": 5, "ti": 5, "remote work": 5,
        "communication": 5, "teamwork": 5, "english": 5, "spanish": 5,
    },
    "score_corte": 10,
}


def normalizar_texto(texto):
    """Remove acentos e padroniza caixa para comparações previsíveis."""
    texto = unicodedata.normalize("NFD", str(texto or ""))
    return "".join(char for char in texto if not unicodedata.combining(char)).casefold()


def contem_termo(texto, termo):
    """Busca termos inteiros, evitando que 'ti' pontue dentro de outra palavra."""
    return bool(re.search(r"(?<!\w)" + re.escape(termo) + r"(?!\w)", texto))


def avaliar_vaga(vaga):
    """Aplica bloqueios e calcula a relevância a partir de título e descrição."""
    texto_completo = normalizar_texto(
        f"{vaga.get('titulo', '')} {vaga.get('descricao', '')}"
    )
    for termo in REGRAS_FILTRO["palavras_proibidas"]:
        termo_normalizado = normalizar_texto(termo)
        if termo_normalizado and contem_termo(texto_completo, termo_normalizado):
            return {"aprovada": False, "score": 0, "matched": [],
                    "motivo": f"termo proibido: {termo}"}

    score, matched = 0, []
    for tecnologia, peso in REGRAS_FILTRO["pesos_tecnologias"].items():
        if contem_termo(texto_completo, tecnologia):
            score += peso
            matched.append(tecnologia)
    return {"aprovada": score >= REGRAS_FILTRO["score_corte"], "score": score,
            "matched": matched, "motivo": None}
