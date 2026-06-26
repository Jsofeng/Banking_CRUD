import { useState, useEffect } from "react";
import AccountCard from "./AccountCard";


function AccountList() {
    const [accounts, setAccounts] = useState([]);
    
    // 1. Fetch data when component loads
    // what you receive after fetching take response.json -> put that data into setAccounts 
    useEffect(() => {
        fetch("http://localhost:8000/accounts")
            .then(response => response.json()) // Convert JSON text → JavaScript objects
            .then(data => setAccounts(data))   // Store the accounts in state
            .catch(error => console.error(error)); 
    }, []);

    // 2. Delete handler (remove from UI after backend delete)
    const handleDelete = (id) => {
        setAccounts(accounts.filter((acc) => acc.id !== id));
    };

    return (
        <div>
        <h2>All Accounts</h2>
        {accounts.map((account) => (
            <AccountCard
            key={account.id}
            account={account}
            onDelete={handleDelete}
            />
        ))}
        </div>
    );
}

export default AccountList