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

    # --- VALORES BASE PADRÃO (Presencial/Geral) ---
    valor_hora_presencial = 750
    valor_hora_acompanhamento_pres = 500
    valor_consulta_online = 550
    valor_hora_acompanhamento_on = 350
    
    # Valores Medicação e Margens Gerais
    margem_lucro_padrao = 1.50 # 50% de lucro (Tirzepatida)
    margem_vit_d = 7.50        # 650% de lucro (Custo x 7.5)
    margem_vit_b12 = 6.00      # 500% de lucro (Custo x 6)
    
    custo_base_tirzepatida = 63.74
    venda_2_5mg = custo_base_tirzepatida * 1 * margem_lucro_padrao
    venda_5_0mg = custo_base_tirzepatida * 2 * margem_lucro_padrao
    venda_7_5mg = custo_base_tirzepatida * 3 * margem_lucro_padrao
    venda_10_0mg = custo_base_tirzepatida * 4 * margem_lucro_padrao
    
    custo_vitamina = 20.00
    venda_vit_d = custo_vitamina * margem_vit_d
    venda_vit_b12 = custo_vitamina * margem_vit_b12

    # --- INTERFACE (BOTÕES E MENUS) ---
    modalidade = st.radio("Modalidade de atendimento:", ["Presencial", "Online (Telemedicina)"])

    st.divider()

    # Variáveis globais zeradas
    valor_medico = 0
    qtd_nutri = 0
    custo_nutri_real = 0 
    total_nutri_venda = 0
    nome_plano = ""
    
    # --- LÓGICA ONLINE ---
    if modalidade == "Online (Telemedicina)":
        opcao = st.selectbox("Escolha o pacote Online:", [
            "Selecione uma opção...",
            "Plano de Acompanhamento Online (2 Meses)",
            "1 Consulta TM",
            "2 Consultas TM"
        ])
        
        if opcao == "Plano de Acompanhamento Online (2 Meses)":
            nome_plano = opcao
            qtd_nutri = 2
            valor_medico = 2 * valor_consulta_online
            # Nutri a 150 + 50 de acompanhamento (2 meses). Margem de 40%
            custo_nutri_real = (2 * 150) + 50          
            total_nutri_venda = custo_nutri_real * 1.40 
                
        elif opcao in ["1 Consulta TM", "2 Consultas TM"]:
            nome_plano = opcao
            if opcao == "1 Consulta TM":
                valor_medico = valor_consulta_online
            else:
                valor_medico = 1000
                
            inclui_nutri = st.radio("Incluir consulta nutricional?", ["Não", "Sim"])
            if inclui_nutri == "Sim":
                qtd_nutri = st.number_input("Quantas consultas com a nutricionista?", min_value=1, step=1)
                # Nutri a 150 sem acompanhamento. Margem de 40%
                custo_nutri_real = qtd_nutri * 150
                total_nutri_venda = custo_nutri_real * 1.40

    # --- LÓGICA PRESENCIAL ---
    elif modalidade == "Presencial":
        opcao = st.selectbox("Escolha o pacote Presencial:", [
            "Selecione uma opção...",
            "Plano de Acompanhamento Básico Inicial (2 Meses)",
            "Plano de Acompanhamento Básico Seguimento (3 Meses)",
            "Plano de Acompanhamento Completo Inicial (2 Meses)",
            "Plano de Acompanhamento Completo Seguimento (3 Meses)",
            "1 Consulta Presencial",
            "2 Consultas Presenciais"
        ])
        
        # LÓGICA DOS PLANOS BÁSICOS
        if opcao == "Plano de Acompanhamento Básico Inicial (2 Meses)":
            nome_plano = opcao
            qtd_nutri = 2
            valor_medico = (2 * valor_hora_presencial) + 200  
            custo_nutri_real = (2 * 200) + 100                
            total_nutri_venda = custo_nutri_real * 1.40       
            
        elif opcao == "Plano de Acompanhamento Básico Seguimento (3 Meses)":
            nome_plano = opcao
            qtd_nutri = 2 
            valor_medico = (3 * valor_hora_presencial) + 300  
            custo_nutri_real = (2 * 200) + 150                
            total_nutri_venda = custo_nutri_real * 1.40       
            
        # LÓGICA DOS PLANOS COMPLETOS
        elif opcao == "Plano de Acompanhamento Completo Inicial (2 Meses)":
            nome_plano = opcao
            qtd_nutri = 2
            valor_medico = (2 * valor_hora_presencial) + (4 * valor_hora_acompanhamento_pres)
            custo_nutri_real = (2 * 200) + 100                
            total_nutri_venda = custo_nutri_real * 1.40
                
        elif opcao == "Plano de Acompanhamento Completo Seguimento (3 Meses)":
            nome_plano = opcao
            qtd_nutri = 2 
            valor_medico = (3 * valor_hora_presencial) + (6 * valor_hora_acompanhamento_pres)
            custo_nutri_real = (2 * 200) + 150                
            total_nutri_venda = custo_nutri_real * 1.40
            
        # LÓGICA DAS CONSULTAS AVULSAS
        elif opcao in ["1 Consulta Presencial", "2 Consultas Presenciais"]:
            nome_plano = opcao
            if opcao == "1 Consulta Presencial":
                valor_medico = valor_hora_presencial
            else:
                valor_medico = 1400
                
            inclui_nutri = st.radio("Incluir consulta nutricional?", ["Não", "Sim"])
            if inclui_nutri == "Sim":
                qtd_nutri = st.number_input("Quantas consultas com a nutricionista?", min_value=1, step=1)
                # Nutrição avulsa presencial a 200 com margem de 40%
                custo_nutri_real = qtd_nutri * 200
                total_nutri_venda = custo_nutri_real * 1.40

    # --- LÓGICA DE MEDICAÇÃO ---
    valor_medicacao_total = 0
    custo_real_medicacao = 0 
    resumo_meds = []
    
    qtd_2_5 = qtd_5_0 = qtd_7_5 = qtd_10_0 = 0
    qtd_vit_d = qtd_vit_b12 = 0

    # 1. TIRZEPATIDA (Apenas para os Planos de Acompanhamento Completo)
    planos_com_tirzepatida = [
        "Plano de Acompanhamento Completo Inicial (2 Meses)",
        "Plano de Acompanhamento Completo Seguimento (3 Meses)"
    ]
    
    if modalidade == "Presencial" and nome_plano in planos_com_tirzepatida:
        st.divider()
        st.subheader("💊 Tirzepatida")
        
        limite_app = 8 if "2 Meses" in nome_plano else 12
        st.write(f"Distribua as **{limite_app} aplicações** inclusas no plano:")
        max_val = limite_app
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: qtd_2_5 = st.number_input("2,5mg", min_value=0, max_value=max_val, step=1)
        with c2: qtd_5_0 = st.number_input("5mg", min_value=0, max_value=max_val, step=1)
        with c3: qtd_7_5 = st.number_input("7,5mg", min_value=0, max_value=max_val, step=1)
        with c4: qtd_10_0 = st.number_input("10mg", min_value=0, max_value=max_val, step=1)
        
        total_selecionado = qtd_2_5 + qtd_5_0 + qtd_7_5 + qtd_10_0
        
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

    # 2. VITAMINAS D e B12 (Aparece para qualquer presencial)
    if modalidade == "Presencial" and nome_plano != "Selecione uma opção...":
        st.divider()
        st.subheader("💉 Vitaminas Injetáveis")
        st.write("Adicione a quantidade de aplicações, se houver:")
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            qtd_vit_d = st.number_input("Qtd Vitamina D", min_value=0, step=1)
        with col_v2:
            qtd_vit_b12 = st.number_input("Qtd Vitamina B12", min_value=0, step=1)
            
        valor_vit_d = qtd_vit_d * venda_vit_d
        valor_vit_b12 = qtd_vit_b12 * venda_vit_b12
        valor_medicacao_total += (valor_vit_d + valor_vit_b12)
        
        custo_real_medicacao += (qtd_vit_d + qtd_vit_b12) * custo_vitamina
        
        if qtd_vit_d > 0:
            resumo_meds.append(f"{qtd_vit_d}x Vitamina D")
        if qtd_vit_b12 > 0:
            resumo_meds.append(f"{qtd_vit_b12}x Vitamina B12")

    # --- CÁLCULO FINAL E ABAS DE RESULTADO ---
    if nome_plano and nome_plano != "Selecione uma opção...":
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
            
            st.code(mensagem_wp, language="text")

        with aba_clinica:
            st.subheader("📊 Análise Financeira")
            
            forma_pagamento = st.radio("Selecione a forma de pagamento do paciente:", ["Pix / Dinheiro", "Cartão de Crédito"], horizontal=True)
            
            valor_imposto = valor_total_bruto * 0.15
            valor_taxa_cartao = valor_total_bruto * 0.0334 if forma_pagamento == "Cartão de Crédito" else 0.0
            
            lucro_liquido = valor_total_bruto - valor_imposto - valor_taxa_cartao - custo_nutri_real - custo_real_medicacao
            
            st.write(f"**Faturamento Bruto:** R$ {valor_total_bruto:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            st.write("---")
            st.write("**Descontos e Custos:**")
            st.write(f"- Impostos (15%): R$ {valor_imposto:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            if valor_taxa_cartao > 0:
                st.write(f"- Taxa Maquininha (3,34%): R$ {valor_taxa_cartao:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            if custo_nutri_real > 0:
                st.write(f"- Repasse Nutricionista: R$ {custo_nutri_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            if custo_real_medicacao > 0:
                st.write(f"- Custo de Farmácia (Medicação): R$ {custo_real_medicacao:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            st.write("---")
            st.info(f"**LUCRO LÍQUIDO (O que sobra na clínica): R$ {lucro_liquido:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))
