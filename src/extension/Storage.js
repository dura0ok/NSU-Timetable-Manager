import {ServerAgent} from "./ServerAgent";
import {CELLS_KEY} from "./consts";

export class Storage {
    #groupID;
    #key

    constructor(groupID) {
        this.#groupID = groupID;
        this.#key = `${this.#groupID}-timetable`;
    }

    #fetch = () => {
        return JSON.parse(localStorage.getItem(this.#key));
    };

    restoreToDefaults = async () => {
        localStorage.removeItem(this.#key)
        await this.fetchTimeTableData()
    }

    store = (data) => {
        const curData = this.#fetch()
        if (curData) {
            curData[CELLS_KEY] = data
            localStorage.setItem(this.#key, JSON.stringify(curData));
            return
        }
        localStorage.setItem(this.#key, JSON.stringify(data))
    };

    clear = () => {
        try {
            const data = this.#fetch();

            data[CELLS_KEY].forEach(item => {
                item.subjects = [];
            });

            this.store(data[CELLS_KEY]);
        } catch (error) {
            console.error("An error occurred while clearing subjects:", error);
            // Handle the error as needed, e.g., log it, show a user-friendly message, etc.
        }
    }

    async fetchTimeTableData() {
        const localData = this.#fetch();
        if (localData) {
            return localData[CELLS_KEY];
        }

        const res = await ServerAgent.fetchTimeTableData(this.#groupID);
        this.store(res)
        return this.#fetch()[CELLS_KEY]
    }

    exportToBlob = () => {
        const data = JSON.stringify(this.#fetch());
        return new Blob([data], {type: 'application/json'});
    };

    importFromBlob = async (blob) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = async () => {
                try {
                    const contentType = blob.type;
                    if (contentType === 'application/json') {
                        const data = JSON.parse(reader.result.toString());
                        await this.restoreToDefaults();
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
