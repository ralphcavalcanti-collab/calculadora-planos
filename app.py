import streamlit as st

# Configuração da aba do navegador
st.set_page_config(page_title="Calculadora de Orçamentos", page_icon="🩺")

# --- TELA DE SENHA ---
st.title("Acesso Restrito 🔒")
senha_digitada = st.text_input("Digite a senha para acessar a calculadora:", type="password")

if senha_digitada == "senha123": 
    
    st.divider()
    st.title("Calculadora de Orçamentos 🩺")
    st.write("Selecione as opções abaixo para gerar o orçamento do paciente.")

    # --- VALORES BASE ---
    valor_hora_presencial = 750
    valor_hora_acompanhamento_pres = 500
    valor_consulta_online = 550
    valor_hora_acompanhamento_on = 350
    valor_nutri = 250
    
    # Valores Medicação (Custos invisíveis para o usuário final)
    margem_lucro = 1.50
    
    custo_base_tirzepatida = 63.74
    venda_2_5mg = custo_base_tirzepatida * 1 * margem_lucro
    venda_5_0mg = custo_base_tirzepatida * 2 * margem_lucro
    venda_7_5mg = custo_base_tirzepatida * 3 * margem_lucro
    venda_10_0mg = custo_base_tirzepatida * 4 * margem_lucro
    
    custo_vitamina = 20.00
    venda_vitamina = custo_vitamina * margem_lucro

    # --- INTERFACE (BOTÕES E MENUS) ---
    col1, col2 = st.columns(2)
    with col1:
        primeira_vez = st.radio("O paciente é de Primeira Vez?", ["Sim", "Não"])
    with col2:
        modalidade = st.radio("Modalidade de atendimento:", ["Online (Telemedicina)", "Presencial"])

    st.divider()

    valor_medico = 0
    qtd_nutri = 0
    nome_plano = ""
    
    # --- LÓGICA ONLINE ---
    if modalidade == "Online (Telemedicina)":
        opcao = st.selectbox("Escolha o pacote Online:", [
            "Selecione uma opção...",
            "Plano de Acompanhamento Online (2 Meses)",
            "1 Consulta TM Avulsa",
            "2
