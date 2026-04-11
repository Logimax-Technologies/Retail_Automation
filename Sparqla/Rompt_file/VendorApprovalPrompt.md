Build complete **Vendor Approval (Karigar Approval)** automation for the Retail Automation project.
Follow the **EXACT same code pattern** as `SmithMetalIssue.py`, `LotGenerate.py`, `QCIssueReceipt.py`, `SupplierBillEntry.py`, `PurchaseReturn.py`, and `DebitCreditEntry.py`.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_Vendor\VendorApproval.py
```

## Update main.py
Add `VendorApproval` case to the module dispatcher.

---

## Controller Details (admin_ret_catalog.php)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
Function: `karigar_approval($type="")`

Switch Cases:
- `list` → Karigar Approval List Page (renders `master/karigar/approval_list`).
- `save` → Save Karigar Approval/Rejection.
- `wastages_list` → AJAX fetch for pending Wastage approvals.
- `stones_list` → AJAX fetch for pending Stone approvals.
- `charges_list` → AJAX fetch for pending Charges.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Note: This module handles approving or rejecting the setup of Karigars (Vendors). Approvals can be for Wastage settings or Stone settings.

## Navigation
| Module | Menu Path | List URL | Add URL |
| :--- | :--- | :--- | :--- |
| **Vendor Approval** | Master → Karigar → Karigar Approval | `admin_ret_catalog/karigar_approval/list` | N/A (List handles actions) |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Form Fields & Mandatory Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### List Page: Karigar Approval (master/karigar/approval_list.php)
**Selection & Filter Section:**
- ✅ **Approval For (Radio)**: `name="app[approval_for]"` 
  - 🔹 0 = Wastage
  - 🔹 1 = Stone
- ✅ **Select Karigar (Select2)**: `id="karigar_sel"`
- ✅ **Search Button**: `id="approval_search"`

**Action Section:**
- ✅ **Select Status (Dropdown)**: `id="select_status"`
  - 🔹 1 = Approve
  - 🔹 2 = Reject
  - 🔹 3 = Hold
- ✅ **Submit Button**: `id="status_submit"`

**Item Selection (Table: `id="karigar_wastage_list"` or `id="karigar_stones_list"`):**
- ✅ **Select All Checkbox**: `id="select_all"` (for Wastage) or `id="select_all_stn"` (for Stones).
- ✅ **Individual Checkboxes**: Within the table body.

**OTP Verification (Modal: `id="vendor_otp_modal"`):**
- ✅ **OTP Input**: `id="vendor_trns_otp"`
- ✅ **Verify Button**: `id="verify_vendor_otp"`
- ✅ **Save & Submit Button**: `.submit_vendor_approval`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Full Business Workflow & Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 1. Wastage Approval
- **Context**: Approving product-level wastage/making charges for a Karigar.
- **Workflow**: 
  1. Set `Approval For` = **Wastage**.
  2. Select `Karigar` and click `Search`.
  3. Select rows from the table (or click `Select All`).
  4. Select `Status` = **Approve**.
  5. Click `Submit`.
  6. If OTP modal appears, enter `OTP` and click `Verify`, then `Save And Submit`.

### 2. Stone Approval
- **Workflow**:
  1. Set `Approval For` = **Stone**.
  2. Select `Karigar` and click `Search`.
  3. Select rows from the table (or click `Select All`).
  4. Select `Status` = **Approve**.
  5. Click `Submit`.

### 3. Reject/Hold Row
- **Workflow**:
  1. Select row(s).
  2. Set `Status` to **Reject** or **Hold**.
  3. Submit. 
  4. Verification: Row should disappear from pending list or show updated status when filtered.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Advanced Logic & Constraints (from Knowledge Brain)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Technical Rules
- **Controller Logic**: Approving a broader rule (Category=All) will automatically update/cascade to specific rows to prevent duplicate active settings.
- **OTP Condition**: Required if `vendor_approval_otp_req` is true in profile settings.
- **Data Flow**: Updates `ret_karikar_items_wastage` (Status: 1=Approve, 2=Reject, 3=Hold).

### UI Automation Gotchas
- **Table Visibility**: `wastages` div and `stones` div switch display based on radio buttons.
- **OTP Modal**: Ensure the `disabled` attribute is removed from the `Save And Submit` button after OTP verification.
- **Checked Attribute**: For checkboxes, directly check `is_selected()` or use JS if standard selenium interaction is blocked by labels.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Expected Excel Sheet Structure (Refined)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Sheet: `VendorApproval`**
| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **TestCaseId** | Unique ID |
| 2 | **TestStatus** | Run / Skip |
| 3 | **ApprovalFor** | 0=Wastage, 1=Stone |
| 4 | **KarigarName** | Name for Select2 |
| 5 | **SelectAllRow** | Yes / No |
| 6 | **TargetKey** | Unique text to find row (e.g. Cat+Prod) |
| 7 | **StatusAction** | 1=Approve, 2=Reject, 3=Hold |
| 8 | **UseOTP** | Yes / No |
| 9 | **OTP** | Expected OTP value |
| 10 | **VerifyInTable** | Yes / No |
| 11 | **ActualStatus** | Success / Fail |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Code Patterns to Follow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **Wait for AJAX Table**: Use `WebDriverWait` for elements inside `<tbody>` to appear after clicking Search.
- **Dynamic ID Selection**:
  - Wastage All: `id="select_all"`.
  - Stone All: `id="select_all_stn"`.
- **OTP Flow**:
  1. Click `Submit`.
  2. If `vendor_otp_modal` is visible:
    a. Enter `OTP` in `id="vendor_trns_otp"`.
    b. Click `id="verify_vendor_otp"`.
    c. Click `.submit_vendor_approval`.
