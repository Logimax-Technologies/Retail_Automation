# Master Prompt: Branch Transfer Automation

Build complete Branch Transfer automation for the Retail Automation project. Follow the EXACT same code pattern as `StockIssue.py`, `QCIssueReceipt.py`, and `HMIssueReceipt.py`.

**File to create**: `c:\Retail_Automation\Sparqla\Test_Inventory\BranchTransfer.py`  
**Update main.py**: Add `BranchTransfer` case.

---

### Module Overview

**Module**: Inventory → Branch Transfer  
**Purpose**: Transfer items from one branch to another. Supports five item types:
1. **Tagged** (`transfer_item_type = 1`) — Tagged jewellery items using Tag Code / Lot No / Estimation No
2. **Non-Tagged** (`transfer_item_type = 2`) — Non-tagged stock via NT Receipt or Product entry
3. **Purchase Return** (`transfer_item_type = 3`) — Purchase return items loaded via date range (always from Head Office)
4. **Packing Items** (`transfer_item_type = 4`) — Other inventory/packaging items with Pcs count entry
5. **Repair Order** (`transfer_item_type = 5`) — Repair orders loaded by Order No

**Other Issue Checkbox** (`id=isOtherIssue`): A special global checkbox that, when checked, **hides the To Branch block** (`class=to_branch_blk`) and sets the destination branch to **Head Office** by default. This checkbox combines with any of the above item types.

---

### Controller Details

**Controller file**: `admin_ret_brntransfer.php`  
**Switch Cases**:
- `list` → Branch Transfer List page
- `add` → Add Branch Transfer form
- `save` → POST — save transfer

**Submission**: Form POST to `admin_ret_brntransfer/branch_transfer/save`

---

### Navigation

- **Menu**: Inventory → Branch Transfer
- **List URL**: `admin_ret_brntransfer/branch_transfer/list`
- **Add URL**: `admin_ret_brntransfer/branch_transfer/add`

---

### Form Fields & Mandatory Status

#### Header / Common Section (visible for all transfer types)

> **Actual UI field order (header row, left → right)**:  
> From Branch → To Branch → Transfer Item Type (Radio) → Other Issue (Checkbox)

- ✅ **From Branch** (Select2): `class=from_branch` / `id=from_brn`  
  — For branch users, auto-filled (disabled). For HO users, select branch from dropdown.
- ✅ **To Branch** (Select2): `id=to_brn`  
  — Populated dynamically based on From Branch selected. Hidden when **Other Issue** is checked.  
  — For Purchase Return (type=3), this is always disabled (Head Office is default).
- ✅ **Transfer Item Type** (Radio group): `name=transfer_item_type`  
  — `value=1` → Tagged  
  — `value=2` → Non-Tagged  
  — `value=3` → Purchase Return  
  — `value=4` → Packing Items  
  — `value=5` → Repair Order  
- ⬜ **Other Issue** (Checkbox): `id=isOtherIssue`  
  — When checked: `.to_branch_blk` is hidden; destination defaults to Head Office; `bt_approval_type` radio is disabled.  
  — When unchecked: `.to_branch_blk` is shown; transfer goes to selected To Branch.

---

#### Flow 1 — Tagged Items (transfer_item_type = 1)

> **Search method**: Use Lot No OR Estimation No OR Tag Code (at least one required).  
> **Multi-value**: All search fields support **pipe `|` separated values** in Excel.  
> Each value triggers an independent: **Set → Search → Select All → Add to Preview** cycle.  
> Results accumulate in `id=bt_list` across all iterations before final submit.

- ⬜ **Lot No** (Select2): `id=lotno` — Single or pipe-separated lot numbers  
  Excel e.g.: `9580` or `9580|9581`  
  → Lot 9580 selected → Search → Select all → Add to Preview → clear → Lot 9581 → Search → Select all → Add to Preview
- ⬜ **Section** (Select2): `id=section_select` — Single or pipe-separated sections  
  Excel e.g.: `HARAM GB` or `HARAM GB|HARAM SECTION`  
  → Section `HARAM GB` → Search → Select all → Add → clear → Section `HARAM SECTION` → Search → Select all → Add
- ⬜ **Product** (Typeahead / Input): `id=product` — Single or pipe-separated products  
  Excel e.g.: `GOLD MALAI` or `GOLD MALAI|SILVER CHAIN`  
  → Product `GOLD MALAI` → Search → Select all → Add → clear → Product `SILVER CHAIN` → Search → Select all → Add
- ⬜ **Design** (Input): `id=design` — Optional design filter (single value only)
- ⬜ **Tag Code** (Input): `id=tag_no` — Single or pipe-separated tag codes  
  Excel e.g.: `GBT-01474` or `GBT-01474|GBT-01476`  
  → Tag `GBT-01474` → Search → Select all → Add → clear → Tag `GBT-01476` → Search → Select all → Add
- ⬜ **Old Tag Code** (Input): `id=old_tag_no` — Single or pipe-separated old tag codes  
  Excel e.g.: `OT-001|OT-002` — same multi-cycle logic as Tag Code
- ⬜ **Estimation No** (Input): `id=esti_no` — Single or pipe-separated estimation numbers  
  Excel e.g.: `1` or `1|2`  
  → Est `1` → click `id=search_est_no` → Select all → Add → clear → Est `2` → click Search → Select all → Add

**Search Button**: `class=btrn_search` → triggers `getTagSearchList()` (for Tag/Lot/Section/Product)  
**Estimation Search Button**: `id=search_est_no` → triggers `getEstiTags()`

**Search Results Grid**: `id=bt_search_list`  
Columns: ☐ | Tag ID | Tag Code | Old Tag Code | Lot Inward Detail | Section | Product | Design | Date | Pcs | Gross Wt | Net Wt | Dia Wt

#### Multi-Value Tagged Flow — Step-by-step

> **Key rule**: For each pipe-separated value → run the full **Set → Search → Select All → Add to Preview** cycle. After ALL values are processed, exactly ONE final submit (`#add_to_transfer`) is clicked.

```
For each value V in pipe-split(LotNo or Section or Product or TagCode or OldTagCode or EstimationNo):
    1. Clear the input field
    2. Set the field to value V
    3. Click Search (btrn_search or search_est_no for EstimationNo)
    4. Wait for bt_search_list tbody to have rows
    5. Check ALL rows in bt_search_list
    6. Click #add_to_list → rows move to bt_list (Preview)
    7. Verify bt_list tbody has rows (cumulative from all previous values)
→ After ALL values processed: click #add_to_transfer (submit once)
```

**Priority order when multiple search field columns are filled:**
1. If `EstimationNo` is filled → use Estimation No loop (use `search_est_no` button)
2. Else if `TagCode` is filled → use TagCode loop (use `btrn_search` button)
3. Else if `OldTagCode` is filled → use OldTagCode loop (use `btrn_search` button)
4. Else if `LotNo` is filled → use LotNo loop (each lot selected separately in `#lotno` Select2)
5. Else if `Section` or `Product` is filled → use Section/Product loop

**Preview Grid**: `id=bt_list`  
Columns: Tag ID | Tag Code | Old Tag Code | Lot Inward Detail | Section | Product | Design | Date | Pcs | Gross Wt | Net Wt | Dia Wt | Remark

**After ALL search cycles**: Verify `id=bt_list` has items → click `id=add_to_transfer`

---

#### Flow 2 — Non-Tagged Items (transfer_item_type = 2)

> **Two loading methods:**  
> (a) **NT Receipt** — Select from `id=nt_receipt` dropdown → Click `class=btrn_search` → calls `getNonTaggedReceiptedItem()`  
> (b) **Product Entry** — Leave `id=nt_receipt` empty → Fill product/design fields → Click `class=btrn_search` → calls `getNonTaggedItem()`

- ⬜ **NT Receipt** (Select2): `id=nt_receipt` — Select a Non-Tagged receipt number to load items
- ⬜ **Section** (Select2): `id=section_select` — Filter by section (used in product entry mode)
- ⬜ **Product** (Input): `id=product` — Product name for search (used in product entry mode)

**Search Results Grid**: `id=bt_nt_search_list`  
Columns: ☐ | Section | Product | Design | Pcs (editable) | Balance Pcs | Gross Wt (editable) | Balance Gross Wt | Net Wt (editable) | Balance Net Wt | Error

**Non-Tagged Row Fields (editable per row)**:
- `.nt_piece` — Number of pieces (cannot exceed `.blc_pieces`)
- `.nt_gross_wt` — Gross weight (cannot exceed `.blc_gross_wt`)
- `.nt_net_wgt` — Net weight (cannot exceed `.blc_net_wgt`)

**Totals** (auto-calculated):
- `.nt_pieces` — Total Pcs selected
- `.nt_grs_wt` — Total Gross Wt
- `.nt_net_wt` — Total Net Wt

**Step-by-step**:
1. Select **From Branch** (`id=from_brn`)
2. Select **To Branch** (`id=to_brn`)
3. Select radio `name=transfer_item_type` value `2`
4. **If NT Receipt mode**: Select receipt from `id=nt_receipt` → Click `class=btrn_search`
5. **If Product Entry mode**: Leave `id=nt_receipt` blank → optionally fill `id=section_select` / `id=product` → Click `class=btrn_search`
6. Wait for rows in `id=bt_nt_search_list`
7. Check items (`.nt_item_sel` checkboxes), adjust Pcs/Weight if needed
8. Click **Add to Transfer** (`id=add_to_transfer`) → builds `non_tagged[]` array → calls `add_to_trans()`

---

#### Flow 3 — Purchase Return (transfer_item_type = 3)

> **Default source branch: Head Office (disabled). Date range selects purchase return items.**

- ✅ **Date Range** (Daterangepicker): `id=bill_date`  
  — From date displayed in `id=rpt_payments1`, To date in `id=rpt_payments2`
- **From Branch**: Disabled; auto-set to Head Office.

**Step-by-step**:
1. Select radio `name=transfer_item_type` value `3`
2. Select **To Branch** (`id=to_brn`) if the destination is not Head Office
3. Select **Date Range** via `id=bill_date` datepicker → dates auto-populate `id=rpt_payments1` and `id=rpt_payments2`
4. Click `class=btrn_search` → calls `get_purchase_items()` → loads purchase return details
5. Check returned items in grid (`id=bt_approval_list_old_metal` / similar grid)
6. Click **Add to Transfer** (`id=add_to_transfer`) → builds `old_metal_data[]` → calls `add_to_trans()`

---

#### Flow 4 — Packing Items (transfer_item_type = 4)

> **Multi-value**: `Select Item` and `No of Pcs` support **pipe `|` separated values** in Excel.  
> Each pair triggers an independent: **Select Item → Enter Pcs → Click Add** cycle.  
> e.g. Excel Item: `PEN|RING BOX`, Pcs: `2|2`

- ✅ **Select Item** (Select2): `id=select_item` — Single or pipe-separated item names
- ✅ **No of Pcs**: `.no_of_pcs` — Single or pipe-separated piece counts

**Packaging List Grid**: `id=packaging_list`  
Columns: Item | No of Pcs | Action (Remove)

Each row contains:
- `.id_other_item` — Hidden item ID
- `.no_of_pcs` — Piece count entered

**Multi-Value Packing Items — Step-by-step**:
```
For each (Item, Pcs) pair in pipe-split(Pack_Item, Pack_Pcs):
    1. Select Item in dropdown (id=select_item)
    2. Enter No of Pcs (.no_of_pcs)
    3. Click Add (id=add_pack_item)
    4. Row appears in id=packaging_list
→ After ALL pairs processed: click Add to Transfer (id=add_to_transfer)
```

**Steps logic**:
1. Select **From Branch** (`id=from_brn`) → triggers `get_invnetory_item()` to populate item dropdown
2. Select **To Branch** (`id=to_brn`)
3. Select radio `name=transfer_item_type` value `4`
4. Execute the loop above
5. Click **Add to Transfer** (`id=add_to_transfer`) → builds `packaging_data[]` → calls `add_to_trans()`

---

#### Flow 5 — Repair Order (transfer_item_type = 5)

> **Multi-value**: `Order No` supports **pipe `|` separated values** in Excel.  
> Each Order No triggers a search that appends items to the results grid.  
> e.g. Excel OrderNo: `ATM25-RE-00019|ATM25-RE-00020`

- ✅ **Order No** (Input): `id=order_no` — Single or pipe-separated repair order numbers
- **Search**: Click `class=btrn_search` → calls `getRepairOrderDetails()`

**Repair Order Grid**: `id=bt_approval_list_orders` (in approval page) or direct search result list in add page (`id=bt_order_search_list`)  
Columns: ☐ | Order No | Customer | Product | Design | Pcs | Gross Wt | Action

Each row contains:
- `name=id_orderdetails[]` checkbox + `.id_orderdetails` hidden value

**Multi-Value Repair Order — Step-by-step**:
```
1. Select From Branch (id=from_brn)
2. Select To Branch (id=to_brn)
3. Select radio name=transfer_item_type value 5
4. For each Order in pipe-split(OrderNo):
    a. Enter Order in id=order_no
    b. Click Search (class=btrn_search)
    c. Rows APPPEND to bt_order_search_list
5. After ALL searches, check ALL checkboxes (name=id_orderdetails[])
6. Click Add to Transfer (id=add_to_transfer)
```

---

#### Other Issue Checkbox Behavior

- **Element**: `id=isOtherIssue` (Checkbox)
- **When Checked**:
  - `.to_branch_blk` → `display: none` (To Branch field is hidden)
  - Destination branch defaults to **Head Office** (`id=other_issue_branch`)
  - `bt_approval_type` radio buttons are disabled
  - If Transfer Type = Tagged (type=1): `.karigar` div becomes visible
- **When Unchecked**:
  - `.to_branch_blk` → `display: block`
  - `bt_approval_type` radio buttons are enabled
  - `.karigar` div hidden (for type=1)
- **Note**: When `isOtherIssue = 1`, the approval flow sends OTP to `verify_other_issue_otp` endpoint instead of the standard approval OTP endpoint.

---

#### Remark Field

- **Remark** (Textarea): `id=remark` — Optional notes for the transfer. Present for all transfer types.

---

#### Action Buttons

- **Search Button**: `class=btrn_search` — Searches for items based on current transfer type and filters
- **Add to List (Tagged preview)**: `id=add_to_list` — Moves selected tagged items from search results to `id=bt_list` preview
- **Estimation No Search**: `id=search_est_no` — Searches tags by estimation number
- **Add to Transfer / Submit**: `id=add_to_transfer` — Sends the transfer data to server via `add_to_trans()`
- **Cancel**: Standard cancel button

---

### Post-Save & ID Capture

After clicking `id=add_to_transfer` (submit), the system completes the transfer and **opens a new browser tab** with the Branch Transfer print page.

#### Print Tab URL Format
```
https://<host>/admin/index.php/admin_ret_brntransfer/branch_transfer/print/{BT_CODE}/{type}/{id}
```
**Example**: `.../branch_transfer/print/05930/4/2`  
→ BT Code = **05930**

#### Step-by-Step Post-Save Logic

1. **Detect new tab**: After `#add_to_transfer` click, wait for a new window/tab handle to appear.
2. **Switch to print tab**: `driver.switch_to.window(new_tab_handle)`
3. **Extract BT Code from URL**:  
   ```python
   current_url = driver.current_url
   # URL: .../branch_transfer/print/05930/4/2
   bt_code = current_url.split('/print/')[1].split('/')[0]  # → "05930"
   ```
4. **Close print tab**: `driver.close()`
5. **Switch back to main window**: `driver.switch_to.window(main_window_handle)`
6. **Capture success banner**: Wait for `.alert-success` or `.alert` div containing  
   `"Records added successfully"` → read text → store as `success_message`.
   - From screenshot: `"✔ Add to Transfer! — 1 Records added successfully."`  
   - Banner class: `.alert.alert-success` or `.alert-box`
7. **Write to Excel**: `ExcelUtils.write_actual_status(row, bt_code + ' | ' + success_message)`

#### List Page Verification

8. **Navigate to List**: `fc.navigate_to_url('admin_ret_brntransfer/branch_transfer/list')`
9. **Set Date Range to Today**: Click **Date range picker** button → select **Today** preset  
   → dates update to today's date in `#from_date` / `#to_date` text elements.
10. **Search by BT Code**: Type the captured BT Code (e.g. `05930`) into the **Search** input box  
    (`input.form-control[type=search]` in DataTables toolbar → `id=bt_list_filter input`).
11. **Wait for filtered row**: Wait for `#bt_list tbody tr` to contain exactly one row matching the BT Code.
12. **Verify row data**:
    - **BT Code** column matches captured `bt_code` (e.g. `05930`)
    - **Type** column matches expected type (e.g. `Packaging Items`, `Tagged Items`, `Non Tagged Items`, `Repair Items`, `Partly / SR`)
    - **From Branch** column matches `FromBranch` Excel value
    - **To Branch** column matches `ToBranch` Excel value
    - **Status** column shows `Yet to Approve` (newly created transfer)

#### List Page Column Reference (from screenshot)

| Column | Notes |
|--------|-------|
| BT Code | Unique transfer code — e.g. `05930` |
| Date | Transfer date (today) |
| Type | `Tagged Items` / `Non Tagged Items` / `Packaging Items` / `Repair Items` / `Partly / SR` |
| From Branch | Source branch name |
| To Branch | Destination branch name |
| Pcs | Number of pieces |
| Gwt | Gross weight |
| Status | `Yet to Approve` for new transfers; `Stock Updated` for approved |
| Action | Print / Download / Approve buttons |

---

### Success / Failure Messages

- **Success Banner (main window)**: `"✔ Add to Transfer! — N Records added successfully."`  
  — Element: `.alert.alert-success` visible on the add page after submit
- **Print Tab**: New tab opens at `.../branch_transfer/print/{BT_CODE}/{type}/{id}`
- **Failure**: `"Unable to proceed the requested process"`
- **No items selected**: Toaster `"Please select tag code to proceed.."` / `"Please Select Order Item.."`
- **Branch not selected**: `"To Branch Required"` / `"Please select branch properly .."`
- **Invalid Pcs/Weight**: Toaster validation for invalid piece count or weight values

---

### Excel Sheet: `BranchTransfer`

- **File Path**: `C:\Users\Dell\Desktop\sqrqlas\Sqarqla_Retail_data2.xlsx`
- **Sheet Name**: `BranchTransfer`

| Col | Header | Description |
|-----|--------|-------------|
| 1 | TestCaseId | Unique test case identifier |
| 2 | TestStatus | `Run` / `Skip` / `Done` |
| 3 | ActualStatus | Populated after run — success/failure message |
| 4 | TransferType | `Tagged` / `NonTagged` / `PurchaseReturn` / `PackingItems` / `RepairOrder` |
| 5 | FromBranch | Branch name for `id=from_brn` |
| 6 | ToBranch | Branch name for `id=to_brn` (blank if OtherIssue=Y) |
| 7 | OtherIssue | `Y` or `N` — whether to check `id=isOtherIssue` |
| 8 | LotNo | Lot No for `id=lotno` (Tagged only, optional) |
| 9 | Section | Section name for `id=section_select` (Tagged/NonTagged optional) |
| 10 | Product | Product name for `id=product` (Tagged/NonTagged optional) |
| 11 | Design | Design name for `id=design` (Tagged optional) |
| 12 | TagCode | Tag code for `id=tag_no` (Tagged) |
| 13 | OldTagCode | Old tag code for `id=old_tag_no` (Tagged, optional) |
| 14 | EstimationNo | Estimation number for `id=esti_no` (Tagged optional) |
| 15 | NT_Receipt | NT Receipt number for `id=nt_receipt` (NonTagged optional) |
| 16 | PR_FromDate | Purchase Return from date (PurchaseReturn only) |
| 17 | PR_ToDate | Purchase Return to date (PurchaseReturn only) |
| 18 | Pack_Item | Packing item name to select (PackingItems) |
| 19 | Pack_Pcs | Number of pcs for packing item (PackingItems) |
| 20 | OrderNo | Repair order number for `id=order_no` (RepairOrder) |
| 21 | Remark | Remarks for `id=remark` |

**Sample Rows**:

| TestCaseId | TestStatus | ActualStatus | TransferType | FromBranch | ToBranch | OtherIssue | LotNo | Section | Product | Design | TagCode | OldTagCode | EstimationNo | NT_Receipt | PR_FromDate | PR_ToDate | Pack_Item | Pack_Pcs | OrderNo | Remark |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC_BT_001 | Run | | Tagged | Head Office | Branch 1 | N | | GOLD CHAIN | | | T001 | | | | | | | | | Tagged Transfer by Tag Code |
| TC_BT_002 | Run | | Tagged | Head Office | Branch 1 | N | LOT001 | | | | | | | | | | | | | Tagged Transfer by Lot No |
| TC_BT_003 | Run | | Tagged | Head Office | Branch 1 | N | | | | | | | EST001 | | | | | | | Tagged Transfer by Estimation No |
| TC_BT_004 | Run | | NonTagged | Head Office | Branch 1 | N | | | | | | | | NT-RCT-001 | | | | | | Non-Tagged via NT Receipt |
| TC_BT_005 | Run | | NonTagged | Head Office | Branch 1 | N | | SILVER | KODI | | | | | | | | | | | Non-Tagged via Product Entry |
| TC_BT_006 | Run | | PurchaseReturn | Head Office | Branch 1 | N | | | | | | | | | 01-03-2026 | 31-03-2026 | | | | Purchase Return Transfer |
| TC_BT_007 | Run | | PackingItems | Head Office | Branch 1 | N | | | | | | | | | | | Box Small | 10 | | Packing Items Transfer |
| TC_BT_008 | Run | | RepairOrder | Head Office | Branch 1 | N | | | | | | | | | | | | | RO-2500 | Repair Order Transfer |
| TC_BT_009 | Run | | Tagged | Head Office | | Y | | | | | T002 | | | | | | | | | Other Issue - Tagged Transfer |

---

### Automation Logic — `BranchTransfer.py`

#### Key Patterns

- **Navigation**: `fc.navigate_to_url(add_url)` → wait for page load.
- **From Branch**: `fc.select2('#from_brn', FromBranch)` or skip if branch user (auto-set).
- **To Branch**: `fc.select2('#to_brn', ToBranch)` — skip if `OtherIssue == 'Y'` (field hidden).
- **Other Issue**: `fc.click_element('#isOtherIssue')` if `OtherIssue == 'Y'`.
- **Transfer Type Radio**: `fc.click_element(f"input[name='transfer_item_type'][value='{type_value}']")` where type_value is 1–5.
- **Section**: `fc.select2('#section_select', Section)` if non-empty.
- **Product**: `fc.input_text('#product', Product)` if non-empty.

#### Tagged Flow

```
if TransferType == 'Tagged':
    if LotNo:
        fc.select2('#lotno', LotNo)
    elif EstimationNo:
        fc.input_text('#esti_no', EstimationNo)
        fc.click_element('#search_est_no')
    elif TagCode:
        fc.input_text('#tag_no', TagCode)
        if OldTagCode:
            fc.input_text('#old_tag_no', OldTagCode)
    fc.click_element('.btrn_search')  # triggers getTagSearchList / getEstiTags
    wait for rows in #bt_search_list tbody
    check all rows: fc.check_all('#bt_search_list input[type=checkbox]')
    fc.click_element('#add_to_list')  # move to preview #bt_list
    wait for rows in #bt_list tbody
    fc.click_element('#add_to_transfer')
```

#### Non-Tagged Flow

```
if TransferType == 'NonTagged':
    if NT_Receipt:
        fc.select2('#nt_receipt', NT_Receipt)
    else:
        fill #section_select, #product if provided
    fc.click_element('.btrn_search')
    wait for rows in #bt_nt_search_list tbody
    check all items: fc.check_all('#bt_nt_search_list input.nt_item_sel')
    fc.click_element('#add_to_transfer')
```

#### Purchase Return Flow

```
if TransferType == 'PurchaseReturn':
    select radio value 3
    set date range via #bill_date datepicker:
        - from date → #rpt_payments1
        - to date → #rpt_payments2
    fc.click_element('.btrn_search')
    wait for items
    check all items
    fc.click_element('#add_to_transfer')
```

#### Packing Items Flow

```
if TransferType == 'PackingItems':
    select radio value 4
    select From Branch (triggers get_invnetory_item())
    wait for item dropdown to populate
    select item from items dropdown
    fc.input_text('.no_of_pcs', Pack_Pcs)
    click Add button → row appears in #packaging_list
    fc.click_element('#add_to_transfer')
```

#### Repair Order Flow

```
if TransferType == 'RepairOrder':
    select radio value 5
    fc.input_text('#order_no', OrderNo)
    fc.click_element('.btrn_search')
    wait for rows in repair order list
    check all order items: fc.check_all("input[name='id_orderdetails[]']")
    fc.click_element('#add_to_transfer')
```

#### Other Issue Flow (Combined with any type above)

```
if OtherIssue == 'Y':
    fc.click_element('#isOtherIssue')  # check the checkbox
    verify .to_branch_blk is hidden
    # ToBranch is defaulted to Head Office; no need to select
    # continue with normal TransferType flow above
```

#### Common End Steps

```
fc.input_text('#remark', Remark)  # if provided
fc.click_element('#add_to_transfer')  # final submit

# --- Post-Save: Print Tab Handling ---
main_window = driver.current_window_handle
WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > 1)
new_tab = [h for h in driver.window_handles if h != main_window][0]
driver.switch_to.window(new_tab)
current_url = driver.current_url  # e.g. .../branch_transfer/print/05930/4/2
bt_code = current_url.split('/print/')[1].split('/')[0]  # → "05930"
driver.close()
driver.switch_to.window(main_window)

# --- Capture Success Banner ---
success_el = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert.alert-success'))
)
success_message = success_el.text.strip()  # "Add to Transfer! 1 Records added successfully."

# --- Write to Excel ---
ExcelUtils.write_actual_status(row, bt_code + ' | ' + success_message)

# --- List Page Verification ---
fc.navigate_to_url('admin_ret_brntransfer/branch_transfer/list')
# Set date range to Today
fc.click_element('#account-dt-btn')  # Date range picker button
fc.click_element('.ranges li:contains("Today")')  # Select 'Today' preset
# Search by captured BT Code
search_box = driver.find_element(By.CSS_SELECTOR, '#bt_list_filter input')
search_box.clear()
search_box.send_keys(bt_code)  # e.g. "05930"
# Wait and verify row
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, '#bt_list tbody tr'))
)
# Assert BT Code, Type, From Branch, To Branch, Status in the row
```

---

### Process Loop

```
for each row in BranchTransfer sheet where TestStatus == "Run":
    navigate to add page
    set Other Issue checkbox if OtherIssue == 'Y'
    select TransferType radio (1–5)
    set FromBranch, ToBranch (if applicable)
    based on TransferType:
        type 1 (Tagged): set lot/est/tag → search → select all → add to preview → submit
        type 2 (NonTagged): set NT receipt or product → search → select all → submit
        type 3 (PurchaseReturn): set date range → search → select all → submit
        type 4 (PackingItems): select item → enter pcs → add → submit
        type 5 (RepairOrder): enter order no → search → select all → submit
    enter remark
    click final submit (#add_to_transfer)
    # Post-save:
    switch to new print tab → extract BT Code from URL → close print tab → switch back
    capture success banner text from .alert.alert-success on main window
    update ActualStatus (bt_code + success_message) in Excel
    # List verification:
    navigate to list page
    set date range to Today
    type BT Code in search box (#bt_list_filter input)
    verify row appears with correct BT Code, Type, From/To Branch, Status='Yet to Approve'
```

---

### Test Scenarios

- **TC_BT_T01**: Tagged transfer by Tag Code → verify item in preview → submit → success toaster.
- **TC_BT_T02**: Tagged transfer by Lot No → search → select all → add to preview → submit.
- **TC_BT_T03**: Tagged transfer by Estimation No → click `#search_est_no` → add → submit.
- **TC_BT_NT01**: Non-Tagged transfer via NT Receipt → search → select all → submit → success.
- **TC_BT_NT02**: Non-Tagged transfer via Product entry → search → select all → adjust pcs → submit.
- **TC_BT_PR01**: Purchase Return transfer → set date range → search → select all → submit.
- **TC_BT_PKG01**: Packing Items transfer → select item → enter pcs → add to list → submit.
- **TC_BT_RO01**: Repair Order transfer → enter order no → search → select → submit.
- **TC_BT_OI01**: Other Issue (Tagged) → check `#isOtherIssue` → verify To Branch hidden → scan tag → submit.
- **TC_BT_VAL01**: Try to submit without items → expect toaster `"Please select tag code to proceed.."`.
- **TC_BT_VAL02**: Try to submit without To Branch (non-OtherIssue) → expect `"To Branch Required"`.

---

### Code Patterns & Notes

- **Select2 fields**: Use `fc.select2(...)` or JS executor for `#from_brn`, `#to_brn`, `#lotno`, `#nt_receipt`, `#section_select`.
- **Radio Buttons**: Use `fc.click_element("input[name='transfer_item_type'][value='N']")` for each type.
- **Date Range**: Use JS executor to set date range values directly in `#rpt_payments1`/`#rpt_payments2` for Purchase Return, or interact with the Bill Date datepicker.
- **Grid Verification**: After `class=btrn_search` click, wait for `#bt_search_list tbody tr` (Tagged) or `#bt_nt_search_list tbody tr` (NonTagged) to appear using explicit wait.
- **Preview Verification (Tagged)**: After `#add_to_list` click, wait for `#bt_list tbody tr` to appear before clicking `#add_to_transfer`.
- **Other Issue Branch Handling**: When `isOtherIssue` is checked, the destination branch is set internally to Head Office (`id=other_issue_branch`). Do not attempt to set `#to_brn` in this case.
- **Select All**: Use `driver.execute_script("$('input[type=checkbox]').prop('checked', true).trigger('change');")` or iterate to check all grid rows.
- **Toaster Capture**: Use explicit wait for `.toast-message` or `$.toaster` alert to appear and capture text for `ActualStatus`.
- **Consistency**: Follow `Sparqla` project structure — use `Function_Call`, `ExcelUtils`, no raw Selenium.
- **Wait Pattern**: Use explicit waits for all AJAX-driven dropdowns and grid row insertions.
