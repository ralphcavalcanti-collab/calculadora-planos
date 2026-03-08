import streamlit as st

# Configuração da aba do navegador
st.set_page_config(page_title="Calculadora de Orçamentos", page_icon="🩺")

# --- TELA DE SENHA ---
st.title("Acesso Restrito 🔒")
senha_digitada = st.text_input("Digite a senha para acessar a calculadora:", type="password")

# Você pode mudar "senha123" para a senha que preferir
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

    # --- INTERFACE (BOTÕES E MENUS) ---
    col1, col2 = st.columns(2)
    with col1:
        modalidade = st.radio("Modalidade de atendimento:", ["Online (Telemedicina)", "Presencial"])
    with col2:
        primeira_vez = st.radio("O paciente é de Primeira Vez?", ["Sim", "Não"])
    

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
            "2 Consultas TM Avulsas"
        ])
        
        if opcao == "Plano de Acompanhamento Online (2 Meses)":
            nome_plano = opcao
            qtd_nutri = 2
            if primeira_vez == "Sim":
                valor_medico = (3 * valor_consulta_online) + (1 * valor_hora_acompanhamento_on)
            else:
                valor_medico = (2 * valor_consulta_online) + (1 * valor_hora_acompanhamento_on)
                
        elif opcao in ["1 Consulta TM Avulsa", "2 Consultas TM Avulsas"]:
            nome_plano = opcao
            if opcao == "1 Consulta TM Avulsa":
                valor_medico = valor_consulta_online
            else:
                valor_medico = 1000
                
            inclui_nutri = st.radio("Incluir consulta nutricional?", ["Não", "Sim"])
            if inclui_nutri == "Sim":
                qtd_nutri = st.number_input("Quantas consultas com a nutricionista?", min_value=1, step=1)

    # --- LÓGICA PRESENCIAL ---
    elif modalidade == "Presencial":
        opcao = st.selectbox("Escolha o pacote Presencial:", [
            "Selecione uma opção...",
            "Plano Inicial (2 Meses)",
            "Plano Seguimento (3 Meses)",
            "1 Consulta Presencial Avulsa",
            "2 Consultas Presenciais Avulsas"
        ])
        
        if opcao == "Plano Inicial (2 Meses)":
            nome_plano = "Plano Inicial Presencial (2 Meses)"
            qtd_nutri = 2
            if primeira_vez == "Sim":
                valor_medico = (3 * valor_hora_presencial) + (4 * valor_hora_acompanhamento_pres)
            else:
                valor_medico = (2 * valor_hora_presencial) + (4 * valor_hora_acompanhamento_pres)
                
        elif opcao == "Plano Seguimento (3 Meses)":
            nome_plano = "Plano de Seguimento Presencial (3 Meses)"
            qtd_nutri = 3
            valor_medico = (3 * valor_hora_presencial) + (6 * valor_hora_acompanhamento_pres)
            
        elif opcao in ["1 Consulta Presencial Avulsa", "2 Consultas Presenciais Avulsas"]:
            nome_plano = opcao
            if opcao == "1 Consulta Presencial Avulsa":
                valor_medico = valor_hora_presencial
            else:
                valor_medico = 1400
                
            inclui_nutri = st.radio("Incluir consulta nutricional?", ["Não", "Sim"])
            if inclui_nutri == "Sim":
                qtd_nutri = st.number_input("Quantas consultas com a nutricionista?", min_value=1, step=1)

    # --- CÁLCULO E TELA FINAL ---
    if nome_plano and nome_plano != "Selecione uma opção...":
        total_nutri = qtd_nutri * valor_nutri
        valor_total = valor_medico + total_nutri

        st.divider()
        st.subheader("📋 Resumo do Orçamento")
        st.write(f"**Pacote Selecionado:** {nome_plano}")
        st.write(f"**Valor da parte Médica:** R$ {valor_medico:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        if total_nutri > 0:
            st.write(f"**Valor repasse Nutricionista ({qtd_nutri}x):** R$ {total_nutri:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        st.success(f"**VALOR TOTAL A COBRAR: R$ {valor_total:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))

elif senha_digitada != "":
    st.error("Senha incorreta. Tente novamente.")
