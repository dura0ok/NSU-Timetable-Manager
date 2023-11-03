import {subjectSelectors, subjectType} from "./subject"
import {ObjectHelper} from "./ObjectHelper"
import {FunctionParser} from "./FunctionParser"
import {CellRender} from "./CellRender";

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

  .close-modal {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
  }

  .close-modal:hover,
  .close-modal:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
`;

export class Modal {
    #modalWrapperNode
    #currentEvent;

    #submitHandlerMap = {
        'room': SubmitHandlers.roomSubmitHandler,
        'type': SubmitHandlers.typeSubmitHandler,
        'tutor': SubmitHandlers.tutorSubmitHandler
    };

    constructor(timeTableData, timeTableManager) {
        this.#modalWrapperNode = this.setupModal()
        this.#modalWrapperNode.querySelector(".modal-form").addEventListener("submit", (e) => this.handleSubmit(e, timeTableData))
        this.#modalWrapperNode.querySelector(".close-modal").addEventListener("click", this.handleClose.bind(this))
        this.timeTableManager = timeTableManager
    }

    setupModal() {
        this.setupCustomRenderFormFunctions()
        const styleElement = document.createElement("style")
        styleElement.innerHTML = modalCss
        document.head.appendChild(styleElement)
        this.setupModalHtml()
        return document.querySelector(".modal-custom-edit")
    }

    setupCustomRenderFormFunctions() {
        window.renderTypeSelect = this.#renderTypeSelect.bind(this)
    }

    setupModalHtml() {
        const modalHtml = `
              <div class="modal-custom-edit">
                <div class="modal-content">
                  <span class="close-modal">&times;</span>
                  <h2>Modal Form</h2>
                  <form class="modal-form">
                    ${subjectSelectors
            .map(({dataKey, placeholder, formRender}) => {
                if (!placeholder) {
                    return ""
                }
                if (formRender) {
                    const customRenderFunc = FunctionParser.parseFunctionName(formRender);
                    if (typeof window[customRenderFunc] === "function") {
                        return window[customRenderFunc](dataKey);
                    }
                }
                return '<input type="text" name="' + dataKey + '" placeholder="' + placeholder + '" />'
            })
            .join("")}
                    <button type="submit" class="submit-edit-modal">Submit</button>
                  </form>
                </div>
              </div>
        `;

        document.body.insertAdjacentHTML("beforeend", modalHtml)
    }

    #renderTypeSelect(dataKey) {
        return `
      <select name="${dataKey}">
        ${Array.from(subjectType, ([name, value]) =>
            `<option value="${value}">${name}</option>`).join("\n")}
      </select>
    `;
    }

    handleEdit(e, timeTableData) {
        e.preventDefault();
        this.#currentEvent = e; // Store the event object
        const subjectData = this.getClickedObjData(e, timeTableData);
        this.fillFormInputs(subjectData)
        this.#modalWrapperNode.style.display = "block"
    }


    getClickedObjData(e, timeTableData) {
        const el = e.target;
        const tdElement = el.closest("td")
        const dataID = parseInt(tdElement.getAttribute("data-id"))
        const cellCount = Array.from(tdElement.children).indexOf(el.parentElement)
        return timeTableData[dataID]["subjects"][cellCount];
    }

    handleSubmit(originalEvent, timeTableData) {
        originalEvent.preventDefault()
        const e = this.#currentEvent;
        if (!e) {
            this.#currentEvent = null;
            return
        }

        console.log(e.target, e.target.closest("td"))
        const formNode = this.#modalWrapperNode.querySelector('.modal-form');
        const formData = Object.fromEntries(new FormData(formNode));
        const subjectData = this.getClickedObjData(e, timeTableData);
        Object.keys(formData).forEach(key => {
            console.log(key)
            ObjectHelper.setValueByDotNotation(subjectData, key, formData[key])
        });
        this.timeTableManager.saveTimeTableData(timeTableData)
        CellRender.renderData(timeTableData)
        this.handleClose(e);
    }

    handleClose(e) {
        e.preventDefault();
        this.#modalWrapperNode.style.display = "none";
        this.#currentEvent = null
    }

    fillFormInputs(subjectData) {
        subjectSelectors.forEach(({dataKey, formRender}) => {
            const input = this.#modalWrapperNode.querySelector(`[name="${dataKey}"]`)
            if (input) {
                const value = ObjectHelper.getValueByDotNotation(subjectData, dataKey)
                if (formRender === "renderTypeSelect()") {
                    input.value = subjectType.get(value)
                    return
                }
                input.value = value || "";
            }
        })
    }
}