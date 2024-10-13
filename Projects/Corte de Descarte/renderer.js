let filePath = ''; // Variável para armazenar o caminho do arquivo CSV

// Função para abrir o seletor de arquivos e definir o caminho do arquivo CSV
document.getElementById("selectFileButton").addEventListener("click", async () => {
    const result = await window.api.selectFile(); // Chama a função do preload.js
    if (result && result.filePaths && result.filePaths[0]) {
        filePath = result.filePaths[0];
        document.getElementById("selectedFilePath").innerText = `Arquivo Selecionado: ${filePath}`;
    } else {
        document.getElementById("selectedFilePath").innerText = "Nenhum arquivo selecionado.";
    }
});

async function searchSheet() {
    const searchInput = document.getElementById("searchInput");
    const sheetCode = searchInput.value.trim();

    // Verifica se o caminho do arquivo e o código da chapa estão disponíveis
    if (!filePath) {
        displayError("Por favor, selecione um arquivo CSV.");
        return;
    }
    if (!sheetCode) {
        displayError("Por favor, insira um código de chapa.");
        return;
    }

    try {
        // Desabilita o campo de entrada e botão durante a busca
        searchInput.disabled = true;
        document.getElementById("searchButton").disabled = true;

        // Chama a função do preload.js para obter os dados, passando o caminho do arquivo e o código da chapa
        const data = await window.api.getSheetData(filePath, sheetCode);

        if (data.error) {
            displayError("Nenhum dado encontrado para o código especificado.");
        } else {
            displaySheetData(data);
        }
    } catch (error) {
        displayError("Erro ao comunicar com o backend: " + error.message);
    } finally {
        // Habilita o campo de entrada e o botão de busca novamente
        searchInput.disabled = false;
        document.getElementById("searchButton").disabled = false;
        searchInput.focus(); // Reposiciona o cursor no campo de entrada
    }
}

function displaySheetData(data) {
    document.querySelector('.sheet-data').style.display = 'block';
    document.getElementById("length").querySelector("span").innerText = data.length;
    document.getElementById("weight").querySelector("span").innerText = data.weight;
    document.getElementById("defects").querySelector("span").innerText = data.defects;
    document.getElementById("cuts").querySelector("span").innerText = data.cuts;
    document.getElementById("weightLoss").querySelector("span").innerText = `${data.weight_loss} ${data.loss_percent}`;
    document.getElementById("new_length").querySelector("span").innerText = data.new_length;
    document.getElementById("new_weight").querySelector("span").innerText = data.new_weight;
    document.getElementById("graph").src = data.graph;

    document.getElementById("errorMessage").style.display = "none";
}

function displayError(message) {
    document.querySelector('.sheet-data').style.display = 'none';
    document.getElementById("errorMessage").innerText = message;
    document.getElementById("errorMessage").style.display = "block";
}

// Força o navegador a "recalcular" o layout após a adição de novos dados
function adjustWindowSize() {
    window.dispatchEvent(new Event('resize'));
}

// Registra o evento de clique para o botão de busca uma única vez
document.getElementById("searchButton").addEventListener("click", searchSheet);
