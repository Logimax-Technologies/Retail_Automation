# Master Prompt: Non-Tag Receipt Automation

Build complete Non-Tag Receipt automation for the Retail Automation project. Follow the EXACT same code pattern as `PurchasePO.py`, `GRNEntry.py`, `SupplierBillEntry.py`, and `LotGenerate.py`.

**File to create**: `c:\Retail_Automation\Sparqla\Test_Inventory\NonTagReceipt.py`
**Update main.py**: Add `NonTagReceipt` case.

---

### Controller Details (`admin_ret_purchase.php`)
**Function**: `nontag_receipt($type="", $id="", $status="")`

**Switch Cases**:
- `list` → Non-Tag Receipt list page.
- `add` → Non-Tag Receipt Form.
- `get_NontagLots` → AJAX to load Lot Nos.
- `save` → Form submission.

---

### Navigation
- **Menu**: Inventory -> Non-Tag Receipt
- **URL**: `admin_ret_purchase/nontag_receipt/list`
- **Add URL**: `admin_ret_purchase/nontag_receipt/add`

---

### Form Fields & Mandatory Status
- **Selection**:
    - ✅ Lot No (Select2): `id=select_lot`
    - ✅ Select Product (Select2): `id=product_sel`
    - ✅ Select Design (Select2): `id=design_sel`
    - ✅ Select Sub Design (Select2): `id=sub_design_sel`
    - ✅ NonTag Branch (Select2): `id=branch_select`
    - ✅ NonTag Section (Select2): `id=select_section`
- **Inputs**:
    - ✅ Pieces: `class=nt_pcs`
    - ✅ Gross Wt: `class=nt_grswt`
    - ⬜ Less Wt: `class=nt_lesswt` (Disabled, auto-calculated or fetched)
    - ✅ Net Wt: `class=nt_netwt`
    - ✅ Remark: `id=remark`
- **Action**:
    - ✅ Save Button: `id=nt_receipt_submit`

---

### Full Business Workflow
1. **Non-Tag Receipt Flow**
    - **Navigate**: Inventory -> Non-Tag Receipt.
    - **Action**: Click the **ADD** button (`id=add_Order`).
    - **Selection**: Select **Lot No** (`id=select_lot`).
    - **Verification**: Wait for details (Metal, Category, Pieces, etc.) to load on the right side and in the summary table.
    - **Entry**: Enter Pieces (`class=nt_pcs`), Gross Wt (`class=nt_grswt`), and Net Wt (`class=nt_netwt`).
    - **Remark**: Enter a remark (`id=remark`).
    - **Save**: Click the **Save** button (`id=nt_receipt_submit`).
    - **Verify**: Confirm success alert: "NonTag Receipt Added Successfully".
    - **Capture**: Optional - capture Receipt No from list if needed.

2. **List Verification Flow**
    - **Navigate**: Inventory -> Non-Tag Receipt List.
    - **Search**: Enter the Lot No or Receipt No in the DataTable search box.
    - **Columns**:
        - Col 2: Date
        - Col 3: Receipt No
        - Col 4: Lot No
        - Col 5: Product
        - Col 7: Net Wt

---

### Success / Failure Messages
- **Success**: "NonTag Receipt Added Successfully"
- **Failure**: "Unable to proceed the requested process"

---

### Excel Sheet: NonTagReceipt
- **Sheet Name**: `NonTagReceipt`
- **Columns**:
    - **Col 1**: TestCaseId
    - **Col 2**: TestStatus
    - **Col 3**: ActualStatus
    - **Col 4**: LotNo
    - **Col 5**: Product
    - **Col 6**: Design
    - **Col 7**: SubDesign
    - **Col 8**: Branch
    - **Col 9**: Section
    - **Col 10**: Pieces
    - **Col 11**: GrossWt
    - **Col 12**: NetWt
    - **Col 13**: Remark
    - **Col 14**: ExpectedStatus

---

### Code Patterns & Logic
- **Wait Pattern**: Use explicit waits for Select2 and value updates in the table.
- **Dynamic Values**: Many fields (Product, Design, Weights) will auto-fill after Lot selection. Verify these match the Excel data or use them as-is.
- **Verification**: Use `Function_Call.assert_text` for toast messages.
- **Consistency**: Ensure the script follows the `Sparqla` project structure (BasePage, Function_Call, etc.).
