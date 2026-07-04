export function authFetch(url, options = {}) {
    const token = localStorage.getItem("token");

    const isFormData = options.body instanceof FormData;

    return fetch(url, {
        ...options,
        headers: {
            ...(isFormData ? {} : { 
                "Content-Type": "application/json" }
            ),
            Authorization: token ? `Bearer ${token}` : "",
            ...options.headers,
        },
    });
}

/*
Login → store token
authFetch → auto-attaches token everywhere
*/
