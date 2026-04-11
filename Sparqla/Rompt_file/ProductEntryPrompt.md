# Master Prompt: Other Inventory Purchase Entry Automation

Build complete **Other Inventory Purchase Details** automation for the Retail Automation project. This module is used to record the stock entry of other inventory items from suppliers.

**File to create**: `c:\Retail_Automation\Sparqla\Test_OtherInventory\ProductPurchaseEntry.py`
**Update main.py**: Add `ProductPurchaseEntry` case.

---

### Controller Details (`admin_ret_other_inventory.php`)
**Function**: `purchase_entry($type="", $id="")`

**Switch Cases**:
- `list` → Purchase List page.
- `add` → Add Purchase Entry form.
- `save` → Form submission.

---

### Navigation
- **Menu**: Other Inventory -> Other Inventory Purchase
- **URL**: `admin_ret_other_inventory/purchase_entry/list`
- **Add URL**: `admin_ret_other_inventory/purchase_entry/add`

---

### Form Fields & Mandatory Status
#### Supplier Details
- ✅ Supplier Name (Select2): `id=select_karigar`
- ✅ Supplier Bill No (Text): `id=sup_refno`
- ✅ Supplier Bill Date (Date): `id=sup_billdate`

#### Item Details (Grid Addition)
- ✅ Select Item (Select2): `id=select_item`
- ✅ Quantity (Number): `id=buy_quantity`
- ✅ Rate/Pcs (Number): `id=buy_rate`
- ✅ GST % (Number): `id=tax_amount`
- ✅ Add Item Button: `id=add_item_info` (Adds to table `pur_details`)

#### Action:
- ✅ Save Button: `id=inventory_submit`

---

### Full Business Workflow
1. **Add Purchase Entry Flow**
    - **Navigate**: Other Inventory -> Other Inventory Purchase.
    - **Action**: Click the **ADD** button (`id=add_pur_details`).
    - **Entry (Supplier)**:
        - **Select Supplier**: `id=select_karigar`.
        - **Enter Bill No**: `id=sup_refno`.
        - **Enter Bill Date**: `id=sup_billdate`.
    - **Entry (Items)**:
        - **Select Item**: `id=select_item`.
        - **Enter Quantity**: `id=buy_quantity`.
        - **Enter Rate**: `id=buy_rate`.
        - **Enter GST %**: `id=tax_amount`.
        - **Add to Grid**: Click `id=add_item_info`. (Repeat for multiple items if needed).
    - **Save**: Click the **Save** button (`id=inventory_submit`).
    - **Verify**: Confirm success alert: "Purchase Entry Added successfully".

2. **List Verification Flow**
    - **Navigate**: Other Inventory -> Purchase List.
    - **Filter**: 
        - Select supplier in `id=select_karigar`.
        - Click **Search** (`id=purchase_item_search`).
    - **Verify Table**: Confirm the purchase record (Order Ref No or Supplier Ref No) appears in the `other_item_pur` table.

---

### Success / Failure Messages
- **Success**: "Purchase Entry Added successfully"
- **Failure**: "Unable to proceed the requested process"

---

### Excel Sheet: ProductPurchaseEntry
- **Sheet Name**: `ProductPurchaseEntry`
- **Columns**:
    - **Col 1**: TestCaseId
    - **Col 2**: TestStatus
    - **Col 3**: ActualStatus
    - **Col 4**: SupplierName
    - **Col 5**: BillNo
    - **Col 6**: BillDate (YYYY-MM-DD)
    - **Col 7**: ItemName
    - **Col 8**: Quantity
    - **Col 9**: Rate
    - **Col 10**: GST
    - **Col 11**: ExpectedStatus

---

### Code Patterns & Logic
- **Grid Handling**: The script must handle adding one or multiple items to the `pur_details` table before clicking Save.
- **Select2 handling**: Standard `Function_Call.dropdown_select` pattern.
- **Date Handling**: Input `sup_billdate` might require specific formatting or standard `send_keys`.
- **Consistency**: Follow the `Sparqla` project structure.
