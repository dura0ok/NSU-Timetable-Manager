import {elementSelectors, modalCss, modalHtml} from "./modal";
import {getValueByDotNotation, setValueByDotNotation} from "./helper";
import {saveApiData} from "./dataLoader";

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
        });
    });
}

export const updateCellContent = (cell, subject) => {
    elementSelectors.forEach(({ selector, property, dataKey }) => {
        const element = cell.querySelector(selector);
        if (element) {
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
    }, );

};

const populateFormInputs = (modalFormNode, clickedObj) => {
    elementSelectors.forEach(({ dataKey }) => {
        const input = modalFormNode.querySelector(`[name="${dataKey}"]`);
        if (input) {
            const value = getValueByDotNotation(clickedObj, dataKey);
            input.value = value || ''; // Set the input value, or an empty string if value is null
        }
    });
}

const submitFormHandler = (e, modalFormNode, clickedObj, apiData) => {
        console.log("submitFormHandler")
        e.preventDefault();
        elementSelectors.forEach(({dataKey}) => {
            const form = modalFormNode.querySelector('.modal-form');
            const input = form.querySelector(`[name="${dataKey}"]`);
            if (input) {
                const inputValue = input.value;
                setValueByDotNotation(clickedObj, dataKey, inputValue);
            }
        });
        saveApiData(apiData);
        closeModal(modalFormNode)
        renderData(apiData)
}

const closeModal = (modalFormNode) => {
    modalFormNode.style.display = 'none';
    const modal = modalFormNode.querySelector('.modal-form')
    modal.replaceWith(modal.cloneNode(true));
    console.log("form closed")
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



