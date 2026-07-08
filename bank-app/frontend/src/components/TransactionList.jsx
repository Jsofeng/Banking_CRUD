import { useEffect, useState } from "react";
import { authFetch } from "../utils/authFetch";

function TransactionList({ accountId }) {
    const [transactions, setTransactions] = useState([]);
    
    useEffect(() => {
        authFetch(`http://localhost:8000/accounts/${accountId}/transaction`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch transactions");
                }
                return response.json();
            })
            .then((data) => setTransactions(data))
            .catch((error) => console.error(error));
    }, [accountId]);
    
    return (
        <div>
            <h4>Transaction History</h4>
            {transactions.length === 0 ? (
                <p>No transactions yet.</p>
            ) : (
                <ul>
                    {transactions.map((transaction) => (
                        <li key={transaction.id}>
                            <strong>{transaction.transaction_type}</strong> — $
                            {transaction.amount} <br />
                            <small>
                                {new Date(transaction.created_at).toLocaleString()}
                            </small>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default TransactionList;