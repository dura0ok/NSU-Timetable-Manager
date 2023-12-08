import {subjectType, subjectTypeNames, weekType} from "./subject";
import {IS_EMPTY_FLAG} from "./consts";

export class CustomRenderHandlersManager {
    static #renderMap = (element, subjectData) => {
        if (subjectData[IS_EMPTY_FLAG]) {
            return
        }

        element.innerText = subjectData["name"]

        const location = subjectData["location"]
        if (location[IS_EMPTY_FLAG]) {
            return;
        }

        const room_view = `room_view('${location.block}', ${location.level}, ${location.x}, ${location.y})`;
        element.setAttribute("onclick", room_view);
    };

    static #renderType = (element, key) => {
        const n = key.toString()
        if (!subjectType.has(n)) {
            return
        }

        const typeClass = subjectType.get(n)
        element.classList.remove(element.classList[1]);
        element.classList.add(typeClass);
        element.innerText = subjectTypeNames.get(n)
    };

    static #renderWeek = (element, subjectData) => {
        const key = subjectData.toString();
        if (weekType.has(key)) {
            element.innerText = weekType.get(key);
        }
    };

    static registerHandlers = () => {
        window.renderMap = this.#renderMap;
        window.renderType = this.#renderType;
        window.renderWeek = this.#renderWeek;
    };
}