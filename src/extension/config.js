export class EnvURLExtractor {
    static #getURL(envVariableName) {
        const envValue = process.env[envVariableName];
        if (envValue === undefined) {
            throw new Error(`${envVariableName} is not defined in env`);
        }
        return new URL(envValue);
    }

    static parseNsuTableURL = () => {
        return EnvURLExtractor.#getURL("NSU_TABLE_URL");
    }

    static parseBackendURL = () => {
        return EnvURLExtractor.#getURL("BACKEND_SERVER_URL");
    }
}

