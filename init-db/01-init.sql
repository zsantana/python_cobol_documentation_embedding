-- Script de inicialização do banco de dados
-- Este script é executado automaticamente quando o container do PostgreSQL é criado

-- Criar a extensão pgvector se não existir
CREATE EXTENSION IF NOT EXISTS vector;

-- Criar schema para documentos COBOL
CREATE SCHEMA IF NOT EXISTS cobol_docs;

-- Tabela para armazenar documentos COBOL vetorizados conforme rotina de ingestão
CREATE TABLE IF NOT EXISTS documentos_vetorizados (
    id SERIAL PRIMARY KEY,
    nome_arquivo VARCHAR(255) NOT NULL,
    step_name VARCHAR(100),
    programa VARCHAR(100),
    dataset VARCHAR(200),
    chunk_id INTEGER NOT NULL,
    conteudo TEXT NOT NULL,
    embedding vector(1536), -- dimensão padrão para OpenAI text-embedding-3-small
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índice para busca de similaridade de vetores
CREATE INDEX IF NOT EXISTS idx_documentos_embedding 
ON documentos_vetorizados 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Índices adicionais para otimizar buscas
CREATE INDEX IF NOT EXISTS idx_documentos_nome_arquivo 
ON documentos_vetorizados (nome_arquivo);

CREATE INDEX IF NOT EXISTS idx_documentos_programa 
ON documentos_vetorizados (programa);

CREATE INDEX IF NOT EXISTS idx_documentos_step_name 
ON documentos_vetorizados (step_name);

CREATE INDEX IF NOT EXISTS idx_documentos_dataset 
ON documentos_vetorizados (dataset);

-- Índice composto para busca por arquivo e chunk
CREATE INDEX IF NOT EXISTS idx_documentos_arquivo_chunk 
ON documentos_vetorizados (nome_arquivo, chunk_id);

-- Função para atualizar timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para atualizar updated_at automaticamente
CREATE TRIGGER update_documentos_updated_at 
    BEFORE UPDATE ON documentos_vetorizados 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comentários nas tabelas e colunas
COMMENT ON TABLE documentos_vetorizados IS 'Tabela para armazenar documentos COBOL vetorizados com embeddings';
COMMENT ON COLUMN documentos_vetorizados.nome_arquivo IS 'Nome do arquivo de origem do documento';
COMMENT ON COLUMN documentos_vetorizados.step_name IS 'Nome do step JCL extraído do documento';
COMMENT ON COLUMN documentos_vetorizados.programa IS 'Nome do programa COBOL identificado';
COMMENT ON COLUMN documentos_vetorizados.dataset IS 'Dataset associado ao documento';
COMMENT ON COLUMN documentos_vetorizados.chunk_id IS 'Identificador do chunk dentro do documento';
COMMENT ON COLUMN documentos_vetorizados.conteudo IS 'Conteúdo textual do chunk do documento';
COMMENT ON COLUMN documentos_vetorizados.embedding IS 'Vetor de embedding do conteúdo (1536 dimensões para OpenAI text-embedding-3-small)';
