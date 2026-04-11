# Master Prompt: Billing Issue Automation (Finalized)

Build complete Billing Issue automation for the Retail Automation project. Follow the logic and patterns implemented in `c:\Retail_Automation\Sparqla\Test_Bill\BillingIssue.py`.

**File to create**: `c:\Retail_Automation\Sparqla\Test_Bill\BillingIssue.py`  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 1. Controller & Navigation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **Controller**: `admin_ret_billing.php`
- **Menu**: Billing → Issue
- **List URL**: `/admin_ret_billing/issue/list`
- **Add URL**: `/admin_ret_billing/issue/add`
- **Add Button Xpath**: `//a[@id="add_billing"]`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 2. Form Details & Automation Logic
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Header Fields (Select2 Dropdowns & Autocomplete)
- **Branch**: `id=branch_select`, uses `dropdown_select`.
- **Issue To**: `id=issue_to`, uses `dropdown_select`. (Employee / Customer / Karigar).
- **Issue Type**: `id=issue_type`, uses `dropdown_select`. (Petty Cash, Credit, Refund, Expenses, Non Jewellery Expense).
- **Account Head**: `id=acc_head`, uses `dropdown_select`. (Populates if Issue Type is Expenses).
- **Name (Autocomplete)**: `id=name`, uses `fill_autocomplete_field`. **MANDATORY**.
- **Amount**: `id=issue_amount`, uses `fill_input`. **MANDATORY**. 
- **Employee**: `id=emp_select`, uses `dropdown_select`. **MANDATORY**. 
- **Narration**: `id=narration`, uses `fill_input`. **MANDATORY**.

### Payment Sections (Main Sheet Mapping)
- **Cash**: Enter amount in `id=cash_pay`.
- **Cheque**: Toggle `Cheque(Yes/No)`. Click `id=cheque_modal`. 
  - Fields: `ChequeDate`, `Bank`, `ChequeNo`, `ChequeAmount`.
  - Save: `//a[@id="save_issue_chq"]`.
- **Net Banking**: Toggle `NB(Yes/No)`. Click `id=net_bank_modal`.
  - Fields: `NBType`, `NBBankDevice`, `NBPaymentDate`, `NBRefNo`, `NBAmount`.
  - Save: `//a[@id="save_issue_net_banking"]`.

**Submission**: Click **Save** button (`id=save_issue`).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 3. Post-Save Logic (Tab Switching & Extraction)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. **Window Handling**: After saving, the system opens the print view in a **new tab**.
2. **Switch**: Switch to the new tab, wait until URL contains `/issue_print/`.
3. **Extraction**: Use `_extract_id_from_url()` to get the numeric ID from the URL (e.g., `5010`).
4. **Cleanup**: Close the print tab and switch back to the main window for list verification.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 4. List Verification Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. **Date Filter**: Apply date range using `//input[@id="dt_range"]` with `FromDate` and `ToDate` from Excel.
2. **Search**: Enter the **Captured ID** in the DataTables search box.
3. **Capture**: Get the Voucher No from column **3** (`td[3]`) of the first result row.
4. **Excel**: Store the captured Voucher No in Column 27 (`CapturedBillNo`).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 5. Excel Mapping: BillingIssue Sheet
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**File Path**: `c:\Retail_Automation\Sqarqla_Retail_data.xlsx` (or project standard path)

| Column | Name | Description |
|---|---|---|
| 1 | TestCaseId | Unique ID |
| 2 | TestStatus | Yes/No or Skip |
| 3 | ActualStatus | Execution Remark |
| 4 | Branch | Dropdown selection |
| 5 | IssueTo | Select2 (Employee/Customer/Karigar) |
| 6 | IssueType | Select2 (Expenses/Refund/etc.) |
| 7 | AccountHead | Select2 (If Expenses) |
| 8 | Name | Autocomplete |
| 9 | Amount | Total Issue Amount |
| 10 | ReferenceNo | Optional ref |
| 11 | Employee | Select2 dropdown |
| 12 | Narration | Text info |
| 13 | CashAmount | Cash portion |
| 14 | Cheque(Yes/No) | Yes trigger |
| 15-19 | Cheque Details | Date, Bank, No, Amount, Action |
| 20 | NB(Yes/No) | Yes trigger |
| 21-26 | NB Details | Type, Bank, Date, RefNo, Amount, Action |
| 27 | CapturedBillNo | Captured Voucher No (from verification) |
| 28 | FromDate | Date search filter Start |
| 29 | ToDate | Date search filter End |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 6. Implementation Notes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **Dropdown Pattern**: 
  ```python
  Function_Call.dropdown_select(self, '//select[@id="..."]/following-sibling::span', text, '//span[@class="select2-search select2-search--dropdown"]/input')
  ```
- **Verification Search**: Always search by the ID extracted from the URL to ensure 100% accuracy in multi-record lists.
- **Table Column**: Verify Voucher No from `td[3]` in the list.

