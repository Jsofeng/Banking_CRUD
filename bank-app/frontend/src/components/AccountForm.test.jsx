import { render, screen } from "@testing-library/react";
import { describe, test, expect } from "vitest";
import AccountForm from "./AccountForm";
import { vi } from "vitest";
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

//test form submission
test("submits account data", async () => {

  const user = userEvent.setup();

  globalThis.fetch = vi.fn(() =>
    Promise.resolve({
      ok: true,
      json: () =>
        Promise.resolve({
          id: 1,
          owner_name: "Jonathan",
          balance: 1000,
          account_type: "chequing",
        }),
    })
  );

  render(<AccountForm />);

  await user.type(
    screen.getByPlaceholderText("Owner Name"),
    "Jonathan"
  );
  
  await user.selectOptions(
    screen.getByRole("combobox"),
    "chequing"
  );

  await user.type(
    screen.getByPlaceholderText("Balance"),
    "1000"
  );

  await user.click(
    screen.getByRole("button", { name: "Create Account" })
  );

  expect(globalThis.fetch).toHaveBeenCalled();
  expect(globalThis.fetch).toHaveBeenCalledWith(
    expect.any(String),
    expect.objectContaining({
      method: "POST",
    })
  );
});