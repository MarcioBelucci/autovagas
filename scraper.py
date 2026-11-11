from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

URL_REMOTAR = "https://remotar.com.br"
SELETORES_VAGAS = (
    "a[href*='/vaga/'], a[href*='/vagas/'], "
    "a[href*='/job/'], a[href*='/jobs/'], a[href*='/search/jobs/']"
)


def buscar_vagas_remotar():
    """Coleta links de vagas do Remotar, usando o texto integral do card."""
    vagas_coletadas = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"),
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()
        try:
            print("🔍 Acessando Remotar para buscar vagas...")
            page.goto(URL_REMOTAR, timeout=60000, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                # A página mantém conexões analíticas abertas; o conteúdo pode já estar pronto.
                pass
            page.wait_for_timeout(2000)
            links = page.query_selector_all(SELETORES_VAGAS)
            print(f"🎯 Links de vagas encontrados: {len(links)}")
            if not links:
                page.screenshot(path="erro_remotar.png")
                return []

            for link_el in links[:20]:
                try:
                    href = link_el.get_attribute("href")
                    texto_card = link_el.inner_text().strip()
                    linhas = [linha.strip() for linha in texto_card.splitlines() if linha.strip()]
                    if not href or not linhas:
                        continue
                    titulo_el = link_el.query_selector(
                        "h2, h3, h4, strong, .title, [class*='title']"
                    )
                    titulo = titulo_el.inner_text().strip() if titulo_el else linhas[0]
                    empresa_el = link_el.query_selector(
                        ".company, .empresa, [class*='company']"
                    )
                    empresa = empresa_el.inner_text().strip() if empresa_el else "Confidencial"
                    vagas_coletadas.append({
                        "titulo": titulo, "empresa": empresa, "local": "Remoto",
                        "link": urljoin(URL_REMOTAR, href), "plataforma": "Remotar",
                        "descricao": texto_card,
                    })
                except Exception as erro:
                    print(f"⚠️ Card ignorado: {erro}")
        except Exception as erro:
            print(f"❌ Erro durante o scraping do Remotar: {erro}")
        finally:
            context.close()
            browser.close()

    return list({vaga["link"]: vaga for vaga in vagas_coletadas}.values())
