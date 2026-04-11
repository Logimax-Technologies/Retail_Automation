# Master Prompt: QC Issue/ Receipt Automation (Refined)

Build complete QC Issue/ Receipt automation for the Retail Automation project. Follow the EXACT same code pattern as `PurchasePO.py`, `GRNEntry.py`, `SupplierBillEntry.py`, and `HMIssueReceipt.py`.

**File to create:** `c:\Retail_Automation\Sparqla\Test_Purchase\QCIssueReceipt.py`  
**Update `main.py`:** Add `QCIssueReceipt` case.

---

## Controller Details (admin_ret_purchase.php)
**Function:** `qc_issue_receipt($type="",$id="")`

### Switch Cases:
- `list` → QC Issue/ Receipt list page.
- `add` → QC Issue Form (Phase 1).
- `qc_entry` → QC Receipt Form (Phase 2).

### Submission Functions:
- `update_qc_issue` → Save Issue.
- `update_qc_status` → Save Receipt.

---

## Navigation
- **Menu:** Purchase Module → QC Issue/ Receipt List
- **URL:** `admin_ret_purchase/qc_issue_receipt/list`
- **Add Issue URL:** `admin_ret_purchase/qc_issue_receipt/add`
- **Add Receipt URL:** `admin_ret_purchase/qc_issue_receipt/qc_entry`

---

## Form Fields & Mandatory Status

### Phase 1: QC Issue (form.php)
- ✅ **PO Ref No** (Select2): `id=select_po_ref_no`
- ✅ **Select Employee** (Select2): `id=emp_select`
- ✅ **Item Selection:** Table `id=item_detail`. Use `id=select_all` or individual checkboxes `class=qc_item_select`.

### Phase 2: QC Receipt (qc_entry.php)
- ✅ **Supplier Bill Entry (PO REF NO)** (Select2): `id=select_ref_no`
- ✅ **Item Table** (`id=item_detail`):
  - ⬜ **Rejected Pcs:** `class=failed_pcs`
  - ⬜ **Rejected Gwt/Lwt/Nwt:** `class=failed_gwt`, `class=failed_lwt`, `class=failed_nwt`
  - ⬜ **Accepted Pcs/Gwt/Lwt/Nwt:** `class=qc_acc_pcs`, `class=qc_acc_gwt`, `class=qc_acc_lwt`, `class=qc_acc_nwt`

---

## Full Business Workflow

### 1. Issue Flow (Creation)
1. Navigate: Purchase Module → QC Issue/ Receipt List.
2. Action: Click the **QC ISSUE** button.
3. Selection: Select PO Ref No (`id=select_po_ref_no`) and Employee (`id=emp_select`).
4. Items: Select the items using the `class=qc_item_select` checkboxes.
5. Save: Click the **UPDATE** button (`id=qc_issue_submit`).
6. Verify: Confirm success alert: "QC Issued successfully."
7. Capture: Capture the generated "Ref No" from the success alert or list.

### 2. Receipt Flow (Completion)
1. Navigate: Purchase Module → QC Issue/ Receipt List.
2. Action: Click the **QC RECEIPT** button.
3. Selection: Select the captured "Ref No" in the `id=select_ref_no` dropdown.
4. Table: Verify item details load in `#item_detail tbody`.
5. Items: Enter Rejected pieces in `class=failed_pcs`. Verify `class=qc_acc_pcs` updates.
6. Save: Click the **UPDATE** button (`id=update_qc_status`).
7. Verify: Confirm success alert: "QC Updated successfully."

---

## Success / Failure Messages
- **Issue Success:** "QC Issued successfully."
- **Receipt Success:** "QC Updated successfully."
- **Validation Failure:** "Please Select Employee." or "No Records Found."

---

## List Verification Flow
**View:** `admin_ret_purchase/qc_issue_receipt/list`  
**Search:** Enter the Captured Ref No in the DataTable search.  
**Columns:**
- Col 2: Ref No
- Col 4: Po No
- Col 5: Karigar
- Col 6: Employee
- Col 15: Action (Verify button presence for status).

---

## Excel Sheet: QCIssueReceipt
**File Path:** `C:\Users\Dell\Desktop\sqrqlas\Sqarqla_Retail_data2.xlsx`  
**Sheet Name:** `QCIssueReceipt`

- **Col 1:** TestCaseId
- **Col 2:** TestStatus
- **Col 3:** ActualStatus
- **Col 4:** FlowType (Issue / Receipt)
- **Col 5:** Employee / Karigar
- **Col 6:** PORefNo
- **Col 7:** ExpectedStatus
- **Col 8:** Remark

---

## Test Scenarios
- **TC_QC_01 (Issue):** Select Employee & PO → Select Items → Update → Verify Status.
- **TC_QC_02 (Receipt):** Select PO Ref No → Update → Verify Status.
- **TC_QC_REJECT_01:** During Receipt, enter Rejected Pcs → Verify it is saved correctly.

---

## Code Patterns & Logic
- **Wait Pattern:** Use explicit waits for Select2 and dynamic table loading.
- **Row Iteration:** Use a loop for multi-item processing if needed.
- **Verification:** Use `Function_Call.assert_text` for toast messages.
