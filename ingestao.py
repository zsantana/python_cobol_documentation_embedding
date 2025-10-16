import os
import psycopg2
from openai import OpenAI
from tqdm import tqdm
from utils_regex import extrair_metadados, dividir_em_chunks_por_tokens
import time
from dotenv import load_dotenv
from rich import print

# Carregar variáveis de ambiente
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Conectar usando variáveis de ambiente ou valores padrão
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    dbname=os.getenv("POSTGRES_DB", "cobol_docs"),
    user=os.getenv("POSTGRES_USER", "admin"),
    password=os.getenv("POSTGRES_PASSWORD", "admin123"),
    port=os.getenv("POSTGRES_PORT", "5432")
)
cur = conn.cursor()

def delete_documento():
    cur.execute("""
        DELETE FROM documentos_vetorizados
    """)
    conn.commit()

def inserir_documento(nome_arquivo, step_name, programa, dataset, chunk_id, conteudo, embedding):
    cur.execute("""
        INSERT INTO documentos_vetorizados
        (nome_arquivo, step_name, programa, dataset, chunk_id, conteudo, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nome_arquivo, step_name, programa, dataset, chunk_id, conteudo, embedding))
    conn.commit()

def vetorizar_documentos(diretorio):
    
    delete_documento()
    
    arquivos = [f for f in os.listdir(diretorio) if f.endswith(".md")]
    for nome_arquivo in tqdm(arquivos, desc="Processando arquivos"):
        caminho = os.path.join(diretorio, nome_arquivo)
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()

        step_name, programa, dataset = extrair_metadados(conteudo)
        chunks = dividir_em_chunks_por_tokens(conteudo)

        for i, chunk in enumerate(chunks):
            success = False
            while not success:
                try:
                    response = client.embeddings.create(
                        model="text-embedding-ada-002",
                        input=chunk
                    )
                    embedding = response.data[0].embedding
                    inserir_documento(nome_arquivo, step_name, programa, dataset, i, chunk, embedding)
                    success = True
                except Exception as e:
                    print(f"Erro ao vetorizar chunk {i} de {nome_arquivo}: {e}")
                    time.sleep(2)  # retry simples

if __name__ == "__main__":
    vetorizar_documentos("documentos")
