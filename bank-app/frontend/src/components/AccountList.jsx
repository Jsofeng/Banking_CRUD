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

    const handleDeposit = (transaction) => {
        setAccounts(prevAccounts =>
            prevAccounts.map(acc =>
                acc.id === transaction.account_id
                    ? {
                        ...acc,
                        balance: transaction.balance_after
                    }
                    : acc
            )
        );
    };

    /*
    "When a withdrawal succeeds, look through all my accounts. Find the account that the transaction belongs to. 
    Make a copy of that account, replace its balance with the backend's balance_after, and leave every other account unchanged."
    - RETRIEVES INFO FROM BACKEND CALL FROM ACCOUNTCARD & USES THAT INFO TO UPDATE ACCOUNT
    */
    const handleWithdrawal = (transaction) => {
        setAccounts(prevAccounts =>
            prevAccounts.map(acc =>
                acc.id === transaction.account_id
                    ? {
                        ...acc,
                        balance: transaction.balance_after
                    }
                    : acc
            )
        );
    };

    const handleTransfer = (transactions) => {
    setAccounts(prevAccounts =>
        prevAccounts.map(acc => {
            const transaction = transactions.find(
                transaction => transaction.account_id === acc.id
            );

            return transaction
                ? {
                    ...acc,
                    balance: transaction.balance_after
                }
                : acc;
            })
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
                onDeposit={handleDeposit}
                onWithdrawal={handleWithdrawal}
                onTransfer={handleTransfer}
            />
        ))}
    </div>
);
}

export default AccountList