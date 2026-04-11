Build complete **Supplier PO Payment** automation for the Retail Automation project.
Follow the **EXACT same code pattern** as `LotGenerate.py`, `QCIssueReceipt.py`, `SupplierBillEntry.py`, and `PurchaseReturn.py`.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_Purchase\SmithSupplierPayment.py
```

## Update main.py
Add `SmithSupplierPayment` case to the module dispatcher.

---

## Controller Details (admin_ret_purchase.php)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
Function: `supplier_po_payment($type="", $id="")`

Switch Cases:

- `list` → Supplier PO Payment List Page.
- `add` → Supplier PO Payment Form.
- `edit` → Edit Supplier PO Payment.
- `save` → Save Payment Entry.
- `cancel_pay_entry` → Cancel Payment Entry.

AJAX / Support:

- `purchase_payment_details` → Load payment details for a PO.
- `get_supplier_pay_details` → Load details for a supplier.
- `supplier_advance_details` → Load advance details.
- `po_pay_details` → Load individual PO payment record.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 

> **Note:** This module covers **Supplier PO Payment** (`popayment/` view) — Bill Type: BILL | RECEIPT; uses Supplier (karigar) select

---

## Navigation

| Module              | Menu Path                          | List URL                                         | Add URL                                         |
|---------------------|------------------------------------|--------------------------------------------------|-------------------------------------------------|
| Supplier PO Payment | Purchase → Supplier Payment        | `admin_ret_purchase/supplier_po_payment/list`    | `admin_ret_purchase/supplier_po_payment/add`    |

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
Form Fields & Mandatory Status 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Main Form: Supplier PO Payment (`popayment/form.php`)

**Header Section:**
- ✅ **Bill Type** (Radio): `name="billing[bill_type]"` (1=BILL, 2=RECEIPT).
- ✅ **Karigar (Supplier)** (Select2): `id="select_karigar"`, `name="billing[id_karigar]"`.
- ✅ **Supplier Balance** (Display): `class="supplierblc"` (Readonly).
- ⬜ **Opening Checkbox** (Checkbox): `id="opening_checkbox"`.

**Pending Bills Table:**
- ✅ **Pending Bills Container**: `id="pending_bills_container"` (Auto-loads after Karigar select).
- ✅ **Bill Selection**: Individual checkboxes within the container to select bills for settlement.

**Payment Details (`id="payment_modes"`):**
- ✅ **Net Amount** (Input): `id="balance_amount"` (Readonly - sum of selected bills).
- ✅ **Cash** (Input): `name="billing[cash_amount]"`, `class="cash_amount"` (⚠️ **Limit: 10,000**).
- ✅ **Net Banking** (Modal Trigger): `id="net_bank_modal"` (Opens `#netbanking_modal`).
- ✅ **Cheque** (Modal Trigger): `id="cheque_modal"` (Opens `#cheque_modal`).
- ✅ **Total Amount** (Input): `id="total_pay_amount"` (Readonly sum).
- ✅ **Balance Amount** (Input): `id="bal_amount"` (Readonly).

**Modals:**

- ✅ **Net Banking Modal** (`#netbanking_modal`):
    - ✅ **Type** (Select): `class="nb_type"` (RTGS / NEFT).
    - ✅ **Bank** (Select): dropdown.
    - ✅ **Amount** (Input): `class="pay_amount"`.
    - ✅ **Ref NO** (Input): `class="ref_no"`.

- ✅ **Cheque Modal** (`#cheque_modal`):
    - ✅ **Cheque No** (Input): `class="cheque_no"`.
    - ✅ **Bank Name** (Input): manual entry.
    - ✅ **Amount** (Input): `class="cheque_amount"`.

- ✅ **Remark** (Textarea): `id="remark"`, `name="billing[remark]"`.

**Action Buttons:**
- ✅ **Save** (Button): `id="pay_submit"`.
- ✅ **Cancel** (Button): `class="btn-cancel"`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 

### Business Rules
- ⚠️ **Cash Limit**: Payments in Cash are restricted to a maximum of **10,000**. If the amount exceeds this, the system should trigger a validation alert.
- **Mixed Payment**: Multiple bills cannot be settled with multiple payment modes (e.g., Cash + Cheque) in a single transaction if the total entry count is greater than 1 (Controller restriction).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 

---

## List Page Verification

### Supplier PO Payment List (`admin_ret_purchase/supplier_po_payment/list`)

| Column | Notes |
|--------|-------|
| Id | Row ID |
| Pay Date | Date of payment |
| Pay Ref No | System-generated payment ref no |
| Supplier | Karigar name |
| Amount | Total payment amount |
| Type | BILL / RECEIPT |
| Status | Payment status |
| Action | Cancel button (opens `#confirm-billcancell` modal with `id="pay_id"` + `id="payment_cancel_remark"`) |

**Date Range Picker:** `id="sp-dt-btn"` → sets hidden `id="sp_date1"` and `id="sp_date2"` for filtering.

---

## Acknowledgment / Receipt (`popayment/payment_ack.php`)

After a successful save, the system renders a **"Issue Of Payment"** receipt. It contains:

| Section | Details |
|---------|---------|
| Header | Company name, address, GST |
| Transaction Type | `$paymentdetails['paydetails']['bill_type']` |
| Issue No | `$paymentdetails['paydetails']['pay_refno']` |
| Issue Date | `$paymentdetails['paydetails']['pay_date']` |
| Paid By | Company details (Name, Address, GST) |
| Paid To | Karigar name, mobile, address, GST |
| Amount | `tot_cash_pay` |
| Payment Breakdown | CASH, CHEQUE (with Chq Ref No, Date, Bank), RTGS (Ref No, Date), IMPS, NEFT |
| Total | Sum of all payment modes |
| Footer | Audited By, Party Sign, Manager Sign, Operator |

> **Extraction Logic:** After save, look for `pay_refno` in the acknowledgment URL/page — extract using regex on the heading or table cells. The window auto-calls `window.print()` — handle this via `ESCAPE` or `wait_for_new_window()` logic similar to PurchaseReturn.

---

## Full Business Workflow

### Add Supplier PO Payment Flow
1. Navigate: `admin_ret_purchase/supplier_po_payment/add`
2. Select **Bill Type** (BILL=1 / RECEIPT=2).
3. Select Karigar from `id="select_karigar"` → Wait for `id="pending_bills_container"` to load.
4. Check pending bills to settle (checkboxes in pending_bills_container).
5. Note auto-filled `id="balance_amount"` (Net Amount).
6. **Optional:** Check `id="opening_checkbox"` for Opening balance payment.
7. Enter payment modes:
   - Cash: Fill `name="billing[cash_amount]"`
   - Net Banking: Click `id="net_bank_modal"` → add rows (Type, Bank, Date, Amount, Ref No) → Save
   - Cheque: Click `id="cheque_modal"` → add rows → Save
8. Verify `id="total_pay_amount"` = sum of all modes; `id="bal_amount"` should be 0 or acceptable balance.
9. **Optional:** Enter remark in `id="remark"`.
10. Click `id="pay_submit"` → Wait for success toast / acknowledgment.
11. Extract **Pay Ref No** from `payment_ack.php` (Issue No field).
12. Navigate to list → filter by date → verify top row (Supplier, Amount, Type, Status).

### Cancel Flow (PO Payment)
1. On list page, click Cancel action for a row.
2. Modal `#confirm-billcancell` opens.
3. Fill `id="payment_cancel_remark"`.
4. Click `id="payment_cancel"` (enabled after remark entry).
5. Verify status changes on list.

---

## Success / Failure Messages

| Scenario | Message |
|----------|---------|
| Success | `$.toaster({ priority: 'success', title: 'Success!', message: '...' })` |
| Validation Failure | "Please fill required fields." or "Please select karigar." |
| No bills selected | "Please select any one bill." or equivalent alert |
| Invalid Amount | Amount mismatch or exceeds balance validation |

---

## Test Scenarios

### Scenario 1: Cash Payment (BILL)
1. **Goal**: Settle outstanding bills using only Cash.
2. **Steps**:
   - Navigate to `admin_ret_purchase/supplier_po_payment/add`.
   - Select Bill Type: **BILL**.
   - Select **Karigar**.
   - Select one or more **Pending Bills**.
   - Enter **Cash Amount** (matching Net Amount).
   - Click **Save**.
3. **Verification**: Extract Ref No from receipt, confirm in list page.

### Scenario 2: Net Banking Payment (RECEIPT)
1. **Goal**: Record a payment receipt via RTGS/NEFT.
2. **Steps**:
   - Select Bill Type: **RECEIPT**.
   - Select **Karigar** and **Bills**.
   - Open **Net Banking Modal**.
   - Add row: Type=RTGS, Enter Bank, Date, Amount, Ref No.
   - Click **Save**.
3. **Verification**: Verify Total Pay Amount reflects modal sum.

### Scenario 3: Cheque Payment
1. **Goal**: Settle bills using a Cheque.
2. **Steps**:
   - Open **Cheque Modal**.
   - Add row: Enter Cheque No, Bank, Date, Amount.
   - Click **Save**.

### Scenario 4: Opening Balance Payment
1. **Goal**: Pay against an opening balance.
2. **Steps**:
   - Check **Opening Checkbox**.
   - Enter payment amount in Cash or modal.
   - Click **Save**.

### Scenario 5: Mixed Payment (Single Bill)
1. **Goal**: Pay a single bill using both Cash and Net Banking.
2. **Context**: Controller restricts multiple bills with multiple modes. Use **one bill selection** for this test.

### Scenario 6: Cancellation Flow
1. **Goal**: Cancel a previously made payment.
2. **Steps**:
   - On List page, click **Cancel** action for a row.
   - Enter **Remark** in modal.
   - Click **Cancel**.
3. **Verification**: Confirm Status in list changes to reflect cancellation.

### Scenario 7: Cash Limit Validation
1. **Goal**: Verify that the system prevents cash payments exceeding 10,000.
2. **Steps**:
   - Select **Karigar** and **Bills** (Total > 10,000).
   - Enter **10,001** in the **Cash Amount** field.
   - Click **Save**.
3. **Verification**: Confirm that a validation alert/toaster appears and the transaction is NOT saved.

---

## Expected Excel Sheet Structure

### File: `Sqarqla_Retail_data2.xlsx`
Add sub-sheets under the existing Master sheet.

---


### Sheet: `SupplierPOPayment`

| Col | Field | Notes |
|-----|-------|-------|
| 1 | TestCaseId | Unique ID |
| 2 | TestStatus | Run / Skip |
| 3 | Bill Type | BILL / RECEIPT |
| 4 | Karigar (Supplier) | Select2 |
| 5 | Opening Balance (Yes/No) | Check opening_checkbox |
| 6 | Bill Selection | All / First N / specific row index |
| 7 | Cash Amount | Direct cash payment |
| 8 | Net Banking (Yes/No) | Triggers net banking modal |
| 9 | NB Type | RTGS / NEFT / IMPS |
| 10 | NB Bank | Bank name |
| 11 | NB Amount | Amount |
| 12 | NB Ref No | Transaction ref |
| 13 | NB Date | Payment date |
| 14 | Cheque (Yes/No) | Triggers cheque modal |
| 15 | Cheque No | Cheque number |
| 16 | Cheque Bank | Bank name |
| 17 | Cheque Date | Cheque date |
| 18 | Cheque Amount | Amount |
| 19 | Remark | Narration / Notes |
| 20 | Expected Net Amount | For balance_amount verification |
| 21 | Expected Pay Ref No | Extracted from ack (post-run) |
| 22 | Expected Status | For list page verification |

---

### Master Sheet Update

Add row:
| Column | Value |
|--------|-------|
| Module Name | SmithSupplierPayment |
| Sheet Name | SmithPayment / SupplierPOPayment |
| Run | Yes |

---

## Code Patterns to Follow

| Pattern | Implementation |
|---------|---------------|
| Dynamic Loading | Use Explicit Waits for `select_karigar`, `pending_bills_container` load. Use `WebDriverWait` + `EC.presence_of_element_located`. |
| Select2 | Use `.send_keys()` + wait for dropdown + click matching option — same as PurchaseReturn. |
| Modal Handling | Click `+` button → Wait for modal → Fill rows → Click Save → Wait for modal close. |
| Net Banking Rows | After `create_net_banking_row`, find last `tr` in `#net_banking_details tbody`, fill `pay_amount`, `nb_type`, `ref_no`. |
| Cheque Rows | Same row-creation pattern as Net Banking. |
| Payment Verification | Read `balance_amount` (Net Amount), sum all mode inputs, verify `total_pay_amount` == sum, `bal_amount` == Net - Total. |
| Acknowledgment | After `pay_submit`, wait for new tab/window or redirect → grab `pay_refno` via regex `r'Issue No\s*[:\-]?\s*(\S+)'` or from page element. Handle `window.print()` via ESCAPE key or close new window. |
| List Verification | Filter date to Today → check first row: Supplier, Amount, Type match inputs. |
| Logger Pattern | Use `logger.info()` for steps, `logger.error()` for mismatch — do NOT hard-fail on amount mismatch, log and continue. |

---

## Calculation Logic (Python Verification)

> Smith Payment and PO Supplier Payment are **pure payment entry modules** with no item-level calculation (unlike Purchase Return). All computations are balance-based.

```python
# Balance Calculation Verification
net_amount = float(balance_amount_field.get_attribute('value'))  # Payable
cash = float(cash_amount_field.get_attribute('value') or 0)
net_banking = sum_of_net_banking_rows()   # from modal
cheque = sum_of_cheque_rows()             # from modal

total_pay = cash + net_banking + cheque
balance = round(net_amount - total_pay, 2)

# Assert total_pay_amount == total_pay
# Assert bal_amount == balance
```

---

## Verification Checklist

- [ ] Supplier PO Payment — BILL type with Karigar + pending bills
- [ ] Supplier PO Payment — RECEIPT type
- [ ] Supplier PO Payment — Cash only payment
- [ ] Supplier PO Payment — Cash + Net Banking mixed
- [ ] Supplier PO Payment — Cheque payment
- [ ] Supplier PO Payment — Opening Balance checkbox
- [ ] Acknowledgment — Extract Pay Ref No
- [ ] List Verification — Filter today + confirm top row
- [ ] Cancel Flow — Verify status change on list

---

## File Summary

| File | Action |
|------|--------|
| `Test_Purchase/SmithSupplierPayment.py` | **[NEW]** Main automation script |
| `main.py` | **[MODIFY]** Add SmithSupplierPayment case |
| `Sqarqla_Retail_data2.xlsx` | **[MODIFY]** Add SupplierPOPayment sheet + Master entry |
