Build complete **Debit/Credit Entry** automation for the Retail Automation project.
Follow the **EXACT same code pattern** as `LotGenerate.py`, `QCIssueReceipt.py`, `SupplierBillEntry.py`, and `PurchaseReturn.py`.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_Purchase\DebitCreditEntry.py
```

## Update main.py
Add `DebitCreditEntry` case to the module dispatcher.

---

## Controller Details (admin_ret_purchase.php)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
Function: `credit_debit_entry($type = "",$id="",$status="")`

Switch Cases:

- `list` → Credit/Debit Entry List Page.
- `add` → Credit/Debit Entry Form.
- `edit` → Edit Credit/Debit Entry.
- `save` → Save Entry.
- `cancel_crdr_entry` → Cancel Entry.
- `credit_debit_acknolodgement` → Print/Acknowledgment.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 

> **Note:** This module covers **Debit/Credit Entry** — handles both Amount and Weight based entries for Suppliers/Smiths/Approvals.

---

## Navigation

| Module              | Menu Path                          | List URL                                         | Add URL                                         |
|---------------------|------------------------------------|--------------------------------------------------|-------------------------------------------------|
| Debit/Credit Entry  | Purchase → Credit/Debit Entry       | `admin_ret_purchase/credit_debit_entry/list`     | `admin_ret_purchase/credit_debit_entry/add`     |

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
Form Fields & Mandatory Status 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Main Form: Credit/Debit Entry (`credit_entry/form.php`)

**Header Section:**
- ✅ **Transaction In** (Toggle): `id="toggle_transaction"` (Checked = Amount, Unchecked = Weight).
- ✅ **Supplier (Karigar)** (Select2): `id="select_karigar"`, `name="credit[karigar]"`.
- ✅ **Type** (Radio): `name="credit[accountto]"` (1=Supplier, 2=Smith, 3=Approvals).
- ✅ **Supplier Bills** (Select2): `id="select_karigar_bills"`, `name="credit[karigar_bills]"`.

**Amount Section (`id="amount_row"`, visible if Amount toggle):**
- ✅ **Amount** (Input): `id="trans_amount"`, `name="credit[transamount]"`.
- ✅ **Transaction Type** (Select): `id="transtype"` (1=Credit, 2=Debit).

**Weight Section (`id="weight_row"`, visible if Weight toggle):**
- ✅ **Weight** (Input): `id="trans_weight"`, `name="credit[transweight]"`.
- ✅ **Weight Transaction Type** (Select): `id="wtranstype"` (1=Credit, 2=Debit).

**Footer Section:**
- ✅ **Narration** (Textarea): `id="naration"`, `name="credit[naration]"`.

**Action Buttons:**
- ✅ **Save** (Button): `id="save_credit_entry"`.
- ✅ **Cancel** (Button): `id="cancel_bill_edit"`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 

---

## List Page Verification

### Credit/Debit Entry List (`admin_ret_purchase/credit_debit_entry/list`)

| Column | Notes |
|--------|-------|
| Trans BillNo | System-generated bill no |
| Trans Date | Date of transaction |
| Supplier | Karigar/Supplier name |
| Transaction Type | Supplier / Smith / Approvals |
| Type | Credit / Debit |
| Amount | Amount of transaction |
| Weight | Weight of transaction |
| Narration | Remark/Notes |
| Status | Success / Cancelled |
| Action | Cancel button (opens `#confirm-creditcancell` modal with `id="credit_cancel_remark"`) |

**Date Range Picker:** `id="rpt_payment_date"`.
**Filters**: `id="transcation_type"` (Credit/Debit), `id="trans_type"` (Supplier/Smith/Approvals), `id="status_type"` (Success/Cancelled).

---

## Full Business Workflow

### Add Debit/Credit Entry Flow
1. Navigate: `admin_ret_purchase/credit_debit_entry/add`
2. Set **Transaction In** toggle (Amount or Weight).
3. Select **Supplier** from `id="select_karigar"`.
4. Select **Type** (Supplier/Smith/Approvals).
5. Select **Supplier Bill** from `id="select_karigar_bills"`.
6. Fill **Amount** and **Type** (Credit/Debit) OR **Weight** and **Type** (Credit/Debit).
7. Enter **Narration** in `id="naration"`.
8. Click **Save** (`id="save_credit_entry"`) → Wait for success toast / redirect to list.
9. Note the **Trans BillNo** from the list page or success context.
10. Navigate to list → filter by date → verify top row (Supplier, Type, Amount/Weight, Status).

### Cancel Flow
1. On list page, click **Cancel** action for a row.
2. Modal `#confirm-creditcancell` opens.
3. Fill `id="credit_cancel_remark"`.
4. Click `id="crdr_cancel"` (enabled after remark entry).
5. Verify status changes to "Cancelled" on list.

### Pure Weight Limit Validation
1. Before saving, if the transaction is weight-based, verify the Pure Weight matches: `(Weight * Touch) / 100`.
2. Ensure the Overall Pure Wt issued does not exceed the Karigar's Outstanding Balance.
3. If excess weight is entered, show a validation error: "Excess pure weight not allowed".

---

## Success / Failure Messages

| Scenario | Message |
|----------|---------|
| Success | `$.toaster({ priority: 'success', title: 'Success!', message: '...' })` |
| Validation Failure | "Please fill required fields." |
| Database Error | "Unable to proceed the requested process" |

---

## Test Scenarios

### Scenario 1: Supplier Credit (Amount)
1. **Goal**: Add a Credit entry for a Supplier in Amount.
2. **Steps**: Toggle to Amount, Select Supplier, Type=Supplier, Select Bill, Enter Amount, Type=Credit, Save.

### Scenario 2: Smith Debit (Weight)
1. **Goal**: Add a Debit entry for a Smith in Weight.
2. **Steps**: Toggle to Weight, Select Supplier, Type=Smith, Select Bill, Enter Weight, Type=Debit, Save.

### Scenario 3: Approvals Entry
1. **Goal**: Add an entry for Approvals ledger.
2. **Steps**: Select Type=Approvals, Select Bill, Enter Amount, Save.

### Scenario 4: Cancellation Flow
1. **Goal**: Cancel a "Success" entry and verify status.

---

## Expected Excel Sheet Structure

### Sheet: `DebitCreditEntry`

| Col | Field | Notes |
|-----|-------|-------|
| 1 | TestCaseId | Unique ID |
| 2 | TestStatus | Run / Skip |
| 3 | TransactionIn | Amount / Weight |
| 4 | Karigar (Supplier) | Select2 |
| 5 | Type | Supplier / Smith / Approvals |
| 6 | SupplierBill | Select Bill No |
| 7 | Amount | If TransactionIn = Amount |
| 8 | TransType | Credit / Debit |
| 9 | Weight | If TransactionIn = Weight |
| 10 | WTransType | Credit / Debit |
| 11 | Narration | Narration |
| 12 | Expected BillNo | Extracted post-run |
| 13 | Expected Status | Success / Cancelled |

---

## Code Patterns to Follow
1. **Toggle Handling**: Check if toggle state matches Excel; click if different.
2. **Dynamic Select2**: Handle `select_karigar` and `select_karigar_bills` with adequate waits.
3. **Modal for Cancel**: Use `WebDriverWait` for `#confirm-creditcancell`.
4. **Receipt extraction**: If needed, from `credit_debit_acknolodgement` URL.
