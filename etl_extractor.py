#!/usr/bin/env python3
import os  # <--- Nova importação necessária
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURAÇÃO DE REDE (Proxy SOCKS5) ---
# Best Practice: Não hardcode IPs. Use variáveis de ambiente.
# Se a variável 'MY_PROXY_URL' não estiver definida, usa o padrão Tor local.
# Exemplo de IP seguro (Tor Default): 'socks5h://127.0.0.1:9050'

DEFAULT_PROXY = 'socks5h://127.0.0.1:9050' # Placeholder genérico seguro
proxy_url = os.getenv('MY_PROXY_URL', DEFAULT_PROXY)

print(f"[*] Configuração de Proxy ativa: {proxy_url}")

proxies = {
    'http': proxy_url,
    'https': proxy_url
}

# Cabeçalho para simular um navegador real no Linux
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def obter_soup(url):
    """
    Realiza a conexão HTTP através do Proxy e retorna o objeto BeautifulSoup.
    """
    try:
        # Timeout de 30s é necessário pois a rede Tor/Proxy pode ser lenta
        response = requests.get(url, proxies=proxies, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"[-] Erro HTTP {response.status_code} ao acessar {url}")
            return None
            
    except Exception as e:
        print(f"[!] Erro de conexão: {e}")
        return None

def processar_dados(soup):
    """
    Extrai os dados brutos do HTML e retorna uma lista de dicionários.
    Captura TODAS as notícias da página (geralmente 30).
    """
    dados_brutos = []
    # Encontra todas as linhas de título (classe CSS usada pelo Hacker News)
    posts = soup.find_all(class_='titleline')
    
    timestamp_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for post in posts:
        try:
            link_tag = post.find('a')
            
            # Verificação de segurança para garantir que a tag existe
            if link_tag:
                item = {
                    'data_coleta': timestamp_atual,
                    'titulo': link_tag.text,
                    'url': link_tag['href'],
                    'origem': 'HackerNews'
                }
                dados_brutos.append(item)
        except AttributeError:
            continue
        
    return dados_brutos

def main():
    print(f"[*] Iniciando Crawler Anônimo via Proxy...")
    print(f"[*] Alvo: Hacker News (Páginas 1 a 3)")
    
    todos_dados = []
    paginas_para_ler = 3  
    
    for pagina in range(1, paginas_para_ler + 1):
        url = f"https://news.ycombinator.com/news?p={pagina}"
        print(f"\n--- Processando Página {pagina}/{paginas_para_ler} ---")
        
        soup = obter_soup(url)
        
        if soup:
            dados_pagina = processar_dados(soup)
            qtd = len(dados_pagina)
            
            if qtd > 0:
                todos_dados.extend(dados_pagina)
                print(f"    [+] {qtd} notícias capturadas nesta página.")
            else:
                print("    [?] Nenhuma notícia encontrada (estrutura do site mudou?).")
        
        # Delay Ético e de Segurança (Evita banimento)
        if pagina < paginas_para_ler:
            tempo_espera = 5
            print(f"    [zZZ] Aguardando {tempo_espera}s para parecer humano...")
            time.sleep(tempo_espera)
            
    # Salvar o Dataset Completo
    if todos_dados:
        df = pd.DataFrame(todos_dados)
        arquivo_saida = 'hackernews_full_dataset.csv'
        
        # Salva em CSV sem o índice numérico
        df.to_csv(arquivo_saida, index=False, encoding='utf-8')
        
        print("\n" + "="*50)
        print(f"[SUCESSO TOTAL] Dataset salvo: {arquivo_saida}")
        print(f"Total de registros: {len(df)}")
        print("="*50)
        
        # Mostra as últimas 3 notícias para confirmação visual
        print("\nÚltimos registros coletados:")
        print(df[['titulo']].tail(3))
    else:
        print("\n[-] Falha: Nenhum dado foi coletado em nenhuma página.")

if __name__ == "__main__":
    main()
