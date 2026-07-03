import { useState } from "react"

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault(); //normally the browser would auto reload but this allows us to apply our own custom react code to handle it

        const formData = new FormData();

        formData.append("username", username);
        formData.append("password", password);

        try {
            const response = await fetch('http://localhost:8000/login', {
                method: "POST",
                body: formData 
            }); // we don't need headers: {"Content-Type", "application/json"} The browser automatically sets the correct Content-Type for FormData.
            
            if (!response.ok) {
                throw new Error("Invalid username or password");
            }

            const data = await response.json();
            localStorage.setItem("token", data.access_token); //Now the browser stores it even if the page is refreshed. 

        } catch (error) {
            alert("Login failed. Please check your username and password")
            console.log(error)
        }

    }

    return (
    <form onSubmit={handleSubmit}>
        <h2>Login</h2>

        <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
        />

        <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
        />

        <button type="submit">
            Login
        </button>
    </form>
    );
}

export default Login