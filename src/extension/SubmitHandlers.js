import {ObjectHelper} from "./ObjectHelper";
import {EnvConfigParser} from "./EnvConfigParser";

export class SubmitHandlers {
    static async #getRoom(room_name) {
        const encoded = encodeURI(room_name);
        const url = EnvConfigParser.parseBackendURL() + '/room/' + encoded;
        const response = await fetch(url);
        const json = await response.json();
        if(!json["isSuccess"]){
            throw new Error("room not found")
        }
        return json.result;
    }

    static roomSubmitHandler(data, dataKey, value) {
        return new Promise(async (resolve, reject) => {
            try{
                ObjectHelper.setValueByDotNotation(data, dataKey, value)
                const r = await SubmitHandlers.#getRoom(value)
                ObjectHelper.setValueByDotNotation(data, "room.location", r["location"])
                resolve()
            }catch (error){
                ObjectHelper.setValueByDotNotation(data, "room.location", {"isEmpty": true})
                resolve()
            }
        });
    }

    static async typeSubmitHandler(data, dataKey, value){
        return 10
    }

    static async tutorSubmitHandler(data, dataKey, value){
        return 1
    }
}