export class FunctionParser {
    static parseFunctionName(s) {
        const regex = /(\w+)\(/;
        const matches = regex.exec(s);

        if (matches && matches.length > 1) {
            return matches[1].trim().toString();
        }

        return "";
    }
}