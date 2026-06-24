/* { account } is a parameter & which receives ONE Account Object from its parent*/

function AccountCard({ account, onDelete }) {

   const handleEdit = async () => {
    const newBalance = prompt("Enter new balance:");
    /* converts newBalance to int -> json string -> backend -> pydantic converts json string to int -> postgres table
        async allows you to compute other stuff and then when that part of the code is finished computing come back to it 
    */
    await fetch(`http://localhost:8000/accounts/${account.id}`, {
        method: "PUT",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify({
        balance: Number(newBalance),
        }),
    });
    };


  const handleDelete = async () => {
    await fetch(`http://localhost:8000/accounts/${account.id}`, {
      method: "DELETE",
    });

    onDelete(account.id);
  };


  return (
    <div style={{ border: "1px solid black", padding: "10px", margin: "10px" }}>
      <h3>{account.owner_name}</h3>
      <p>Type: {account.account_type}</p>
      <p>Balance: ${account.balance}</p>

     
      <button onClick={handleDelete}>Delete Account</button>
      <button onClick={handleEdit}>Update Balance</button>
    </div>
  );
}

export default AccountCard;