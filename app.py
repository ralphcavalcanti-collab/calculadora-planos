import streamlit as st

# Configuração da aba do navegador
st.set_page_config(page_title="Calculadora de Orçamentos", page_icon="🩺")

# --- SISTEMA DE MEMÓRIA (SESSION STATE) ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# --- TELA DE SENHA ---
if not st.session_state.autenticado:
    st.title("Acesso Restrito 🔒")
    senha_digitada = st.text_input("Digite a senha para aceder à calculadora:", type="password")
    
    if senha_digitada == "senha123": 
        st.session_state.autenticado = True
        st.rerun() 
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
    valor_hora_acompanhamento_on = 350 # Mantido na base caso seja necessário no futuro
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
        modalidade = st.radio("Modalidade de atendimento:", ["Presencial", "Online (Telemedicina)"])
    with col2:
        primeira_vez = st.radio("O paciente é de Primeira Vez?", ["Sim", "Não"])

    st.divider()

    valor_medico = 0
    qtd_nutri = 0
    valor_venda_nutri = valor_custo_nutri 
    nome_plano = ""
    
    # --- LÓGICA ONLINE ---
    if modalidade == "Online (Telemedicina)":
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
            # Nova matemática: apenas 2 consultas online, sem hora de acompanhamento
            valor_medico = 2 * valor_consulta_online
                
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
                valor_venda_nutri = valor_custo_nutri * margem_lucro

    # --- LÓGICA DE MEDICAÇÃO ---
    valor_medicacao_total = 0
    custo_real_medicacao = 0 
    resumo_meds = []
    
    qtd_2_5 = qtd_5_0 = qtd_7_5 = qtd_10_0 = 0
    qtd_vit_d = qtd_vit_b12 = 0

    # 1. TIRZEPATIDA 
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
            max_val = 24 
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: qtd_2_5 = st.number_input("2,5mg", min_value=0, max_value=max_val, step=1)
        with c2: qtd_5_0 = st.number_input("5mg", min_value=0, max_value=max_val, step=1)
        with c3: qtd_7_5 = st.number_input("7,5mg", min_value=0, max_value=max_val, step=1)
        with c4: qtd_10_0 = st.number_input("10mg", min_value=0, max_value=max_val, step=1)
        
        total_selecionado = qtd_2_5 + qtd_5_0 + qtd_7_5 + qtd_10_0
        
        if is_plano_fechado:
            if total_selecionado != limite_app:
                st.warning(f"⚠️ Atenção: Selecionou {total_selecionado} aplicações. O plano exige {limite_app}.")
            else:
                st.success("✅ Quantidade de aplicações correta!")
                
        valor_tirzepatida = (qtd_2_5 * venda_2_5mg) + (qtd_5_0 * venda_5_0mg) + (qtd_7_5 * venda_7_5mg) + (qtd_10_0 * venda_10_0mg)
        valor_medicacao_total += valor_tirzepatida
        
        custo_real_medicacao += (qtd_2_5 * custo_base_tirzepatida * 1) + \
                                (qtd_5_0 * custo_base_tirzepatida * 2) + \
                                (qtd_7_5 * custo_base_tirzepatida * 3) + \
                                (qtd_10_0 * custo_base_tirzepatida * 4)
        
        if total_selecionado > 0:
            resumo_meds.append(f"Tirzepatida ({total_selecionado} aplicações)")

    # 2. VITAMINAS D e B12
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
        
        custo_real_medicacao += (qtd_vit_d + qtd_vit_b12) * custo_vitamina
        
        if qtd_vit_d > 0:
            resumo_meds.append(f"{qtd_vit_d}x Vitamina D")
        if qtd_vit_b12 > 0:
            resumo_meds.append(f"{qtd_vit_b12}x Vitamina B12")

    # --- CÁLCULO FINAL E ABAS DE RESULTADO ---
    if nome_plano and nome_plano != "Selecione uma opção...":
        total_nutri_venda = qtd_nutri * valor_venda_nutri
        custo_nutri_real = qtd_nutri * valor_custo_nutri
        
        valor_total_bruto = valor_medico + total_nutri_venda + valor_medicacao_total

        st.divider()
        
        aba_paciente, aba_clinica = st.tabs(["🗣️ Visão do Paciente", "💰 Visão da Clínica (Lucro Real)"])
        
        with aba_paciente:
            st.subheader("📋 Resumo do Orçamento")
            st.write(f"**Pacote Selecionado:** {nome_plano}")
            st.write(f"**Serviço Médico:** R$ {valor_medico:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            
            if total_nutri_venda > 0:
                st.write(f"**Acompanhamento Nutricional ({qtd_nutri}x):** R$ {total_nutri_venda:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                
            if valor_medicacao_total > 0:
                meds_texto = " + ".join(resumo_meds)
                st.write(f"**Medicação ({meds_texto}):** R$ {valor_medicacao_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            
            st.success(f"**VALOR TOTAL A COBRAR: R$ {valor_total_bruto:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))

            # --- GERAÇÃO DA MENSAGEM PARA O WHATSAPP ---
            st.write("---")
            st.write("📱 **Copie o texto abaixo para enviar ao paciente:**")
            
            # Montando o texto da mensagem
            mensagem_wp = f"Olá! Tudo bem? Segue o detalhamento do seu orçamento:\n\n"
            mensagem_wp += f"📋 *Pacote:* {nome_plano}\n"
            
            if "Acompanhamento" in nome_plano or "Inicial" in nome_plano or "Seguimento" in nome_plano:
                mensagem_wp += f"👨‍⚕️ *Consultas e Acompanhamento Médico inclusos*\n"
            else:
                mensagem_wp += f"👨‍⚕️ *Serviço Médico incluso*\n"
                
            if total_nutri_venda > 0:
                mensagem_wp += f"🥗 *{qtd_nutri}x Consultas com Nutricionista*\n"
                
            if valor_medicacao_total > 0:
                meds_texto = " + ".join(resumo_meds)
                mensagem_wp += f"💊 *Medicação Injetável:* {meds_texto}\n"
                
            mensagem_wp += f"\n💰 *Investimento Total:* R$ {valor_total_bruto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            mensagem_wp += f"\n\nQualquer dúvida, estou à disposição!"
            
            # Caixa de código com botão de cópia nativo
            st.code(mensagem_wp, language="text")

        with aba_clinica:
            st.subheader("📊 Análise Financeira")
            
            forma_pagamento = st.radio("Selecione a forma de pagamento do paciente:", ["Pix / Dinheiro", "Cartão de Crédito"], horizontal=True)
            
            valor_imposto = valor_total_bruto * 0.15
            valor_taxa_cartao = valor_total_bruto * 0.0334 if forma_pagamento == "Cartão de Crédito" else 0.0
            
            lucro_liquido = valor_total_bruto - valor_imposto - valor_taxa_cartao - custo_nutri_real - custo_real_medicacao
            
            st.write(f"**Faturação Bruta:** R$ {valor_total_bruto:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            st.write("---")
            st.write("**Descontos e Custos:**")
            st.write(f"- Impostos (15%): R$ {valor_imposto:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            if valor_taxa_cartao > 0:
                st.write(f"- Taxa Multibanco/Cartão (3,34%): R$ {valor_taxa_cartao:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            if custo_nutri_real > 0:
                st.write(f"- Repasse Nutricionista: R$ {custo_nutri_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            if custo_real_medicacao > 0:
                st.write(f"- Custo de Farmácia (Medicação): R$ {custo_real_medicacao:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            st.write("---")
            st.info(f"**LUCRO LÍQUIDO (O que sobra na clínica): R$ {lucro_liquido:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))
