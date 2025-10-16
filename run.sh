#!/bin/bash

# Script de inicialização para o projeto COBOL Documentation Embedding
# Este script facilita a execução dos diferentes componentes do sistema

echo "🚀 Sistema de Documentação COBOL com Embeddings"
echo "=============================================="

# Verificar se o .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📝 Crie um arquivo .env com as seguintes variáveis:"
    echo ""
    echo "OPENAI_API_KEY=sua_api_key_aqui"
    echo "POSTGRES_HOST=localhost"
    echo "POSTGRES_DB=cobol_docs"
    echo "POSTGRES_USER=admin"
    echo "POSTGRES_PASSWORD=admin123"
    echo "POSTGRES_PORT=5432"
    echo ""
    exit 1
fi

# Menu de opções
echo ""
echo "Escolha uma opção:"
echo "1) 📊 Executar Dashboard de Gráficos (porta 8501)"
echo "2) 🔎 Executar Busca Semântica (porta 8502)"
echo "3) 🗄️ Executar Ingestão de Documentos"
echo "4) 🐳 Iniciar Docker Compose (PostgreSQL)"
echo "5) 🛑 Parar Docker Compose"
echo "6) 📋 Instalar Dependências Python"
echo "0) ❌ Sair"
echo ""

read -p "Digite sua opção: " option

case $option in
    1)
        echo "📊 Iniciando Dashboard de Gráficos..."
        streamlit run dashboard_graficos.py --server.port 8501
        ;;
    2)
        echo "🔎 Iniciando Busca Semântica..."
        streamlit run app_streamlit.py --server.port 8502
        ;;
    3)
        echo "🗄️ Executando ingestão de documentos..."
        python ingestao.py
        ;;
    4)
        echo "🐳 Iniciando Docker Compose..."
        docker-compose up -d
        echo "✅ PostgreSQL iniciado! Aguarde alguns segundos para inicialização completa."
        ;;
    5)
        echo "🛑 Parando Docker Compose..."
        docker-compose down
        echo "✅ Serviços parados."
        ;;
    6)
        echo "📋 Instalando dependências Python..."
        pip install -r requirements.txt
        echo "✅ Dependências instaladas."
        ;;
    0)
        echo "👋 Saindo..."
        exit 0
        ;;
    *)
        echo "❌ Opção inválida!"
        exit 1
        ;;
esac
