import { useState } from "react";
import { authFetch } from "../utils/authFetch";

function AccountForm() {
  const [ownerName, setOwnerName] = useState(""); /* owner_name = current value, setOwnerName = function to change value, useState starts off as an empty string*/
  const [accountType, setAccountType] = useState("chequing");
  const [balance, setBalance] = useState("");
  const [error, setError] = useState("");

  /* when user clicks button */
  const handleSubmit = async (e) => {
    e.preventDefault();

    if(ownerName.trim() === "") {
        setError("Owner name cannot be empty");
        return;
    }

    if (Number(balance) < 0) {
        setError("Balance cannot be negative");
        return;
    }

    setError(""); //clear error if valid

    /* react uses camelCase & python uses snake_case */ 
    const newAccount = {
      owner_name: ownerName,
      account_type: accountType,
      balance: Number(balance),
    };

    try {
        const response = await authFetch("http://localhost:8000/accounts", 
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

        setOwnerName("");
        setAccountType("chequing");
        setBalance("");
    
    } catch (error) {
        alert("Something went wrong while creating the account.");
        console.error(error);
    }
    };


  return (
    <form onSubmit={handleSubmit}>
      <h2>Create Account</h2>
      
      {error && <p className="error">{error}</p>}
      
      <input
        type="text"
        value={ownerName}
        onChange={(e) => setOwnerName(e.target.value)}
        placeholder="Owner Name"
      />
    
      <select
        value={accountType}
        onChange={(e) => setAccountType(e.target.value)} // accountType is the selected Value to be changed (when the user chooses either accountType onChange it will set accountType to that)
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