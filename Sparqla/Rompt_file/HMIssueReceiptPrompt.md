# Master Prompt: HM Issue/ Receipt Automation (Finalized)

Build complete HM Issue/ Receipt automation for the Retail Automation project. Follow the EXACT same code pattern as **PurchasePO.py**, **GRNEntry.py**, and **SupplierBillEntry.py**.

**File to create**: `c:\Retail_Automation\Sparqla\Test_Purchase\HMIssueReceipt.py`  
**Update main.py**: Add `HMIssueReceipt` case.

> [!IMPORTANT]
> **Business Rule**: This module is utilized only when the **Hallmark** radio button is set to **No** in the **Supplier Bill Entry** module.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Controller Details (admin_ret_purchase.php)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Function**: `halmarking_issue_receipt($type="")`

**Switch Cases**:
- `list` → HM Issue/ Receipt list page.
- `add` → Halmarking Issue Form (Phase 1).
- `hm_receipt` → Halmarking Receipt Form (Phase 2).

**Submission Functions**:
- `update_halmarking_issue` → Save Issue.
- `update_halmarking_receipt` → Save Receipt.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Navigation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Menu**: Purchase Module → HM Issue/ Receipt
**List URL**: `admin_ret_purchase/halmarking_issue_receipt/list`
**Add Issue URL**: `admin_ret_purchase/halmarking_issue_receipt/add`
**Add Receipt URL**: `admin_ret_purchase/halmarking_issue_receipt/hm_receipt`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Form Fields & Mandatory Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Phase 1: Halmarking Issue (form.php)
- ✅ **PO Ref No** (Select2): `id=select_po_ref_no` (Selecting this auto-fills Karigar or vice versa).
- ✅ **Select Karigar** (Select2): `id=select_karigar`
- ✅ **Item Selection**: Table `id=item_detail`. Use `id=select_all` or individual checkboxes.

### Phase 2: Halmarking Receipt (hm_receipt.php)
- ✅ **HM REF NO** (Select2): `id=select_hm_ref_no` (Select the reference created in Phase 1).
- ✅ **Vendor Ref No** (Input): `id=hm_vendor_ref_id`
- ✅ **Item Table** (id=item_detail):
    - ⬜ **Rejected Pcs/Gwt**: `class=hm_rejected_pcs`, `class=hm_rejected_gwt`
    - ✅ **H.M Charge/Pcs** (Input): `class=hm_charges` (**MANDATORY**).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Full Business Workflow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 1. Issue Flow (Creation)
1. **Navigate**: Purchase Module → HM Issue/ Receipt.
2. **Action**: Click the `ISSUE` button.
3. **Selection**: Select `PO Ref No` and `Karigar`.
4. **Items**: Select the items to be issued using the checkboxes in the table.
5. **Save**: Click the **UPDATE** button (id=halmarking_issue).
6. **Verify**: Confirm success alert: "Halmarking Issued successfully."
7. **Verification (List)**: Navigate to the List page and verify that a new **HM Ref No** has been generated and appears in the table with "Issued" status.

### 2. Receipt Flow (Completion)
1. **Navigate**: Purchase Module → HM Issue/ Receipt.
2. **Action**: Click the `RECEIPT` button.
3. **Selection**: Select the `HM REF NO` from the dropdown.
4. **References**: Enter the `Vendor Ref No`.
5. **Charges**: For each item row, enter the `H.M Charge/Pcs`.
6. **Calculations**: Automation verification of `Received Pcs` and `Total Amount`.
7. **Save**: Click the **Save** button (id=hm_receipt_submit).
8. **Verify**: Confirm success alert: "Halmarking Receipt added successfully."
9. **Verification (List)**: Navigate to the List page, search for the **HM Ref No**, and verify its status is now **Completed**.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Success / Failure Messages
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **Issue Success**: "Halmarking Issued successfully."
- **Receipt Success**: "Halmarking Receipt added successfully."
- **Validation Failure**: "Please Select Ref No." or "Enter The Valid Pieces."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
List Verification Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. **Switch to List View**: The application redirects to `admin_ret_purchase/halmarking_issue_receipt/list`.
2. **Search**: Enter the `HMRefNo` in the search field.
3. **Confirm Entry**: Verify the row appears with correct:
    - **HM Ref No**
    - **Karigar name**
    - **Status** (1=Issued, 2=Completed)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Excel Sheet: HMIssueReceipt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**File Path**: `C:\Users\Dell\Desktop\sqrqlas\Sqarqla_Retail_data2.xlsx`
**Sheet Name**: `HMIssueReceipt`

- Col 1: TestCaseId
- Col 2: TestStatus
- Col 3: ActualStatus
- Col 4: FlowType (Issue / Receipt)
- Col 5: Karigar (Required for Issue)
- Col 6: PORefNo (Required for Issue)
- Col 7: HMRefNo (Required for Receipt)
- Col 8: VendorRefNo (Required for Receipt)
- Col 9: HMChargePerPcs (Required for Receipt)
- Col 10: ExpectedStatus
- Col 11: Remark

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **TC_HM_01 (Issue)**: Select Karigar & PO → Select Items → Update → Verify "Issued" Status in List.
- **TC_HM_02 (Receipt)**: Select HM Ref No → Enter Charges → Save → Verify "Completed" Status in List.
- **TC_HM_REJECT_01**: During Receipt, enter Rejected Pcs → Verify Received Pcs is calculated correctly.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Code Patterns & Logic
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **Wait Pattern**: Use explicit waits for Select2 and dynamic table loading.
- **Row Iteration**: Use a loop to iterate through table rows for multi-item charging.
- **Verification**: Use `Function_Call.assert_text` for toast messages.
