import {elementSelectors, modalCss, modalHtml} from "./modal";
import {getValueByDotNotation, setValueByDotNotation} from "./helper";
import {getRoom, getTutor, NSU_TABLE_URL, saveApiData} from "./dataLoader";

export const renderData = (apiData) => {
    const tds = document.querySelectorAll(
        '.time-table tr:not(:first-child) td:not(:first-child)'
    );
    tds.forEach((td, dataID) => {
        //console.log(apiData.cells[dataID], dataID)
        td.setAttribute('data-id', dataID.toString());
        const cells = td.querySelectorAll('.cell');
        cells.forEach((cell, index) => {
            const data = apiData.cells[dataID]['subjects'][index];
            updateCellContent(cell, data);
            const block = data["room"]["location"]
            const element = cell.querySelector(".room a");
            if (element) {
                const room_view = `return room_view('${block.block}', ${block.level}, ${block.x}, ${block.y});`;
                element.setAttribute("onclick", room_view)
                console.log(element)
            }

        });
    });
}

export const updateCellContent = (cell, subject) => {
    elementSelectors.forEach(({selector, property, dataKey}) => {
        const element = cell.querySelector(selector);
        if (element) {
            //console.log(subject, dataKey, getValueByDotNotation(subject, dataKey))
            const value = getValueByDotNotation(subject, dataKey);
            if (value !== null) {
                element[property] = value;
                //element.addEventListener('click', handleEdit);
            }
        }
    });
}

export const setupCellEditing = (apiData) => {
    const styleElement = document.createElement('style');
    styleElement.innerHTML = modalCss;
    document.head.appendChild(styleElement);
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modalFormNode = document.querySelector('.modal-custom-edit');

    document.querySelector('.close-modal').addEventListener('click', (e) => {
        closeModal(modalFormNode);
    },);

};

const populateFormInputs = (modalFormNode, clickedObj) => {
    elementSelectors.forEach(({dataKey}) => {
        const input = modalFormNode.querySelector(`[name="${dataKey}"]`);
        if (input) {
            const value = getValueByDotNotation(clickedObj, dataKey);
            input.value = value || ''; // Set the input value, or an empty string if value is null
        }
    });
}

const submitFormHandler = (e, modalFormNode, clickedObj, apiData) => {
    //console.log("submitFormHandler")
    e.preventDefault();
    for (const {dataKey} of elementSelectors) {
        const form = modalFormNode.querySelector('.modal-form');
        const input = form.querySelector(`[name="${dataKey}"]`);
        if (input) {
            const inputValue = input.value;
            if (dataKey === "tutor.name" && inputValue !== "") {
                getTutor(inputValue)
                    .then(response => {
                        const data = response.data
                        if (data != null && !data["isEmpty"]) {
                            const href = new URL(data["href"], NSU_TABLE_URL).href
                            setValueByDotNotation(clickedObj, "tutor.href", href)
                        } else {
                            setValueByDotNotation(clickedObj, "tutor.href", "#")
                        }
                        saveApiData(apiData)
                        renderData(apiData)
                    })

            }

            if (dataKey === "room.name" && inputValue !== "") {
                getRoom(inputValue)
                    .then(response => {
                        const data = response.data
                        if (data != null && !data["isEmpty"]) {
                            setValueByDotNotation(clickedObj, "room.name", data["name"])
                            setValueByDotNotation(clickedObj, "room.location", data["location"])
                            saveApiData(apiData)
                            renderData(apiData)
                        }
                    })

            }

            setValueByDotNotation(clickedObj, dataKey, inputValue);
            console.log(clickedObj)
        }
    }

    console.log(clickedObj)
    saveApiData(apiData);
    closeModal(modalFormNode)
    renderData(apiData)
}

const closeModal = (modalFormNode) => {
    modalFormNode.style.display = 'none';
    const modal = modalFormNode.querySelector('.modal-form')
    modal.replaceWith(modal.cloneNode(true));
    //console.log("form closed")
}

export const handleEdit = (e, apiData) => {

    e.preventDefault();
    const el = e.target;
    const tdElement = el.closest('td');
    const dataID = parseInt(tdElement.getAttribute('data-id'));
    const cellCount = Array.from(tdElement.children).indexOf(el.parentElement);
    const clickedObj = apiData.cells[dataID]['subjects'][cellCount];
    const submitEditModal = document.querySelector('.submit-edit-modal');
    const modalFormNode = document.querySelector('.modal-custom-edit');
    const submitFormEventListener = (e) =>
        submitFormHandler(e, modalFormNode, clickedObj, apiData);

    modalFormNode.querySelector('.modal-form').addEventListener('submit', submitFormEventListener)

    populateFormInputs(modalFormNode, clickedObj)
    modalFormNode.style.display = 'block';
};



