import {EnvConfigParser} from "./EnvConfigParser";

export class TimeTableManager {
    constructor(group_id) {
        this.group_id = group_id
    }

    async #parseDataFromBackend() {
        const url = `${EnvConfigParser.parseBackendURL()}/timetable/${this.group_id}`;
        return (await fetch(url)).json();
    }

    #saveTimeTableData(data) {
        localStorage.setItem(`${this.group_id}-timetable`, JSON.stringify(data));
    }

    #getTimeTableData() {
        return localStorage.getItem(`${this.group_id}-timetable`);
    }

    async loadTimeTableData() {
        const localData = this.#getTimeTableData();

        if (localData) {
            console.log("Data available in local storage");
            return JSON.parse(localData);
        } else {
            const apiData = await this.#parseDataFromBackend();

            if (!apiData["isSuccess"]) {
                throw new Error("Can't load data from the server.");
            }

            TimeTableManager.#saveTimeTableData(
                apiData["result"]["cells"]
            );
            return apiData;
        }
    }
}