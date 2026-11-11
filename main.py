import os
from database import inicializar_banco, salvar_vaga
from scraper import buscar_vagas_remotar
from filter import avaliar_vaga
from telegram import enviar_alerta_telegram

# CONFIGURAÇÕES DO TELEGRAM (Substitua pelos seus dados quando criar o bot)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "SEU_BOT_TOKEN_AQUI")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "SEU_CHAT_ID_AQUI")

def executar_automacao():
    print("🚀 Iniciando varredura diária de vagas...")
    
    # 1. Garante que o banco existe
    inicializar_banco()
    
    # 2. Executa a coleta nas fontes configuradas
    vagas_brutas = buscar_vagas_remotar()
    print(f"📊 Total de vagas brutas encontradas: {len(vagas_brutas)}")
    
    novas_notificadas = 0
    
    for vaga in vagas_brutas:
        # 3. Valida se a vaga é inédita no banco (evita duplicatas pelo link UNIQUE)
        # Salvamos inicialmente para testar se já existe
        vaga['score'] = 0
        inserida_agora = salvar_vaga(vaga)
        
        if not inserida_agora:
            continue # Se já existe no banco, pula para a próxima
            
        # 4. Aplica o filtro inteligente e pontuação
        resultado_filtro = avaliar_vaga(vaga)
        
        if resultado_filtro["aprovada"]:
            vaga['score'] = resultado_filtro["score"]
            vaga['technologies_matched'] = resultado_filtro["matched"]
            
            # 5. Dispara o alerta no Telegram
            sucesso = enviar_alerta_telegram(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, vaga)
            if sucesso:
                print(f"✅ Alerta enviado: {vaga['titulo']} ({vaga['empresa']}) - Score: {vaga['score']}")
                novas_notificadas += 1
                
    print(f"✨ Varredura concluída! {novas_notificadas} novas vagas compatíveis notificadas.")

if __name__ == "__main__":
    executar_automacao()