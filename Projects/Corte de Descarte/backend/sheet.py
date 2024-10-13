import pandas as pd
import numpy as np
from control import *

class Sheet:
    """
    Classe para manipulação de dados de uma chapa com base em um código específico.
    
    A classe oferece métodos para obter o comprimento máximo da chapa e identificar
    comprimentos onde a deformação está fora do intervalo especificado.
    """
    
    def __init__(self, file_path: str, sheet_code: str):
        """
        Inicializa a instância da classe Sheet.
        
        Parameters:
            file_path (str): O caminho do arquivo CSV.
            sheet_code (str): O código da chapa a ser analisada.
        """

        self.file_path = file_path
        self.sheet_code = sheet_code

        self.length = 0
        self.new_length = 0
        self.weight = 0
        self.new_weight = 0
        self.defects = []
        self.cuts = ()
        self.loss = 0
        self.loss_percent = 0

        # Carrega o arquivo com os dados
        data_type = {
            2: str,
            23: str,
            25: str,
        }

        # .csv
        self.data = pd.read_csv(file_path, sep=';', header=None, usecols=[1, 2, 14, 23, 24, 25], dtype=data_type)

        # .xlsx
        #self.data = pd.read_excel(file_path, sheet_name='Sheet1', header=None, usecols=[1, 2, 14, 23, 24, 25], dtype=data_type)

        # Converte a coluna do código para string e remove espaços extras
        self.data[1] = self.data[1].astype(str).str.strip()

        # Filtra a planilha pelo código da chapa
        self.data = self.data[self.data[1] == self.sheet_code]

        if not self.data.empty:
            # Preenchendo atributos do objeto
            self.get_length()
            self.get_weight()
            self.get_defects()
            self.get_cuts()
            self.get_weight_loss()
        else:
            raise('Nenhuma chapa com esse código')

    def get_length(self) -> float:
        """
        Retorna o comprimento máximo da chapa com o código especificado.
        
        Returns:
            float: Comprimento máximo encontrado para a chapa | 0.0 caso não exista chapa com o código
        """

        # Retorna o comprimento e preenche o atributo de comprimento
        self.length = int(self.data[25].iloc[0])
        return self.length
    
    def get_weight(self) -> float:
        """
        Calcula o peso da chapa com base na espessura, largura e comprimento.
        
        Returns:
            float: Peso da chapa em kg | 0.0 se algum valor estiver faltando.
        """
        # Obtém a espessura, largura e comprimento
        thickness = float(str(self.data[24].iloc[0]).replace(',', '.'))  # Coluna de espessura
        width = float(str(self.data[23].iloc[0]).replace(',', '.'))  # Coluna de largura
        length = self.length  # Comprimento obtido pelo método get_length

        # Valida se os valores estão disponíveis e são numéricos
        if pd.notna(thickness) and pd.notna(width) and pd.notna(length):
            # Calcula o peso e preenche o atributo de peso
            self.weight = ((thickness / 1000) * (width / 1000) * length * 7850)  # 7850 é a densidade do aço
            return self.weight

    def get_defects(self, lower_limit: float = -LIMIT, upper_limit: float = LIMIT) -> list:
        """
        Retorna uma lista de comprimentos onde a deformação está fora do intervalo especificado.
        
        Parameters:
            lower_limit (float): Limite inferior para o intervalo de deformação. Padrão é -1.
            upper_limit (float): Limite superior para o intervalo de deformação. Padrão é 1.
        
        Returns:
            list: Lista de comprimentos (coluna 2) onde a deformação (coluna 14) está fora do intervalo. | Lista vazia caso não exista chapa com aquele código.
        """

        # Converte valores não numéricos para NaN e depois para float, ignorando erros
        self.data[14] = self.data[14].apply(lambda x: float(str(x).replace(',', '.')) if pd.notna(x) else np.nan)
        
        # Filtra apenas as linhas onde a deformação está fora do intervalo
        data_out_of_range = self.data[(self.data[14] < lower_limit) | (self.data[14] > upper_limit)]
        
        # Preenche o atributo de defeitos com os comprimentos fora do intervalo
        for defect in data_out_of_range[2].tolist():
            self.defects.append(int(defect))
        return self.defects

    def get_cuts(self, tolerance: float = TOLERANCE) -> tuple | str:
        """
        Retorna uma tupla com os comprimentos em que os cortes deverão ser realizados.

        Parameters:
            tolerance (float): Tolerância em porcentagem da distância das bordas em relação ao comprimentoa da chapa.
        
        Returns:
            tuple: Tupla com as posições, inicial e final respectivamente, de onde deverão ser realizados os cortes da chapa.
            str: Chapa defeituosa | Nenhum defeito encontrado
        """

        tolerance /= 100
        if self.length > 0 and self.defects != []:
            # Calcula os limites de 15% da chapa
            left_limit = self.length * tolerance
            right_limit = self.length * (1 - tolerance)

            # Defeitos nas regiões de 15% (início e fim)
            left_defects = [d for d in self.defects if d <= left_limit]
            right_defects = [d for d in self.defects if d >= right_limit]

            # Verificação de defeitos entre os dois limites de 15%
            if left_defects + right_defects != self.defects:
                self.cuts = 'Chapa defeituosa'
            else:
                # Encontrar o defeito mais próximo dos 15% iniciais e finais, se houver
                self.cuts = (max(left_defects, default=0), min(right_defects, default=0))
        else:
            if self.defects == []:
                self.cuts = 'Sem cortes necessários'
        
        # Retorna resultado depois de preencher atributo
        return self.cuts
    
    def get_weight_loss(self):
        """
        Retorna o peso perdido pós o processo de corte, das partes cortadas da chapa.

        Returns
            float: Peso das partes cortadas da chapa
        """

        # Verificando se existe chapa com esse código e se existem cortes válidos
        if isinstance(self.cuts, tuple):
            length = self.length
            weight = self.weight
            left_cut, right_cut = self.cuts[0], self.cuts[1]

            # Cálculo da perda de peso
            left_loss = left_cut * (weight/length)  # Peso do corte esquerdo
            right_loss = (length - right_cut) * (weight / length) if right_cut != 0 else 0  # Peso do corte direito

            # Preenchendo atributo com soma das perdas
            self.loss = left_loss + right_loss
            self.loss_percent = self.loss*100 / weight
            self.new_weight = weight - self.loss
            
            self.new_length = length - left_cut if right_cut == 0 else right_cut - left_cut
        else:
            # Caso nenhuma chapa encontrada com o código ou chapa não será cortada
            self.loss = 0.0
        return self.loss
