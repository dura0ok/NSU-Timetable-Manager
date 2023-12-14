import {DotNotationHelper} from "./DotNotationHelper";
import {IS_EMPTY_FLAG} from "./consts";
import {ServerAgent} from "./ServerAgent";

export class SubmitHandler {

    static roomSubmitHandler(data, dataKey, value) {
        return new Promise(async (resolve) => {
            try {
                DotNotationHelper.setValueByDotNotation(data, dataKey, value)
                const r = await ServerAgent.getRoom(value)
                DotNotationHelper.setValueByDotNotation(data, "room.location", r["location"])
                resolve()
            } catch (error) {
                DotNotationHelper.setValueByDotNotation(data, "room.name", value)
                console.log(IS_EMPTY_FLAG)
                DotNotationHelper.setValueByDotNotation(data, "room.location", {[IS_EMPTY_FLAG]: true});
                resolve()
            }
        });
    }

    static async typeSubmitHandler(data, dataKey, value) {
        return new Promise(async (resolve) => {
            DotNotationHelper.setValueByDotNotation(data, dataKey, value)
            resolve()
        })
    }

    static async tutorSubmitHandler(data, dataKey, value) {
        return new Promise(async (resolve) => {
            try {
                const r = await ServerAgent.getTutor(value)
                //debugger;
                DotNotationHelper.setValueByDotNotation(data, dataKey, r["name"])
                DotNotationHelper.setValueByDotNotation(data, "tutor.href", r["href"])
                resolve()
            } catch (error) {
                DotNotationHelper.setValueByDotNotation(data, "tutor.name", value)
                DotNotationHelper.setValueByDotNotation(data, "tutor.href", "#")
                resolve()
            }
        });
    }
}