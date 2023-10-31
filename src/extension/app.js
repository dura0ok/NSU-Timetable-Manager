import {TimeTableManager} from "./TimeTableManager";
import {CellRender} from "./CellRender";
import {Modal, ModalForm} from "./Modal";

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

    const m = new Modal()
    console.log(m.modalWrapperNode)
} catch (e) {
    console.error("[Timetable extension] Something went wrong: ", e.message);
    console.log(e)
}


