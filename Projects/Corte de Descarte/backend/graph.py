import matplotlib.pyplot as plt
import os
from sheet import Sheet
from control import GRAPHS_DIR

def plot_sheet(sheet: Sheet) -> str:
    """
    Plota um gráfico com as deformidades na chapa e salva como PNG.
    
    Parameters:
        Sheet (Sheet): Objeto sheet da chapa a ser gerado o gráfico
    
    Returns:
        str: Caminho do arquivo PNG salvo.
    """
    
    # Verifica se o diretório existe, se não existir, cria
    output_dir = GRAPHS_DIR
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Definir o caminho do arquivo
    output_path = os.path.join(output_dir, f"{sheet.sheet_code}.png")
    
    # Extrair informações da chapa
    sheet_length, defect_positions, cut_positions = sheet.length, sheet.defects, sheet.cuts

    # Criar a figura do gráfico
    fig, ax = plt.subplots(figsize=(10, 2))  # Define o tamanho da figura

    # Representação da chapa como uma linha horizontal
    ax.plot([0, sheet_length], [0, 0], color='silver', linewidth=200)  # Chapa (não será incluída na legenda)

    # Adiciona deformidades como barras verticais roxas
    defect_lines = []
    for pos in defect_positions:
        line = ax.axvline(x=pos, color='purple', linewidth=6, alpha=0.7)  # Defeitos
        defect_lines.append(line)

    # Adiciona cortes como barras verticais vermelhas
    cut_lines = []
    if isinstance(cut_positions, tuple):
        for pos in cut_positions:
            if pos != 0:
                line = ax.axvline(x=pos, color='red', linewidth=6, alpha=0.7)  # Cortes
                cut_lines.append(line)
    
    # Configuração dos eixos
    ax.set_xlim(0, sheet_length)
    ax.set_ylim(-1, 1)  # Limita o eixo Y para manter as deformidades visíveis
    ax.set_xticks(range(0, int(sheet_length) + 1, int(sheet_length // 10)))  # Marcas no eixo X a cada 10% do comprimento

    # Títulos e legendas
    ax.set_title(f"Chapa: {sheet.sheet_code}")
    ax.set_xlabel("Comprimento (m)")
    ax.get_yaxis().set_visible(False)  # Oculta o eixo Y
    
    # Criar handles e labels personalizados para a legenda
    if isinstance(cut_positions, tuple):
        handles = [defect_lines[0], cut_lines[0]]
        labels = ['Defeitos', 'Cortes']
        legend = True
    elif defect_positions != []:
        handles = [defect_lines[0]]
        labels = ['Defeitos']
        legend = True
    else:
        legend = False

    # Adiciona legenda pequena no canto inferior esquerdo
    if legend:
        ax.legend(handles, labels, fontsize='medium', handletextpad=0.5, bbox_to_anchor=(1.05, 0.6), borderaxespad=0.)

    # Salva o gráfico como PNG
    plt.savefig(output_path, bbox_inches='tight')
    plt.close(fig)  # Fecha a figura para liberar memória
    
    # Retorna o caminho do arquivo salvo
    return output_path
