import pandas as pd

# Código para identificar irregularidades de uma chapa de aço na CSN

# Caminho do arquivo Excel e configurações
file_path = "teste.xlsx"
valor_procurado = "Identificação da folha de aço"
limite_superior = 1
limite_inferior = -1

# Carregar as colunas especificadas
planilha = pd.read_excel(file_path, sheet_name='Sheet1', header=None, usecols=[1, 14]) # coluna 1 - local valor procurado e coluna 14 - local de checagem dos limites

# Remover espaços em branco e garantir que a coluna B é string
planilha[1] = planilha[1].astype(str).str.strip()

# Aplicar o filtro para localizar as linhas onde:
filtro = (planilha[1] == "Identificação da folha de aço") & (
    planilha[14].notna() & ((planilha[14] > limite_superior) | (planilha[14] < limite_inferior))
)

# Obter os índices das linhas que atendem aos critérios
linhas_resultado = planilha[filtro].index.tolist()

# Exibir o resultado
print(f"Linhas onde a folha'{valor_procurado}' está irregular são: {linhas_resultado}")
