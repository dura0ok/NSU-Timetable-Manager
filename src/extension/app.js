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
} catch (e) {
    console.error("[Timetable extension] Something went wrong: ", e.message);
    console.log(e)
}


