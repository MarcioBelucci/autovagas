import requests

def enviar_alerta_telegram(bot_token, chat_id, vaga):
    """
    Envia a notificação formatada via API do Telegram.
    """
    if not bot_token or not chat_id:
        print("⚠️ Token ou Chat ID do Telegram não configurados.")
        return False
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    mensagem = f"""
<b>🚨 NOVA VAGA COMPATÍVEL! (Score: {vaga['score']})</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 <b>Cargo:</b> {vaga['titulo']}
🏢 <b>Empresa:</b> {vaga['empresa']}
📍 <b>Local:</b> {vaga['local']}
🌐 <b>Plataforma:</b> {vaga['plataforma']}

⚡ <b>Stack Encontrada:</b>
<i>{', '.join(vaga['technologies_matched'])}</i>

📝 <b>Resumo:</b>
<i>{vaga['descricao'][:180]}...</i>
"""

    payload = {
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "🔗 Acessar e Aplicar", "url": vaga['link']}]
            ]
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar mensagem no Telegram: {e}")
        return False