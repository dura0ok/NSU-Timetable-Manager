export const getNsuTableUrl = () => {
    const envTableUrl = process.env.NSU_TABLE_URL
    if (envTableUrl === undefined) {
        throw new Error("NSU_TABLE_URL is not defined in env")
    }
    return new URL(envTableUrl)
}

export const getBackendUrl = () => {
    const envBackendUrl = process.env.BACKEND_SERVER_URL
    if (envBackendUrl === undefined) {
        throw new Error("BACKEND_SERVER_URL is not defined in env")
    }
    return new URL(envBackendUrl)
}