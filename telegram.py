from html import escape

import requests


def enviar_alerta_telegram(bot_token, chat_id, vaga):
    """Envia uma notificação e retorna (sucesso, detalhe_de_erro)."""
    if not bot_token or not chat_id:
        return False, "Token ou Chat ID do Telegram não configurados."

    def texto(chave, limite=None):
        valor = str(vaga.get(chave, ""))
        return escape(valor[:limite] if limite else valor)

    mensagem = f"""
<b>🚨 NOVA VAGA COMPATÍVEL! (Score: {vaga['score']})</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 <b>Cargo:</b> {texto('titulo')}
🏢 <b>Empresa:</b> {texto('empresa')}
📍 <b>Local:</b> {texto('local')}
🌐 <b>Plataforma:</b> {texto('plataforma')}

⚡ <b>Stack Encontrada:</b>
<i>{escape(', '.join(vaga['technologies_matched']))}</i>

📝 <b>Resumo:</b>
<i>{texto('descricao', 180)}...</i>
"""
    payload = {
        "chat_id": chat_id, "text": mensagem, "parse_mode": "HTML",
        "reply_markup": {"inline_keyboard": [[{
            "text": "🔗 Acessar e Aplicar", "url": vaga["link"]
        }]]},
    }
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json=payload, timeout=10,
        )
        if response.ok:
            return True, None
        return False, f"Telegram {response.status_code}: {response.text[:300]}"
    except requests.RequestException as erro:
        return False, str(erro)
