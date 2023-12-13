import {getWeekNum, subjectSelectors, subjectType, subjectTypeNames, weekType} from "./subject"
import {ObjectHelper} from "./ObjectHelper"
import {FunctionParser} from "./FunctionParser"
import {SubmitHandlers} from "./SubmitHandlers"
import {HIDE, PERIODICITY, RENDER_DATA_EVENT, SHOW, SUBJECT_KEY, SUBJECT_NAME_KEY} from "./consts";
import {showErrorToast} from "./toasts";

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
  
  .delete-btn{
    background:red;
    color:white;
  }
`;

export class Modal {
    #modalWrapperNode
    #originalEvent;
    #storage;

    #submitHandlerMap = new Map(Object.entries({
        'room': SubmitHandlers.roomSubmitHandler,
        'type': SubmitHandlers.typeSubmitHandler,
        'tutor': SubmitHandlers.tutorSubmitHandler
    }));


    constructor(storage, eventEmitter) {
        this.#modalWrapperNode = this.setupModal()
        this.#modalWrapperNode.querySelector(".modal-form").addEventListener("submit", (e) => this.handleSubmit(e))
        this.#modalWrapperNode.querySelector(".close-modal").addEventListener("click", this.handleClose.bind(this))
        this.eventEmitter = eventEmitter;
        this.#storage = storage;
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
        window.renderWeekSelect = this.#renderWeekSelect.bind(this)
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
                    <button type="submit" class="submit-delete-modal" name="delete">Delete</button>
                    <button type="submit" class="submit-edit-modal" name="submit">Submit</button>
                  </form>
                </div>
              </div>
        `;

        document.body.insertAdjacentHTML("beforeend", modalHtml)
    }

    #renderTypeSelect(dataKey) {
        return `
      <select name="${dataKey}">
        ${Array.from(subjectType, ([name]) =>
            `<option value="${name}">${subjectTypeNames.get(name.toString())}</option>`).join("\n")}
      </select>
    `;
    }

    #renderWeekSelect(dataKey) {
        return `
      <select name="${dataKey}">
        ${Array.from(weekType, ([, value]) =>
            `<option value="${value}">${value}</option>`).join("\n")}
      </select>
    `;
    }

    async handleEdit(e) {
        e.preventDefault();
        this.#originalEvent = e;
        const timeTableData = await this.#storage.fetchTimeTableData()
        let subjectData = this.getClickedObjData(e, timeTableData);
        if (!timeTableData) {
            this.#modalWrapperNode.querySelector(".submit-delete-modal").style.display = HIDE
            subjectData = {}
        } else {
            this.#modalWrapperNode.querySelector(".submit-delete-modal").style.display = SHOW
        }

        this.fillFormInputs(subjectData)
        if (!timeTableData) {
            this.#modalWrapperNode.querySelectorAll("select").forEach((select) => {
                select.value = select.options[0].value;
            })
        }
        this.#modalWrapperNode.style.display = SHOW
    }


    getCellInfo(e) {
        const el = e.target;
        const tdElement = el.closest("td");
        const dataID = parseInt(tdElement.getAttribute("data-id"));
        const cellCount = Array.from(tdElement.children).indexOf(el.parentElement);

        return {dataID, cellCount};
    }

    getClickedObjData(e, timeTableData) {
        if (timeTableData === null) {
            return null;
        }

        const {dataID, cellCount} = this.getCellInfo(e);
        const subjectData = timeTableData[dataID]?.[SUBJECT_KEY]?.[cellCount];

        return subjectData || null;
    }


    removeClickedObjData(e, timeTableData) {
        const {dataID, cellCount} = this.getCellInfo(e);
        timeTableData[dataID][SUBJECT_KEY].splice(cellCount, 1)
        this.#storage.store(timeTableData);
    }

    async handleSubmit(currentEvent) {
        currentEvent.preventDefault();
        const e = this.#originalEvent;

        if (!e) {
            this.#originalEvent = null;
            return;
        }
        const timeTableData = await this.#storage.fetchTimeTableData()

        const formNode = this.#modalWrapperNode.querySelector('.modal-form');
        const formData = Object.fromEntries(new FormData(formNode));
        let subjectData = this.getClickedObjData(e, timeTableData);
        if (!subjectData) {
            const res = this.getCellInfo(e)
            subjectData = {}
            subjectData.isEmpty = false
            timeTableData[res.dataID][SUBJECT_KEY].push(subjectData)
        }

        const submitterName = currentEvent.submitter.name
        if (submitterName === "delete") {
            this.removeClickedObjData(e, timeTableData)
            const updatedData = await this.#storage.fetchTimeTableData()
            this.eventEmitter.emit(RENDER_DATA_EVENT, updatedData)
            this.handleClose(e);
            return
        }

        const asyncTasks = [];

        if (formData[SUBJECT_NAME_KEY].trim() === "") {
            this.handleClose(e);
            showErrorToast("Имя предмета не может быть пустым!!")
            return
        }

        Object.keys(formData).forEach(dataKey => {
            const key = dataKey.split(".")[0];
            //if (key !== "room") return;

            if (this.#submitHandlerMap.has(key)) {
                const f = this.#submitHandlerMap.get(key);

                const task = f(subjectData, dataKey, formData[dataKey])
                asyncTasks.push(task);
            } else {
                let value = formData[dataKey]
                if (dataKey === PERIODICITY) {
                    value = parseInt(getWeekNum(value))
                }
                ObjectHelper.setValueByDotNotation(subjectData, dataKey, value);
            }
        });

        await Promise.all(asyncTasks);
        this.#storage.store(timeTableData);
        const updatedData = await this.#storage.fetchTimeTableData()
        this.eventEmitter.emit(RENDER_DATA_EVENT, updatedData)
        this.handleClose(e);
    }


    handleClose(e) {
        e.preventDefault();
        this.#modalWrapperNode.style.display = HIDE;
        this.#originalEvent = null
    }

    fillFormInputs(subjectData) {
        subjectSelectors.forEach(({dataKey}) => {
            const input = this.#modalWrapperNode.querySelector(`[name="${dataKey}"]`)
            if (input) {
                const value = ObjectHelper.getValueByDotNotation(subjectData, dataKey)
                if (!value) {
                    input.value = ""
                    return
                }
                if (dataKey === PERIODICITY) {
                    input.value = weekType.get(value.toString())
                    return
                }
                input.value = value
            }
        })
    }
}