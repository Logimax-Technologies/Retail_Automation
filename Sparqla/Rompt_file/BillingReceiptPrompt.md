# Master Prompt: Billing Receipt Automation

Build the automation script for the **Billing Receipt** module. Follow the patterns established in `BillingIssue.py` and other retail modules.

**File to create**: `c:\Retail_Automation\Sparqla\Test_Bill\BillingReceipt.py`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 1. Module Context
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **Controller**: `admin_ret_billing.php`
- **Function**: `receipt($type="", $id="", $billno="")`
- **Menu**: Billing → Receipt
- **Navigation**: Click `Add Receipt` button (`id=add_billing`) on the list page.
- **Form URL**: `/admin_ret_billing/receipt/add`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 2. Form Fields & Mandatory Logic
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Header Section
- **Branch**: `id=branch_select`. (Select2 Dropdown).
- **Customer**: `id=name`. (Autocomplete - Type Name/Mobile and select).
- **Receipt Type**: Radio buttons `name="receipt[receipt_type]"`.
  - Values: 1 (Credit Collection), 2 (Advance), 6 (Chit Close), 8 (Petty Cash), 9 (Amount Receipt).
- **Against Est**: Radios `id=is_aganist_est_yes` / `id=is_aganist_est_no`.
- **Esti No**: `id=esti_no`. (Search if Against Est is Yes).
- **Receipt As**: Radios `id=receipt_as1` (Amount) / `id=receipt_as2` (Weight).
- **Store As**: Radios `id=store_receipt_as_1` (Amount) / `id=store_receipt_as_2` (Weight).
- **Amount**: `id=amount`. (Input).
- **Weight**: `id=weight`. (Input).
- **Date**: `id=receipt_date`. (DatePicker).
- **Employee**: `id=emp_select`. (Dropdown).
- **Narration**: `id=narration`. (Textarea).

### Payment Section (Make Payment Card)
- **Cash**: Input `id=make_pay_cash`.
- **Card**: Click `id=card_detail_modal`. Modal `id=card-detail-modal`.
  - Modal Add: `id=new_card`.
  - Modal Save: `id=add_card`.
- **Cheque**: Click `id=cheque_modal`. Modal `id=cheque-detail-modal`.
  - Modal Add: `id=new_chq`.
  - Modal Save: `id=save_chq`.
- **Net Banking**: Click `id=net_bank_modal`. Modal `id=net_banking_modal`.
  - Modal Add: `id=new_net_bank`.
  - Modal Save: `id=save_net_banking`.

### Submission
- **Save Button**: `id=save_receipt`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 2.1 Mandatory Business Rules
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **High-Value Validation**: If **Amount** > **200,000** (2 Lakhs):
    - **PAN No** (`id=pan_no`) is **Mandatory**.
    - **Adhaar No** (`id=aadhar_no`) is **Mandatory**.
    - **Image/Proof** (`id=pan_images`) is **Mandatory**.
- **Receipt Type Specifics**:
    - **Petty Cash (Employee)** requires **Employee** selection.
    - **Advance Against Est** requires **Esti No** and a successful **Search**.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 3. Automation Workflow (Tester's Perspective)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Step 1: Add Receipt
1. Navigate to the Receipt list page.
2. Click **Add Receipt**.
3. Fill mandatory header fields: Branch, Customer (Autocomplete), Receipt Type, Amount, Employee.
4. **Petty Cash (Employee) Scenario**:
    - Select **Receipt Type**: `Petty` (`id=receipt_type8`).
    - Select **Receipt To**: `Employee` (`id=receipt_to_emp`).
    - Select **Against Est**: `No` (`id=is_aganist_est_no`).
    - Fill **Amount** (`id=amount`) to be received.
    - **CREDIT DETAILS Modal**: A modal (`id=credit_collection`) appears showing previous employee issues.
        - Locate the relevant issue in table `id=issue_list`.
        - Select the record by checking the checkbox in column 1 (`td[1]/input`).
        - Enter the **Received** amount in column 7 (`td[7]/input`).
        - Example: If Issue is 1000 and Paid is 500, enter Balance 500 in **Received**.
        - Click **Save** on the modal (`id=save_credit_collection`).
5. **Advance Against Estimation Scenario**:
    - Select **Receipt Type**: `Advance` (`id=receipt_type2`).
    - Select **Against Est**: `Yes` (`id=is_aganist_est_yes`).
    - Enter **Esti No** (`id=esti_no`) and click **Search** (`id=est_search`).
    - This will populate the **Product Details** table (Tag, Product, G.Wt, N.Wt, etc.) and pre-fill related fields.
    - Fill/Verify **Amount** (`id=amount`) to be received as advance.
6. **Advance Adjustment Scenario** (Utilize existing Advance):
    - In the **Make Payment** section, click the **+** button next to **Advance Adj** (`id=adv_adj_modal`).
    - The **Advance Adjustment** modal (`id=adv-adj-confirm-add`) appears.
    - Locate the previous receipt in table `id=bill_adv_adj`.
    - Select the checkbox for the record.
    - Enter the **Adjusted Amount** to be used.
    - Click **Save** (`id=save_receipt_adv_adj`).
    - The adjusted amount will be added to the payment total.
7. Fill **Make Payment** section in the main form for any remaining balance.
8. Click **Save** (`id=save_receipt`).
9. **Window Handling & ID Extraction**:
    - After clicking **Save**, the system typically opens the receipt in a **new tab** (Print Preview).
    - **Current Window Index 0**: Main application.
    - **New Window Index 1**: Receipt Print Tab.
    - Switch to **Index 1**.
    - Extract the **Receipt ID** from the current URL (pattern: `.../receipt_print/5010`).
    - Capture the ID for search purposes.
    - **Close the tab** and switch back to **Index 0**.
    - Navigate to the **Receipt List** page.

### Step 2: List Verification
1. On the Receipt List page, apply the **Date Filter** (`id=dt_range`) and click **Search** (`id=receipt_search`).
2. Type the **Extracted ID** (captured from the print tab) into the DataTable's search box.
3. Locate the first result.
4. **Capture**: Get the **Bill No** from column **3** (`td[3]`) and save to Excel.
5. Verify Tot.Amount (Col 11) matches the input amount.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 4. Excel Mapping: BillingReceipt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Col | Field | Note |
|---|---|---|
| Col | Field | Note |
|---|---|---|
| 1 | TestCaseId | |
| 2 | TestStatus | Yes/No |
| 3 | ActualStatus | |
| 4 | Branch | |
| 5 | Customer | |
| 6 | ReceiptType | 1 to 9 |
| 7 | Amount | |
| 8 | Employee | |
| 9 | Narration | |
| 10 | CashAmount | |
| 11 | Card(Yes/No) | Modal trigger |
| 12-16 | Card Details | Type, Bank, CardNo, ExpDate, Amount |
| 17 | Cheque(Yes/No) | Modal trigger |
| 18-21 | Cheque Details | Date, Bank, No, Amount |
| 22 | NB(Yes/No) | Modal trigger |
| 23-27 | NB Details | Type, Bank, Date, RefNo, Amount |
| 28 | AdvAdj(Yes/No) | Modal trigger |
| 29-30 | AdvAdj Details | Receipt No, Adjusted Amount |
| 31 | EmpCreditRecNo | (Petty/Employee Credit) |
| 32 | EmpCreditAmt | (Petty/Employee Credit) |
| 33 | BillNo | (Captured after verification) |
| 34 | FromDate | Search Filter |
| 35 | ToDate | Search Filter |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 5. Test Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. **TC_BR_01 (Advance)**: Regular Advance Receipt with Cash.
2. **TC_BR_02 (Multi-Mode)**: Receipt with partial Cash and partial Cheque.
3. **TC_BR_03 (Petty - Employee Issue Recovery)**: 
    - Select **Receipt Type**: Petty.
    - Select **Receipt To**: Employee.
    - Select an employee issued with expenses (from Billing Issue module).
    - Recover the balance amount using the **CREDIT DETAILS** modal.
    - Save and verify the receipt.
4. **TC_BR_04 (Credit Collection)**: Collect against existing customer bills.
5. **TC_BR_05 (Advance against Estimation)**:
    - Select **Receipt Type**: Advance.
    - Select **Against Est**: Yes.
    - Enter a valid **Esti No** and click **Search**.
    - Verify the product details are loaded in the table.
    - Enter the advance amount and save.
6. **TC_BR_06 (Advance Adjustment)**:
    - Select a customer with an existing advance balance.
    - Click **Advance Adj (+)**.
    - Select an existing advance receipt in the modal.
    - Enter the adjustment amount and save.
    - Verify the adjusted amount is deducted from the total payable.
7. **TC_BR_ERROR_01**: Submit without selecting Customer or providing Amount.
8. **TC_BR_ERROR_02 (High-Value Validation)**:
    - Enter **Amount** > **200,000**.
    - Leave **PAN No** and **Adhaar No** empty.
    - Click **Save**.
    - Verify that the system prevents submission and requests PAN/Aadhar details.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 6. Technical Requirements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Use `Function_Call.dropdown_select` for Select2 dropdowns.
- Use `Function_Call.fill_autocomplete_field` for Customer.
- Implement `_extract_id_from_url` with window handle switching.
- Handle modals for Card/Cheque/NB similar to `BillingIssue.py`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 7. Advance Transfer Module
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **URL**: `/admin_ret_billing/advance_transfer/add`
- **Fields**:
    - **Branch**: `id=branch_select`.
    - **From Customer**: `id=adv_trns_from_cust` (Autocomplete).
    - **To Customer**: `id=adv_trns_to_cust` (Autocomplete).
- **Workflow**:
    1. Select Branch and From Customer.
    2. Selected customer's advances load in table `id=advance_trns_list`.
    3. Select a receipt via checkbox.
    4. Enter **Transfer Amount** in column 4 (`td[4]/input`).
    5. Select **To Customer**.
    6. Click **Save** (`id=submit_advance_transfer`).
    7. **OTP Handling**: If OTP modal `id=otp_modal` appears:
        - Enter fixed OTP or capture from system (if applicable).
        - Click **Verify** (`id=verify_advance_transfer_otp`).
        - Click final **Save And Submit** (`.submit_advance_transfer`).

- **Test Scenario (TC_AT_01)**:
    - Transfer 1000 from Customer A to Customer B.
    - Verify "Total Transfer Amount" matches.
    - Handle OTP if enabled.
