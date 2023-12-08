import {ServerAgent} from "./ServerAgent";

export class Storage {
    #groupID;
    #key

    constructor(groupID) {
        this.#groupID = groupID;
        this.#key = `${this.#groupID}-timetable`;
    }

    #fetch = () => {
        return localStorage.getItem(this.#key);
    };

    store = (data) => {
        localStorage.setItem(this.#key, JSON.stringify(data));
    };

    async fetchTimeTableData() {
        const localData = this.#fetch();

        if (localData) {
            console.log("Data available in local storage");
            return JSON.parse(localData);
        }

        const res = await ServerAgent.fetchTimeTableData(this.#groupID);
        this.store(res)
        return JSON.parse(this.#fetch())
    }

    exportToBlob = () => {
        const data = this.#fetch();
        return new Blob([data], {type: 'application/json'});
    };

    importFromBlob = (blob) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                try {
                    const contentType = blob.type;
                    if (contentType === 'application/json') {
                        const data = JSON.parse(reader.result.toString());
                        this.store(data);
                        resolve(data);
                    } else {
                        reject(new Error('Invalid file format. Expected JSON file.'));
                    }
                } catch (error) {
                    reject(error);
                }
            };
            reader.readAsText(blob);
        });
    };
}
