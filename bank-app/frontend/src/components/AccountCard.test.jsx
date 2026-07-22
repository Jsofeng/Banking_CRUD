import { describe, test, expect, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/react";
import AccountCard from "./AccountCard";


describe("AccountCard", () => {

    test("updates account information", async () => {

        const user = userEvent.setup();

        const mockAccount = {
            id: 1,
            owner_name: "Jonathan",
            account_type: "chequing",
            balance: 1000,
            frozen: false
        };


        const mockOnEdit = vi.fn(); //“Create a function that remembers when it gets called.”


        //fake fetch(PUT /accounts/1)
        globalThis.fetch = vi.fn(() =>
            Promise.resolve({
                ok: true,
                json: () =>
                    Promise.resolve({
                        id: 1,
                        owner_name: "Alex",
                        account_type: "savings",
                        balance: 1000,
                        frozen: false
                    })
            })
        );

        /*
        CREATES

        <AccountCard
            account={
                {
                owner_name:"Jonathan"
                }
            }
        />
        */
        render(
            <AccountCard
                account={mockAccount}
                onEdit={mockOnEdit}
                onDelete={vi.fn()}
            />
        );

        // user click edit button
        await user.click(
            screen.getByRole("button", { name: "Edit" })
        );

        //before clicking -> Jonathan -> after clicking -> <input value="Jonathan"/> since component does setEditing(true)
        //then looks for <input value="Jonathan"/> and stores it 
        const ownerInput = screen.getByDisplayValue("Jonathan");

        // <input value= ""> -> <input value="Alex"
        await user.clear(ownerInput);
        await user.type(ownerInput, "Alex");

        //Runs handleUpdate() & sends fetch to that endpoint 
        await user.click(
            screen.getByRole("button", { name: "Save" })
        );

        /* 

        Verifies this happened
        fetch(
            "/accounts/1",
            {
                method:"PUT"
            }
            )
        
        */
        expect(globalThis.fetch).toHaveBeenCalledWith(
            expect.any(String),
            expect.objectContaining({
                method: "PUT"
            })
        );

        //checks if the component called onEdit(updatedAccount) aka onEdit(mockOnEdit)
        expect(mockOnEdit).toHaveBeenCalledWith(
            expect.objectContaining({
                owner_name: "Alex"
            })
        );

    });

});