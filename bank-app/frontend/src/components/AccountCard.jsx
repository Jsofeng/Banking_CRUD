/* { account } is a parameter & which receives ONE Account Object from its parent*/
import { useState } from "react";
import { authFetch } from "../utils/authFetch";

function AccountCard({ account, onDelete, onEdit }) {
   const [amount, setAmount] = useState("");
   const [type, setType] = useState("deposit");

   //above -> only use const [..., ...] = useState() when user is interacting with it (input fields, dropdowns checkboxes, temporary UI changes)
   // DO NOT USE IT when the backend owns it (e.g account.frozen, account.balance, account.account_type)
   const handleTransaction = async () => {
    try {
        if (!amount) return;
        /* converts newBalance to int -> json string -> backend -> pydantic converts json string to int -> postgres table
            async allows you to compute other stuff and then when that part of the code is finished computing come back to it 
        */
    
        const response = await authFetch(`http://localhost:8000/accounts/${account.id}/transaction`, 
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    amount: Number(amount),
                    transaction_type: type,
                }),
            }    
        );
    
        if (!response.ok) {
            throw new Error("Transaction Failed");
        }

        const updatedAccount = await response.json();
        // <Account onEdit={handleEdit} />
        // calls parent class (AccountList) and says “Hey parent component, here is the latest version of the account. Update yourself.”
        onEdit(updatedAccount); 
        
        setAmount("");

    } catch (error) {
        alert("Transaction Failed. Try again.");
        console.error(error);
    }

    };
    //toggle button so that if your account is frozen then you can only unfreeze it vice versa
    const handleFreeze = async () => {
        try {
            const response = await authFetch(
                `http://localhost:8000/accounts/${account.id}/set_freeze`, {
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

    // not using async here bc backend delete endpoint returns json so response.json() can read it 
    
    const handleDelete = async () => {
        try {
            const response = await authFetch(
                `http://localhost:8000/accounts/${account.id}`, 
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
            <h3>{account.owner_name}</h3>
            <p className={account.account_type}>
                Type: {account.account_type}
            </p>
            <p>Balance: ${account.balance}</p>
            {/* Transaction UI */}
            <input
                type="number"
                placeholder="Amount"
                value={amount}
                onChange={(e) => setAmount(e.target.value)} //when user types in the box amount=setAmount(e.target.value)
            />
            <select
                value={type}
                onChange={(e) => setType(e.target.value)} // GRAB transaction_type FIRST then onClick={handelTransaction} connects to backend with choice
            >
                <option value="deposit">Deposit</option>
                <option value="withdrawal">Withdraw</option>
            </select>
            <button onClick={handleTransaction}> 
                Submit Transaction 
            </button>
            <button onClick={handleFreeze}>{account.frozen ? "Unfreeze Account" : "Freeze"}</button>
            <button onClick={handleDelete}>
                Delete Account
            </button>
        </div>
    );
}

export default AccountCard;