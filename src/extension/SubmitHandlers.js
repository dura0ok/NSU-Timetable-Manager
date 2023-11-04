import {ObjectHelper} from "./ObjectHelper";
import {EnvConfigParser} from "./EnvConfigParser";

export class SubmitHandlers {
    static async fetchData(endpoint, room_name) {
        const encoded = encodeURI(room_name);
        const url = EnvConfigParser.parseBackendURL() + '/' + endpoint + '/' + encoded;
        const response = await fetch(url);
        const json = await response.json();
        if (!json["isSuccess"]) {
            throw new Error(`${endpoint} not found`);
        }
        return json.result;
    }

    static async #getRoom(roomName) {
        return this.fetchData('room', roomName);
    }

    static async #getTutor(tutorName) {
        return this.fetchData('tutor', tutorName);
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
        return new Promise(async (resolve, reject) => {
            ObjectHelper.setValueByDotNotation(data, dataKey, value)
            resolve()
        })
    }

    static async tutorSubmitHandler(data, dataKey, value){
        return new Promise(async (resolve, reject) => {
            try{
                const r = await SubmitHandlers.#getTutor(value)
                console.log(r)
                ObjectHelper.setValueByDotNotation(data, dataKey, r["name"])
                ObjectHelper.setValueByDotNotation(data, "tutor.href", r["href"])
                resolve()
            }catch (error){
                ObjectHelper.setValueByDotNotation(data, "tutor.href", "#")
                resolve()
            }
        });
    }
}