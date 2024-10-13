const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("api", {
    selectFile: () => ipcRenderer.invoke("select-file"),  // Abre o seletor de arquivos
    getSheetData: (filePath, sheetCode) => ipcRenderer.invoke("get-sheet-data", filePath, sheetCode)
});
