# Master Prompt: Inventory Category Automation

Build complete **Inventory Category** automation for the Retail Automation project. This submodule is located under the **Other Inventory** main module. Follow the EXACT same code pattern as `NonTagReceipt.py`, `LotGenerate.py`, and other existing inventory scripts.

**File to create**: `c:\Retail_Automation\Sparqla\Test_OtherInventory\InventoryCategory.py`
**Update main.py**: Add `InventoryCategory` case.

---

### Controller Details (`admin_ret_other_inventory.php`)
**Function**: `inventory_category($type="", $id="")`

**Switch Cases**:
- `list` → Inventory Category list page.
- `add` → Inventory Category Form.
- `save` → Form submission.
- `update` → Record update.
- `delete` → Record deletion.

---

### Navigation
- **Menu**: Other Inventory -> Inventory Category
- **URL**: `admin_ret_other_inventory/inventory_category/list`
- **Add URL**: `admin_ret_other_inventory/inventory_category/add`

---

### Form Fields & Mandatory Status
- **Inputs**:
    - ✅ Name (Text): `id=name`
- **Radio Buttons**:
    - ✅ Outward Type: `name="item[outward_type]"`
        - Estimation: `id=outward_type2` (Value: 2)
        - Billing: `id=outward_type1` (Value: 1)
    - ✅ As billable: `name="item[as_bill]"`
        - Free: `id=as_bill1` (Value: 0)
        - Cost: `id=as_bill2` (Value: 1)
    - ✅ Expiry Date Validate: `name="item[exp_date]"`
        - No validity: `id=exp_date1` (Value: 0)
        - Having: `id=exp_date2` (Value: 1)
    - ✅ Reorder Level: `name="item[reorder_level]"`
        - Yes: `id=reorder_level1` (Value: 1)
        - No: `id=reorder_level2` (Value: 2)
- **Action**:
    - ✅ Save Button: `type=submit` (within class `btn-primary`)

---

### Full Business Workflow
1. **Add Inventory Category Flow**
    - **Navigate**: Other Inventory -> Inventory Category.
    - **Action**: Click the **ADD** button (Look for button with "Add other details" or standard Add button icon).
    - **Entry**: Enter Category **Name** (`id=name`).
    - **Selection**: Select **Outward Type** (Billing or Estimation) via Radio Buttons.
    - **Selection**: Select **As Billable** (Free or Cost) via Radio Buttons.
    - **Selection**: Select **Expiry Date Validate** (No validity or Having) via Radio Buttons.
    - **Selection**: Select **Reorder Level** (Yes or No) via Radio Buttons.
    - **Save**: Click the **Save** button.
    - **Verify**: Confirm success alert: "Category added successfully".

2. **List Verification Flow**
    - **Navigate**: Other Inventory -> Inventory Category List.
    - **Search**: Enter the Category Name in the DataTable search box.
    - **Columns**:
        - Col 2: Name
        - Col 3: Outward Type
        - Col 4: Billable
        - Col 5: Expiry Date Validate
        - Col 6: Reorder Level

---

### Success / Failure Messages
- **Success**: "Category added successfully"
- **Failure**: "Unable to proceed your request"

---

### Excel Sheet: InventoryCategory
- **Sheet Name**: `InventoryCategory`
- **Columns**:
    - **Col 1**: TestCaseId
    - **Col 2**: TestStatus
    - **Col 3**: ActualStatus
    - **Col 4**: Name
    - **Col 5**: OutwardType (1=Billing, 2=Estimation)
    - **Col 6**: AsBillable (0=Free, 1=Cost)
    - **Col 7**: ExpiryDateValidate (0=No validity, 1=Having)
    - **Col 8**: ReorderLevel (1=Yes, 2=No)
    - **Col 9**: ExpectedStatus

---

### Code Patterns & Logic
- **Wait Pattern**: Use explicit waits for form elements and toast messages.
- **Verification**: Use `Function_Call.assert_text` for alert messages.
- **Consistency**: Ensure the script follows the `Sparqla` project structure (BasePage, Function_Call, etc.).
- **URL Handling**: Directly navigate if the menu click is unreliable, but prioritize menu interaction.
