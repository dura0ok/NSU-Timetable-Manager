import {StringHelper} from "./StringHelper";
import {EnvConfigParser} from "./EnvConfigParser";
import {REQUEST_SUCCESS_FLAG} from "./consts";

export class ServerAgent {
    static async fetchTimeTableData(groupID) {
        const url = StringHelper.concatHostPath(EnvConfigParser.parseBackendURL().toString(), `timetable/${groupID}`);
        const apiData = await fetch(url).then((response) => response.json());
        if (!apiData[REQUEST_SUCCESS_FLAG]) {
            throw new Error("Can't load data from the server.");
        }

        return apiData["result"];
    }

    static async #fetchData(endpoint, value) {
        const encoded = encodeURI(value);
        const url = StringHelper.concatHostPath(EnvConfigParser.parseBackendURL().toString(), endpoint + "/" + encoded)

        const response = await fetch(url);
        const json = await response.json();
        if (!json[REQUEST_SUCCESS_FLAG]) {
            throw new Error(`${endpoint} not found`);
        }
        return json.result;
    }

    static async getRoom(roomName) {
        return this.#fetchData('room', roomName);
    }

    static async getTutor(tutorName) {
        return this.#fetchData('tutor', tutorName);
    }
}