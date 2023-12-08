import {CellRenderer} from "./CellRenderer";
import {Modal} from "./Modal";
import {EventEmitter} from "./EventEmitter";
import {Storage} from "./Storage";
import {getGroupNumberFromURL} from "./Helper";

const initializeApp = async () => {
    try {
        const groupID = getGroupNumberFromURL();
        const emitter = new EventEmitter();
        const storage = new Storage(groupID);
        const timetableData = await storage.fetchTimeTableData(groupID);
        console.log(timetableData);
        initializeModal(timetableData, storage, emitter);
        initializeCellRenderer(timetableData, emitter);
        initializeExportImportButtons(storage);

        // Resolve the promise when initialization is complete
        return Promise.resolve();
    } catch (error) {
        console.error("Initialization error:", error.message);
        return Promise.reject(error);
    }
};

const initializeModal = (timetableData, storage, emitter) => {
    const m = new Modal(timetableData, storage, emitter);

    document.querySelectorAll(".subject").forEach((el) => {
        el.addEventListener("click", (e) => m.handleEdit(e, timetableData));
    });
};

const initializeCellRenderer = (timetableData, emitter) => {
    const cellRenderer = new CellRenderer(timetableData, new Modal(), emitter);
    cellRenderer.renderData(timetableData);
};


const initializeExportImportButtons = (storage) => {
    const navbar = document.querySelector(".main_head");

    const exportBtn = createButton("Экспортировать", () => handleExport(storage));
    const importBtn = createButton("Импортировать", () => handleImport(storage));

    navbar.appendChild(exportBtn);
    navbar.appendChild(importBtn);
};

const createButton = (text, clickHandler) => {
    const button = document.createElement("button");
    button.innerText = text;
    button.addEventListener("click", clickHandler);
    return button;
};

const handleExport = (storage) => {
    const blob = storage.exportToBlob();
    const blobURL = URL.createObjectURL(blob);
    downloadBlob(blobURL, "data.json");
};

const handleImport = (storage) => {
    const fileInput = createFileInput();
    fileInput.addEventListener("change", (event) => handleFileInputChange(event, storage));
    fileInput.click();
};

const createFileInput = () => {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.style.display = "none";
    document.querySelector(".main_head").appendChild(fileInput);
    return fileInput;
};

const handleFileInputChange = (event, storage) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
        storage.importFromBlob(selectedFile)
            .then((data) => console.log("Imported data:", data))
            .catch((error) => console.error("Import error:", error.message));
    }
};

const downloadBlob = (blobURL, filename) => {
    const a = document.createElement("a");
    a.href = blobURL;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(blobURL);
};

// Call initializeApp and handle the promise
initializeApp()
    .then(() => {
        console.log("Initialization completed successfully");
    })
    .catch((error) => {
        console.error("Initialization error:", error.message);
    });
