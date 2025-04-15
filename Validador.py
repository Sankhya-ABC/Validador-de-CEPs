# Importa bibliotecas necessárias
import streamlit as st              # Biblioteca para criação de apps web interativos
import pandas as pd                 # Manipulação de dados com DataFrame
import io                           # Manipulação de fluxos de dados 
import matplotlib.pyplot as plt     # Geração de gráficos
import requests                     # Realiza requisição HTTP (utilizada para consultar CEP via API)

# Título da  no topo da interface
st.title("Validador de CEPs")

# Permite o upload de arquivos do tipo CSV ou XLSX
uploaded_file = st.file_uploader("Envie sua planilha com a coluna 'CEP'", type=["csv", "xlsx"])

# Verifica se um arquivo foi enviado
if uploaded_file:
    # Lê o arquivo dependendo do tipo
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file, dtype=str) # Lê como CSV
    else:
        df = pd.read_excel(uploaded_file, dtype=str) # Lê como Excel

    # Garante a existência da coluna 'CODPARC', mesmo que vazia
    if 'CODPARC' not in df.columns:
        df['CODPARC'] = ''

    # Identifica a coluna do CEP, mesmo que com nome escrito de forma diferente
    cep_col = None
    for col in df.columns:
        if col.strip().upper() == "CEP":
            cep_col = col
            break

    # Se a columa CEP não for encontrada, exibe erro        
    if cep_col is None:
        st.error("Erro: A planilha enviada não possui uma coluna chamada 'CEP'. Verifique o nome da coluna e tente novamente.")
    else:
        # Renomeia a coluna identifivsfs para 'CEP' oficialmente
        df.rename(columns={cep_col: 'CEP'}, inplace=True)

        # Remove espaços e formata CEPs com 8 dígitos (com zero à esquerda se necessário)
        df['CEP'] = df['CEP'].str.strip()
        df['CEP_Formatado'] = df['CEP'].apply(
            lambda x: str(x).zfill(8) if pd.notna(x) and str(x).strip() != "" else ""
        )
        # Valida o formato do CEP (deve ter 8 dígitos)
        df['Status'] = df['CEP'].apply(
            lambda x: 'Inválido' if pd.isna(x) or len(str(x)) != 8 else 'Válido'
        )

        # Exibe tabela com a nova coluna de status
        st.subheader("Tabela com validação de CEPs")
        st.dataframe(df)

        # Filtra os CEPs inválidos
        invalid_df = df[df['Status'] == 'Inválido']
        valid_count = (df['Status'] == 'Válido').sum()
        invalid_count = (df['Status'] == 'Inválido').sum()

        # Cria gráfico de pizza com proporção de válidos e inválidos
        st.subheader("Gráfico de CEPs válidos vs inválidos")
        fig, ax = plt.subplots()
        ax.pie([valid_count, invalid_count],
               labels=['Válidos', 'Inválidos'],
               autopct='%1.1f%%',
               startangle=90,
               colors=['#00FF00', '#FF0000']) # Verde para válidos, vermelho para inválidos
        ax.axis('equal')
        st.pyplot(fig)

        # Botão de downLoad dos CEPs inválidos (se houver)
        st.subheader("Download dos CEPs inválidos")
        if not invalid_df.empty:
            csv = invalid_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar CEPs inválidos em CSV",
                data=csv,
                file_name='ceps_invalidos.csv',
                mime='text/csv'
            )
        else:
            st.success("Todos os CEPs são válidos!")


        # Botão de downLoad dos CEPs válidos (se houver)
        st.subheader("Download dos CEPs válidos")
        valid_df = df[df['Status'] == 'Válido']
        if not valid_df.empty:
            csv = valid_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar CEPs válidos em CSV",
                data=csv,
                file_name='ceps_validos.csv',
                mime='text/csv'
            )
        else:
            st.warning("Não há CEPs válidos para download.")

# -----------------------------------------------------
# Bloco separado para consulta de CEP via BrasilLAPI
# -----------------------------------------------------

# Linha de separação visual
st.markdown("---")
st.header("Consulta de Endereço por CEP")

# Campo de entrada de texto para digitar o CEP
input_cep = st.text_input("Digite um CEP para buscar (somente números):", max_chars=8)

# Se o CEP digitado for válido (8 números)
if input_cep and len(input_cep) == 8 and input_cep.isdigit():
    try:
        # Faz a requisição para a BrasilLAPI
        response = requests.get(f"https://brasilapi.com.br/api/cep/v1/{input_cep}", timeout=10)
        # Se encontrado, exibe os dados
        if response.status_code == 200:
            data = response.json()
            st.success("CEP encontrado!")
            st.write(f"**CEP**: {data['cep']}")
            st.write(f"**Endereço**: {data['street']}")
            st.write(f"**Bairro**: {data['neighborhood']}")
            st.write(f"**Cidade**: {data['city']}")
            st.write(f"**Estado**: {data['state']}")
        else:
            st.error("CEP não encontrado na BrasilAPI.")
    # Trata falhas de conexão ou problemas na requisição
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao consultar a API {e}")
# Se o CEP estiver incompleto ou inválido com 8 números.
elif input_cep:
    st.warning("CEP inválido. Digite um CEP inválido")