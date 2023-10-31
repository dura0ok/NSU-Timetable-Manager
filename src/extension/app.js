import {TimeTableManager} from "./TimeTableManager";
import {renderData} from "./render";

try {
    const groupID = new URL(window.location.href).pathname.split("/")[2]
    const timeTableManager = new TimeTableManager(groupID)
    const timeTableData = await timeTableManager.loadTimeTableData()
    console.log(timeTableData)
    timeTableData[3]["subjects"][0].name["shortName"] = "123"
    renderData(timeTableData)
} catch (e) {
    console.error("[Timetable extension] Something went wrong: ", e.message);
    console.log(e)
}


