import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./components/login";
import Register from "./components/register";
import AccountList from "./components/AccountList";
import AccountForm from "./components/AccountForm";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />

                <Route path="/register" element={<Register />} />

                <Route
                    path="/accounts"
                    element={
                        <>
                            <AccountForm />
                            <AccountList />
                        </>
                    }
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;