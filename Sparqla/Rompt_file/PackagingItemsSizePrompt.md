# Master Prompt: Packaging Item Size Automation

Build complete **Packaging Item Size** automation for the Retail Automation project. This submodule is located under the **Other Inventory** main module. Follow the EXACT same code pattern as `InventoryCategory.py` and other master scripts.

**File to create**: `c:\Retail_Automation\Sparqla\Test_OtherInventory\PackagingItemSize.py`
**Update main.py**: Add `PackagingItemSize` case.

---

### Controller Details (`admin_ret_other_inventory.php`)
**Function**: `item_size($type="", $id="")`

**Switch Cases**:
- `list` → Packaging Item Size list page.
- `save` → Modal form submission for adding a new size.
- `update` → Record update via modal.
- `delete` → Record deletion.

---

### Navigation
- **Menu**: Other Inventory -> Packaging Item Size
- **URL**: `admin_ret_other_inventory/item_size/list`

---

### Form Fields & Mandatory Status (Modal: `#confirm-add`)
- **Inputs**:
    - ✅ Size (Text): `id=size_name`
- **Action**:
    - ✅ Add Button (on List Page): `id=add_issue_details` (Click to open modal)
    - ✅ Save Button (in Modal): `id=add_item_size`

---

### Full Business Workflow
1. **Add Packaging Item Size Flow**
    - **Navigate**: Other Inventory -> Packaging Item Size.
    - **Action**: Click the **ADD** button (`id=add_issue_details`) to open the Add Size modal.
    - **Entry**: Enter **Size Name** (`id=size_name`).
    - **Save**: Click the **Save** button (`id=add_item_size`).
    - **Verify**: Confirm success alert: "Item Size Added successfully".

2. **List Verification Flow**
    - **Navigate**: Other Inventory -> Packaging Item Size List.
    - **Search**: Enter the Size Name in the DataTable search box (`//input[@type='search']`).
    - **Columns**:
        - Col 2: Size
        - Col 3: Status

---

### Success / Failure Messages
- **Success**: "Item Size Added successfully"
- **Failure**: "Unable to proceed the requested process"

---

### Excel Sheet: PackagingItemSize
- **Sheet Name**: `PackagingItemSize`
- **Columns**:
    - **Col 1**: TestCaseId
    - **Col 2**: TestStatus
    - **Col 3**: ActualStatus
    - **Col 4**: SizeName
    - **Col 5**: ExpectedStatus

---

### Code Patterns & Logic
- **Modal Handling**: Ensure the script waits for the modal to be visible before interacting with the form fields.
- **Wait Pattern**: Use explicit waits for modal elements and toast messages.
- **Verification**: Use `Function_Call.assert_text` for alert messages.
- **Consistency**: Ensure the script follows the `Sparqla` project structure (BasePage, Function_Call, etc.).
