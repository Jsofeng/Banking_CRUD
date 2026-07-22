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


        const mockOnEdit = vi.fn();


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


        render(
            <AccountCard
                account={mockAccount}
                onEdit={mockOnEdit}
                onDelete={vi.fn()}
            />
        );


        await user.click(
            screen.getByRole("button", { name: "Edit" })
        );


        const ownerInput = screen.getByDisplayValue("Jonathan");


        await user.clear(ownerInput);
        await user.type(ownerInput, "Alex");


        await user.click(
            screen.getByRole("button", { name: "Save" })
        );


        expect(globalThis.fetch).toHaveBeenCalledWith(
            expect.any(String),
            expect.objectContaining({
                method: "PUT"
            })
        );


        expect(mockOnEdit).toHaveBeenCalledWith(
            expect.objectContaining({
                owner_name: "Alex"
            })
        );

    });

});