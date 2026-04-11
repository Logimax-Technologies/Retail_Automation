# Old Metal Process Module Automation

Build the **Old Metal Process** automation for the Retail Automation project. This module manages the workflow of issuing and receiving metal for processes like Melting, Testing, Refining, and Polishing.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_OldMetalProcess\OldMetalProcess.py
```

## Update main.py
Add `OldMetalProcess` to the module dispatcher.

---

## Controller & View Logic
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
**Controller**: `Admin_ret_metal_process`  
**Function**: `metal_process_issue($type = 'list')`  
**View**: `ret_metal_process/metal_process/form.php` (Add) / `list.php` (List)

**Main AJAX Calls:**
- `get_ActiveMetalProcess`: Loads process types (Melting, Testing, etc.) into `#select_process`.
- `get_karigar`: Loads vendors into `#karigar`.
- `metal_list`: Fetches pockets/items based on filter.
- `save`: Processes the save operation for Issue/Receipt.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 

## Navigation
- **Menu**: Main Module → Process Issue/Receipt (or direct URL)
- **Add URL**: `admin_ret_metal_process/metal_process_issue/add`
- **List URL**: `admin_ret_metal_process/metal_process_issue/list`

---

## Form Fields & IDs

### 1. Main Header Section
- ✅ **Process For** (Radio): 
  - Issue: `id="issue_process"` (Value: 1)
  - Receipt: `id="receipt_process"` (Value: 2)
- ✅ **Process Type** (Select2): `id="select_process"`, `name="process[id_metal_process]"`
  - *Values: 1=Melting, 2=Testing, 3=Refining, 4=Polishing*
- ✅ **Select Vendor** (Select2): `id="karigar"`, `name="process[id_karigar]"`
- ✅ **Search Button**: `id="process_filter"`

### 2. Melting Issue Section (If Process=Melting & For=Issue)
- ✅ **Select Type** (Select): `id="melting_trans_type"` (1=Old Metal, 2=Tagged, 3=Non Tagged)
- ✅ **Select Pocket** (Select2): `id="select_pocket"`
- ✅ **Details Table**: `id="pocket_details"` (Old Metal) / `id="tagged_pocket_details"` (Tagged) / `id="non_tagged_pocket_details"` (Non Tagged)
- ✅ **Checkbox (per row)**: `name="old_metal_select[]"` or similar (Check the 'all' checkbox: `id="old_metal_select_all"`)

### 3. Receipt Section (If For=Receipt)
- ✅ **Against Melting** (Radio - only for Testing/Refining): 
  - Yes: `id="against_melting_yes"` (Value: 1)
  - No: `id="against_melting_no"` (Value: 2)
- ✅ **Receipt Tables**:
  - Melting: `id="melting_receipt"`
  - Testing: `id="testing_receipt"`
- ✅ **Modal Fields (Weight Adjustment)**:
  - If adding weight details, use the `category_modal` (ID: `update_category` for save).

### 4. Footer Section
- ✅ **Remark**: `id="remark"`, `name="process[remark]"`
- ✅ **Save Button**: `id="issue_submit"`
- ✅ **Cancel Button**: `class="btn-cancel"`

---

## Business Logic & Validations

1. **Workflow Sequence**:
   - Metal is first **Issued** for Melting.
   - Then it is **Received** from Melting (Weight/Purity updated).
   - Received metal can then be **Issued** for Testing/Refining.
2. **Against Melting Logic**:
   - When receiving for Testing, if "Against Melting" = Yes, it fetches items from previous Melting Receipt.
3. **Weight/Loss Calculation**:
   - `Recd WT` + `Prod Loss` should generally reflect the issued weight logic in the system.
4. **Dynamic UI**:
   - Changing "Process For" or "Process Type" hides/shows different boxes (e.g., `.melting_issue`, `.testing_issue`, `.receipt_det`).

---

## Test Scenarios

### Scenario 1: Melting Issue (Old Metal) - Primary Flow
1. **Navigate**: Go to `admin_ret_metal_process/metal_process_issue/add`.
2. **Select Process For**: Click "ISSUE" radio button (`id="issue_process"`).
3. **Select Process Type**: Select "MELTING" from the dropdown (`id="select_process"`).
4. **Select Vendor**: Select a vendor (e.g., "Thirumala") from the dropdown (`id="karigar"`).
5. **Search**: Click the blue "Search" button (`id="process_filter"`).
6. **Wait**: Ensure the `.melting_issue` section becomes visible.
7. **Select Type**: Select "Old Metal" from the dropdown (`id="melting_trans_type"`).
8. **Select Pocket**: Select a pocket number (e.g., "00032") from the Select2 dropdown (`id="select_pocket"`).
9. **Table Verification**: 
   - Verify that rows appear in the `pocket_details` table.
   - Verify columns: Pocket No, Metal Type, Category, Pcs, G.Wt (Grams), N.Wt (Grams), etc.
10. **Select Item**: Click the checkbox for the target pocket number in the first column.
11. **Remark**: Enter a remark in the `#remark` textarea.
12. **Save**: Scroll down (if needed) and click the "Save" button (`id="issue_submit"`).
13. **Verify List & Capture ID**:
    - Redirect to `admin_ret_metal_process/metal_process_issue/list`.
    - Select **DateRange** = Today.
    - Search for the **Karigar** name.
    - Match the first row and capture the **Process No.**.
    - This ID is automatically stored in the Excel sheet for the next **Receipt** test case.


### Scenario 2: Melting Receipt - Detailed Flow
1. **Navigate**: Go to `admin_ret_metal_process/metal_process_issue/add`.
2. **Select Process For**: Click "RECEIPT" radio button (`id="receipt_process"`).
3. **Select Process Type**: Select "MELTING" from the dropdown (`id="select_process"`).
4. **Search**: Click the blue "Search" button (`id="process_filter"`).
5. **Table**: Locate the `melting_receipt` table and the target **Process No** (e.g., "00045").
6. **Open Modal**: Click the green "plus" button (`.btn-success` inside the Category column) for the target row to open the **Add Weight** modal (`id="category_modal"`).
7. **Fill Modal**:
   - Select **Category**, **Section**, **Product**, **Design**, **Sub Design**.
   - Enter **Pcs** and **Weight**.
   - Click **Save** inside the modal (`id="update_category"`).
8. **Verify Reflection**: 
   - The **Weight** value from the modal must reflect in the **Recd WT(Grams)** column of the main table.
   - Verify that **Prod Loss(Grams)** is automatically calculated as: `G.Wt (Grams)` - `Recd WT(Grams)`.
9. **Finalize Row**: 
   - Enter **Charges(RS)** if applicable.
   - Enter **Ref No**.
10. **Save**: Click the main "Save" button (`id="issue_submit"`).
11. **Verify**: Check the list page for the updated process status.

### Scenario 3: Testing Issue
1. **Navigate**: Go to `admin_ret_metal_process/metal_process_issue/add`.
2. **Select Process For**: Click "ISSUE" radio button (`id="issue_process"`).
3. **Select Process Type**: Select "TESTING" from the dropdown (`id="select_process"`).
4. **Select Vendor**: Select a vendor (e.g., "Thirumala") and click "Search" (`id="process_filter"`).
5. **Wait**: Ensure the `.testing_issue` section and the `testing_process_details` table are visible.
6. **Select Item**: 
   - Locate the row matching the target **Process No** (e.g., "00051").
   - Click the checkbox in the first column.
   - Verify that **Received Wt (Grams)** and **Purity** are populated from the previous Melting flow.
7. **Save**: Click the main "Save" button (`id="issue_submit"`).

### Scenario 4: Testing Receipt (Against Melting)
1. **Navigate**: Go to `admin_ret_metal_process/metal_process_issue/add`.
2. **Select Process For**: Click "RECEIPT" radio button (`id="receipt_process"`).
3. **Select Against Melting**: Click "Yes" radio button (`id="against_melting_yes"`).
4. **Select Process Type**: Select "TESTING" from the dropdown (`id="select_process"`).
5. **Search**: Click "Search" (`id="process_filter"`).
6. **Selection Options**:
   - **Select Process**: Choose the process from the dropdown (`id="select_metal_process"`).
   - **Mode**: Choose "Add to Next Process" (`id="add_to_next_process"`) or "Add to Stock" (`id="add_to_acc_stock"`).
   - **Purity**: Enter the purity details in the table's purity field.
7. **Table Verification**:
   - Verify that the item details appear in the `against_melting_receipt` and `testing_issue_details` tables.
   - Verify **PROD LOSS WT** calculation.
8. **Save**: Click the main "Save" button (`id="issue_submit"`).

---

## Excel Data Structure

### Sheet: `OldMetalProcess`

| TestCaseId | TestStatus | Actual Status | ProcessFor | AgainstMelting | ProcessType | Vendor | MeltingType | PocketNo | ProcessNo | ModalCategory | ModalSection | ModalProduct | ModalDesign | ModalSubDesign | ModalPcs | ModalWeight | Mode | Purity | Charges | RefNo | Remark |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC001 | Run | | Issue | | Melting | Thirumala | Old Metal | 00032 | | | | | | | | | | | | | Issue Melting |
| TC002 | Run | | Receipt | | Melting | Thirumala | | | 00045 | Gold 916 | G Section | Product1 | Design1 | SubDesign1 | 1 | 19.5 | | | 150 | REF123 | Receipt Melting |
| TC003 | Run | | Issue | | Testing | Thirumala | | | 00051 | | | | | | | | | | | | Issue Testing |
| TC004 | Run | | Receipt | Yes | Testing | | | | | | | | | | | Add to Stock | 91.6 | 200 | REF456 | Receipt Testing |

---

## Code Pattern Hints
- **Select2**: Use standard handlers for `#karigar`, `#select_process`, `#select_pocket`, and `#select_metal_process`.
- **Radio Buttons**: Handle "Process For" (`#issue_process`/`#receipt_process`), "Against Melting" (`#against_melting_yes`/`#against_melting_no`), and "Mode" (`#add_to_next_process`/`#add_to_acc_stock`).
- **Modal Handling**: 
  - After clicking the green `+` button, wait for `#category_modal` to be visible.
  - After clicking "Save" in the modal, wait for the modal to disappear and the main table to update.
- **Calculations**: Use `get_attribute('value')` to fetch weights and verify the subtraction logic for `Prod Loss`.
- **Dynamic Linkage**: The script captures the `Process No` after an **Issue** and updates the `PocketNo` for the subsequent **Receipt** row in Excel to ensure continuity.
- **Tables**: Use `id="process_list"` on the list page to verify row data after saving.
