import psycopg2
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
conn = psycopg2.connect(
    host="localhost",
    dbname="documentos",
    user="postgres",
    password="senha"
)
cur = conn.cursor()

def buscar_similares(consulta, programa=None, dataset=None, top_k=5):
    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=consulta
    ).data[0].embedding

    query = """
        SELECT nome_arquivo, step_name, programa, dataset, conteudo,
               1 - (embedding <=> %s::vector) AS similaridade
        FROM documentos_vetorizados
    """
    filtros = []
    params = [embedding]

    if programa:
        filtros.append("programa = %s")
        params.append(programa)
    if dataset:
        filtros.append("dataset = %s")
        params.append(dataset)

    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    query += " ORDER BY embedding <=> %s::vector LIMIT %s"
    params.extend([embedding, top_k])

    cur.execute(query, params)
    return cur.fetchall()
