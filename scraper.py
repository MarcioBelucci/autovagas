from playwright.sync_api import sync_playwright

def buscar_vagas_remotar():
    """
    Scraper atualizado para extrair vagas abertas no Remotar com seletores robustos.
    """
    vagas_coletadas = []
    
    with sync_playwright() as p:
        # Lançamos o navegador no modo headless (ou com headless=False para ver o navegador abrindo)
        # Adicionamos argumentos para evitar detecção de bot
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        
        # Criamos um contexto com um User-Agent real de navegador Chrome
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        
        try:
            print("🔍 Acessando Remotar para buscar vagas...")
            # Aumentamos o timeout e usamos 'domcontentloaded' para garantir o carregamento
            page.goto("https://remotar.com.br", timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(3000) # Aguarda a renderização do React/JS
            
            # Tentamos múltiplos seletores possíveis que o Remotar costuma usar em seus cards
            seletores_cards = ["article", ".job-card", "div[class*='job']", "a[href*='/vaga/']"]
            
            cards = []
            for seletor in seletores_cards:
                cards = page.query_selector_all(seletor)
                if len(cards) > 0:
                    print(f"🎯 Elementos encontrados com o seletor: '{seletor}' (Total: {len(cards)})")
                    break
            
            if not cards:
                print("⚠️ Nenhum card encontrado com os seletores padrão. Salvando página para análise...")
                page.screenshot(path="erro_remotar.png")
                return []
            
            for card in cards[:20]: # Analisa até os 20 primeiros elementos
                try:
                    titulo_el = card.query_selector("h2, h3, h4, a span, strong, .title, [class*='title']")
                    empresa_el = card.query_selector(".company, .empresa, span[class*='company']")
                    link_el = card.query_selector("a")
                    
                    # Tenta capturar o texto de data/tempo (ex: "há 2 dias", "1 semana atrás")
                    data_el = card.query_selector("time, .date, span[class*='date'], span[class*='time']")
                    texto_data = data_el.inner_text().lower() if data_el else card.inner_text().lower()
                    
                    titulo = titulo_el.inner_text().strip() if titulo_el else ""
                    if not titulo or len(titulo) < 3:
                        titulo = card.inner_text().split("\n")[0].strip()
                        
                    empresa = empresa_el.inner_text().strip() if empresa_el else "Confidencial"
                    link = link_el.get_attribute("href") if link_el else ""
                    
                    if link:
                        if not link.startswith("http"):
                            link = f"https://remotar.com.br{link}"
                        
                        if titulo and len(titulo) > 3:
                            vagas_coletadas.append({
                                "titulo": titulo,
                                "empresa": empresa,
                                "local": "Remoto",
                                "link": link,
                                "plataforma": "Remotar",
                                "descricao": f"{titulo} {empresa}",
                                "texto_data": texto_data  # Guardamos para filtrar depois
                            })
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"❌ Erro durante o scraping do Remotar: {e}")
        finally:
            browser.close()
            
    # Remove duplicatas baseadas no link coletado na mesma rodada
    vagas_unicas = {v['link']: v for v in vagas_coletadas}.values()
    return list(vagas_unicas)

if __name__ == "__main__":
    # Teste isolado do scraper
    resultados = buscar_vagas_remotar()
    print(f"✨ Vagas válidas extraídas: {len(resultados)}")
    for v in resultados[:5]:
        print(f"- {v['titulo']} | {v['empresa']} | {v['link']}")