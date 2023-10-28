export const getRawData = async () => {
    const url = 'http://127.0.0.1:5000/timetable/21203';

    try {
        const response = await fetch(url);
        const json = await response.json();

        return { ok: true, data: json.result };
    } catch (error) {
        return { ok: false, error };
    }
};

export const saveApiData = (apiData) => {
    localStorage.setItem('data', JSON.stringify(apiData));
}

export const loadApiData = async () => {
    const rawData = localStorage.getItem('data');
    if (rawData) {
        console.log("Data available in local storage")
        return JSON.parse(rawData);
    } else {
        // If data is not available in local storage, fetch it from the API
        const apiData = await getRawData();
        const data = apiData.data
        saveApiData(apiData)

        return data;
    }
};
