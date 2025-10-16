# 📊 Dashboard de Gráficos - Documentos COBOL Vetorizados

Este dashboard apresenta visualizações interativas dos dados vetorizados dos documentos COBOL/JCL.

## 🚀 Como Executar

### Opção 1: Dashboard Independente
```bash
streamlit run dashboard_graficos.py
```

### Opção 2: Via App Principal
```bash
streamlit run app_streamlit.py
```
Depois selecione "📊 Dashboard de Gráficos" na barra lateral.

### Opção 3: Via Script de Inicialização
```bash
./run.sh
```
Escolha a opção 1 no menu.

## 📈 Recursos do Dashboard

### 1. Métricas Resumidas
- Total de documentos processados
- Número total de chunks
- Programas únicos identificados
- Datasets únicos encontrados

### 2. Análise de Distribuição
- **Chunks por Arquivo**: Quantos chunks cada documento foi dividido
- **Tamanho do Conteúdo**: Volume de texto por documento
- **Palavras por Arquivo**: Contagem de palavras por documento
- **Distribuição de Programas**: Gráfico pizza dos programas identificados

### 3. Visualização de Embeddings
- **PCA**: Redução de dimensionalidade com Principal Component Analysis
- **t-SNE**: Visualização não-linear com t-Distributed Stochastic Neighbor Embedding
- Pontos coloridos por arquivo de origem
- Hover interativo com informações detalhadas

### 4. Análise de Conteúdo
- **Histograma de Tamanhos**: Distribuição dos tamanhos dos chunks
- **Histograma de Palavras**: Distribuição do número de palavras
- **Chunks por Step**: Análise por step name do JCL
- **Timeline**: Quando os documentos foram processados

### 5. Filtros Interativos
- Filtro por arquivos específicos
- Filtro por programas COBOL
- Atualização automática de todos os gráficos

### 6. Dados Detalhados
- Tabela completa com todos os dados processados
- Exportação possível (via interface Streamlit)

## 🔧 Configuração Necessária

### Variáveis de Ambiente (.env)
```
OPENAI_API_KEY=sua_chave_api_openai
POSTGRES_HOST=localhost
POSTGRES_DB=cobol_docs
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_PORT=5432
```

### Dependências Python
```bash
pip install -r requirements.txt
```

### Banco de Dados
O PostgreSQL deve estar rodando com dados já processados via `ingestao.py`.

## 🎯 Interpretando os Gráficos

### Visualização de Embeddings
- **Pontos próximos**: Documentos com conteúdo semanticamente similar
- **Cores diferentes**: Arquivos de origem diferentes
- **Clusters**: Agrupamentos naturais de documentos relacionados

### PCA vs t-SNE
- **PCA**: Melhor para entender a variância dos dados
- **t-SNE**: Melhor para visualizar clusters e padrões locais

### Distribuições
- **Histogramas**: Identificam padrões nos tamanhos dos chunks
- **Timeline**: Mostra quando os dados foram processados
- **Barras**: Comparam volumes entre diferentes categorias

## 🐛 Troubleshooting

### Erro de Conexão com Banco
- Verifique se o PostgreSQL está rodando: `docker-compose up -d`
- Confirme as variáveis de ambiente no arquivo `.env`

### Dados Não Carregam
- Execute primeiro: `python ingestao.py`
- Verifique se há documentos na pasta `documentos/`

### Erro de Embedding
- Confirme se a API key da OpenAI está correta
- Verifique se os embeddings foram processados corretamente

### Performance Lenta
- Para muitos documentos, use filtros para reduzir o conjunto de dados
- t-SNE é mais lento que PCA para datasets grandes

## 📊 Exemplos de Uso

1. **Identificar Documentos Similares**: Use a visualização de embeddings para encontrar clusters
2. **Analisar Distribuição**: Veja como os documentos foram divididos em chunks
3. **Monitorar Processamento**: Use a timeline para acompanhar o progresso da ingestão
4. **Filtrar por Contexto**: Use os filtros para focar em programas ou arquivos específicos

## 🔄 Atualizações

Para atualizar os dados após nova ingestão:
1. Clique em "🔄 Regenerar Visualização" 
2. Ou reinicie o dashboard: `Ctrl+C` e execute novamente
