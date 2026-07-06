import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./components/Temp";
import Register from "./components/TempR";
import AccountList from "./components/AccountList";
import AccountForm from "./components/AccountForm";
import PrivateRoute from "./components/PrivateRoute";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />

                <Route path="/register" element={<Register />} />

                <Route
                    path="/accounts"
                    element={
                        <PrivateRoute>
                            <>
                                <AccountForm />
                                <AccountList />
                            </>
                        </PrivateRoute>
                    }
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;