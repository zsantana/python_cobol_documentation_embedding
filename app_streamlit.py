import streamlit as st
from consulta import buscar_similares

st.set_page_config(page_title="Explorador COBOL/JCL", layout="wide")
st.title("🔎 Buscador Semântico de Programas COBOL/JCL")

consulta = st.text_input("Descreva o que deseja encontrar (ex: 'rotinas de cálculo do INSS')")

col1, col2 = st.columns(2)
programa = col1.text_input("Filtrar por programa (opcional)")
dataset = col2.text_input("Filtrar por dataset (opcional)")

if consulta:
    resultados = buscar_similares(consulta, programa, dataset, top_k=5)
    for nome, step, prog, dsn, conteudo, score in resultados:
        with st.expander(f"📄 {nome} | {prog or '-'} | step {step or '-'} | similaridade {score:.3f}"):
            st.markdown(f"**Dataset:** {dsn or '-'}\n\n---\n{conteudo}")
