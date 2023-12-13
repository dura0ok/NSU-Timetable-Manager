import {CellRenderer} from "./CellRenderer";
import {Modal} from "./Modal";
import {EventEmitter} from "./EventEmitter"
import {Storage} from "./Storage";
import {getGroupNumberFromURL} from "./Helper";
import {RENDER_DATA_EVENT} from "./consts";
import {showErrorToast} from "./toasts"
import "toastify-js/src/toastify.css"

try {
    const groupID = getGroupNumberFromURL()
    const emitter = new EventEmitter()
    const storage = new Storage(groupID)
    const timetableData = await storage.fetchTimeTableData(groupID)
    const m = new Modal(storage, emitter)
    const cellRenderer = new CellRenderer(m, emitter)
    cellRenderer.renderData(timetableData)


    const navbar = document.querySelector(".main_head")
    const navbarStyles = document.createElement("style")
    navbarStyles.innerHTML = `
        .main_head button{
              background-color: #e7e7e7;
              border: none;
              color: black;
              width: 140px;
              height: 50px;
              margin: 20px;
              text-align: center;
              text-decoration: none;
              font-size: 17px;
        }
    `
    navbar.appendChild(navbarStyles)

    const exportBtn = document.createElement("button")
    exportBtn.innerText = "Экспортировать"
    navbar.appendChild(exportBtn)


    const importBtn = document.createElement("button")
    importBtn.innerText = "Импортировать"
    navbar.appendChild(importBtn)

    const clearBtn = document.createElement("button")
    clearBtn.innerText = "Очистить"
    navbar.appendChild(clearBtn)

    clearBtn.addEventListener("click", async () => {
        storage.clear()
        const updatedData = await storage.fetchTimeTableData()
        console.log("Cleared", updatedData)
        emitter.emit(RENDER_DATA_EVENT, updatedData)
    })

    const truncateBtn = document.createElement("button")
    truncateBtn.innerText = "Восстановить"
    navbar.appendChild(truncateBtn)

    truncateBtn.addEventListener("click", async () => {
        storage.truncate()
        const updatedData = await storage.fetchTimeTableData()
        emitter.emit(RENDER_DATA_EVENT, updatedData)
    })

    exportBtn.addEventListener("click", () => {
        const blob = storage.exportToBlob();
        const blobURL = URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = blobURL;
        a.download = "data.json"; // Specify the filename

        // Append the anchor element to the body and simulate a click
        document.body.appendChild(a);
        a.click();

        // Remove the anchor element and revoke the URL to free up resources
        document.body.removeChild(a);
        URL.revokeObjectURL(blobURL);
    });


    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.style.display = "none"; // Hide the file input
    navbar.appendChild(fileInput);

// Attach a click event listener to the Import button
    importBtn.addEventListener("click", () => {
        // Trigger a click event on the hidden file input
        fileInput.click();
    });


    fileInput.addEventListener("change", (event) => {
        const selectedFile = event.target["files"][0]

        if (selectedFile) {
            // Use the importFromBlob method with the selected file
            storage.importFromBlob(selectedFile)
                .then(async () => {
                    const updatedData = await storage.fetchTimeTableData()
                    emitter.emit(RENDER_DATA_EVENT, updatedData)
                })
                .catch((error) => {
                    showErrorToast("Import error: " + error.message)
                });
        }
    });


} catch (e) {
    console.error("[Timetable extension] Something went wrong: ", e.message);
    console.log(e)
}
