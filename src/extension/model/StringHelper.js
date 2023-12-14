export class StringHelper {
    static concatHostPath = (host, path) => {
        // Remove trailing slash from host and leading slash from path to avoid double slashes
        const cleanedHost = host.replace(/\/$/, '');
        const cleanedPath = path.replace(/^\//, '');

        // Concatenate host and path with a slash in between
        return `${cleanedHost}/${cleanedPath}`;
    }

    static getGroupNumberFromURL = () => {
        return new URL(window.location.href).pathname.split("/")[2];
    }
}
