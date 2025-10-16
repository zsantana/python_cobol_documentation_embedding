# Setup Docker para PostgreSQL com pgvector

Este projeto inclui um ambiente Docker com PostgreSQL habilitado com a extensão pgvector e pgAdmin para administração.

## Serviços Incluídos

### PostgreSQL com pgvector
- **Imagem**: `pgvector/pgvector:pg16`
- **Porta**: 5432
- **Banco**: cobol_docs
- **Usuário**: admin
- **Senha**: admin123

### pgAdmin
- **Imagem**: `dpage/pgadmin4:latest`
- **Porta**: 5050
- **Email**: admin@admin.com
- **Senha**: admin123

## Como usar

### 1. Iniciar os serviços
```bash
docker-compose up -d
```

### 2. Verificar status dos containers
```bash
docker-compose ps
```

### 3. Acessar pgAdmin
Abra o navegador e acesse: http://localhost:5050

- Email: admin@admin.com
- Senha: admin123

### 4. Conectar ao PostgreSQL via pgAdmin
Após fazer login no pgAdmin, adicione um novo servidor:

- **Host**: postgres (nome do container)
- **Port**: 5432
- **Database**: cobol_docs
- **Username**: admin
- **Password**: admin123

### 5. Conectar via aplicação Python
```python
import psycopg2

# String de conexão
conn_string = "postgresql://admin:admin123@localhost:5432/cobol_docs"

# Ou usando variáveis de ambiente
import os
from dotenv import load_dotenv

load_dotenv()
conn_string = os.getenv('DATABASE_URL')
```

## Recursos Disponíveis

### Extensão pgvector
A extensão pgvector está habilitada e permite:
- Armazenamento de vetores de embedding
- Busca por similaridade usando índices otimizados
- Funções de distância: coseno, euclidiana, produto interno

### Schema e Tabelas
O banco é inicializado com:
- Tabela `documentos_vetorizados` para armazenar documentos COBOL processados
- Campos: nome_arquivo, step_name, programa, dataset, chunk_id, conteudo, embedding
- Índices otimizados para busca vetorial e consultas por metadados

### Exemplo de uso com embeddings
```sql
-- Inserir documento com embedding
INSERT INTO documentos_vetorizados (nome_arquivo, step_name, programa, dataset, chunk_id, conteudo, embedding)
VALUES (
    'exemplo_cobol.md',
    'STEP010',
    'PROGRAMA01',
    'PROD.COBOL.SOURCE',
    0,
    'IDENTIFICATION DIVISION...',
    '[0.1, 0.2, 0.3, ...]'::vector
);

-- Buscar documentos similares
SELECT nome_arquivo, programa, conteudo, 
       1 - (embedding <=> '[0.1, 0.2, 0.3, ...]'::vector) AS similarity
FROM documentos_vetorizados
ORDER BY embedding <=> '[0.1, 0.2, 0.3, ...]'::vector
LIMIT 5;

-- Buscar por programa específico
SELECT * FROM documentos_vetorizados WHERE programa = 'PROGRAMA01';

-- Estatísticas por programa
SELECT programa, COUNT(*) as total_chunks, 
       COUNT(DISTINCT nome_arquivo) as arquivos
FROM documentos_vetorizados 
GROUP BY programa 
ORDER BY total_chunks DESC;
```

## Comandos Úteis

### Parar os serviços
```bash
docker-compose down
```

### Parar e remover volumes (CUIDADO: apaga dados)
```bash
docker-compose down -v
```

### Ver logs
```bash
docker-compose logs postgres
docker-compose logs pgadmin
```

### Backup do banco
```bash
docker-compose exec postgres pg_dump -U admin cobol_docs > backup.sql
```

### Restaurar backup
```bash
docker-compose exec -T postgres psql -U admin cobol_docs < backup.sql
```

## Configuração

Copie o arquivo `.env.example` para `.env` e ajuste as configurações conforme necessário:

```bash
cp .env.example .env
```

## Troubleshooting

### Problema: Container não inicia
- Verifique se as portas 5432 e 8080 não estão em uso
- Execute: `docker-compose logs` para ver os erros

### Problema: Não consegue conectar ao banco
- Verifique se o container está rodando: `docker-compose ps`
- Teste a conexão: `docker-compose exec postgres psql -U admin -d cobol_docs`

### Problema: pgAdmin não carrega
- Aguarde alguns segundos para o serviço inicializar completamente
- Verifique os logs: `docker-compose logs pgadmin`
