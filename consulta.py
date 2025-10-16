import psycopg2
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    dbname=os.getenv("POSTGRES_DB", "cobol_docs"),
    user=os.getenv("POSTGRES_USER", "admin"),
    password=os.getenv("POSTGRES_PASSWORD", "admin123"),
    port=os.getenv("POSTGRES_PORT", "5432")
)
cur = conn.cursor()

def buscar_similares(consulta, top_k=5):
    embedding = client.embeddings.create(
        model="text-embedding-ada-002",
        input=consulta
    ).data[0].embedding

    query = """
        SELECT nome_arquivo, step_name, programa, dataset, conteudo,
               1 - (embedding <=> %s::vector) AS similaridade
        FROM documentos_vetorizados
    """
    filtros = []
    params = [embedding]

    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    query += " ORDER BY embedding <=> %s::vector LIMIT %s"
    params.extend([embedding, top_k])

    cur.execute(query, params)
    return cur.fetchall()
