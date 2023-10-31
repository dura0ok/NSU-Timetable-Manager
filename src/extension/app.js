import {loadTimeTableData} from "./network";
import {renderData} from "./render";

try {
    const groupID = new URL(window.location.href).pathname.split("/")[2]
    const timeTableData = await loadTimeTableData(groupID)
    timeTableData[3]["subjects"][0].name["shortName"] = "123"
    renderData(timeTableData)
} catch (e) {
    console.error("[Timetable extension] Something went wrong: ", e.message);
}


