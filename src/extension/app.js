import {getNsuTableUrl} from "./config";
import {loadTimeTableData} from "./network";

try{
    const groupID = new URL(window.location.href).pathname.split("/")[2]
    const timeTableData = await loadTimeTableData(groupID)
    console.log(timeTableData)
}catch (e){
    console.error("[Timetable extension] Something went wrong: ", e.message);
}


