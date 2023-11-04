import {ObjectHelper} from "./ObjectHelper"
import {subjectSelectors, weekType} from "./subject"
import {FunctionParser} from "./FunctionParser"
import {CustomRenderHandlersManager} from "./customRenderHandlers"

export class CellRenderer {
    static #tds = document.querySelectorAll(
        '.time-table tr:not(:first-child) td:not(:first-child)'
    )
    static #renderCell = (cell, apiData, cellIndex, index) => {
        const subjectData = apiData[cellIndex]['subjects'][index]
        this.#renderSubject(cell, subjectData)
    };

    static #renderSubject = (el, subjectData) => {
        CustomRenderHandlersManager.registerHandlers()
        subjectSelectors.forEach(({selector, property, dataKey}) => {
            const element = el.querySelector(selector);
            const funcName = FunctionParser.parseFunctionName(property)

            if (element) {
                const value = ObjectHelper.getValueByDotNotation(subjectData, dataKey)
                if (value !== null) {
                    if (funcName !== "") {
                        window[funcName](element, value)
                        return
                    }
                    element[property] = value
                }
            }
        });
        const weekElement = el.querySelector(".week")
        if (weekElement) {
            weekElement.remove()
        }

        const weekNum = subjectData["periodicity"]
        if (weekNum === 2) {
            return
        }
        const week = document.createElement("div")
        week.classList.add("week")
        week.innerText = weekType.get(weekNum.toString())
        el.appendChild(week)
    };

    static renderData = (apiData) => {
        this.#tds.forEach((td, dataID) => {
            td.setAttribute('data-id', dataID.toString())
            const cells = td.querySelectorAll('.cell')
            // if(cells.length > 1){
            //     debugger;
            // }
            cells.forEach((cell, index) => {
                this.#renderCell(cell, apiData, dataID, index)
            })
        })
    }
}
