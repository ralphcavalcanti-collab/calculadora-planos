import streamlit as st

# Configuração da aba do navegador
st.set_page_config(page_title="Calculadora de Orçamentos", page_icon="🩺")

# --- SISTEMA DE MEMÓRIA (SESSION STATE) ---
# Verifica se o usuário já está "logado" nesta sessão
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# --- TELA DE SENHA ---
if not st.session_state.autenticado:
    st.title("Acesso Restrito 🔒")
    senha_digitada = st.text_input("Digite a senha para acessar a calculadora:", type="password")
    
    if senha_digitada == "senha123": 
        st.session_state.autenticado = True
        st.rerun() # Atualiza a página imediatamente para sumir com o login
    elif senha_digitada != "":
        st.error("Senha incorreta. Tente novamente.")

# --- CALCULADORA (SÓ APARECE SE AUTENTICADO) ---
if st.session_state.autenticado:
    
    st.title("Calculadora de Orçamentos 🩺")
    st.write("Selecione as opções abaixo para gerar o orçamento do paciente.")

    # --- VALORES BASE ---
    valor_hora_presencial = 750
    valor_hora_acompanhamento_pres = 500
    valor_consulta_online = 550
    valor_hora_acompanhamento_on = 350
    valor_custo_nutri = 250
    
    # Valores Medicação e Margens
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
        modalidade = st.radio("Modalidade de atendimento:", ["Online (Telemedicina)", "Presencial"])
    with col2:
        primeira_vez = st.radio("O paciente é de Primeira Vez?", ["Sim", "Não"])

    st.divider()

    valor_medico = 0
    qtd_nutri = 0
    valor_venda_nutri = valor_custo_nutri # Começa com o valor de repasse padrão
    nome_plano = ""
    
    # --- LÓGICA ONLINE ---
    if modalidade == "Online (Telemedicina)":
        
        # Adiciona a margem de 50% na nutrição para QUALQUER pacote online
        valor_venda_nutri = valor_custo_nutri * margem_lucro 
        
        opcao = st.selectbox("Escolha o pacote Online:", [
            "Selecione uma opção...",
            "Plano de Acompanhamento Online (2 Meses)",
            "1 Consulta TM",
            "2 Consultas TM"
        ])
        
        if opcao == "Plano de Acompanhamento Online (2 Meses)":
            nome_plano = opcao
            qtd_nutri = 2
            if primeira_vez == "Sim":
                valor_medico = (3 * valor_consulta_online) + (1 * valor_hora_acompanhamento_on)
            else:
                valor_medico = (2 * valor_consulta_online) + (1 * valor_hora_acompanhamento_on)
                
        elif opcao in ["1 Consulta TM", "2 Consultas TM"]:
            nome_plano = opcao
            if opcao == "1 Consulta TM":
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
            "Plano de Seguimento (3 Meses)",
            "1 Consulta Presencial",
            "2 Consultas Presenciais"
        ])
        
        if opcao == "Plano Inicial (2 Meses)":
            nome_plano = opcao
            qtd_nutri = 2
            if primeira_vez == "Sim":
                valor_medico = (3 * valor_hora_presencial) + (4 * valor_hora_acompanhamento_pres)
            else:
                valor_medico = (2 * valor_hora_presencial) + (4 * valor_hora_acompanhamento_pres)
                
        elif opcao == "Plano de Seguimento (3 Meses)":
            nome_plano = opcao
            qtd_nutri = 3
            valor_medico = (3 * valor_hora_presencial) + (6 * valor_hora_acompanhamento_pres)
            
        elif opcao in ["1 Consulta Presencial", "2 Consultas Presenciais"]:
            nome_plano = opcao
            if opcao == "1 Consulta Presencial":
                valor_medico = valor_hora_presencial
            else:
                valor_medico = 1400
                
            inclui_nutri = st.radio("Incluir consulta nutricional?", ["Não", "Sim"])
            if inclui_nutri == "Sim":
                qtd_nutri = st.number_input("Quantas consultas com a nutricionista?", min_value=1, step=1)
                # Adiciona a margem de 50% na nutrição apenas nestes pacotes avulsos presenciais
                valor_venda_nutri = valor_custo_nutri * margem_lucro

    # --- LÓGICA DE MEDICAÇÃO ---
    valor_medicacao_total = 0
    resumo_meds = []

    # 1. TIRZEPATIDA (Liberada para todos os pacotes Presenciais)
    if modalidade == "Presencial" and nome_plano != "Selecione uma opção...":
        st.divider()
        st.subheader("💊 Tirzepatida")
        
        is_plano_fechado = "Meses" in nome_plano
        
        if is_plano_fechado:
            limite_app = 8 if "2 Meses" in nome_plano else 12
            st.write(f"Distribua as **{limite_app} aplicações** inclusas no plano:")
            max_val = limite_app
        else:
            st.write("Adicione a quantidade de aplicações avulsas, se houver:")
            max_val = 24 # Limite flexível para consultas avulsas
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: qtd_2_5 = st.number_input("2,5mg", min_value=0, max_value=max_val, step=1)
        with c2: qtd_5_0 = st.number_input("5mg", min_value=0, max_value=max_val, step=1)
        with c3: qtd_7_5 = st.number_input("7,5mg", min_value=0, max_value=max_val, step=1)
        with c4: qtd_10_0 = st.number_input("10mg", min_value=0, max_value=max_val, step=1)
        
        total_selecionado = qtd_2_5 + qtd_5_0 + qtd_7_5 + qtd_10_0
        
        if is_plano_fechado:
            if total_selecionado != limite_app:
                st.warning(f"⚠️ Atenção: Você selecionou {total_selecionado} aplicações. O plano exige {limite_app}.")
            else:
                st.success("✅ Quantidade de aplicações correta!")
                
        valor_tirzepatida = (qtd_2_5 * venda_2_5mg) + (qtd_5_0 * venda_5_0mg) + (qtd_7_5 * venda_7_5mg) + (qtd_10_0 * venda_10_0mg)
        valor_medicacao_total += valor_tirzepatida
        
        if total_selecionado > 0:
            resumo_meds.append(f"Tirzepatida ({total_selecionado} aplicações)")

    # 2. VITAMINAS D e B12 (Apenas para a modalidade Presencial)
    if modalidade == "Presencial" and nome_plano != "Selecione uma opção...":
        st.divider()
        st.subheader("💉 Vitaminas Injetáveis")
        st.write("Adicione a quantidade de aplicações, se houver:")
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            qtd_vit_d = st.number_input("Qtd Vitamina D", min_value=0, step=1)
        with col_v2:
            qtd_vit_b12 = st.number_input("Qtd Vitamina B12", min_value=0, step=1)
            
        valor_vit_d = qtd_vit_d * venda_vitamina
        valor_vit_b12 = qtd_vit_b12 * venda_vitamina
        
        valor_medicacao_total += (valor_vit_d + valor_vit_b12)
        
        if qtd_vit_d > 0:
            resumo_meds.append(f"{qtd_vit_d}x Vitamina D")
        if qtd_vit_b12 > 0:
            resumo_meds.append(f"{qtd_vit_b12}x Vitamina B12")

    # --- CÁLCULO E TELA FINAL ---
    if nome_plano and nome_plano != "Selecione uma opção...":
        total_nutri = qtd_nutri * valor_venda_nutri
        valor_total = valor_medico + total_nutri + valor_medicacao_total

        st.divider()
        st.subheader("📋 Resumo do Orçamento")
        st.write(f"**Pacote Selecionado:** {nome_plano}")
        st.write(f"**Valor da parte Médica:** R$ {valor_medico:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        if total_nutri > 0:
            if valor_venda_nutri > valor_custo_nutri:
                st.write(f"**Valor Nutrição ({qtd_nutri}x):** R$ {total_nutri:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            else:
                st.write(f"**Valor repasse Nutricionista ({qtd_nutri}x):** R$ {total_nutri:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            
        if valor_medicacao_total > 0:
            meds_texto = " + ".join(resumo_meds)
            st.write(f"**Medicação ({meds_texto}):** R$ {valor_medicacao_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        st.success(f"**VALOR TOTAL A COBRAR: R$ {valor_total:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))
