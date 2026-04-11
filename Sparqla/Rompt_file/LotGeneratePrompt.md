# Master Prompt: Lot Generate Automation (Refined)

Build complete Lot Generate automation for the Retail Automation project. Follow the EXACT same code pattern as `PurchasePO.py`, `GRNEntry.py`, `SupplierBillEntry.py`, and `QCIssueReceipt.py`.

**File to create**: `c:\Retail_Automation\Sparqla\Test_lot\LotGenerate.py`
**Update main.py**: Add `LotGenerate` case.

### Controller Details (`admin_ret_purchase.php`)
**Function**: `lot_generate($type="")`

**Switch Cases**:
- `list` → Lot Generate list page.
- `add` → Lot Generate Form.
- `po_details` → AJAX to load PO Ref Nos.
- `get_po_balance_details` → AJAX to load items.

**Submission Function**:
- `generateLot` (POST request to `admin_ret_purchase/generateLot`)

---

### Navigation
- **Menu**: Purchase Module → Lot Generate
- **URL**: `admin_ret_purchase/lot_generate/list`
- **Add Lot URL**: `admin_ret_purchase/lot_generate/add`

---

### Form Fields & Mandatory Status
- **Selection**:
    - ✅ Financial Year (Select2): `id=pur_fin_year_select`
    - ✅ PO Ref No (Select2): `id=select_po_ref_no`
    - ✅ Select Employee (Select2): `id=emp_select`
    - ✅ Remark: `id=remark`
- **Item Table (`id=item_detail`)**:
    - ✅ Item Selection: Table `id=item_detail`. Use `id=select_all` or individual checkboxes `class=qc_item_select`.
    - ✅ Hidden Fields (Verify presence): `class=po_item_id`, `class=cat_id`, `class=pro_id`.
    - ⬜ Pcs/Gwt/Nwt: `class=lot_pcs`, `class=lot_gross_wt`, `class=lot_net_wt` (Readonly).
- **Update Action**:
    - ✅ Button: `id=generate_lot`

---

### Full Business Workflow
1. **Lot Generation Flow**
    - **Navigate**: Purchase Module → Lot Generate List.
    - **Action**: Click the **ADD** button (`id=add_Order`).
    - **Selection**: Select Financial Year and PO Ref No (`id=select_po_ref_no`). Select Employee (`id=emp_select`).
    - **Items**: Select the items using the `class=qc_item_select` checkboxes.
    - **Save**: Click the **UPDATE** button (`id=generate_lot`).
    - **Verify**: Confirm success alert: "Lot Created successfully."
    - **Capture**: Capture the generated "Ref No" from the success alert or list search.

2. **List Verification Flow**
    - **Navigate**: Inventory → Lot Generate List (`admin_ret_lot/lot_inward/list`).
    - **Filter (Optional)**:
        - ✅ Click Date Range Picker (`id=ltInward-dt-btn`).
        - ✅ Select range (e.g., **Today**).
        - ✅ Select **Metal** (`id=metal`).
        - ✅ Select **Employee** (`id=select_emp`).
        - ✅ Select **Stock Type** (`id=lot_type` - Non Tag/Tagged).
        - ✅ Click **Search** (`id=lot_inward_search`).
    - **Search**: Enter the Captured Ref No in the DataTable search box (`//div[@id="lot_inward_list_filter"]//input`).
    - **Columns**:
        - Col 2: Ref No (Lot No)
        - Col 4: Employee
        - Col 8: Net Wt
        - Col 12: Action (Verify Delete/Edit buttons presence).

---

### Success / Failure Messages
- **Success**: "Lot Created successfully."
- **Validation Failure**: "Please Select Any One Item" or "Please Select The Item".

---

### Excel Sheet: LotGenerate
- **File Path**: `C:\Users\Dell\Desktop\sqrqlas\Sqarqla_Retail_data2.xlsx`
- **Sheet Name**: `LotGenerate`

- **Col 1**: TestCaseId
- **Col 2**: TestStatus
- **Col 3**: ActualStatus
- **Col 4**: FlowType
- **Col 5**: Employee
- **Col 6**: PORefNo
- **Col 7**: ExpectedStatus
- **Col 8**: Remark

---

### Test Scenarios
- **TC_LG_01**: Select PO Ref No → Select Employee → Select Items → Update → Verify Status.
- **TC_LG_MULTI_01**: Process multiple items from a single PO Ref No.
- **TC_LG_REMARK_01**: Add a remark and verify it is saved (manual check or DB).

---

### Code Patterns & Logic
- **Wait Pattern**: Use explicit waits for Select2 and dynamic table loading (wait for `#item_detail tbody tr`).
- **Row Iteration**: Use a loop for multi-item processing.
- **Verification**: Use `Function_Call.assert_text` for toast messages.
- **Consistency**: Ensure the script follows the `Sparqla` project structure (BasePage, Function_Call, etc.).
