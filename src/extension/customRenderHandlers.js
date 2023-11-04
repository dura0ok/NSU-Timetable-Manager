import {subjectType, weekType} from "./subject";

export class CustomRenderHandlersManager {
    static #renderMap = (element, subjectData) => {
        if (subjectData["isEmpty"]) {
            element.setAttribute("onclick", "")
            return
        }
        const room_view = `room_view('${subjectData.block}', ${subjectData.level}, ${subjectData.x}, ${subjectData.y})`
        element.setAttribute("onclick", room_view)
    };

    static #renderType = (element, subjectData) => {
        if (subjectData["isEmpty"]) {
            return;
        }

        const shortName = subjectData["shortName"];
        if (subjectType.has(shortName)) {
            element.classList.remove(element.classList[1])
            element.classList.add(subjectType.get(shortName))
        }
    };

    static #renderWeek = (element, subjectData) => {
        const key = subjectData.toString()
        if (weekType.has(key)) {
            element.innerText = weekType.get(key)
        }
    };

    static registerHandlers = () => {
        window.renderMap = this.#renderMap;
        window.renderType = this.#renderType;
        window.renderWeek = this.#renderWeek;
    };
}