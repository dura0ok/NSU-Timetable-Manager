import {TimeTableManager} from "./TimeTableManager";
import {CellRenderer} from "./CellRenderer";
import {Modal} from "./Modal";
import {EventEmitter} from "./EventEmitter"

const getGroupNumberFromURL = () => {
    return new URL(window.location.href).pathname.split("/")[2];
}

try {
    const groupID = getGroupNumberFromURL()
    const timeTableManager = new TimeTableManager(groupID)
    const timeTableData = await timeTableManager.loadTimeTableData()
    const emitter = new EventEmitter()
    const m = new Modal(timeTableData, timeTableManager, emitter)
    const cellRenderer = new CellRenderer(timeTableData, m, emitter)
    cellRenderer.renderData(timeTableData)

    document.querySelectorAll(".subject").forEach((el) => {
        el.addEventListener("click", (e) => m.handleEdit(e, timeTableData));
    });
} catch (e) {
    console.error("[Timetable extension] Something went wrong: ", e.message);
    console.log(e)
}


