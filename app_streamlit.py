import streamlit as st
from consulta import buscar_similares
import subprocess
import sys

st.set_page_config(page_title="Explorador COBOL/JCL", layout="wide")

# Sidebar para navegação
st.sidebar.title("� Navegação")
page = st.sidebar.selectbox(
    "Escolha uma página:",
    ["�🔎 Busca Semântica", "📊 Dashboard de Gráficos"]
)

if page == "🔎 Busca Semântica":
    st.title("🔎 Buscador Semântico de Programas COBOL/JCL")
    
    consulta = st.text_input("Descreva o que deseja encontrar (ex: 'rotinas de cálculo do INSS')")
    
    if consulta:
        with st.spinner("Buscando documentos similares..."):
            resultados = buscar_similares(consulta, top_k=5)
        
        if resultados:
            st.success(f"Encontrados {len(resultados)} resultados:")
            for nome, step, prog, dsn, conteudo, score in resultados:
                with st.expander(f"📄 {nome} | {prog or '-'} | step {step or '-'} | similaridade {score:.3f}"):
                    st.markdown(f"**Dataset:** {dsn or '-'}\n\n---\n{conteudo}")
        else:
            st.warning("Nenhum resultado encontrado para a consulta.")

elif page == "📊 Dashboard de Gráficos":
    st.title("📊 Dashboard - Análise dos Dados Vetorizados")
    
    if st.button("🚀 Abrir Dashboard Completo", help="Abre o dashboard em uma nova aba"):
        st.info("Para abrir o dashboard completo, execute no terminal:")
        st.code("streamlit run dashboard_graficos.py --server.port 8502", language="bash")
    
    st.markdown("---")
    st.markdown("### 📋 Prévia do Dashboard")
    st.info("O dashboard completo inclui:")
    st.markdown("""
    - 📊 **Métricas Resumidas**: Total de documentos, chunks, programas e datasets
    - 📈 **Gráficos de Distribuição**: Análise por arquivo, tamanho e palavras
    - 🔍 **Visualização de Embeddings**: Representação em 2D usando PCA ou t-SNE
    - 📋 **Análise de Conteúdo**: Histogramas e timeline de criação
    - 🎛️ **Filtros Interativos**: Por arquivo e programa
    - 📄 **Dados Detalhados**: Tabela com informações completas
    """)
    
    # Importar e executar uma versão simplificada
    try:
        exec(open('/home/rsantana/projetos/llm/azure/embedding_cobol_doc/dashboard_graficos.py').read())
    except Exception as e:
        st.error(f"Erro ao carregar dashboard: {e}")
        st.info("Execute o dashboard separadamente com: `streamlit run dashboard_graficos.py`")
