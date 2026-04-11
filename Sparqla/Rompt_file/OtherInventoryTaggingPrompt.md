# Master Prompt: Other Inventory Tagging Automation

Build complete **Other Inventory Tagging** automation for the Retail Automation project. This module is used to generate individual pieces/tags for items brought in through Purchase Entry.

**File to create**: `c:\Retail_Automation\Sparqla\Test_OtherInventory\OtherInventoryTagging.py`
**Update main.py**: Add `OtherInventoryTagging` case.

---

### Controller Details (`admin_ret_other_inventory.php`)
**Functions**:
- `product_details/list` → Page with tagging history.
- `product_details/add` → Tagging form.
- `product_details/save` → Form submission.

---

### Navigation
- **Menu**: Other Inventory -> Other Inventory Tagging
- **URL**: `admin_ret_other_inventory/product_details/list`
- **Add URL**: `admin_ret_other_inventory/product_details/add`

---

### UI Elements (Add Page)
- **Select Ref No (Select2)**: `id=select_ref_no` (This is the Reference No from the Purchase Entry module).
- **Select All Checkbox**: `id=select_all`
- **Tagging Table**: `id=prod_details`
- **Save Button**: `id=prod_inventory_submit`

---

### Full Business Workflow
1. **Tagging Flow**
    - **Navigate**: Other Inventory -> Other Inventory Tagging.
    - **Action**: Click the **Add** button.
    - **Select Reference**: Choose a purchase reference from `id=select_ref_no`.
    - **Wait**: Wait for the table `prod_details` to populate with items.
    - **Select Items**: Click the **Select All** checkbox (`id=select_all`).
    - **Save**: Click the **Save** button (`id=prod_inventory_submit`).
    - **Verify**: Confirm success alert: "Product Details Added successfully".

2. **List Verification Flow**
    - **Navigate**: Other Inventory -> Other Inventory Tagging List.
    - **Filter**: 
        - Enter Ref No in the search box.
    - **Verify Table**: Confirm the tagged records appear in the list.

---

### Success / Failure Messages
- **Success**: "Product Details Added successfully"
- **Failure**: "Unable to proceed the requested process"

---

### Excel Sheet: OtherInventoryTagging
- **Sheet Name**: `OtherInventoryTagging`
- **Columns**:
    - **Col 1**: TestCaseId
    - **Col 2**: TestStatus
    - **Col 3**: ActualStatus
    - **Col 4**: RefNo (Purchase Reference to tag)
    - **Col 5**: ExpectedStatus

---

### Code Patterns & Logic
- **Dynamic Table Handling**: After selecting the Reference No, the table is populated via AJAX. The script must wait for the table rows to appear before clicking "Select All".
- **Select2 handling**: Standard `Function_Call.dropdown_select` pattern for Ref No.
- **Consistency**: Follow the `Sparqla` project structure.
