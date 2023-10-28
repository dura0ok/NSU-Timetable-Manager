import { fakeJSON } from './fake';
import { modalHtml, modalCss, elementSelectors } from './modal';
import { getValueByDotNotation, setValueByDotNotation } from './helper';
import {loadApiData} from "./dataLoader";
import {handleEdit, renderData, saveApiData, setupCellEditing} from "./render";

let apiData = await loadApiData();
console.log(apiData)

// document.querySelectorAll(".cell").forEach((el) => {
//     el.addEventListener("click", (e) => handleEdit(e, apiData));
// });

document.querySelector('.time-table').addEventListener('click', (e) => {

    if (e.target.parentNode.classList.contains('cell')) {
        console.log(e.target)
        handleEdit(e, apiData);
    }
});
renderData(apiData);
setupCellEditing(apiData)
