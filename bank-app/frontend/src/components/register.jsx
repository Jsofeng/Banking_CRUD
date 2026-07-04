import { useState } from "react";

function Register() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault()
        
        if (username.trim() == "") {
            setError("Username cannot be empty");
            return;
        }

        if (email.trim() == "") {
            setError("Email cannot be empty");
            return;
        }

        if (password.trim() == "") {
            setError("Password cannot be empty");
            return;
        }

        setError("");
        
        const newUser = {
            username,
            email,
            password,
        };

        try {
            const response = await fetch("http://localhost:8000/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newUser),
            });
            
            if (!response.ok) {
                throw new Error("Invalid Username or Password")
            }

            const data = await response.json()
            console.log(data)

            alert("Registration successful! Please log in.");

            setUsername("");
            setEmail("");
            setPassword("");

        } catch (error) {
            setError("Registration failed.");
            console.error(error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Register</h2>

            {error && <p className="error">{error}</p>}

            <input 
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />

            <input 
                type="text"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
    
            <input 
                type="text"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <button type="submit">
                Register
            </button>
        </form>
    );
}

export default Register;