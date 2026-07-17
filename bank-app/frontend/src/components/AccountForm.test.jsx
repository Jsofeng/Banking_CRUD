import { render, screen } from "@testing-library/react";
import { describe, test, expect } from "vitest";
import AccountForm from "./AccountForm";
import { vi } from "vitest";
import userEvent from "@testing-library/user-event";
import AccountList from "./AccountList"
import { MemoryRouter } from "react-router-dom";

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

// Test that submitting the form sends a POST request
test("submits account data", async () => {

  // Creates a simulated user that can type, click, and interact with the page
  const user = userEvent.setup();

  // Replace the real fetch() with a fake function (mock).
  // This prevents an actual HTTP request from being sent.
  globalThis.fetch = vi.fn(() =>

    // Pretend the API responded successfully.
    Promise.resolve({

      // Simulate fetch's Response.ok property
      ok: true,

      // Simulate response.json()
      json: () =>
        Promise.resolve({

          // Fake JSON returned by the backend
          id: 1,
          owner_name: "Jonathan",
          balance: 1000,
          account_type: "chequing",
        }),
    })
  );

  // Render the AccountForm component into the virtual DOM
  render(<AccountForm />);

  // Find the Owner Name input and simulate typing "Jonathan"
  await user.type(
    screen.getByPlaceholderText("Owner Name"),
    "Jonathan"
  );

  // Find the dropdown (<select>) and choose "chequing"
  await user.selectOptions(
    screen.getByRole("combobox"),
    "chequing"
  );

  // Find the Balance input and type 1000
  await user.type(
    screen.getByPlaceholderText("Balance"),
    "1000"
  );

  // Find the Create Account button and simulate clicking it.
  // This should trigger your handleSubmit() function.
  await user.click(
    screen.getByRole("button", { name: "Create Account" })
  );

  // Verify that fetch() was called at least once.
  // If this fails, your form never attempted to contact the backend.
  expect(globalThis.fetch).toHaveBeenCalled();

  // Verify fetch() was called correctly.
  expect(globalThis.fetch).toHaveBeenCalledWith(

    // We don't care exactly what URL was used.
    // It just has to be some string.
    expect.any(String),

    // Check only part of the options object.
    expect.objectContaining({

      // Make sure the request method is POST.
      method: "POST",
    })
  );
});

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