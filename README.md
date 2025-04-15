# Validador-de-CEPs
## Descrição
Este projeto é uma aplicação web interativa construída com o Streamlit, que tem como objetivo principal a validação de CEPs em massa a partir de planilhas em formato CSV ou XLSX. A aplicação valida se os CEPs estão no formato correto e gera relatórios detalhados com a quantidade de CEPs válidos e inválidos. Além disso, o sistema permite a consulta de endereços através de um CEP informado, utilizando a API BrasilAPI.

## Funcionalidades
### Validação de CEPs em Planilhas:
* O usuário pode enviar uma planilha contendo uma coluna com CEPs, que será lida e processada.
* A aplicação valida o formato de cada CEP (verificando se tem exatamente 8 dígitos).
* É gerada uma tabela com os status de cada CEP (válido ou Inválido).
* Gráfico de pizza é exibido mostrando a proporção de CEPs válidos e inválidos.
* O usuário pode fazer o download dos CEPs válidos e inválidos em formato CSV.
### Consulta de CEP via API (BrasilAPI):
* O usuário pode digitar um CEP para buscar o endereço associado.
* A busca é realizada por meio da BrasilAPI, que retorna informações sobre o endereço, bairro, cidade e estado.
* O sistema retorna os dados ou exibe mensagens de erro, caso o CEP não seja encontrado ou a API não esteka disponível.

## Como Usar
#### 1. Carregar Arquivo de CEPs:
* Clique em "Enviar sua planilha com a coluna 'CEP'" para carregar um arquivo no formato CSV ou XLSX.
* Certifique-se de que a planilha contenha uma coluna chamada "CEP" ou um nome similar. Caso contrário, o código indentificará a coluna corretamente, desde que o nome corresponda ao padrão.
#### 2. Visualização de resultado:
* Após o upload, a aplicação exibirá uma tabela com todos os CEPs validados, além de um gráfico de pizza indicando a proporção de CEPs válidos e inválidos.
* Você poderá realizar o download dos CEPs válidos e inválidos, conforme sua necessidade.
#### 3. Consulta de Endereço por CEP:
* Abaixo da tabela, há um campo de texto para que o usuário insira um CEP de 8 dígitos.
* A aplicação realizará a consulta à BrasilAPI e exibirá as informações do endereço correspondente ao CEP digitado.

## Dependências
Este aplicativo depende das seguintes bibliotecas Python:
* **Streamlit**: Para criação da interface web.
* **Pandas**: Para a manipulação de dados e leitura dos arquivos CSV/ XLSX.
* **Matplotlib**: Para criação dos gráficos.
* **Requests**: Para realizar requisições HTTP à BrasilAPI.

## Como Instalar
Caso queira rodar o código localmente, siga os passos abaixo:
1. Clone o repositório: git clone <link_do_repositório>
2. Instale as dependências necessárias: pip install streamlit pandas matplotlib requests
3. Execute o aplicativo: streamlit run <nome_do_arquivo>.py

## Exemplo de Uso
1. **Exemplo de CEP Válido**:
* Digite um CEP válido como "01001000" para consultar o endereço correspondente.
2. **Exemplo de CEP Inválido**:
* Digite um CEP incorreto ou incompleto, como "1234567", para ver uma mensagem de erro.