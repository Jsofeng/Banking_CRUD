import { describe, test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";
import AccountList from "./AccountList";

//test AccountList renders accounts
describe("AccountList", () => {
    test("renders accounts after loading", async () => {

        globalThis.fetch = vi.fn(() => 
            Promise.resolve({
                ok: true,
                json: () => //create two accounts
                    Promise.resolve([
                        {
                            id: 1,
                            owner_name: "Jonathan",
                            balance: 1000,
                            account_type: "chequing",
                        },
                        {
                            id: 2,
                            owner_name: "Bob",
                            balance: 2500,
                            account_type: "savings",
                        },
                    ]),
            })
        
        );
        // Render the component
        /* Normally your app looks like
            <BrowserRouter>
                <App />
            </BrowserRouter>
        */
        // MemoryRouter is a lightweight router made specifically for tests.
        render(
        <MemoryRouter>
            <AccountList />
        </MemoryRouter>
        );

        //ensure both account names appear on the screen after component loads
        expect(await screen.findByText("Jonathan")).toBeInTheDocument();
        expect(await screen.findByText("Bob")).toBeInTheDocument();

        // Optional: verify fetch was actually called
        expect(globalThis.fetch).toHaveBeenCalled(1)
    })
})