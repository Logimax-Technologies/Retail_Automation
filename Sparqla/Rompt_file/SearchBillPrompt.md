Build complete **Search Bill** automation for the Retail Automation project.
Follow the **EXACT same code pattern** as `SmithMetalIssue.py`, `LotGenerate.py`, `QCIssueReceipt.py`, `SupplierBillEntry.py`, `PurchaseReturn.py`, and `DebitCreditEntry.py`.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_Billing\SearchBill.py
```

## Update main.py
Add `SearchBill` case to the module dispatcher.

---

## Controller Details (admin_ret_billing.php)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
Function: `billing($type = "", $id = "", $billno = "")`

Switch Cases:
- `list` → Billing List Page (renders `billing/list`).
- `ajax` → AJAX fetch for billing records.
- `cancell` → Cancel Bill action.
- `billing_invoice` → Generate Bill Receipt.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Note: This module handles searching, viewing, and cancelling existing sales bills.

## Navigation
| Module | Menu Path | List URL | Add URL |
| :--- | :--- | :--- | :--- |
| **Search Bill** | Billing → Search Bill | `admin_ret_billing/billing/list` | N/A (List handles search) |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Form Fields & Mandatory Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### List Page: Billing List (billing/list.php)
**Search Section:**
- ✅ **Branch (Select)**: `id="branch_select"` (Visible if multi-branch enabled)
- ✅ **Date Range Picker**: `id="rpt_date_picker"`
  - 🔹 Uses hidden fields `id="rpt_from_date"` and `id="rpt_to_date"`.
- ✅ **Bill No (Input)**: `id="filter_bill_no"` (Wait: ensure it's not commented out in real DOM)
- ✅ **Search Button**: `id="bill_search"`

**Billing List Table (Table: `id="billing_list"`):**
- ✅ **Table Data**: Fetches via AJAX. Columns include: Id, Bill Date, Branch, Bill No, Customer, Mobile, Bill Type, Tot. Amount, Status, Emp, Action.

**Action Column Buttons:**
- ✅ **Print Receipt**: `.btn-print` (Opens new tab)
- ✅ **Print Thermal**: `.btm-print` (Opens new tab)
- ✅ **Edit Payment**: `.btn-edit`
- ✅ **Cancel Bill**: `.btn-warning` (Triggers `confirm_delete` function)

**Cancel Bill Modal (Modal: `id="confirm-billcancell"`):**
- ✅ **OTP Input**: `id="cancel_otp"` (If required)
- ✅ **Verify Button**: `id="verify_otp"`
- ✅ **Remarks**: `id="cancel_remark"`
- ✅ **Confirm Cancel Button**: `id="cancell_delete"`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Full Business Workflow & Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 1. Search by Date Range
- **Workflow**:
  1. Navigate to Billing List.
  2. Select Date Range using the picker.
  3. Click `Search`.
  4. Verify the table contains records within the date range.

### 2. Search by Bill Number
- **Workflow**:
  1. Enter Bill Number in `filter_bill_no`.
  2. Click `Search`.
  3. Verify the specific bill appears in the list.

### 3. Print Bill Receipt
- **Workflow**:
  1. Find target bill in the list.
  2. Click `Print Receipt` icon.
  3. Verify a new tab opens (handle window handles).

### 4. Cancel Bill (with/without OTP)
- **Workflow**:
  1. Locate target bill.
  2. Click `Cancel` (Close icon).
  3. Enter `Cancel Remark`.
  4. If OTP input is visible, enter `OTP` and click `Verify`.
  5. Click `Cancel` in the modal.
  6. Verification: Bill status should update to "Cancelled" or disappear from the active list.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Advanced Logic & Constraints (from Knowledge Brain)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### UI Automation Gotchas
- **Date Range Interaction**: Clicking the daterangepicker button requires selecting a predefined range (e.g., "Today", "Last 30 Days") or custom range via the calendar popup.
- **Table Loading**: Always wait for `#billing_list tbody tr` to be visible after searching.
- **Cancel Button Status**: The "Cancel" button in the modal may be disabled until Remarks are entered or OTP is verified.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Expected Excel Sheet Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Sheet: `SearchBill`**
| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **TestCaseId** | Unique ID |
| 2 | **TestStatus** | Run / Skip |
| 3 | **FromDate** | DD-MM-YYYY |
| 4 | **ToDate** | DD-MM-YYYY |
| 5 | **BillNo** | Search query |
| 6 | **Action** | Search / Print / Cancel |
| 7 | **Remarks** | For cancellation |
| 8 | **UseOTP** | Yes / No |
| 9 | **OTP** | For cancellation |
| 10 | **VerifyStatus** | Expected status (e.g. Cancelled) |
| 11 | **ActualStatus** | Success / Fail |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Code Patterns to Follow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **Window Switching**: Use `self.driver.switch_to.window(self.driver.window_handles[-1])` for print operations.
- **Date Range Handling**:
  ```python
  wait.until(EC.element_to_be_clickable((By.ID, "rpt_date_picker"))).click()
  # Select range (e.g. "Last 30 Days")
  wait.until(EC.element_to_be_clickable((By.XPATH, "//li[text()='Last 30 Days']"))).click()
  ```
- **Table Interaction**: Use `//table[@id='billing_list']/tbody/tr[contains(., '{bill_no}')]` to find the target row.
