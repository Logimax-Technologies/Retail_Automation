# Master Prompt: Other Inventory Item Automation

Build complete **Other Inventory Item** automation for the Retail Automation project. This module is used to create specific items (e.g., Packaging Boxes, Gifts) under the categories defined in the Inventory Category module.

**File to create**: `c:\Retail_Automation\Sparqla\Test_OtherInventory\OtherInventory.py`
**Update main.py**: Add `OtherInventory` case.

---

### Controller Details (`admin_ret_other_inventory.php`)
**Function**: `other_inventory($type="", $id="")`

**Switch Cases**:
- `list` → Items list page.
- `add` → Add New Item Form (Multi-tab).
- `save` → Form submission.

---

### Navigation
- **Menu**: Other Inventory -> Other Inventory (or Items)
- **URL**: `admin_ret_other_inventory/other_inventory/list`
- **Add URL**: `admin_ret_other_inventory/other_inventory/add`

---

### Form Fields & Mandatory Status
#### Tab: ITEM DETAILS
- **Selections**:
    - ✅ Item For (Select2): `id=itemfor` (Populated from Categories)
    - ✅ Select Size (Select2): `id=select_size` (Populated from Sizes)
    - ✅ Issue Preference (Dropdown): `name="other[issue_preference]"` (FIFO/FILO)
- **Inputs**:
    - ✅ Name (Text): `id=name`
    - ✅ Unit Price (Number): `name="other[unit_price]"`
- **Checkboxes** (Optional for now):
    - ⬜ Gift Issue to: `name="select_customer_type"`

#### Tab: REORDER DETAILS
- **Table**: `id=total_items`
- **Inputs** (Per Branch):
    - ✅ Min Pcs: `class=min_pcs`
    - ✅ Max Pcs: `class=max_pcs`

#### Action:
- ✅ Save Button: `id=inventory_type_submit`

---

### Full Business Workflow
1. **Add Other Inventory Item Flow**
    - **Navigate**: Other Inventory -> Other Inventory.
    - **Action**: Click the **ADD** button (Look for "Add New Item" or standard Add icon).
    - **Tab 1 (Item Details)**:
        - **Select Item For**: Select category from `id=itemfor`.
        - **Enter Name**: Enter unique item name in `id=name`.
        - **Select Size**: Select size from `id=select_size`.
        - **Enter Unit Price**: Enter price in `name="other[unit_price]"`.
        - **Select Issue Preference**: Choose FIFO/FILO.
    - **Tab 2 (Reorder Details)**:
        - **Click Tab**: Click on "REORDER DETAILS" tab (`//a[contains(text(), 'REORDER DETAILS')]`).
        - **Entry**: Enter Min/Max Pcs in the table for at least the first branch.
    - **Save**: Click the **Save** button (`id=inventory_type_submit`).
    - **Verify**: Confirm success alert: "Item added successfully".

2. **List Verification Flow**
    - **Navigate**: Other Inventory -> Items List.
    - **Search**: Enter the Item Name in the DataTable search box.
    - **Columns**:
        - Col 2: Name
        - Col 3: Size
        - Col 4: Category (Item For)

---

### Success / Failure Messages
- **Success**: "Item added successfully"
- **Failure**: "Unable to proceed your request"

---

### Excel Sheet: OtherInventory
- **Sheet Name**: `OtherInventory`
- **Columns**:
    - **Col 1**: TestCaseId
    - **Col 2**: TestStatus
    - **Col 3**: ActualStatus
    - **Col 4**: ItemFor (Category Name)
    - **Col 5**: Name (Item Name)
    - **Col 6**: Size
    - **Col 7**: UnitPrice
    - **Col 8**: IssuePreference (1=FIFO, 2=FILO)
    - **Col 9**: MinPcs
    - **Col 10**: MaxPcs
    - **Col 11**: ExpectedStatus

---

### Code Patterns & Logic
- **Tab Switching**: Ensure the script clicks the "REORDER DETAILS" tab before attempting to fill Min/Max Pcs.
- **Select2 handling**: Standard `Function_Call.dropdown_select` pattern for Item For and Size.
- **Table Handling**: Use relative XPaths to find inputs within the `total_items` table rows.
- **Consistency**: Follow the `Sparqla` project structure.
