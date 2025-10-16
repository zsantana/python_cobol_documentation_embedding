import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Dashboard - Documentos COBOL Vetorizados",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def get_database_connection():
    """Conecta ao banco de dados PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            dbname=os.getenv("POSTGRES_DB", "cobol_docs"),
            user=os.getenv("POSTGRES_USER", "admin"),
            password=os.getenv("POSTGRES_PASSWORD", "admin123"),
            port=os.getenv("POSTGRES_PORT", "5432")
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar com o banco de dados: {e}")
        return None

@st.cache_data
def load_vectorized_data():
    """Carrega os dados vetorizados do banco de dados"""
    conn = get_database_connection()
    if conn is None:
        return None
    
    try:
        query = """
        SELECT 
            id,
            nome_arquivo,
            step_name,
            programa,
            dataset,
            chunk_id,
            conteudo,
            embedding,
            created_at
        FROM documentos_vetorizados
        ORDER BY nome_arquivo, chunk_id
        """
        
        df = pd.read_sql_query(query, conn)
        
        # Converter embedding de string/lista para array numpy
        if not df.empty:
            def parse_embedding(x):
                if x is None:
                    return None
                try:
                    if isinstance(x, str):
                        # Remove caracteres extras e converte para lista
                        clean_str = x.replace('[', '').replace(']', '').replace('\n', '').replace(' ', '')
                        return np.array([float(val) for val in clean_str.split(',') if val])
                    elif isinstance(x, list):
                        return np.array(x)
                    else:
                        return np.array(x)
                except Exception as e:
                    st.warning(f"Erro ao processar embedding: {e}")
                    return None
            
            df['embedding_array'] = df['embedding'].apply(parse_embedding)
            df['tamanho_conteudo'] = df['conteudo'].str.len()
            df['numero_palavras'] = df['conteudo'].str.split().str.len()
        
        return df
    
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

def create_summary_metrics(df):
    """Cria métricas resumidas dos dados"""
    if df is None or df.empty:
        st.warning("Nenhum dado encontrado no banco de dados.")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📄 Total de Documentos", df['nome_arquivo'].nunique())
    
    with col2:
        st.metric("🧩 Total de Chunks", len(df))
    
    with col3:
        st.metric("💻 Programas Únicos", df['programa'].nunique())
    
    with col4:
        st.metric("📊 Datasets Únicos", df['dataset'].nunique())

def create_documents_distribution_chart(df):
    """Gráfico de distribuição de documentos por arquivo"""
    if df is None or df.empty:
        return
    
    doc_counts = df.groupby('nome_arquivo').agg({
        'chunk_id': 'count',
        'tamanho_conteudo': 'sum',
        'numero_palavras': 'sum'
    }).reset_index()
    doc_counts.columns = ['Arquivo', 'Chunks', 'Tamanho Total', 'Palavras Totais']
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Chunks por Arquivo', 'Tamanho do Conteúdo por Arquivo', 
                       'Palavras por Arquivo', 'Distribuição de Programas'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "pie"}]]
    )
    
    # Chunks por arquivo
    fig.add_trace(
        go.Bar(x=doc_counts['Arquivo'], y=doc_counts['Chunks'], 
               name='Chunks', marker_color='lightblue'),
        row=1, col=1
    )
    
    # Tamanho por arquivo
    fig.add_trace(
        go.Bar(x=doc_counts['Arquivo'], y=doc_counts['Tamanho Total'], 
               name='Tamanho', marker_color='lightgreen'),
        row=1, col=2
    )
    
    # Palavras por arquivo
    fig.add_trace(
        go.Bar(x=doc_counts['Arquivo'], y=doc_counts['Palavras Totais'], 
               name='Palavras', marker_color='orange'),
        row=2, col=1
    )
    
    # Distribuição de programas
    programa_counts = df['programa'].value_counts()
    fig.add_trace(
        go.Pie(labels=programa_counts.index, values=programa_counts.values,
               name='Programas'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="📊 Análise dos Documentos Vetorizados")
    return fig

def create_embedding_visualization(df, method='PCA'):
    """Visualização dos embeddings em 2D usando PCA ou t-SNE"""
    if df is None or df.empty or 'embedding_array' not in df.columns:
        st.warning("Dados de embedding não disponíveis para visualização.")
        return None
    
    try:
        # Filtrar embeddings válidos (não None)
        valid_embeddings = df[df['embedding_array'].notna()].copy()
        if valid_embeddings.empty:
            st.warning("Nenhum embedding válido encontrado.")
            return None
        
        # Preparar os embeddings - verificar se todos têm o mesmo tamanho
        embedding_list = []
        valid_indices = []
        
        for idx, embedding in enumerate(valid_embeddings['embedding_array'].values):
            if embedding is not None and len(embedding) > 0:
                embedding_list.append(embedding)
                valid_indices.append(idx)
        
        if len(embedding_list) < 2:
            st.warning("Número insuficiente de embeddings válidos para visualização (mínimo 2).")
            return None
        
        embeddings_matrix = np.vstack(embedding_list)
        valid_df = valid_embeddings.iloc[valid_indices].copy()
        
        # Redução de dimensionalidade
        if method == 'PCA':
            reducer = PCA(n_components=2, random_state=42)
            embeddings_2d = reducer.fit_transform(embeddings_matrix)
            title = f"Visualização PCA dos Embeddings (Variância Explicada: {reducer.explained_variance_ratio_.sum():.2%})"
        else:  # t-SNE
            perplexity = min(30, len(valid_df) - 1)
            if perplexity < 1:
                perplexity = 1
            reducer = TSNE(n_components=2, random_state=42, perplexity=perplexity)
            embeddings_2d = reducer.fit_transform(embeddings_matrix)
            title = "Visualização t-SNE dos Embeddings"
        
        # Criar DataFrame para plotagem
        valid_df['x'] = embeddings_2d[:, 0]
        valid_df['y'] = embeddings_2d[:, 1]
        
        # Criar gráfico interativo
        fig = px.scatter(
            valid_df,
            x='x', y='y',
            color='nome_arquivo',
            hover_data={
                'programa': True,
                'step_name': True,
                'chunk_id': True,
                'numero_palavras': True,
                'x': False,
                'y': False
            },
            title=title,
            labels={'x': f'{method} Componente 1', 'y': f'{method} Componente 2'}
        )
        
        fig.update_traces(marker=dict(size=8, opacity=0.7))
        fig.update_layout(height=600)
        
        return fig
    
    except Exception as e:
        st.error(f"Erro ao criar visualização de embeddings: {e}")
        return None

def create_content_analysis_chart(df):
    """Análise do conteúdo dos chunks"""
    if df is None or df.empty:
        return None
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Distribuição do Tamanho dos Chunks', 'Distribuição do Número de Palavras',
                       'Chunks por Step Name', 'Timeline de Criação'),
        specs=[[{"type": "histogram"}, {"type": "histogram"}],
               [{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # Histograma do tamanho dos chunks
    fig.add_trace(
        go.Histogram(x=df['tamanho_conteudo'], nbinsx=20, name='Tamanho', 
                    marker_color='skyblue'),
        row=1, col=1
    )
    
    # Histograma do número de palavras
    fig.add_trace(
        go.Histogram(x=df['numero_palavras'], nbinsx=20, name='Palavras', 
                    marker_color='lightcoral'),
        row=1, col=2
    )
    
    # Chunks por step name
    step_counts = df['step_name'].value_counts()
    fig.add_trace(
        go.Bar(x=step_counts.index, y=step_counts.values, 
               name='Steps', marker_color='gold'),
        row=2, col=1
    )
    
    # Timeline de criação
    df['created_date'] = pd.to_datetime(df['created_at']).dt.date
    timeline_counts = df.groupby('created_date').size().reset_index(name='count')
    fig.add_trace(
        go.Scatter(x=timeline_counts['created_date'], y=timeline_counts['count'],
                  mode='lines+markers', name='Documentos Criados', line_color='green'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, 
                     title_text="📈 Análise Detalhada do Conteúdo")
    return fig

def main():
    """Função principal do dashboard"""
    st.title("📊 Dashboard - Documentos COBOL Vetorizados")
    st.markdown("---")
    
    # Sidebar para filtros
    st.sidebar.header("🎛️ Controles")
    
    # Carregar dados
    with st.spinner("Carregando dados do banco..."):
        df = load_vectorized_data()
    
    if df is None or df.empty:
        st.error("Não foi possível carregar os dados ou não há dados no banco.")
        st.info("Execute o script de ingestão primeiro para popularizar o banco de dados.")
        return
    
    # Filtros na sidebar
    arquivos_selecionados = st.sidebar.multiselect(
        "Filtrar por Arquivos:",
        options=df['nome_arquivo'].unique(),
        default=df['nome_arquivo'].unique()
    )
    
    programas_selecionados = st.sidebar.multiselect(
        "Filtrar por Programas:",
        options=df['programa'].dropna().unique(),
        default=df['programa'].dropna().unique()
    )
    
    # Aplicar filtros
    df_filtered = df[
        (df['nome_arquivo'].isin(arquivos_selecionados)) &
        (df['programa'].isin(programas_selecionados) | df['programa'].isna())
    ]
    
    # Métricas resumidas
    st.subheader("📋 Resumo dos Dados")
    create_summary_metrics(df_filtered)
    
    st.markdown("---")
    
    # Gráficos de distribuição
    st.subheader("📊 Análise de Distribuição")
    fig_dist = create_documents_distribution_chart(df_filtered)
    if fig_dist:
        st.plotly_chart(fig_dist, use_container_width=True)
    
    st.markdown("---")
    
    # Visualização de embeddings
    st.subheader("🔍 Visualização dos Embeddings")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        method = st.selectbox("Método de Redução:", ["PCA", "t-SNE"])
        if st.button("🔄 Regenerar Visualização"):
            st.cache_data.clear()
            st.rerun()
    
    with col1:
        fig_embed = create_embedding_visualization(df_filtered, method)
        if fig_embed:
            st.plotly_chart(fig_embed, use_container_width=True)
    
    st.markdown("---")
    
    # Análise de conteúdo
    st.subheader("📈 Análise de Conteúdo")
    fig_content = create_content_analysis_chart(df_filtered)
    if fig_content:
        st.plotly_chart(fig_content, use_container_width=True)
    
    st.markdown("---")
    
    # Tabela de dados detalhados
    if st.checkbox("📋 Mostrar Dados Detalhados"):
        st.subheader("Dados Brutos")
        st.dataframe(
            df_filtered[['nome_arquivo', 'programa', 'step_name', 'dataset', 
                        'chunk_id', 'numero_palavras', 'tamanho_conteudo', 'created_at']],
            use_container_width=True
        )

if __name__ == "__main__":
    main()
