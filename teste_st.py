import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")
# Título do Dashboard
st.title('Dashboard do Edu Máquina')
# Filtros
st.sidebar.header('Filtros')
search_id_filter=True
# Aplicar filtros
if search_id_filter:
    # Criação das abas
    tab1, tab2, tab3 = st.tabs(["Perfil da Busca", "Ranking de Engajamento", "Engajamento por Sub-Temas"])
    with tab1:
        st.header("Perfil da Busca")
        col1, col2 = st.columns([0.4, 0.6], gap="large")
        with col1:
            st.subheader('Aspectos semânticos...')
        
        with col2:
            st.subheader('Grandes números...')
    with tab2:
        st.header("Ranking de Engajamento")
        st.subheader("Dados Detalhados dos Vídeos")
    with tab3:
        st.header("Engajamento por Sub-Temas")
        
        # Seleção entre temas pais e temas filhos
        theme_type = st.selectbox('Selecione o tipo de tema', ['Temas Pais', 'Temas Filhos'])