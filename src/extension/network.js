import {getBackendUrl} from "./config";

const parseDataFromBackend = async (group_id) => {
    const url = getBackendUrl() + '/timetable/' + group_id
    return (await fetch(url)).json()
};

const saveTimeTableData = (group_id, data) => {
    localStorage.setItem(`${group_id}-timetable`, JSON.stringify(data));
};

const getTimeTableData = (group_id) => {
    return localStorage.getItem(`${group_id}-timetable`);
};

export const loadTimeTableData = async (group_id) => {
    const localData = getTimeTableData(group_id)
    if (localData) {
        console.log("Data available in local storage")
        return JSON.parse(localData);
    } else {
        const apiData = await parseDataFromBackend(group_id);

        if (!apiData["isSuccess"]) {
            throw new Error("Can`t load data from server.")
        }

        saveTimeTableData(group_id, apiData["result"]["cells"])
        return apiData;
    }
}