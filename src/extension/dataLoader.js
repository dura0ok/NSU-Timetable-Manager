export const NSU_TABLE_URL = new URL("https://table.nsu.ru/")
const BACKEND_SERVER_URL = "http://127.0.0.1:5000/"

export const getRawData = async (group_id) => {
    //const url = 'http://127.0.0.1:5000/timetable/21203';
    const url = BACKEND_SERVER_URL + '/timetable/' + group_id

    try {
        const response = await fetch(url);
        const json = await response.json();

        return {ok: true, data: json.result};
    } catch (error) {
        return {ok: false, error};
    }
};

export const getRoom = async (fio) => {
    const encoded = encodeURI(fio)
    const url = BACKEND_SERVER_URL + '/room/' + encoded
    try {
        const response = await fetch(url);
        const json = await response.json();

        return {ok: true, data: json.result};
    } catch (error) {
        return {ok: false, error};
    }
}

export const getTutor = async (room_name) => {
    const encoded = encodeURI(room_name)
    const url = BACKEND_SERVER_URL + '/tutor/' + encoded
    try {
        const response = await fetch(url);
        const json = await response.json();

        return {ok: true, data: json.result};
    } catch (error) {
        return {ok: false, error};
    }
}

export const saveApiData = (apiData) => {
    localStorage.setItem('data', JSON.stringify(apiData));
}

export const loadApiData = async (group_id) => {
    const rawData = localStorage.getItem('data');
    if (rawData) {
        console.log("Data available in local storage")
        return JSON.parse(rawData);
    } else {
        // If data is not available in local storage, fetch it from the API
        const apiData = await getRawData(group_id);
        console.log("Raw data from server: ", JSON.stringify(apiData))
        const data = apiData.data
        saveApiData(data)

        return data;
    }
};
