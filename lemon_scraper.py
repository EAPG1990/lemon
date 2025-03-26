from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

def setup_driver(headless=False):
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--lang=es-ES")
    if headless:
        chrome_options.add_argument("--headless")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)
    return driver

def get_all_links(driver, url):
    print("\nObteniendo todos los enlaces de la página principal...")
    driver.get(url)
    
    links = driver.find_elements(By.TAG_NAME, 'a')
    href_dict_list = []
    
    for link in links:
        try:
            href = link.get_attribute('href')
            if href and ('help.lemon.me' in href or href.startswith('/')):
                href_dict = {href: []}
                href_dict_list.append(href_dict)
        except Exception as e:
            print(f"Error procesando enlace: {e}")
    
    print(f"Total de enlaces encontrados: {len(href_dict_list)}")
    return href_dict_list

def process_collections(driver, collections_list):
    print("\nProcesando colecciones para obtener artículos...")
    
    # Filtrar solo las URLs de colecciones (que contienen '/collections/')
    filtered_collections = [
        d for d in collections_list 
        if '/collections/' in list(d.keys())[0]]
    
    final_result = []
    
    for collection in filtered_collections:
        collection_url = list(collection.keys())[0]
        print(f"\nProcesando colección: {collection_url}")
        
        try:
            driver.get(collection_url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.flex.flex-col.gap-5")))
            
            articles_container = driver.find_element(By.CSS_SELECTOR, "div.flex.flex-col.gap-5")
            article_links = articles_container.find_elements(By.TAG_NAME, "a")
            
            article_urls = []
            for link in article_links:
                try:
                    href = link.get_attribute('href')
                    if href and '/articles/' in href:
                        article_urls.append(href)
                        print(f" - Artículo encontrado: {href}")
                except Exception as e:
                    print(f"Error procesando enlace: {e}")
            
            final_result.append({collection_url: article_urls})
            time.sleep(2)  # Pausa entre colecciones
            
        except Exception as e:
            print(f"Error procesando colección {collection_url}: {e}")
            final_result.append(collection)  # Mantenemos la colección aunque falle
    
    print("\nProceso de colecciones completado.")
    return final_result

def extract_articles_content(driver, final_result):
    print("\nExtrayendo contenido de los artículos...")
    articles_data = []
    article_id = 1
    
    for collection_dict in final_result:
        for collection_url, article_urls in collection_dict.items():
            print(f"\nProcesando artículos de: {collection_url}")
            
            for article_url in article_urls:
                print(f"\nExtrayendo artículo {article_id}: {article_url}")
                
                try:
                    driver.get(article_url)
                    article_div = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.article.intercom-force-break")))
                    
                    full_text = article_div.text.strip()
                    title = full_text.split('\n')[0] if '\n' in full_text else full_text
                    content = '\n'.join(full_text.split('\n')[1:]).strip() if '\n' in full_text else ""
                    
                    # Extraer categoría del título de la colección
                    driver.get(collection_url)
                    try:
                        category = driver.find_element(By.TAG_NAME, 'h1').text.strip()
                    except:
                        category = "Otro"
                    
                    articles_data.append({
                        "id": f"faq-{article_id}",
                        "title": title,
                        "content": content,
                        "category": category,
                        "url": article_url
                    })
                    article_id += 1
                    time.sleep(1)  # Pausa entre artículos
                    
                except Exception as e:
                    print(f"Error extrayendo artículo {article_url}: {str(e)[:100]}")
    
    print(f"\nExtracción completada. Total de artículos procesados: {len(articles_data)}")
    return articles_data

def main():
    base_url = 'https://help.lemon.me/es/'
    driver = setup_driver()
    
    try:
        # Paso 1: Obtener todos los enlaces
        all_links = get_all_links(driver, base_url)
        
        # Paso 2: Procesar colecciones para obtener artículos
        collections_with_articles = process_collections(driver, all_links)
        
        # Paso 3: Extraer contenido de los artículos
        faq_data = extract_articles_content(driver, collections_with_articles)
        
        # Guardar resultados en JSON
        with open('faq.json', 'w', encoding='utf-8') as f:
            json.dump(faq_data, f, ensure_ascii=False, indent=2)
        
        print("\nProceso completado exitosamente!")
        print(f"Datos guardados en: lemon_faq_complete.json")
        
        # Mostrar ejemplo del resultado
        if faq_data:
            print("\nEjemplo de artículo extraído:")
            print(json.dumps(faq_data[0], indent=2, ensure_ascii=False))
    
    except Exception as e:
        print(f"\nError durante el proceso: {str(e)}")
    
    finally:
        input("\nPresiona Enter para cerrar el navegador...")
        driver.quit()
        print("Navegador cerrado.")

if __name__ == "__main__":
    main()