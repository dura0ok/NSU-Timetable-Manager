import {loadApiData} from "./dataLoader";
import {handleEdit, renderData, setupCellEditing} from "./render";

const groupID = new URL(window.location.href).pathname.split("/")[2]
let apiData = await loadApiData(groupID);
//console.log(JSON.stringify(apiData))
console.log(apiData)
document.querySelectorAll(".cell").forEach((el) => {
    el.addEventListener("click", (e) => handleEdit(e, apiData));
});

renderData(apiData);
setupCellEditing(apiData)
