# 🔍 COBOL/JCL Semantic Search

🚀 Projeto para ingestão de documentação COBOL/JCL, vetorização via OpenAI embeddings (text-embedding-3-small) e busca semântica com PostgreSQL + pgvector.

## 🛠️ Setup

### 📦 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 🗄️ 2. Configurar PostgreSQL com pgvector
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```
*(Crie a tabela `documentos_vetorizados` conforme instruções do script)*

### 🔑 3. Configurar Variável de Ambiente
```bash
export OPENAI_API_KEY="sua_chave"
```

### 📁 4. Adicionar Documentos
Coloque seus arquivos `.md` na pasta `documentos/`

### ⚡ 5. Executar Ingestão
```bash
python ingestao.py
```

### 🌐 6. Executar Interface Streamlit
```bash
streamlit run app_streamlit.py
```

## 📊 Métricas de Similaridade

### 1️⃣ Distância Euclidiana (L2 norm)

📐 A distância euclidiana mede o "espaço" entre dois vetores:

```
d(u,v) = √(Σ(uᵢ - vᵢ)²)
```

✅ **Regra**: Vetores mais próximos → menor distância → mais similares

💻 **No PostgreSQL + pgvector**:
```sql
embedding <=> %s::vector
```

ℹ️ O operador `<=>` retorna a distância Euclidiana (L2)

🔧 No `consulta.py`, já usamos `embedding <=> %s::vector` para ordenar por similaridade crescente.

### 2️⃣ Similaridade do Cosseno (Cosine similarity)

📈 Outra abordagem muito usada em NLP é a similaridade do cosseno:

```
cosine_sim(u,v) = (u·v) / (||u|| ||v||)
```

📏 **Valor**: entre -1 e 1, mais próximo de 1 = vetores mais similares

💻 **Com pgvector**, você pode usar o operador `<#>`:
```sql
embedding <#> %s::vector
```

⚡ **Observação**: No caso da OpenAI embeddings, a distância euclidiana e a similaridade do cosseno são praticamente equivalentes para rankings, porque os vetores já são normalizados.

## 📋 Comparação das Métricas

| 📊 Métrica | 🔄 Ordem de similaridade | ⚙️ Quando usar |
|------------|-------------------------|----------------|
| 📐 Euclidiana | menor → mais similar | padrão, rápido, compatível com ivfflat |
| 📈 Cosseno | maior → mais similar | mais intuitivo para NLP puro, funciona bem para vetores normalizados |

## 💡 Dica Final

🎯 Como já estamos usando `<=>` com `ORDER BY embedding <=> %s::vector`, a busca já está funcionando como "proximal similarity".

🔄 Mas se você quiser **cosine similarity**, é só trocar `<=>` por `<#>` e ordenar `DESC`.