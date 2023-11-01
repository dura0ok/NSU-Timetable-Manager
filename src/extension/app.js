import {TimeTableManager} from "./TimeTableManager";
import {CellRender} from "./CellRender";
import {Modal} from "./Modal";

const getGroupNumberFromURL = () => {
    return new URL(window.location.href).pathname.split("/")[2];
}

try {
    const groupID = getGroupNumberFromURL()
    const timeTableManager = new TimeTableManager(groupID)
    const timeTableData = await timeTableManager.loadTimeTableData()
    console.log(timeTableData)
    timeTableData[3]["subjects"][0].name["shortName"] = "123"
    CellRender.renderData(timeTableData)

    const m = new Modal(timeTableData, timeTableManager)

    document.querySelectorAll(".subject").forEach((el) => {
        el.addEventListener("click", (e) => m.handleEdit(e, timeTableData));
    });


} catch (e) {
    console.error("[Timetable extension] Something went wrong: ", e.message);
    console.log(e)
}


