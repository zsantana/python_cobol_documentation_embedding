import re
import tiktoken
from rich import print

def extrair_metadados(texto: str):
    # Step name (//STEP001 EXEC ...)
    step = re.findall(r"//(\w+)\s+EXEC", texto)
    step_name = step[0] if step else None

    # Programa chamado (PGM=ABC123)
    programa = re.findall(r"PGM=([\w\d]+)", texto)
    programa = programa[0] if programa else None

    # Dataset (DSN=XXXX.YYYY.ZZZZ)
    dataset = re.findall(r"DSN=([\w\.\-]+)", texto)
    dataset = dataset[0] if dataset else None

    return step_name, programa, dataset

def dividir_em_chunks_por_tokens(texto, max_tokens=400, overlap=80, modelo="text-embedding-ada-002"):
    """
    Divide o texto em chunks baseados em tokens, com sobreposição.
    """
    enc = tiktoken.encoding_for_model(modelo)
    tokens = enc.encode(texto)

    print(f"Total tokens: {len(tokens)}")
    print(f"Max tokens: {max_tokens}")
    print(f"Overlap: {overlap}")
    

    # Dividir em chunks
    chunks = []
    inicio = 0

    while inicio < len(tokens):
        fim = inicio + max_tokens
        chunk_tokens = tokens[inicio:fim]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text.strip())
        inicio += max_tokens - overlap  # move com sobreposição

    return chunks
