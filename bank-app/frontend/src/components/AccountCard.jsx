/* { account } is a parameter & which receives ONE Account Object from its parent*/

function AccountCard({ account, onDelete, onEdit }) {

   const handleEdit = async () => {
    try {
        const newBalance = prompt("Enter new balance:");
        /* converts newBalance to int -> json string -> backend -> pydantic converts json string to int -> postgres table
            async allows you to compute other stuff and then when that part of the code is finished computing come back to it 
        */

        if (!newBalance) return;
    
        const response = await fetch(`http://localhost:8000/accounts/${account.id}`, 
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                balance: Number(newBalance),
                }),
            }    
        );
    
        if (!response.ok) {
            throw new Error("Failed to update account");
        }

        const updatedAccount = await response.json();
        onEdit(updatedAccount);

    } catch (error) {
        alert("Could not update account. Try again.");
        console.error(error);
    }

    };

    // not using async here bc backend delete endpoint returns json so response.json() can read it 
    
    const handleDelete = async () => {
        try {
            const response = await fetch(
                `http://localhost:8000/accounts/${account.id}`, 
                {
                    method: "DELETE"
                }
            );

            if(!response.ok) {
                throw new Error("Failed to delete account");
            }
            
            const data = response.json();
            console.log(data.message);

            onDelete(account.id);

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
        <button onClick={handleDelete}>Delete Account</button>
        <button onClick={handleEdit}>Update Balance</button>
    </div>
   );
}

export default AccountCard;