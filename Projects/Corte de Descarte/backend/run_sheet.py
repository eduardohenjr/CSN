import sys
import json
from sheet import Sheet
from graph import plot_sheet

def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Caminho do arquivo e código da chapa são obrigatórios"}))
        return
    
    # Caminho do arquivo e código da chapa
    file_path = sys.argv[1]
    sheet_code = str(sys.argv[2]).upper()
    
    try:
        # Cria uma instância da classe Sheet com o caminho do arquivo e código da chapa
        sheet = Sheet(file_path, sheet_code)

        # Formatação de stiring dos defeitos
        if sheet.defects == []:
            defects_str = 'Chapa sem defeitos'
        else:
            defects_str = ' m, '.join(str(n) for n in sheet.defects) + ' m'

        # Formatação da string dos cortes
        if isinstance(sheet.cuts, tuple):
            left_cut = f"{sheet.cuts[0]} m" if sheet.cuts[0] != 0 else 'Não necessita'
            right_cut = f"{sheet.length - sheet.cuts[1]} m" if sheet.cuts[1] != 0 else 'Não necessita'
            cuts_str = f"Inicial: {left_cut} | Final: {right_cut}"
        else:
            cuts_str = sheet.cuts

        # Formatação da string da perda de peso
        loss_str = f"{sheet.loss:.2f} kg" if sheet.loss != 0 else 'Sem alterações'
        loss_percent_str = f"({sheet.loss_percent:.2f} %)" if sheet.loss != 0 else ''

        # Formatação da string do novo comprimento
        new_length_str = f"{sheet.new_length} m" if sheet.new_length != 0 else 'Sem alterações'

        # Formatação da string do novo peso
        new_weight_str = f"{sheet.new_weight:.2f} kg" if sheet.new_length != 0 else 'Sem alterações'

        # Extrai os dados relevantes da instância Sheet
        sheet_data = {
            "length": f"{sheet.length} m",
            "weight": f"{sheet.weight:.2f} kg",
            "defects": defects_str,
            "cuts": cuts_str,
            "weight_loss": loss_str,
            "loss_percent": loss_percent_str,
            "graph": plot_sheet(sheet),
            "new_weight": new_weight_str,
            "new_length": new_length_str
        }
        
        # Imprime os dados no formato JSON para facilitar o recebimento no Electron
        print(json.dumps(sheet_data))

    except Exception as e:
        # Captura e retorna erros em formato JSON
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
