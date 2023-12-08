export const concatHostPath = (host, path) => {
    // Remove trailing slash from host and leading slash from path to avoid double slashes
    const cleanedHost = host.replace(/\/$/, '');
    const cleanedPath = path.replace(/^\//, '');

    // Concatenate host and path with a slash in between
    return `${cleanedHost}/${cleanedPath}`;
}

export const getGroupNumberFromURL = () => {
    return new URL(window.location.href).pathname.split("/")[2];
}

export const parseFunctionName = (s) => {
    const regex = /(\w+)\(/
    const matches = regex.exec(s)

    if (matches && matches.length > 1) {
        return matches[1].trim().toString()
    }

    return ""
}