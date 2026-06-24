import { useState, useEffect } from "react";
import AccountCard from "./AccountCard";


function AccountList() {
    const [accounts, setAccounts] = useState([]);
    
    // 1. Fetch data when component loads
    useEffect(() => {
        const fetchAccounts = async () => {
        const response = await fetch("http://localhost:8000/accounts"); /* what you receive */
        const data = await response.json(); /* what you input Convert backend response → JavaScript array */
        setAccounts(data); // same accounts get store in setAccounts now

        };
        
        fetchAccounts(); 
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