import { useState, useEffect } from "react";
import AccountCard from "./AccountCard";
import { authFetch } from "../utils/authFetch";
import Logout from "./Logout";
import { API_URL } from "../config";

function AccountList() {
    const [accounts, setAccounts] = useState([]);
    
    // 1. Fetch data when component loads
    // can only use then when it's not async/await fetch
    // what you receive after fetching take response.json -> put that data into setAccounts 
    useEffect(() => {
        authFetch(`${API_URL}/accounts`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to fetch accounts");
                }
                return response.json()
            }) // Convert JSON text → JavaScript objects

            .then(data => setAccounts(data))   // Store the accounts in state
            .catch(error => console.error(error)); 
    }, []);

    // 2. Delete handler updates accountlist UI in frontend by removing that specific account then deletes it from the database

    const handleDelete = (id) => {
        setAccounts(accounts.filter((acc) => acc.id !== id));
    };

    // Searches the accounts hashmap Find the account that was edited, replace it with the new version, keep everything else the same.
    const handleEdit = (updatedAccount) => {
    setAccounts(prevAccounts =>
        prevAccounts.map(acc =>
            acc.id === updatedAccount.id
                ? updatedAccount
                : acc
            )
        );
    };

    return (
    <div>
        <div style={{ display: "flex", justifyContent: "space-between" }}>
            <h2>All Accounts</h2>
            <Logout />
        </div>
        {accounts.map((account) => (
            <AccountCard
                key={account.id}
                account={account}
                onDelete={handleDelete}
                onEdit={handleEdit}
            />
        ))}
    </div>
);
}

export default AccountList