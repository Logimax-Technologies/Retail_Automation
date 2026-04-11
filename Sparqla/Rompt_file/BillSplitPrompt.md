# Bill Split Automation Prompt

This document provides the technical details, field mappings, and logical workflows required to automate the **Bill Split** module. This module allows splitting a single estimation/bill into multiple bills with varied payment modes and customer details.

---

## 1. Module Context & Navigation
- **Module Name**: Bill Split
- **Navigation**: Billing -> Bill Split
- **URL**: `index.php/admin_ret_billing/bill_split/list`

---

## 2. Form Field Mapping & Element IDs

### A. Header & Configuration Section
| Field Label | Element Type | Element ID | Description |
| :--- | :--- | :--- | :--- |
| **EstNo.** | Input Text | `filter_est_no` | Enter Estimation Number (e.g., "2"). |
| **Search Button** | Button | `search_est_no` | Click to search both Sales and Purchase items. |
| **Bill Type** | Radio | `bill_typesales` / `bill_type_salesPurch` | **SALES** or **Sales & Purchase**. |
| **Split Type** | Radio | `billing[split_type]` | **Auto** or **Manual** (for Sales). |
| **Purchase Split** | Input Text | `pu_no_of_split` | Comma-separated values for splitting purchase items. |
| **Purchase Split Button**| Button | `apply_pu_split` | Click to execute the purchase split logic. |

### B. Tables & Results
- **Original Sales Table**: `billing_sale_details`
- **Original Purchase Table**: `split_purchase_item_details` (middle section)
- **Split Sales Table**: `billing_split_sale_details` (bottom section)
- **Split Purchase Table**: `split_purchase_item_details` (bottom-most section)

---

## 3. Automation Workflow & Tester's Logic

### Scenario 1: Sales Only Split (Auto)
1. Select **SALES** as Bill Type.
2. Search by **EstNo**, set **No.of Bills** (e.g., 2), select **Auto**, and click **Split**.
3. Verify row count and validate that total **G.Wt** and **Amount** match the original.

### Scenario 2: Sales & Purchase (Exchange) Split
1. Select **Sales & Purchase** as Bill Type.
2. Search by **EstNo**.
3. **Sales Split**: Select **Auto**, click **Split**. Verify split rows appear in `billing_split_sale_details`.
4. **Purchase Split**:
   - Locate the **Purchase Items** table.
   - Enter comma-separated values (e.g., `5,5`) in the **Purchase Split** input (`pu_no_of_split`).
   - Click the orange **Purchase Split** button (`apply_pu_split`).
   - Verify rows appear in the **Split Purchase Items** table calculation.
5. **Purchase Integrity**:
   - Verify `Sum(Split Purchase G.Wt)` == `Original Purchase G.Wt`.
   - Verify `Sum(Split Purchase Amount)` == `Original Purchase Amount`.

### Step 4: Multi-mode Payment Processing
1. For each sales split row, click the green **Payment (+)** button.
2. Process payments (CSH, CC, CHQ, NB, VCH) as per reference screenshots.
3. Ensure **Balance Amount** for each row's modal becomes `0.00`.

### Step 5: Final Tab Verification & Save
1. Navigate to the **Make Payment** tab.
2. Verify aggregated totals for Cash, Card, NB, and Cheque.
3. Once all row payments are successfully completed, click the final **Save** button (`pay_submit`).

---

## 4. Test Scenarios

| Scenario ID | Scenario Description | Expected Outcome |
| :--- | :--- | :--- |
| **SC_08** | **Both Sales & Purchase Split**: Simultaneously split sales items and purchase/exchange items. | Both tables populate with split rows; Weights and amounts are balanced for both types. |
| **SC_09** | **Exchange Adjustment**: Verify that purchase split values correctly deduct from the corresponding sales split rows. | Net calculation matches expected customer pay amount. |
| **SC_10** | **Final Summary Match**: Verify "Make Payment" tab correctly sums up split payments. | Correct allocation across modes in the final summary view. |

---

## 5. Technical Requirements for Automation Script
- **Table Detection**: The user may need to scroll to reach the `split_purchase_item_details` table at the bottom.
- **Async Handling**: Wait for split tables to re-render after clicking `apply_split` or `apply_pu_split`.
- **Validation Consistency**: Always check total `G.Wt` from original vs split sum before proceeding to payment.
