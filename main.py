import os
from database import inicializar_banco, salvar_vaga
from scraper import buscar_vagas_remotar
from filter import avaliar_vaga
from telegram import enviar_alerta_telegram
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def executar_automacao():
    print("🚀 Iniciando varredura diária de vagas...")
    
    # 1. Garante que o banco existe
    inicializar_banco()
    
    # 2. Executa a coleta nas fontes configuradas
    vagas_brutas = buscar_vagas_remotar()
    print(f"📊 Total de vagas brutas encontradas: {len(vagas_brutas)}")
    
    novas_notificadas = 0

    for vaga in vagas_brutas:
            # 1. Aplica o filtro inteligente e pontuação PRIMEIRO
            resultado_filtro = avaliar_vaga(vaga)
            
            # Se a vaga foi reprovada pelo filtro, nem precisamos salvar no banco (ou salvamos como rejeitada, dependendo do critério)
            if not resultado_filtro["aprovada"]:
                continue
                
            # Se foi aprovada, preenchemos os dados de score
            vaga['score'] = resultado_filtro["score"]
            vaga['technologies_matched'] = resultado_filtro["matched"]
            
            # 2. Valida se a vaga é inédita no banco
            inserida_agora = salvar_vaga(vaga)
            
            if not inserida_agora:
                continue # Se já existe no banco, pula para a próxima para não mandar duplicado no Telegram
                
            # 3. Dispara o alerta no Telegram se passou em tudo
            sucesso = enviar_alerta_telegram(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, vaga)
            if sucesso:
                print(f"✅ Alerta enviado: {vaga['titulo']} ({vaga['empresa']}) - Score: {vaga['score']}")
                novas_notificadas += 1
                
            print(f"✨ Varredura concluída! {novas_notificadas} novas vagas compatíveis notificadas.")

if __name__ == "__main__":
    executar_automacao()