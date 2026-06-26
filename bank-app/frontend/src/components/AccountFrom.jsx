import { useState } from "react";

function AccountForm() {
  const [ownerName, setOwnerName] = useState(""); /* owner_name = current value, setOwnerName = function to change value, useState starts off as an empty string*/
  const [accountType, setAccountType] = useState("chequing");
  const [balance, setBalance] = useState(0);

  /* when user clicks button */
  const handleSubmit = async (e) => {
    e.preventDefault();

    /* react uses camelCase & python uses snake_case */ 
    const newAccount = {
      owner_name: ownerName,
      account_type: accountType,
      balance: Number(balance),
    };

    try {
        const response = await fetch("http://localhost:8000/accounts", 
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newAccount),
            }
        );
        
        if (!response.ok) {
            throw new Error("Failed to create account");
        }
        
        const data = await response.json();
        console.log(data);
    
    } catch (error) {
        alert("Something went wrong while creating the account.");
        console.error(error);
    }
    };


  return (
    <form onSubmit={handleSubmit}>
      <h2>Create Account</h2>

      <input
        type="text"
        value={ownerName}
        onChange={(e) => setOwnerName(e.target.value)}
        placeholder="Owner Name"
      />
    
      <select
        value={accountType}
        onChange={(e) => setAccountType(e.target.value)}
      >
        <option value="chequing">Chequing</option> 
        <option value="savings">Savings</option>
      </select>

      <input
        type="number"
        value={balance}
        onChange={(e) => setBalance(e.target.value)}
        placeholder="Balance"
      />

      <button type="submit">Create Account</button>
    </form>
  );
}

export default AccountForm;