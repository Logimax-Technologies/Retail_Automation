# Jewel Not Delivered Automation Prompt

This document provides all the technical details, field mappings, and logical workflows required to automate the **Jewel Not Delivered (Item Delivery)** module in the Retail Automation system.

---

## 1. Module Context & Navigation
- **Module Name**: Jewel Not Delivered / Item Delivery
- **Navigation**: Billing -> Jewel Not Delivered
- **URL**: `index.php/admin_ret_billing/item_delivery/list`
- **Purpose**: To search for items that have been billed but not yet delivered, and to mark them as "Delivered".

---

## 2. Form Field Mapping & Element IDs

### A. Search & Filter Section
| Field Label | Element Type | Element ID | Description |
| :--- | :--- | :--- | :--- |
| **Bill No** | Input Text | `filter_bill_no` | Enter the specific Bill Number to filter the list. |
| **Branch** | Select2 / Hidden | `branch_select` / `branch_filter` | Select branch (if available). |
| **Date Range** | DateRangePicker | `dt_range` | Select the From and To date range for billed items. |
| **Search Button** | Button | `item_delivery_search` | Click to populate the delivery list table. |

### B. Action Section
| Field Label | Element Type | Element ID | Description |
| :--- | :--- | :--- | :--- |
| **Deliver Button** | Button | `item_deliver` | Click to mark selected items as delivered. |

### C. Delivery List Table
- **Table ID**: `delivery_list`
- **Columns**:
    1. **Bill No**: Contains a checkbox `name="bill_det_id[]"` (only if status is "Yet to Deliver").
    2. **Bill Date**: Date of the transaction.
    3. **Branch**: Branch name.
    4. **Customer**: Customer Name.
    5. **Mobile**: Customer Mobile Number.
    6. **Product**: Product Name/Description.
    7. **Status**: Badge indicating "Yet to Deliver" (Red) or "Delivered" (Green).
    8. **Delivered Date**: Date of delivery (populated after action).
    9. **Delivered By**: Name of the user who delivered (populated after action).

---

## 3. Automation Workflow (Tester's Perspective)

### Step 1: Search for Undelivered Item
1. Enter the target **Bill No** in the `filter_bill_no` field.
2. Select the appropriate **Date Range** using the `dt_range` picker.
3. Click the **Search** button (`item_delivery_search`).
4. Wait for the `delivery_list` table to refresh and show results.

### Step 2: Select and Deliver
1. Locate the row matching the target Bill No in the `delivery_list` table.
2. Verify the **Status** is "Yet to Deliver".
3. Click the **Checkbox** (`name="bill_det_id[]"`) for that specific row.
4. Click the **Deliver** button (`item_deliver`).

### Step 3: Verification
1. Wait for the success toaster notification (e.g., "Delivery Status Updated Successfully.").
2. Verify the table refreshes automatically.
3. Confirm the **Status** for the target Bill No has changed to "Delivered".
4. (Optional) Verify the **Delivered Date** matches the current system date.

---

## 4. Excel Data Mapping (`JewelNotDelivered.xlsx`)

| Column Name | Description | Example Value |
| :--- | :--- | :--- |
| **TestCaseId** | Unique identifier for the test case | TC_JND_01 |
| **TestStatus** | Run this test? (Yes/No) | Yes |
| **ActualStatus** | Result (Pass/Fail) - updated by script | Pass |
| **Branch** | Branch name for filtering | HEAD OFFICE |
| **BillNo** | Target Bill Number | BILL-2026-001 |
| **FromDate** | Search range start date | 01-03-2026 |
| **ToDate** | Search range end date | 21-03-2026 |
| **ExpectedResult** | Expected outcome | Status update to Delivered |

---

## 5. Test Scenarios

| Scenario ID | Scenario Description | Expected Outcome |
| :--- | :--- | :--- |
| **SC_01** | Deliver a single item by searching Bill No | Success message and row status update. |
| **SC_02** | Deliver multiple items by checking multiple checkboxes | Success message for all items. |
| **SC_03** | Search for a delivered item | Verify checkbox is NOT available/visible. |
| **SC_04** | Click Deliver without selecting any bill | Warning toaster: "Please Select The Bill No". |

---

## 6. Technical Requirements for Automation Script
- **Wait Policy**: Wait for `div.overlay` to be hidden before interacting with the table after search.
- **Handling Checkboxes**: Ensure the script only clicks the checkbox if the status is "Yet to Deliver".
- **Toaster Verification**: Use `WebDriverWait` to capture the `$.toaster` notification.
- **Refresh Check**: The script should re-search or verify the row status after the "Deliver" action completes.
