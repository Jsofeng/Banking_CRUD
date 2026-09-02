/* { account } is a parameter & which receives ONE Account Object from its parent*/
import { useState } from "react";
import { authFetch } from "../utils/authFetch";
import TransactionList from "./TransactionList";
import { API_URL } from "../config";

function AccountCard({ account, onDelete, onEdit, onDeposit, onWithdrawal, onTransfer}) {
   const [editing, setEditing] = useState(false);

   const [ownerName, setOwnerName] = useState(account.owner_name);
   const [accountType, setAccountType] = useState(account.account_type);
   const [recipientAccounts, setRecipientAccounts] = useState([]);
   const [selectedAccount, setSelectedAccount] = useState("");
   const [toEmail, setToEmail] = useState("")

   const [amount, setAmount] = useState("");
   const [showTransactions, setShowTransactions] = useState(false);
   const [showTransfer, setShowTransfer] = useState(false);

   //above -> only use const [..., ...] = useState() when user is interacting with it (input fields, dropdowns checkboxes, temporary UI changes)
   // DO NOT USE IT when the backend owns it (e.g account.frozen, account.balance, account.account_type)
   const handleDeposit = async () => {
    try {
        if (!amount) return;
        /* converts newBalance to int -> json string -> backend -> pydantic converts json string to int -> postgres table
            async allows you to compute other stuff and then when that part of the code is finished computing come back to it 
        */
        
        const idempotencyKey = crypto.randomUUID();

        const response = await authFetch(`${API_URL}/accounts/${account.id}/deposit`, 
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    amount: Number(amount),
                    idempotency_key : idempotencyKey
                }),
            }    
        );
    
        if (!response.ok) {
            throw new Error("Transaction Failed");
        }

        const transaction = await response.json();
        // <Account onEdit={handleEdit} />
        // calls parent class (AccountList) and says “Hey parent component, here is the latest version of the account. Update yourself.”
        onDeposit(transaction); 
        
        setAmount("");

    } catch (error) {
        alert("Transaction Failed. Try again.");
        console.error(error);
    }

    };

    const handleWithdrawal = async () => {
        try {

            const idempotencyKey = crypto.randomUUID()
            
            const response = await authFetch(
                `${API_URL}/accounts/${account.id}/withdrawal`, {
                    method : "PATCH",
                    headers : {
                        "Content-Type" : "application/json"
                    },
                    body : JSON.stringify({
                        amount : Number(amount),
                        idempotency_key: idempotencyKey
                    }),
                }
            )

            if (!response.ok) {
                throw new Error("Transaction Failed");
            }

            const transaction = await response.json();

            onWithdrawal(transaction);
            
            setAmount("")
        } catch (error) {
            alert("Transaction Failed. Try again.");
            console.error(error);
        }
    };
    
    const handleTransfer = async () => { //E-Transfer -> SHOW ACCOUNT'S USER NAMES INSTEAD OF account_type
        try {
            const idempotencyKey = crypto.randomUUID()

            const response = await authFetch(
                `${API_URL}/accounts/${account.id}/transfer`, {
                    method : "PATCH",
                    headers : {
                        "Content-Type" : "application/json"
                    },
                    body: JSON.stringify({
                        from_account: account.id,
                        to_account: selectedAccount,
                        amount: Number(amount),
                        idempotency_key: idempotencyKey
                    }),
                }
            );

            if (!response.ok) {
                throw new Error("Transaction Failed");
            }

            const transactions = await response.json();

            onTransfer(transactions);
            setRecipientAccounts([]);
            setSelectedAccount("");
            setAmount("");
            setShowTransfer(false);

        } catch (error) {
            alert("Transaction Failed. Try again");
            console.error("TRANSFER ERROR:", error);
        }
    };

    const findRecipient = async () => {
        try {
            const response = await authFetch(
                `${API_URL}/accounts/by-email/${encodeURIComponent(toEmail)}`
            );

            if (!response.ok) {
                throw new Error("Recipient not found");
            }

            const accounts = await response.json();

            setRecipientAccounts(accounts);
        } catch (error) {
            alert("Recipient not found");
            console.error(error);
        }
    };

    //toggle button so that if your account is frozen then you can only unfreeze it vice versa
    const handleFreeze = async () => {
        try {
            const response = await authFetch(
                `${API_URL}/accounts/${account.id}/set_freeze`, {
                    method : "PATCH",
                    headers : {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        freeze : !account.frozen
                    }),
                });

            if (!response.ok) {
                throw new Error("Failed to update freeze state");
            }

            const updatedAccount = await response.json();
            onEdit(updatedAccount);


        } catch (error) {
            console.error(error);
            alert("Could not update freeze state");
        }
    }

    const handleUpdate = async () => {
        try {
            const response = await authFetch(
                `${API_URL}/accounts/${account.id}`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        owner_name: ownerName,
                        account_type: accountType,
                    }),
                }
            );

            if (!response.ok) {
                const error = await response.json();
                console.log("Backend error:", error);
                throw new Error("Failed to update account");
            }

            const updatedAccount = await response.json();

            onEdit(updatedAccount);
            setEditing(false);

        } catch (error) {
            console.error(error);
            alert("Failed to update account");
        }
    };

    // not using async here bc backend delete endpoint returns json so response.json() can read it 
    
    const handleDelete = async () => {
        try {
            const response = await authFetch(
                `${API_URL}/accounts/${account.id}`, 
                {
                    method: "DELETE"
                }
            );

            if(!response.ok) {
                throw new Error("Failed to delete account");
            }
            
            const data = await response.json();
            console.log(data.message);

            onDelete(account.id); // connects to AccountList -> handleDelete

        } catch (error) {
            alert("Something went wrong while deleting the account.");
            console.error(error);
        }
        
    };


    return (
        <div className="card">
            {/* Owner Name */}
            {editing ? (
                <input
                    value={ownerName}
                    onChange={(e) => setOwnerName(e.target.value)}
                />
            ) : (
                <h3>{account.owner_name}</h3>
            )}

            {/* Account Type */}
            {editing ? (
                <select
                    value={accountType}
                    onChange={(e) => setAccountType(e.target.value)}
                >
                    <option value="chequing">Chequing</option>
                    <option value="savings">Savings</option>
                </select>
            ) : (
                <p className={account.account_type}>
                    Type: {account.account_type}
                </p>
            )}

            {/* Balance */}
            <p>Balance: ${account.balance}</p>


            {/* Transaction UI */}
            <input
                type="number"
                placeholder="Amount"
                value={amount}
                onChange={(e) => setAmount(e.target.value)} //when user types in the box amount=setAmount(e.target.value)
            />
 
            <button onClick={handleDeposit}>
                Deposit
            </button>
 
            <button onClick={handleWithdrawal}>
                Withdrawal
            </button>
            
            {showTransfer && ( // show this if showTransfer is true (when "E-transfer is pressed")
                <>
                    <input
                        type="email"
                        placeholder="Recipient email"
                        value={toEmail}
                        onChange={(e) => setToEmail(e.target.value)}
                    />

                    <button onClick={findRecipient}>
                        Find Recipient
                    </button>
                </>
            )}

            {recipientAccounts.length > 0 && (
                <select
                    value={selectedAccount}
                    onChange={(e) => setSelectedAccount(e.target.value)}
                >
                    <option value="">Select account</option>

                    {recipientAccounts.map((recipientAccount) => (
                        <option
                            key={recipientAccount.account_id}
                            value={recipientAccount.account_id}
                        >
                            {recipientAccount.account_type}
                        </option>
                    ))}
                </select>
            )}

            {showTransfer && (
                <input 
                    type="number"
                    placeholder="Amount"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                
                /> 
            )}

            <button onClick={() => setShowTransfer(true)}>
                E-transfer
            </button>

            {showTransfer && (
                <button onClick={handleTransfer}>
                    Send
                </button>
            )}

            <button onClick={() => setShowTransactions(!showTransactions)}>{showTransactions ? "Hide Transaction History" : "Transaction History"}</button> 
            <button onClick={handleFreeze}>{account.frozen ? "Unfreeze Account" : "Freeze"}</button>
            { editing ? (
                <>
                    <button onClick={handleUpdate}>
                        Save
                    </button>

                    <button onClick={() => setEditing(false)}>
                        Cancel
                    </button>
                </>
            ) : (
                <button onClick={() => setEditing(true)}>
                    Edit
                </button>
            )}
            <button onClick={handleDelete}>
                Delete Account
            </button>

            {showTransactions && (
                <TransactionList accountId={account.id} /> // “Only render <TransactionList /> if showTransactions is true.”
            )}

        </div>
    );
}

export default AccountCard;