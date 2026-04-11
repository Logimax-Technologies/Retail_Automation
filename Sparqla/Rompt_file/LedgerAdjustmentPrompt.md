# Ledger Adjustment Module Automation

Build the **Ledger Adjustment** automation for the Retail Automation project.
Follow the standard pattern used in `BillSplit.py` and `BillingDenomination.py`.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_Bill\LedgerAdjustment.py
```

## Update main.py
Add `LedgerAdjustment` to the module dispatcher.

---

## Controller & View Logic
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
**Controller**: `Admin_ret_billing`  
**Function**: `bank_ledger_transfer($type = 'list')`  
**View**: `billing/ledger_transfer_form` (Add) / `billing/ledger_transfer_list` (List)

**AJAX Modes (handled in controller):**
- `get_ledgers`: Loads all ledger accounts into Select2.
- `get_balance`: Fetches `bal_amount` based on selected `from_ledger`.
- `transfer`: Processes the save operation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 

## Navigation
- **Menu**: Billing → Ledger Adjustment (or direct URL)
- **Add URL**: `admin_ret_billing/bank_ledger_transfer/add`
- **List URL**: `admin_ret_billing/bank_ledger_transfer/list`

---

## Form Fields & IDs

### 1. Mode Selection (Toggle Buttons)
- **Ledger Transfer**: `id="btn_mode_transfer"` (Value: 1)
- **Manual Credit/Debit**: `id="btn_mode_manual"` (Value: 2)

### 2. Form Fields
- ✅ **From Ledger** (Select2): `id="from_ledger"`, `name="from_ledger"`  
  *(Note: After selecting From Ledger, wait for `id="bal_amount"` to update)*
- ✅ **Current Balance** (Readonly): `id="bal_amount"`
- ✅ **To Ledger** (Select2): `id="to_ledger"`, `name="to_ledger"`  
  *(Visible only if Mode = Ledger Transfer)*
- ✅ **Transaction Type** (Select): `id="transaction_type"`, `name="transaction_type"`  
  *(Visible only if Mode = Manual Credit/Debit. Options: 1=Credit, 2=Debit)*
- ✅ **Amount** (Input): `id="amount"`, `name="amount"`
- ✅ **Narration** (Textarea): `id="narration"`, `name="narration"`

### 3. Action Buttons
- ✅ **Submit**: `id="submit_transfer"`
- ✅ **Cancel**: `class="btn-danger"` (Goes back to list)

---

## Business Logic & Validations

1. **Balance Check**:
   - For **Ledger Transfer**: Amount cannot exceed `bal_amount`.
   - For **Manual Debit**: Amount cannot exceed `bal_amount`.
   - For **Manual Credit**: No balance check needed.
2. **AJAX Loading**:
   - Selecting `from_ledger` triggers a call to fetch balance. The automation must wait for the field to be populated.
3. **UI Toggles**:
   - Clicking "Manual Credit/Debit" should hide "To Ledger" and show "Transaction Type".
   - Clicking "Ledger Transfer" should show "To Ledger" and hide "Transaction Type".

---

## Test Scenarios

### Scenario 1: Successful Ledger Transfer
1. Navigate to Add page.
2. Select "Ledger Transfer" mode (default).
3. Select **From Ledger** (e.g., Bank A).
4. Verify **Current Balance** is displayed.
5. Select **To Ledger** (e.g., Cash).
6. Enter **Amount** (Less than or equal to balance).
7. Enter **Narration**.
8. Click **Submit**.
9. Verify redirect to List Page and check top row.

### Scenario 2: Manual Credit
1. Select "Manual Credit/Debit" mode.
2. Select **From Ledger**.


3. Select **Transaction Type** = Credit.
4. Enter **Amount**.
5. Enter **Narration**.
6. Click **Submit**.
7. Verify on List Page.

### Scenario 3: Insufficient Balance Validation
1. Select "Ledger Transfer".
2. Select **From Ledger**.
3. Enter **Amount** > **Current Balance**.
4. Click **Submit**.
5. Verify error toast: "Transfer amount exceeds current balance."

---

## Excel Data Structure

### Sheet: `LedgerAdjustment`

| TestCaseId | TestStatus | TransferMode | FromLedger | ToLedger | TransactionType | Amount | Narration | ExpectedResult |
|------------|------------|--------------|------------|----------|-----------------|--------|-----------|----------------|
| TC001      | Run        | Transfer     | Bank A     | Cash     |                 | 500    | Transfer  | Success        |
| TC002      | Run        | Manual       | Sales      |          | Credit          | 1000   | Adj       | Success        |
| TC003      | Run        | Transfer     | Bank A     | Cash     |                 | 999999 |           | Insufficient   |

---

## Code Pattern Hints
- Use `Select2` handling logic for `from_ledger` and `to_ledger`.
- Use a `WebDriverWait` for `bal_amount` text to not be empty after selecting `from_ledger`.
- Handle the error toast using the standard `$.toaster` selector if applicable, or check for the message in the redirect logic.
