import {CellRenderer} from "./CellRenderer";
import {Modal} from "./Modal";
import {EventEmitter} from "./EventEmitter"
import {Storage} from "./Storage";
import {getGroupNumberFromURL} from "./Helper";

try {
    const groupID = getGroupNumberFromURL()
    const emitter = new EventEmitter()
    const storage = new Storage(groupID)
    const timetableData = await storage.fetchTimeTableData(groupID)
    console.log(timetableData)
    const m = new Modal(timetableData, storage, emitter)
    const cellRenderer = new CellRenderer(timetableData, m, emitter)
    cellRenderer.renderData(timetableData)

    document.querySelectorAll(".subject").forEach((el) => {
        el.addEventListener("click", (e) => m.handleEdit(e, timetableData));
    });


    const navbar = document.querySelector(".main_head")
    const exportBtn = document.createElement("button")
    exportBtn.innerText = "Экспортировать"
    navbar.appendChild(exportBtn)

    const importBtn = document.createElement("button")
    importBtn.innerText = "Импортировать"
    navbar.appendChild(importBtn)

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
                .then((data) => {
                    // Handle the imported data as needed
                    console.log("Imported data:", data);
                })
                .catch((error) => {
                    // Handle errors during the import process
                    console.error("Import error:", error.message);
                });
        }
    });


} catch (e) {
    console.error("[Timetable extension] Something went wrong: ", e.message);
    console.log(e)
}


