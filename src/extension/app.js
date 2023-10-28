import { fakeJSON } from './fake';
import { modalHtml, modalCss, elementSelectors } from './modal';
import { getValueByDotNotation, setValueByDotNotation } from './helper';


const tds = document.querySelectorAll('.time-table tr:not(:first-child) td:not(:first-child)');

const getRawData = async () => {
  const url = 'http://127.0.0.1:5000/timetable/21203';

  try {
    const response = await fetch(url);
    const json = await response.json();

    return { ok: true, data: json.result };
  } catch (error) {
    return { ok: false, error };
  }
};

const loadApiData = async () => {
  const rawData = localStorage.getItem('data');
  console.log("ASDASD", rawData)
  if (rawData) {
    // If data is available in local storage, parse and return it
    return JSON.parse(rawData);
  } else {
    // If data is not available in local storage, fetch it from the API
    const apiData = await getRawData();
    const data = apiData.data
    
    // Store the fetched data in local storage for future use
    localStorage.setItem('data', JSON.stringify(data));

    return data;
  }
};



let apiData = await loadApiData();
console.log(apiData);




function saveApiData() {
  console.log(apiData);

  localStorage.setItem('data', JSON.stringify(apiData));
}

function populateFormInputs(clickedObj) {
  elementSelectors.forEach(({ dataKey }) => {
    const input = modalFormNode.querySelector(`[name="${dataKey}"]`);
    if (input) {
      const value = getValueByDotNotation(clickedObj, dataKey);
      input.value = value || ''; // Set the input value, or an empty string if value is null
    }
  });
}

const ass = (e, options) => {
  e.preventDefault();
  const { clickedObj } = options;
  const form = modalFormNode.querySelector('.modal-form');

  // Update the clickedObj with values from the form inputs
  elementSelectors.forEach(({ dataKey }) => {
    const input = form.querySelector(`[name="${dataKey}"]`);
    if (input) {
      const inputValue = input.value;
      setValueByDotNotation(clickedObj, dataKey, inputValue);
    }
  });

  // Hide the modal form
  modalFormNode.style.display = 'none';

  // Update the localStorage or send the changes to your server
  saveApiData();

  // Reinitialize cell editing to reflect the changes
  setupCellEditing();
};

function handleEdit(event) {
  debugger;
  event.preventDefault();
  const el = event.target;
  const tdElement = el.closest('td');
  const dataID = parseInt(tdElement.getAttribute('data-id'));
  const cellCount = Array.from(tdElement.children).indexOf(el.parentElement);
  const clickedObj = apiData.cells[dataID]['subjects'][cellCount];
  const submitEditModal = document.querySelector('.submit-edit-modal');

  // Display the modal form
  modalFormNode.style.display = 'block';

  // Populate the form inputs with values from the clickedObj
  populateFormInputs(clickedObj);

  const saveChangesHandler = (e) => {
    ass(e, { clickedObj });

    // После выполнения функции saveChanges, удаляем слушатель
    submitEditModal.removeEventListener('click', saveChangesHandler);
  };

  // Handle form submission
  submitEditModal.addEventListener('click', saveChangesHandler);
}

function updateCellContent(cell, subject) {
  elementSelectors.forEach(({ selector, property, dataKey }) => {
    const element = cell.querySelector(selector);
    if (element) {
      const value = getValueByDotNotation(subject, dataKey);
      if (value !== null) {
        element[property] = value;
        element.addEventListener('click', handleEdit);
      }
    }
  });
}

function setupCellEditing() {
  tds.forEach((td, dataID) => {
    console.log(apiData.cells[dataID], dataID)
    td.setAttribute('data-id', dataID.toString());
    const cells = td.querySelectorAll('.cell');
    cells.forEach((cell, index) => {
      const data = apiData.cells[dataID]['subjects'][index];
      updateCellContent(cell, data);
    });
  });
}

// Event listener to handle form submission when the enter key is pressed

// Initialize cell editing
setupCellEditing();

// Insert the modal HTML and CSS
const styleElement = document.createElement('style');
styleElement.innerHTML = modalCss;
document.head.appendChild(styleElement);
document.body.insertAdjacentHTML('beforeend', modalHtml);
const modalFormNode = document.querySelector('.modal-custom-edit');

modalFormNode.querySelector('.modal-form').addEventListener('submit', (e) => {
  e.preventDefault();
  modalFormNode.querySelector('.submit-edit-modal').click();
});

document.querySelector('.close-modal').addEventListener('click', () => {
  modalFormNode.style.display = 'none';
});

console.log('%cHello World!', 'color: #f709bb; font-family: sans-serif; text-decoration: underline;');
