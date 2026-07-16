import { render, screen } from "@testing-library/react";
import { describe, test, expect } from "vitest";
import AccountForm from "./AccountForm";

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