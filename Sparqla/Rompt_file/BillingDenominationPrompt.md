# Master Prompt: Billing Denomination (Cash Collection) Automation

Build the automation script for the **Billing Denomination** (Cash Collection) module. Follow the patterns established in `BillingReceipt.py` and other retail modules.

**File to create**: `c:\Retail_Automation\Sparqla\Test_Bill\BillingDenomination.py`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 1. Module Context
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **Controller**: `admin_ret_billing.php`
- **Function**: `cash_collection($type="", $id="")`
- **Menu**: Billing → Cash Collection
- **Navigation**: Click `Add` button (`id=add_lot`) on the list page.
- **Form URL**: `/admin_ret_billing/cash_collection/add`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 2. Form Fields & Mandatory Logic
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Search Filters
- **Branch**: `id=branch_select`. (Select2 Dropdown).
- **Date**: `id=cash_coll_date`. (DatePicker).
- **Counter**: `id=counter_sel`. (Dropdown).
- **Cash Type**: Radio buttons `name="cash[cash_type]"`.
  - Values: 1 (CRM), 2 (Retail), 3 (All).
- **Search Button**: `id=cash_coll_search`.

### Denomination Section
- **Table**: `id=denomination`.
- **Note/Coin Quantity**: Input `name="cash[denomination][value][]"`. (Class: `cash_count`).
- **Hidden Values**: `class="cash_value"` (contains the multiplier like 2000, 500, etc.).
### Collection Summary Section
- **Cash**: `id=cash_received`. (Read-only, populated after Search. Can be negative in some scenarios).
- **Opening Balance**: `id=cash_opening_balance`. (Input).
- **Total**: `id=cash_total`. (Read-only. Calculation: **Cash + Opening Balance**).
- **Difference**: `id=total_diff`. (Read-only. Calculation: **Total Denomination - Total**).

> [!IMPORTANT]
> **Mathematical Verification**: 
> 1. Total Denomination (Sum of all notes/coins) must match the **Total** field.
> 2. **Difference** should be **0.00** for a balanced entry.

### Submission
- **Save Button**: `id=cash_coll_save`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 3. Automation Workflow (Tester's Perspective)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Step 1: Search Cash Details
1. Navigate to **Billing → Cash Collection**.
2. Click **Add**.
3. Select **Branch**, **Date**, **Counter**, and **Cash Type**.
4. Click **Search**.
5. Verify the **Cash Received** field is populated (even if 0).

### Step 2: Denomination Entry
1. Iterate through the rows in table `id=denomination`.
2. For each currency value specified in Excel (e.g., 2000 x 5, 500 x 10):
    - Locate the row matching the currency value (`class="cash_value"`).
    - Enter the quantity in the `cash_count` input.
3. Verify that the **Total Denomination** updating correctly.

### Step 3: Balance & Difference
1. Enter the **Opening Balance** from Excel.
2. The **Total Cash** should be `Cash Received + Opening Balance`.
3. The **Difference** should be `Total Denomination - Total Cash`.
4. **Logic Check**: If Difference is NOT zero, the automation should still proceed but log the variance as a warning.

### Step 4: Submission & Verification
1. Click **Save**.
2. Handle the success alert (`Cash Collection Added successfully`).
3. Navigate to **Cash Collection List** page.
4. Apply the Date Filter and click Search.
5. Verify the record exists with correct Sales Amount and Cash In Hand.
6. Verify the **Difference** matches the calculated value from the form.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 4. Excel Mapping: BillingDenomination
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Col | Field | Note |
|---|---|---|
| 1 | TestCaseId | |
| 2 | TestStatus | |
| 3 | Branch | |
| 4 | Date | |
| 5 | Counter | |
| 6 | CashType | 1, 2, or 3 |
| 7 | OpeningBalance | |
| 8-15| Denom_2000, 500, 200, 100, 50, 20, 10, 5 | Quantities |
| 16-20| Coins_20, 10, 5, 2, 1 | Quantities |
| 21 | ExpectedDiff | (Calculated for verification) |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 5. Test Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. **TC_BD_01**: Balanced collection (Difference = 0).
2. **TC_BD_02**: Collection with shortage (Difference is Negative).
3. **TC_BD_03**: Collection with excess (Difference is Positive).
4. **TC_BD_04**: CRM-only Cash Type search and save.
5. **TC_BD_05**: Retail-only Cash Type search and save.
6. **TC_BD_ERROR_01**: Submit without entering any denominations.
7. **TC_BD_ERROR_02**: Submit without Opening Balance (should default to 0).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 6. Technical Requirements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Use `Function_Call.dropdown_select` for Select2.
- Implement numeric entry for denominations using a loop over the table rows.
- Capture the "Search Result" cash before entering denominations to ensure math consistency.
- Standard error logging and screenshot capture for mismatches.
