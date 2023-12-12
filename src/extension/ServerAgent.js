import {concatHostPath} from "./Helper";
import {EnvConfigParser} from "./EnvConfigParser";
import {REQUEST_SUCCESS_FLAG} from "./consts";

export class ServerAgent {
    static async fetchTimeTableData(groupID) {
        const key = `${groupID}-timetable`;

        const url = concatHostPath(EnvConfigParser.parseBackendURL().toString(), `timetable/${groupID}`);
        const apiData = await fetch(url).then((response) => response.json());
        if (!apiData[REQUEST_SUCCESS_FLAG]) {
            throw new Error("Can't load data from the server.");
        }

        return apiData["result"];
    }
}