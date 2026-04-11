Build complete **Rate Fix Against GST Purchase** automation for the Retail Automation project.
Follow the **EXACT same code pattern** as `GRNEntry.py`, `PurchaseReturn.py`, `SmithSupplierPayment.py`, and `DebitCreditEntry.py`.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_Purchase\RateFixGSTPurchase.py
```

## Update main.py
Add `RateFixGSTPurchase` case to the module dispatcher.

---

## Controller Details (admin_ret_purchase.php)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
Function: `rate_fixing($type="")`

Switch Cases:
- `list` → Rate Fixing List Page (renders `ret_purchase/rate_fixing/list`)
- `add`  → Rate Fixing Add Form (renders `ret_purchase/rate_fixing/form`)
- `save` → Save Rate Fix Entry (POST handler)
- `cancel_rate_fix` → Cancel a rate fix entry
- `approve` → Approve pending rate fix entries
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Note: This module fixes the gold/metal rate (price per gram) against outstanding PO (Purchase Order) balances for GST-compliant purchase billing. Tax (CGST+SGST for intrastate / IGST for interstate) is auto-calculated based on company state vs supplier state.

## Navigation
| Module | Menu Path | List URL | Add URL |
| :--- | :--- | :--- | :--- |
| **Rate Fix** | Purchase → Rate Fixing | `admin_ret_purchase/rate_fixing/list` | `admin_ret_purchase/rate_fixing/add` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Form Fields & Mandatory Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Add Form: Rate Fixing (rate_fixing/form.php)
**Header Section:**
- ✅ **Select Karigar (Select2)**: `id="select_karigar"`, `name="order[id_karigar]"`
  - 🔹 Selecting Karigar triggers AJAX load of PO Ref No dropdown for that karigar.
- ✅ **Financial Year (Select)**: `id="pur_fin_year_select"` (inline with PO Ref No)
  - 🔹 Active financial year is pre-selected. Change FY to view POs from other years.
- ✅ **Select PO REF NO (Select2)**: `id="select_po_ref_no"`, `name="order[rate_fix_po_item_id]"`
  - 🔹 Selecting PO Ref No auto-loads rows into the `#item_details` table via AJAX.
- ⬜ **Remark (Textarea)**: `name="rate_fix[remark]"` (Optional)
- 🔒 **Hidden Fields**:
  - `id="id_karigar"` — stores loaded karigar's PO ID
  - `id="rate_fix_type"`, `name="rate_fix[rate_fix_type]"` — value always `1`
  - `id="cmp_country"` — company country (for GST computation)
  - `id="cmp_state"` — company state (for GST computation: IGST vs CGST+SGST)

**Item Details Table (auto-loaded): `id="item_details"`**

| Column | Notes |
| :--- | :--- |
| **PO REF NO** | Read-only — loaded from selected PO |
| **DATE** | Read-only — PO date |
| **PURE WT** | Read-only — total pure weight of PO |
| **FIXED WT** | Read-only — already fixed weight so far |
| **RET WT** | Read-only — returned weight |
| **BAL WT** | Read-only — balance weight available to fix |
| **FIX WT** | ✅ **Editable** — weight being fixed in this entry (≤ BAL WT) |
| **RATE Excl. Tax** | ✅ **Editable** — rate per gram excluding GST |
| **Taxable Amount** | Read-only — auto-calculated: FIX WT × RATE |
| **Tax** | Read-only — auto-calculated GST (IGST or CGST+SGST) |
| **Payable** | Read-only — Taxable Amount + Tax |

**Action Buttons:**
- ✅ **Save Button**: `id="rate_fix_submit"`
- ⬜ **Cancel Button**: `class="btn btn-default btn-cancel"` (navigates back to list)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## List Page Fields (rate_fixing/list.php)
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
| 8 | **Bill Status** | Bill status: Active / Cancelled |
| 9 | **Action** | Cancel button (btn-warning) |

**Cancel Modal: `id="confirm-billcancell"`**
- Hidden field: `id="ratefix_id"` (stores ID of record to cancel)
- ✅ **Cancel Remark (Textarea)**: `id="ratefix_cancel_remark"` *(mandatory — button stays disabled until filled)*
- ✅ **Confirm Cancel Button**: `id="ratefix_cancel"` (starts `disabled`, enables when remark typed)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Full Business Workflow & Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 1. Standard Rate Fix Entry (Add Flow)
- **Context**: Fix the purchase rate against an outstanding PO balance after metal is received.
- **Workflow**:
  1. Navigate to `admin_ret_purchase/rate_fixing/add`.
  2. Select **Karigar** (`id="select_karigar"`). Wait for PO Ref No to load.
  3. Select **Financial Year** if needed (`id="pur_fin_year_select"`).
  4. Select **PO REF NO** (`id="select_po_ref_no"`). Wait for `#item_details` table to populate via AJAX.
  5. In the loaded table row(s): Enter **FIX WT** (≤ BAL WT) and **RATE Excl. Tax**.
  6. Optionally enter **Remark** (`name="rate_fix[remark]"`).
  7. Click **Save** (`id="rate_fix_submit"`).
  8. Capture success message and extract Rate Fix ID from list page.

### 2. Cancel Flow
- **Context**: Cancel an existing rate fix entry from the list page.
- **Workflow**:
  1. Navigate to list page, filter by Today (`id="rf-dt-btn"` → Today).
  2. Search for the Rate Fix ID in the DataTable search box.
  3. Click **Cancel** button (btn-warning) in the Action column.
  4. Enter **Cancel Remark** in `id="ratefix_cancel_remark"` modal.
  5. Wait for `id="ratefix_cancel"` to become enabled.
  6. Click **Confirm Cancel**.
  7. Verify: Row's Bill Status column updates to "Cancelled".

### 3. Approve Flow (Manager Role)
- **Context**: Approve pending rate fix entries.
- **Workflow**:
  1. Navigate to list page. Filter by date range (Today).
  2. Select checkbox of pending row(s) in `#payment_list`.
  3. Click **Approve** (`id="rate_fix_approve"`).
  4. Verify: Status column updates from "Pending" → "Approved".

### 4. Partial Rate Fix (BAL WT split)
- **Context**: Fix only part of the outstanding balance weight.
- **Workflow**:
  1. Enter FIX WT < BAL WT.
  2. Save → system records partial fix; BAL WT on next entry reduces accordingly.
  3. Verify saved FIX WEIGHT in list is the partial amount entered.

### 5. Multiple SALES ITEMS Rows Handling
- **Context**: When a PO REF NO has more than one item row loaded in the SALES ITEMS `#item_details` table (e.g., multiple partial PO lines against the same karigar), each row must have its own FIX WT and RATE Excl. Tax filled independently.
- **Data Source**: Read per-row values from the `RateFixGSTItems` Excel sheet matched by `TestCaseId`.
- **Workflow**:
  1. After PO Ref No is selected and `#item_details` table loads, count the total number of `tbody tr` rows rendered.
  2. For each row (1 to N), fetch the corresponding row-level data from `RateFixGSTItems` sheet using the row index or `PORefNo` as the matching key.
  3. Locate the **FIX WT** input in that specific row using positional XPath by row index `[N]` targeting `@name='rate_fix[fix_wt][]'`.
  4. Clear the FIX WT field and enter the value from `RateFixGSTItems.FixWt` for that row.
  5. Locate the **RATE Excl. Tax** input in the same row using positional XPath targeting `@name='rate_fix[rate_excl_tax][]'`.
  6. Clear and enter the value from `RateFixGSTItems.RateExclTax` for that row.
  7. After filling each row, verify that **Taxable Amount**, **Tax**, and **Payable** columns auto-update in the UI (read-only calculated fields).
  8. Repeat for all remaining rows before clicking Save.
  - 🔹 **Rule**: If `RateFixGSTItems` has no matching rows for a `TestCaseId`, treat as single-row and use FIX WT / RateExclTax from the main `RateFixGST` sheet.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Advanced Logic & Constraints (from Knowledge Brain)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Technical Rules
- **FIX WT Validation**: FIX WT entered must be ≤ BAL WT. If exceeded, system shows validation error.
- **Rate Mandatory**: RATE Excl. Tax is mandatory — validation fires on save if empty.
- **GST Logic**: `cmp_state == supplier_state` → CGST + SGST (each = GST% / 2); otherwise → IGST (full GST%). Standard GST for gold = **3%**.
- **Approval Dependency**: Rate Fix with Status = Pending cannot be used for payment until Approved.
- **Cancel Lock**: Once Approved or used in payment, Cancel button may be disabled (check `is_enabled()`).
- **Data Flow**: Updates `ret_rate_fixing` table; linked to `ret_karigar_po_items`.

### UI Automation Gotchas
- **Select2 AJAX Wait**: After selecting PO Ref No, wait up to 5s for `#item_details tbody tr` to appear before interacting.
- **Input Clearing**: FIX WT and RATE fields may have pre-filled values — always `.clear()` before `.send_keys()`.
- **Multiple Row Detection**: After AJAX load, count all `tbody tr` rows in `#item_details` — if count > 1, switch to row-by-row loop using positional XPath `(//table[@id='item_details']/tbody/tr)[N]` where N is 1-based row index.
- **Row Data Matching**: Match each rendered row to the `RateFixGSTItems` sheet row by index order (1st rendered row → 1st `RateFixGSTItems` row for that `TestCaseId`).
- **Read-only Column Skip**: Columns PO REF NO, DATE, PURE WT, FIXED WT, RET WT, BAL WT, Taxable Amount, Tax, Payable are read-only — do NOT attempt to send keys to them; only read their values for verification.
- **Cancel Button State**: `id="ratefix_cancel"` starts disabled. Wait for `is_enabled()` after typing remark.
- **DataTable filter ID**: List table search input is at `//div[@id='payment_list_filter']//input`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Test Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Scenario 1: Standard Rate Fix (Single Item)
1. **Goal**: Fix the rate for a single PO item row.
2. **Steps**:
   - Navigate to Rate Fixing Add form.
   - Select Karigar and Financial Year.
   - Select PO Ref No (single item loads).
   - Enter Fix Wt and RateExclTax from `RateFixGST` sheet.
   - Verify Taxable, Tax, and Payable auto-calculation.
   - Click Save.
3. **Verification**: Verify "Rate Fixed Successfully" toast and confirm entry in List page.

### Scenario 2: Standard Rate Fix (Multiple Items)
1. **Goal**: Fix the rate against a PO that loads multiple item rows.
2. **Steps**:
   - Select Karigar, FY, and PO Ref No.
   - Iterate through loaded `#item_details` rows.
   - For each row, read Fix Wt and Rate from `RateFixGSTItems` child sheet based on `RowIndex`.
   - Enter Fix Wt and Rate for each row.
   - Verify per-row Taxable, Tax, and Payable computations.
   - Click Save.
3. **Verification**: Confirm success message and presence in List page.

### Scenario 3: Cancel Rate Fix
1. **Goal**: Cancel an existing Rate Fix entry.
2. **Steps**:
   - Create a new Rate Fix entry.
   - Locate the entry in the List page using Search.
   - Click Cancel action button.
   - Enter Cancel Reason in modal remark.
   - Click Confirm Cancel.
3. **Verification**: Verify success message.

### Scenario 4: Approve Rate Fix
1. **Goal**: Approve a pending Rate Fix entry.
2. **Steps**:
   - Create a new Rate Fix entry.
   - Locate the entry in the List page using Search.
   - Select row checkbox.
   - Click Approve button.
3. **Verification**: Verify success message.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Expected Excel Sheet Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Sheet: `RateFixGST`**
| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **TestCaseId** | Unique ID — use `CANCEL_` prefix for cancel flow, `APPROVE_` for approve flow |
| 2 | **TestStatus** | Run / Skip |
| 3 | **ActualStatus** | Auto-populated by script (Pass/Fail) |
| 4 | **Karigar** | Karigar/Supplier name for Select2 |
| 5 | **FinancialYear** | e.g., `FY 25-26` (leave blank for current active year) |
| 6 | **PORefNo** | PO Reference No to select from Select2 |
| 7 | **FixWt** | Weight to fix (must be ≤ BAL WT) |
| 8 | **RateExclTax** | Rate per gram excluding GST |
| 9 | **GSTPercent** | Expected GST % (e.g., 3) |
| 10 | **Remark** | Optional note |
| 11 | **ExpectedTaxable** | Python-calculated expected taxable amount |
| 12 | **ExpectedPayable** | Python-calculated expected payable amount |
| 13 | **CancelReason** | Reason (used in CANCEL_ flow) |
| 14 | **ExpectedStatus** | Pending / Approved / Cancelled |
| 15 | **CapturedRateFixId** | Auto-populated by script after save |

**Sheet: `RateFixGSTItems`** *(Child sheet — one row per SALES ITEMS table row, matched by TestCaseId)*
| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **TestCaseId** | Matches the TestCaseId in `RateFixGST` header sheet |
| 2 | **RowIndex** | 1-based index of the row in `#item_details` table (1, 2, 3…) |
| 3 | **PORefNo** | PO Reference No shown in that row (read-only, for identification) |
| 4 | **FixWt** | Weight to fix for this specific row (must be ≤ row's BAL WT) |
| 5 | **RateExclTax** | Rate per gram excluding GST for this specific row |
| 6 | **GSTPercent** | Expected GST % for this row (e.g., 3) |
| 7 | **ExpectedTaxable** | Expected Taxable Amount for verification after entry |
| 8 | **ExpectedPayable** | Expected Payable amount for verification after entry |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Code Patterns to Follow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **AJAX Table Load**: Wait using `WebDriverWait` for at least one `tbody tr` inside `#item_details` to be present before proceeding. Use 10s timeout.
- **Row Count Detection**: After table loads, find all `tbody tr` elements in `#item_details`. Store the count. If count > 1, switch to multi-row fill loop.
- **Single Row Fill Logic**: Locate FIX WT input using `@name='rate_fix[fix_wt][]'` and RATE input using `@name='rate_fix[rate_excl_tax][]'` — clear each and enter value from `RateFixGST` sheet.
- **Multi-Row Fill Loop Logic**: Iterate rows 1 to N using 1-based positional XPath on `#item_details tbody tr`. For each row index, fetch the matching `RateFixGSTItems` sheet entry by `RowIndex`. Clear and fill FIX WT and RATE Excl. Tax inputs found within that specific positional row. After filling each row, read back the auto-calculated Taxable Amount, Tax, and Payable from that row's read-only cells for verification.
- **Cancel Enable Wait**: Wait for the Confirm Cancel button (`id="ratefix_cancel"`) to become clickable after remark is typed — check enabled state before clicking.
- **List Search Logic**: Locate the search input inside `#payment_list_filter` div, clear it, type the captured Rate Fix ID, and wait for DataTable to filter before reading the result row.
- **Success Capture**: Use `_capture_save_result` pattern (same as `GRNEntry.py`) with expected message `"Rate Fixed Successfully"`.

## Calculation Verification Logic
Implement a `calculation_verification(fix_wt, rate, gst_percent)` helper method with the following logic:
- Convert `fix_wt`, `rate`, and `gst_percent` to float. Default `gst_percent` to **3** if blank.
- **Taxable Amount** = `round(fix_wt × rate, 2)`
- **Tax Amount** = `round(taxable_amount × (gst_percent ÷ 100), 2)`
- **Payable** = `round(taxable_amount + tax_amount, 2)`
- Return a dict with keys `taxable`, `tax`, `payable`.
- Call this method per-row when verifying multi-row SALES ITEMS entries — pass each row's FIX WT, RATE, and GST% from `RateFixGSTItems` sheet and compare with the UI-displayed values read from the read-only Taxable Amount, Tax, and Payable cells of that row.
- **GST Split Rule**: If `cmp_state == supplier_state` → split tax as CGST = Tax/2 and SGST = Tax/2 (intrastate). Otherwise → full Tax is IGST (interstate).

## Success / Failure Messages
- **Add Success**: `"Rate Fixed Successfully"` or `"Rate Fix Added Successfully"`
- **Cancel Success**: `"Rate Fix Cancelled Successfully"`
- **Approve Success**: `"Rate Fix Approved Successfully"`
- **Validation Error**: Alert/toast when FIX WT > BAL WT or Rate is empty.
