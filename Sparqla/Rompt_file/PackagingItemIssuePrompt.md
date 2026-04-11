# Master Prompt: Packaging Items Issue Automation

Build complete **Packaging Items Issue** automation for the Retail Automation project. This module is used to issue items (like gift boxes or bags) to customers or branches, potentially linked to a sales bill.

**File to create**: `c:\Retail_Automation\Sparqla\Test_OtherInventory\PackagingItemIssue.py`
**Update main.py**: Add `PackagingItemIssue` case.

---

### Controller Details (`admin_ret_other_inventory.php`)
**Functions**:
- `issue_item/list` → Page with issue history and "Add" modal.
- `issue_item/save` → Modal form submission.

---

### Navigation
- **Menu**: Other Inventory -> Packaging Item Issue
- **URL**: `admin_ret_other_inventory/issue_item/list`

---

### UI Elements (Add Modal: `#confirm-add`)
- **Open Modal Button**: `id=add_issue_details`
- **Select Branch (Select2)**: `id=branch_select`
- **Select Item (Select2)**: `id=select_item`
- **Select Bill No (Select2)**: `id=select_bill_no` (Optional)
- **No of Piece (Number)**: `id=issue_total_pcs`
- **Description (Textarea)**: `id=remarks`
- **Save Button**: `id=item_issue`

---

### Full Business Workflow
1. **Issue Packaging Item Flow**
    - **Navigate**: Other Inventory -> Packaging Item Issue.
    - **Action**: Click the **Add** button (`id=add_issue_details`) to open the modal.
    - **Select Branch**: `id=branch_select` (if available, otherwise use default).
    - **Select Item**: `id=select_item` (e.g., "Gift Box").
    - **Select Bill No**: `id=select_bill_no` (Search by bill number if available).
    - **Enter Pieces**: `id=issue_total_pcs` (e.g., "5").
    - **Enter Remarks**: `id=remarks` (e.g., "Issued to customer").
    - **Save**: Click the **Save & Close** button (`id=item_issue`).
    - **Verify**: Confirm success alert: "Item Issued successfully".

2. **List Verification Flow**
    - **Navigate**: Other Inventory -> Packaging Item Issue List.
    - **Filter**: 
        - Use Branch filter / Date range if needed.
        - Click **Search** (`id=search_issue_item`).
    - **Verify Table**: Confirm the mapping appears in the `issue_list` table with correct Item Name and Pieces.

---

### Success / Failure Messages
- **Success**: "Item Issued successfully"
- **Failure**: "Unable to proceed the requested process"

---

### Excel Sheet: PackagingItemIssue
- **Sheet Name**: `PackagingItemIssue`
- **Columns**:
    - **Col 1**: TestCaseId
    - **Col 2**: TestStatus
    - **Col 3**: ActualStatus
    - **Col 4**: BranchName
    - **Col 5**: ItemName
    - **Col 6**: BillNo
    - **Col 7**: Pieces
    - **Col 8**: Remarks
    - **Col 9**: ExpectedStatus

---

### Code Patterns & Logic
- **Modal Handling**: The script must click the Add button, wait for the modal `#confirm-add` to be visible, and then fill the fields.
- **Select2 handling**: Standard `Function_Call.dropdown_select` pattern for Branch, Item, and Bill No.
- **Consistency**: Follow the `Sparqla` project structure.
