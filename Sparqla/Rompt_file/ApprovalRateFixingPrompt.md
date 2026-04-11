Build complete **Approval Rate Fixing** automation for the Retail Automation project.
Follow the **EXACT same code pattern** as `GRNEntry.py`, `PurchaseReturn.py`, `SmithSupplierPayment.py`, and `RateFixGSTPurchase.py`.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_Purchase\ApprovalRateFixing.py
```

## Update main.py
Add `ApprovalRateFixing` case to the module dispatcher.

---

## Controller Details (admin_ret_purchase.php)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
Function: `rate_fixing($type="")`

Switch Cases:
- `approval_rate_fixing` → Approval Rate Fixing List Page (renders `ret_purchase/rate_fixing/approval_rate_fixing/list`)
- `approval_rate_fixing_add`  → Approval Rate Fixing Add Form (renders `ret_purchase/rate_fixing/approval_rate_fixing/form`)
- `save` → Save Rate Fix Entry (POST handler, `rate_fix_type` will be `2`)
- `cancel` → Cancel a rate fix entry
- `approve` → Approve pending rate fix entries
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Note: This module fixes the gold/metal rate (price per gram) against previously cut approval rates for GST-compliant purchase billing.

## Navigation
| Module | Menu Path | List URL | Add URL |
| :--- | :--- | :--- | :--- |
| **Approval Rate Fixing** | Purchase → Approval Rate Fixing | `admin_ret_purchase/rate_fixing/approval_rate_fixing` | `admin_ret_purchase/rate_fixing/approval_rate_fixing_add` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Form Fields & Mandatory Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Add Form: Approval Rate Fixing (approval_rate_fixing/form.php)
**Header Section:**
- ✅ **Select Karigar (Select2)**: `id="select_karigar"`, `name="order[id_karigar]"`
  - 🔹 Selecting Karigar triggers AJAX load of Approval Ratefix No dropdown for that karigar.
- ✅ **Approval Ratefix No (Select2)**: `id="select_approval_ref_no"`, `name="order[id_approval_ratecut]"`
  - 🔹 Selecting this auto-loads rows into the `#item_details` table via AJAX.
- ⬜ **Remark (Textarea)**: `name="rate_fix[remark]"` (Optional)
- 🔒 **Hidden Fields**:
  - `id="id_karigar"` — stores loaded karigar's PO ID
  - `id="rate_fix_type"`, `name="rate_fix[rate_fix_type]"` — value always `2`

**Item Details Table (auto-loaded): `id="item_details"`**

| Column | Notes |
| :--- | :--- |
| **REF NO** | Read-only — PO Ref No shown here |
| **DATE** | Read-only — PO date |
| **PURE WT** | Read-only — total pure weight of PO |
| **FIXED WT** | Read-only — already fixed weight so far |
| **RET WT** | Read-only — returned weight |
| **BAL WT** | Read-only — balance weight available to fix |
| **FIX WT** | ✅ **Editable** — weight being fixed in this entry (≤ BAL WT) |
| **RATE Excl.Tax** | ✅ **Editable** — rate per gram excluding GST |
| **Taxable amount** | Read-only — auto-calculated: FIX WT × RATE |
| **Tax** | Read-only — auto-calculated GST (IGST or CGST+SGST) |
| **Payable**| Read-only — Taxable Amount + Tax |

**Action Buttons:**
- ✅ **Save Button**: `id="rate_fix_submit"`
- ⬜ **Cancel Button**: `class="btn btn-default btn-cancel"` (navigates back to list)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## List Page Fields (approval_rate_fixing/list.php)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Filters:**
- ✅ **Date Range Picker**: `id="rf-dt-btn"` (hidden date spans: `id="rf_date1"`, `id="rf_date2"`)
  - 🔹 Click → select "Today" from daterangepicker dropdown.
- ✅ **Approve Button**: `id="rate_fix_approve"` (visible only if user has edit permission)
  - 🔹 Selects checked rows in list and approves them (Manager role).

**List Table: `id="payment_list"`**

| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **Id** | Auto-generated Rate Fix ID |
| 2 | **PO REF NO** | PO Reference Number |
| 3 | **KARIGAR** | Supplier/Karigar name |
| 4 | **FIX WEIGHT** | Weight fixed in this entry |
| 5 | **FIX RATE** | Rate per gram (Excl. Tax) |
| 6 | **AMOUNT** | Payable amount (incl. GST) |
| 7 | **Status** | Approval status: Pending / Approved |
| 8 | **Action** | Cancel button (btn-warning) |

**Cancel Modal: `id="confirm-billcancell"`**
- Hidden field: `id="ratefix_id"` (stores ID of record to cancel)
- ✅ **Cancel Remark (Textarea)**: `id="ratefix_cancel_remark"` *(mandatory — button stays disabled until filled)*
- ✅ **Confirm Cancel Button**: `id="ratefix_cancel"` (starts `disabled`, enables when remark typed)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Full Business Workflow & Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 1. Standard Approval Rate Fix Entry (Add Flow)
- **Context**: Fix the approval rate against an outstanding approval cut after metal is received.
- **Workflow**:
  1. Navigate to `admin_ret_purchase/rate_fixing/approval_rate_fixing_add`.
  2. Select **Karigar** (`id="select_karigar"`). Wait for `select_approval_ref_no` to load.
  3. Select **Approval Ratefix No** (`id="select_approval_ref_no"`). Wait for `#item_details` table to populate via AJAX.
  4. In the loaded table row(s): Enter **FIX WT** (≤ BAL WT) and **RATE Excl.Tax**.
  5. Optionally enter **Remark** (`name="rate_fix[remark]"`).
  6. Click **Save** (`id="rate_fix_submit"`).
  7. Capture success message and extract Rate Fix ID from list page.

### 2. Cancel Flow
- **Context**: Cancel an existing approval rate fix entry from the list page.
- **Workflow**:
  1. Navigate to list page, filter by Today (`id="rf-dt-btn"` → Today).
  2. Search for the Rate Fix ID in the DataTable search box.
  3. Click **Cancel** button (btn-warning) in the Action column.
  4. Enter **Cancel Remark** in `id="ratefix_cancel_remark"` modal.
  5. Wait for `id="ratefix_cancel"` to become enabled.
  6. Click **Confirm Cancel**.
  7. Verify: Row is successfully cancelled.

### 3. Approve Flow (Manager Role)
- **Context**: Approve pending approval rate fix entries.
- **Workflow**:
  1. Navigate to list page. Filter by date range (Today).
  2. Select checkbox of pending row(s) in `#payment_list`.
  3. Click **Approve** (`id="rate_fix_approve"`).
  4. Verify: Status column updates from "Pending" → "Approved".

### 4. Multiple SALES ITEMS Rows Handling
- **Context**: When an Approval Ratefix No has more than one item row loaded in the SALES ITEMS `#item_details` table, each row must have its own FIX WT and RATE Excl.Tax filled independently.
- **Data Source**: Read per-row values from the `ApprovalRateFixingItems` Excel sheet matched by `TestCaseId`.
- **Workflow**:
  1. After Approval Ratefix No is selected and `#item_details` table loads, count the total number of `tbody tr` rows rendered.
  2. For each row (1 to N), fetch the corresponding row-level data from `ApprovalRateFixingItems` sheet using the row index matching key.
  3. Locate the **FIX WT** input in that specific row using positional XPath by row index `[N]` targeting `@name='rate_fix[fix_wt][]'`.
  4. Clear the FIX WT field and enter the value from `ApprovalRateFixingItems.FixWt` for that row.
  5. Locate the **RATE Excl.Tax** input in the same row using positional XPath targeting `@name='rate_fix[rate_excl_tax][]'`.
  6. Clear and enter the value from `ApprovalRateFixingItems.RateExclTax` for that row.
  7. After filling each row, verify that **Taxable amount**, **Tax**, and **Payable** columns auto-update in the UI.
  8. Repeat for all remaining rows before clicking Save.
  - 🔹 **Rule**: If `ApprovalRateFixingItems` has no matching rows for a `TestCaseId`, treat as single-row and use FIX WT / RateExclTax from the main `ApprovalRateFixing` sheet.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Advanced Logic & Constraints (from Knowledge Brain)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **FIX WT Validation**: FIX WT entered must be ≤ BAL WT. If exceeded, system shows validation error.
- **Rate Mandatory**: RATE Excl.Tax is mandatory — validation fires on save if empty.
- **Select2 AJAX Wait**: After selecting Karigar or Approval Ratefix No, wait up to 5s for the next element/table to appear.
- **Input Clearing**: FIX WT and RATE fields may have pre-filled values — always `.clear()` before `.send_keys()`.
- **Multiple Row Detection**: After AJAX load, count all `tbody tr` rows in `#item_details` — if count > 1, switch to row-by-row loop.
- **Read-only Column Skip**: Columns REF NO, DATE, PURE WT, FIXED WT, RET WT, BAL WT, Taxable amount, Tax, Payable are read-only — do NOT send keys, only read.
- **Cancel Button State**: `id="ratefix_cancel"` starts disabled. Wait for `is_enabled()` after typing remark.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Expected Excel Sheet Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Sheet: `ApprovalRateFixing`**
| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **TestCaseId** | Unique ID — use `CANCEL_` prefix for cancel flow, `APPROVE_` for approve flow |
| 2 | **TestStatus** | Run / Skip |
| 3 | **ActualStatus** | Auto-populated by script (Pass/Fail) |
| 4 | **Karigar** | Karigar/Supplier name for Select2 |
| 5 | **ApprovalRatefixNo**| Approval Ratefix No to select from Select2 |
| 6 | **FixWt** | Weight to fix (must be ≤ BAL WT) |
| 7 | **RateExclTax** | Rate per gram excluding GST |
| 8 | **GSTPercent** | Expected GST % (e.g., 3) |
| 9 | **Remark** | Optional note |
| 10 | **ExpectedTaxable**| Python-calculated expected taxable amount |
| 11 | **ExpectedPayable**| Python-calculated expected payable amount |
| 12 | **CancelReason** | Reason (used in CANCEL_ flow) |
| 13 | **ExpectedStatus** | Pending / Approved / Cancelled |
| 14 | **CapturedRateFixId**| Auto-populated by script after save |

**Sheet: `ApprovalRateFixingItems`** *(Child sheet)*
| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **TestCaseId** | Matches the TestCaseId in `ApprovalRateFixing` header sheet |
| 2 | **RowIndex** | 1-based index of the row in `#item_details` table (1, 2, 3…) |
| 3 | **PORefNo** | PO Reference No shown in that row (read-only) |
| 4 | **FixWt** | Weight to fix for this specific row (must be ≤ row's BAL WT) |
| 5 | **RateExclTax** | Rate per gram excluding GST for this specific row |
| 6 | **GSTPercent** | Expected GST % for this row (e.g., 3) |
| 7 | **ExpectedTaxable**| Expected Taxable Amount for verification after entry |
| 8 | **ExpectedPayable**| Expected Payable amount for verification after entry |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Code Patterns to Follow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **AJAX Table Load**: Wait using `WebDriverWait` for at least one `tbody tr` inside `#item_details` to be present before proceeding.
- **Single Row Fill Logic**: Locate FIX WT input using `@name='rate_fix[fix_wt][]'` and RATE input using `@name='rate_fix[rate_excl_tax][]'`.
- **Cancel Enable Wait**: Wait for the Confirm Cancel button (`id="ratefix_cancel"`) to become clickable after remark is typed.
- **Success Capture**: Use `_capture_save_result` pattern (same as `GRNEntry.py`) with expected message `"Rate Fixed successfully."`

## Success / Failure Messages
- **Add Success**: `"Rate Fixed successfully."`
- **Cancel Success**: `"Ratefix Cancelled Successfully"`
- **Approve Success**: `"Rate Fix Approved Successfully"` (check spelling in existing)
