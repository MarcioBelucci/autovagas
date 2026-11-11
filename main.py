from database import atualizar_status, inicializar_banco, salvar_vaga, status_vaga
from filter import REGRAS_FILTRO, avaliar_vaga
from scraper import buscar_vagas_remotar
from telegram import enviar_alerta_telegram
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def executar_automacao():
    print("🚀 Iniciando varredura diária de vagas...")
    inicializar_banco()
    vagas_brutas = buscar_vagas_remotar()
    print(f"📊 Total de vagas brutas encontradas: {len(vagas_brutas)}")
    novas_notificadas = 0

    for vaga in vagas_brutas:
        resultado = avaliar_vaga(vaga)
        print(f"\n🔍 VAGA LIDA: '{vaga.get('titulo')}'")
        print(f"📊 Score: {resultado['score']} (mínimo: {REGRAS_FILTRO['score_corte']})")
        print(f"🎯 Termos: {resultado['matched']}")
        if not resultado["aprovada"]:
            print(f"⏭️ Reprovada: {resultado['motivo'] or 'score insuficiente'}")
            continue

        vaga["score"] = resultado["score"]
        vaga["technologies_matched"] = resultado["matched"]
        inserida = salvar_vaga(vaga)
        status_atual = "pendente" if inserida else status_vaga(vaga["link"])
        if status_atual == "enviada":
            print("⏭️ Já notificada anteriormente.")
            continue

        sucesso, erro = enviar_alerta_telegram(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, vaga)
        if sucesso:
            atualizar_status(vaga["link"], "enviada")
            novas_notificadas += 1
            print(f"✅ Alerta enviado: {vaga['titulo']} ({vaga['empresa']})")
        else:
            atualizar_status(vaga["link"], "falha", erro)
            print(f"❌ Alerta não enviado; será tentado novamente: {erro}")

    print(f"✨ Varredura concluída! {novas_notificadas} novas vagas notificadas.")


if __name__ == "__main__":
    executar_automacao()
