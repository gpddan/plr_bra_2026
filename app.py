import streamlit as st
import json
import os

# Configuração da página
st.set_page_config(
    page_title="Calculadora de PLR",
    page_icon="💰",
    layout="centered"
)

# Constantes com as suas atualizações
PERCENTUAL_AUMENTO = 4.60
VLR_ANTECIPACAO = 2217.26
VLR_ANTEC_PARC_ADIC = 3837.03

# Arquivo para persistir o contador de acessos/cálculos
CONTADOR_FILE = "contador.json"

def carregar_contador():
    if os.path.exists(CONTADOR_FILE):
        try:
            with open(CONTADOR_FILE, "r") as f:
                data = json.load(f)
                return data.get("total_calculos", 0)
        except Exception:
            return 0
    return 0

def incrementar_contador():
    total = carregar_contador() + 1
    with open(CONTADOR_FILE, "w") as f:
        json.dump({"total_calculos": total}, f)
    return total

def calcular_plr_bancarios(salario, rec_fev, ir_fev):
    salario_corrigido = salario * (1 + (PERCENTUAL_AUMENTO / 100))
    parcela_54 = salario_corrigido * 0.54
    bruto_setembro = parcela_54 + VLR_ANTECIPACAO + VLR_ANTEC_PARC_ADIC
    
    base_ir = rec_fev + bruto_setembro
    
    if base_ir <= 8214.40:
        aliquota, deducao = 0.0, 0.0
    elif base_ir <= 9922.28:
        aliquota, deducao = 0.075, 573.06
    elif base_ir <= 13167.00:
        aliquota, deducao = 0.15, 1317.23
    elif base_ir <= 16380.38:
        aliquota, deducao = 0.225, 2304.76
    else:
        aliquota, deducao = 0.275, 3123.78
        
    ir_total = (base_ir * aliquota) - deducao
    ir_setembro = max(0.0, ir_total - ir_fev)
    
    contrib_negocial = min(bruto_setembro * 0.015, 248.21)
    liquido_setembro = bruto_setembro - ir_setembro - contrib_negocial
    
    return salario_corrigido, parcela_54, bruto_setembro, base_ir, ir_setembro, contrib_negocial, liquido_setembro

# Cabeçalho
st.title("💰 Calculadora de PLR (Setembro)")
st.write("Preencha as informações abaixo para simular a estimativa da sua PLR líquida.")

# Formulário de Entrada
with st.form("form_plr"):
    salario = st.number_input(
        "1. Salário Bruto de Agosto (R$)",
        min_value=0.0,
        value=9876.40,
        step=100.0,
        format="%.2f",
        help="Informe o salário bruto de agosto."
    )
    
    rec_fev = st.number_input(
        "2. Valor Bruto da PLR Paga em Fevereiro (R$)",
        min_value=0.0,
        value=10397.58,
        step=100.0,
        format="%.2f",
        help="Refere-se ao valor bruto da PLR recebida em FEV, não ao salário."
    )
    
    ir_fev = st.number_input(
        "3. Imposto de Renda (IR) Pago na PLR em Fevereiro (R$)",
        min_value=0.0,
        value=242.41,
        step=50.0,
        format="%.2f",
        help="Refere-se ao IR retido especificamente na PLR de FEV. Se não teve, coloque 0."
    )
    
    btn_calcular = st.form_submit_button("🚀 Calcular PLR")

if btn_calcular:
    # Registra o cálculo no contador
    total = incrementar_contador()
    
    sal_corr, p54, bruto_set, base_ir, ir_set, contrib, liquido = calcular_plr_bancarios(salario, rec_fev, ir_fev)
    
    st.divider()
    st.subheader("📊 Resultado da Simulação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"• **Salário Corrigido (4,60%):** R$ {sal_corr:,.2f}")
        st.markdown(f"• **Parcela (54%):** R$ {p54:,.2f}")
        st.markdown(f"• **Antecipação (Fixo):** R$ {VLR_ANTECIPACAO:,.2f}")
        st.markdown(f"• **Parcela Adicional (Fixo):** R$ {VLR_ANTEC_PARC_ADIC:,.2f}")
        st.markdown(f"• **PLR Bruto Setembro:** R$ {bruto_set:,.2f}")
        
    with col2:
        st.markdown(f"• **Base de Cálculo do IR:** R$ {base_ir:,.2f}")
        st.markdown(f"• **IR Devido (Setembro):** R$ {ir_set:,.2f}")
        st.markdown(f"• **Contribuição Negocial:** R$ {contrib:,.2f}")
        
    st.success(f"### 💰 **PLR Líquida (Setembro):** R$ {liquido:,.2f}")
    
    st.warning("⚠️ **ATENÇÃO:** O VALOR CALCULADO TRATA-SE DE UMA ESTIMATIVA! NÃO FAÇA DÍVIDAS COM AGIOTA OU APOSTE NO TIGRINHO ANTES DE VER O HOLERITE 😂")

# Exibe a contagem no rodapé
total_acessos = carregar_contador()
st.caption(f"📈 Total de simulações realizadas até agora: **{total_acessos}**")
