import { render, screen } from "@testing-library/react";
import { describe, test, expect } from "vitest";
import AccountForm from "./AccountForm";
import userEvent from "@testing-library/user-event";

describe("AccountForm", () => {
    test("render account form inputs", () => {

        render(<AccountForm />);
        
        expect(
            screen.getByPlaceholderText("Owner Name") // MUST MATCH AccountForm.jsx "placeholder"
        ).toBeInTheDocument();

        expect(
            screen.getByPlaceholderText("Balance")
        ).toBeInTheDocument();

        expect(
            screen.getByRole("combobox")
        ).toBeInTheDocument();

        expect(
            screen.getByRole("button", { name: "Create Account" })
        ).toBeInTheDocument();
    });
});

//simulates real user typing into owner name field
test("updates owner name input", async () => {
    render(<AccountForm />);

    const user = userEvent.setup();
    const ownerInput = screen.getByPlaceholderText("Owner Name");

    await user.type(ownerInput, "Joe");
    expect(ownerInput).toHaveValue("Joe");

});
