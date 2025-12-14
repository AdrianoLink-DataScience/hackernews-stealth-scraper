#!/usr/bin/env python3
import pandas as pd
from collections import Counter
import re

def analisar_frequencia():
    # Aponta para o dataset completo
    arquivo = 'hackernews_full_dataset.csv'
    
    try:
        print(f"[*] Lendo dados de: {arquivo}")
        df = pd.read_csv(arquivo)
        print(f"[*] Volume analisado: {len(df)} manchetes")
        
        todos_titulos = " ".join(df['titulo'])
        palavras_brutas = re.findall(r'\b\w+\b', todos_titulos.lower())
        
        # Lista expandida de Stop Words para remover ruído
        stop_words = {
            'of', 'the', 'and', 'to', 'a', 'in', 'for', 'is', 'on', 
            'as', 'i', 'my', 'with', 'by', 'at', 'from', 'be', 'it', 'an',
            'how', 'why', 'what', 'show', 'hn', 'ask', 'are', 'this',
            'that', 'do', 'or', 'can', 'use', 'using', 'over', 'years', 'new', 'not'
        }
        
        palavras_uteis = [p for p in palavras_brutas if p not in stop_words and len(p) > 2]
        
        contador = Counter(palavras_uteis)
        top_10 = contador.most_common(10)
        
        print("\n--- TOP 10 TENDÊNCIAS REAIS (Sem Ruído) ---")
        print(f"{'PALAVRA':<15} | {'FREQ':<6} | {'GRÁFICO'}")
        print("-" * 45)
        
        for palavra, freq in top_10:
            barra = '█' * freq
            print(f"{palavra:<15} | {freq:<6} | {barra}")

        print("\n--- MONITORAMENTO ESPECÍFICO ---")
        termos = ['linux', 'ai', 'llm', 'python', 'rust', 'google', 'security']
        for termo in termos:
            if contador[termo] > 0:
                print(f"-> {termo.title()}: {contador[termo]}")

    except Exception as e:
        print(f"[ERRO] {e}")

if __name__ == "__main__":
    analisar_frequencia()
