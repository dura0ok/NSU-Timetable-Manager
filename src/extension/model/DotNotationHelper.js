export class DotNotationHelper {
    static getValueByDotNotation(obj, key) {
        const keys = key.split('.');
        let value = obj;
        for (const key of keys) {
            if (value && value.hasOwnProperty(key)) {
                value = value[key];
            } else {
                return null;
            }
        }
        return value;
    }

    static setValueByDotNotation(obj, key, value) {
        const keys = key.split('.');
        let currentObj = obj;
        for (let i = 0; i < keys.length - 1; i++) {
            const currentKey = keys[i];
            if (!currentObj[currentKey]) {
                currentObj[currentKey] = {};
            }
            currentObj = currentObj[currentKey];
        }
        currentObj[keys[keys.length - 1]] = value;
    }
}