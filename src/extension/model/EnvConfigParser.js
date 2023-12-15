export class EnvConfigParser {
    static #getURL(envVariableName) {
        const envValue = process.env[envVariableName];
        if (envValue === undefined) {
            throw new Error(`${envVariableName} is not defined in env`);
        }
        return new URL(envValue);
    }

    static parseNsuTableURL = () => {
        return EnvConfigParser.#getURL("NSU_TABLE_URL");
    }

    static parseBackendURL = () => {
        return EnvConfigParser.#getURL("BACKEND_SERVER_URL");
    }
}

