from playwright.sync_api import sync_playwright
import time

def buscar_vagas_remotar():
    """
    Exemplo de scraper utilizando Playwright para coletar vagas abertas no Remotar.
    """
    vagas_coletadas = []
    
    with sync_playwright() as p:
        # headless=True roda o navegador invisível em segundo plano
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print("🔍 Acessando Remotar para buscar vagas...")
            page.goto("https://remotar.com.br/vagas", timeout=60000)
            page.wait_for_timeout(3000) # Aguarda renderizar
            
            # Seletores de exemplo baseados na estrutura pública do site
            cards = page.query_selector_all(".job-card, article")
            
            for card in cards[:15]: # Limita às 15 primeiras por varredura
                try:
                    titulo_el = card.query_selector("h3, h2")
                    empresa_el = card.query_selector(".company-name, .empresa")
                    link_el = card.query_selector("a")
                    
                    titulo = titulo_el.inner_text().strip() if titulo_el else "Não informado"
                    empresa = empresa_el.inner_text().strip() if empresa_el else "Confidencial"
                    link = link_el.get_attribute("href") if link_el else ""
                    
                    if link and not link.startswith("http"):
                        link = f"https://remotar.com.br{link}"
                        
                    vagas_coletadas.append({
                        "titulo": titulo,
                        "empresa": empresa,
                        "local": "Remoto",
                        "link": link,
                        "plataforma": "Remotar",
                        "descricao": titulo # Usando título provisoriamente se não houver resumo na listagem
                    })
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"Erro durante o scraping do Remotar: {e}")
        finally:
            browser.close()
            
    return vagas_coletadas