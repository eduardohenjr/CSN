// main.js
const { app, BrowserWindow, ipcMain, dialog } = require("electron");
const path = require("path");
const { exec } = require("child_process");

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 900,
        icon: "imgs/icon.ico",
        autoHideMenuBar: true,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            nodeIntegration: false,
            contextIsolation: true,
        }
    });

    win.loadFile("index.html");
}

// Função para abrir o seletor de arquivos e retornar o caminho selecionado
ipcMain.handle("select-file", async () => {
    const result = await dialog.showOpenDialog({
        properties: ["openFile"],
        filters: [{ name: "CSV Files", extensions: ["csv"] }]
    });
    return result;
});

// Função para executar o script Python e retornar os dados
ipcMain.handle("get-sheet-data", async (event, filePath, sheetCode) => {
    return new Promise((resolve, reject) => {
        exec(`python3 backend/run_sheet.py "${filePath}" "${sheetCode}"`, (error, stdout, stderr) => {
            if (error) {
                reject({ error: stderr });
            } else {
                try {
                    const data = JSON.parse(stdout); // JSON <--> Python
                    resolve(data);
                } catch (parseError) {
                    reject({ error: "Erro ao processar dados do Python" });
                }
            }
        });
    });
});

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
});
