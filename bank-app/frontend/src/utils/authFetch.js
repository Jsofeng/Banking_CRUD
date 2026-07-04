export function authFetch(url, options = {}) {
    const token = localStorage.getItem("token");

    const isFormData = options.body instanceof FormData;

    //auto fetches the url with added Authorization 

    /*
    Without authFetch:

    You must tell the restaurant every time:

    “Here is my name, my ID, and my payment info”

    With authFetch:

    You give the waiter your “membership card” once, and they handle it for every order.
    */
    
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
