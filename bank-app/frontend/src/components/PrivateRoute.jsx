import { Navigate } from "react-router-dom";

function PrivateRoute({ children }) {
    const token = localStorage.getItem("token");

    if (!token) {
        return <Navigate to="/login" replace />; //React Router immediately redirects to /login.
    }
    return children;
}

export default PrivateRoute;