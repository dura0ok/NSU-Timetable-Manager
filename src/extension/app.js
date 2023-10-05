import {
    Lesson,
    LessonType,
    getByLessonType,
    Teacher,
    Periodicity,
    getByPeriodicityType
} from "./cell"

import {
    fakeJSON
} from "./fake";
import {modalHtml, modalCss} from "./modal";


const tds = document.querySelectorAll('.time-table tr:not(:first-child) td:not(:first-child)');
const rawData = localStorage.getItem("data")
const apiData = rawData == null ? JSON.parse(fakeJSON) : JSON.parse(rawData)


tds.forEach((td, dataID) => {
    td.setAttribute('data-id', dataID);
    const id = parseInt(td.getAttribute('data-id'))
    // console.log(td, apiData.cells[dataID])
    const cells = td.querySelectorAll('.cell')
    cells.forEach((cell) => {
        const origShortName = cell.querySelector(".subject").textContent.trim()
        //console.log(origShortName)
        const subjectsInCell = apiData.cells[dataID]["subjects"]
        subjectsInCell.forEach((subject, subjectID) => {

            const subj = cell.querySelector(".subject")
            if (subj) {
                subj.textContent = subject["subjectName"]["shortName"]
                subj.addEventListener("click", handleEdit);
            }

            const room = cell.querySelector(".room a")
            if (room) {
                room.textContent = subject["room"]["name"]
                room.addEventListener("click", handleEdit);
            }

            const type = cell.querySelector(".type")
            if (type) {
                cell.querySelector(".type").textContent = subject["subjectType"]["shortName"]
                type.addEventListener("click", handleEdit);
            }


            const tutor = cell.querySelector(".tutor a")
            if (tutor) {
                tutor.textContent = subject["tutor"]["name"]
                tutor.href = subject["tutor"]["href"]
                tutor.addEventListener("click", handleEdit);
            }


        })
        //console.log(JSON.stringify(subjectsInCell))
        //cell.querySelector(".subject").textContent = foundElement["subjectName"]["shortName"]
    })
})


function handleEdit(event) {
    console.log("asd")
    event.preventDefault()
    const el = event.target
    const tdElement = el.closest("td")
    const dataID = parseInt(tdElement.getAttribute("data-id"))
    const cellCount = Array.from(tdElement.children).indexOf(el.parentElement);
    const clickedObj = apiData.cells[dataID]["subjects"][cellCount]
    modalFormNode.style.display = "block"

    modalFormNode.querySelector(".submit-edit-modal").addEventListener("click", (e) => {
         e.preventDefault()
         const form = document.querySelector(".modal-form")
         console.log(clickedObj, form.elements["subject-name"].value)
         clickedObj["subjectName"]["shortName"] = form.elements["subject-name"].value
         modalFormNode.style.display = "none"
         console.log(clickedObj)

         localStorage.setItem("data", JSON.stringify(apiData))
    })
}


const styleElement = document.createElement("style");
styleElement.innerHTML = modalCss;
document.head.appendChild(styleElement);
document.body.insertAdjacentHTML('beforeend', modalHtml);

const modalFormNode = document.querySelector(".modal-custom-edit")

document.querySelector(".close-modal").addEventListener("click", () => {
    modalFormNode.style.display = "none"
})


document.querySelector(".close-modal").addEventListener("click", () => {
    modalFormNode.style.display = "none"
})

