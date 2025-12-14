#!/usr/bin/env python3
import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt

# --- CONFIGURAÇÕES DO GRÁFICO ---
ARQUIVO_DADOS = 'hackernews_full_dataset.csv'
ARQUIVO_IMAGEM = 'tendencias_hackernews.png'
TOP_N = 15  # Vamos mostrar as top 15 palavras

# --- FUNÇÕES AUXILIARES (Reutilizando a lógica de limpeza) ---
def limpar_e_contar_palavras(df):
    todos_titulos = " ".join(df['titulo'])
    palavras_brutas = re.findall(r'\b\w+\b', todos_titulos.lower())
    
    stop_words = {
        'of', 'the', 'and', 'to', 'a', 'in', 'for', 'is', 'on', 
        'as', 'i', 'my', 'with', 'by', 'at', 'from', 'be', 'it', 'an',
        'how', 'why', 'what', 'show', 'hn', 'ask', 'are', 'this',
        'that', 'do', 'or', 'can', 'use', 'using', 'over', 'years', 'new', 'not',
        'out', 'up', 'we', 'your', 'its', 'has' # Adicionando mais stop words comuns
    }
    
    palavras_uteis = [p for p in palavras_brutas if p not in stop_words and len(p) > 2]
    return Counter(palavras_uteis)

def gerar_grafico():
    try:
        print(f"[*] Lendo dados de: {ARQUIVO_DADOS}")
        df = pd.read_csv(ARQUIVO_DADOS)
        
        # 1. Processa os dados
        contador = limpar_e_contar_palavras(df)
        top_palavras = contador.most_common(TOP_N)
        
        # Separa em listas para o Matplotlib
        palavras = [item[0] for item in top_palavras]
        frequencias = [item[1] for item in top_palavras]
        
        # Inverte a ordem para o gráfico horizontal (mais frequente no topo)
        palavras.reverse()
        frequencias.reverse()
        
        print(f"[*] Gerando gráfico para as Top {TOP_N} palavras...")
        
        # 2. Cria a figura
        plt.figure(figsize=(10, 8)) # Define o tamanho da imagem
        
        # Cria o gráfico de barras horizontal (barh)
        # Cor 'skyblue' para um visual limpo
        plt.barh(palavras, frequencias, color='skyblue')
        
        # Adiciona títulos e rótulos
        plt.title(f'Top {TOP_N} Tendências no Hacker News (Baseado em {len(df)} manchetes)', fontsize=14)
        plt.xlabel('Frequência de Menções', fontsize=12)
        plt.ylabel('Palavras-Chave', fontsize=12)
        
        # Adiciona os valores exatos na ponta das barras
        for index, value in enumerate(frequencias):
            plt.text(value, index, str(value), va='center')
            
        plt.tight_layout() # Ajusta o layout para nada ficar cortado
        
        # 3. Salva em arquivo PNG
        plt.savefig(ARQUIVO_IMAGEM, dpi=100)
        print(f"[SUCESSO] Gráfico salvo como: {ARQUIVO_IMAGEM}")
        print("Você pode abrir este arquivo no seu explorador de arquivos do Kali.")
        
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{ARQUIVO_DADOS}' não encontrado.")
    except Exception as e:
        print(f"[ERRO] Falha na geração do gráfico: {e}")

if __name__ == "__main__":
    gerar_grafico()
