from playwright.sync_api import sync_playwright

def buscar_vagas_remotar():
    """
    Scraper atualizado para extrair vagas abertas no Remotar com seletores robustos.
    """
    vagas_coletadas = []
    
    with sync_playwright() as p:
        # headless=True roda o navegador invisível em segundo plano
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print("🔍 Acessando Remotar para buscar vagas...")
            # Aumentamos o timeout e usamos 'domcontentloaded' para garantir o carregamento
            page.goto("https://remotar.com.br", timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(4000) # Aguarda a renderização do React/JS
            
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
                    # Busca específica por títulos em tags de cabeçalho ou links internos
                    titulo_el = card.query_selector("h2, h3, h4, a span, strong, .title, [class*='title']")
                    empresa_el = card.query_selector(".company, .empresa, span[class*='company']")
                    link_el = card.query_selector("a")
                    
                    titulo = titulo_el.inner_text().strip() if titulo_el else ""
                    if not titulo or len(titulo) < 3:
                        # Fallback: se o card inteiro tiver texto limpo
                        titulo = card.inner_text().split("\n")[0].strip()
                        
                    empresa = empresa_el.inner_text().strip() if empresa_el else "Confidencial"
                    link = link_el.get_attribute("href") if link_el else ""
                    
                    if link:
                        if not link.startswith("http"):
                            link = f"https://remotar.com.br{link}"
                        
                        # Evita títulos vazios ou lixo
                        if titulo and len(titulo) > 3 and "vaga" not in titulo.lower() or len(titulo) > 10:
                            vagas_coletadas.append({
                                "titulo": titulo,
                                "empresa": empresa,
                                "local": "Remoto",
                                "link": link,
                                "plataforma": "Remotar",
                                "descricao": f"{titulo} {empresa}" # Usa título e empresa para dar mais termos ao filtro
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