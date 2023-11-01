import {subjectSelectors} from "./subject";
import {ObjectHelper} from "./ObjectHelper";
const modalCss = `
  .modal-custom-edit {
    display: none;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.4);
  }

  .modal-content {
    background-color: #fefefe;
    margin: 0 auto;
    margin-top: 10%;
    max-width: 400px;
    padding: 20px;
    border: 1px solid #888;
  }

  .close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
  }
  
  .close:hover,
  .close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
`;

const modalHtml = `
    <div class="modal-custom-edit">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <h2>Modal Form</h2>
            <form class="modal-form">
                ${subjectSelectors.map(({dataKey, placeholder }) => {
                if (!placeholder) {
                    return ''
                }
                return '<input type="text" name="' + dataKey + '" placeholder="' + placeholder + '" />';
                
                }).join('')}
                <button type="submit" class="submit-edit-modal">Submit</button>
            </form>
        </div>
    </div>
`;

export class Modal{
    #modalWrapperNode
    constructor() {
        this.#modalWrapperNode = this.setupCellEditing()
        this.#modalWrapperNode.querySelector(".modal-form").addEventListener("submit", this.handleSubmit)
        this.#modalWrapperNode.querySelector(".close-modal").addEventListener("click", this.handleClose.bind(this))
    }
    get modalWrapperNode() {
        return this.#modalWrapperNode;
    }

    setupCellEditing() {
        const styleElement = document.createElement('style');
        styleElement.innerHTML = modalCss;
        document.head.appendChild(styleElement);
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        return  document.querySelector('.modal-custom-edit');
    }

    handleSubmit(e){
        e.preventDefault()
        console.log("handle submit")
    }

    handleEdit(e, timeTableData){
        e.preventDefault();
        const el = e.target;
        const tdElement = el.closest('td');
        const dataID = parseInt(tdElement.getAttribute('data-id'));
        const cellCount = Array.from(tdElement.children).indexOf(el.parentElement);
        const subjectData = timeTableData[dataID]['subjects'][cellCount];
        this.fillFormInputs(subjectData)
        this.modalWrapperNode.style.display = 'block';
    }

    handleClose(e) {
        e.preventDefault()
        this.modalWrapperNode.style.display = 'none';
    }

    fillFormInputs(subjectData){
        subjectSelectors.forEach(({dataKey}) => {
            const input = this.modalWrapperNode.querySelector(`[name="${dataKey}"]`);
            if (input) {
                const value = ObjectHelper.getValueByDotNotation(subjectData, dataKey);
                input.value = value || '';

            }
        });
    }
}