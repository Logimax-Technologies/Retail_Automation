# Master Prompt: Stock Issue Automation

Build complete Stock Issue / Receipt automation for the Retail Automation project. Follow the EXACT same code pattern as `QCIssueReceipt.py`, `HMIssueReceipt.py`, and `LotGenerate.py`.

**File to create**: `c:\Retail_Automation\Sparqla\Test_StockIssue\StockIssue.py`  
**Update main.py**: Add `StockIssue` case.

---

### Controller Details (`admin_ret_stock_issue.php`)
**Function**: `stock_issue($type="", $id="", $received_time="")`

**Switch Cases**:
- `list` → Stock Issue List page.
- `add`  → Add Stock Issue / Receipt Form.
- `save` → POST — save Issue or Receipt.

**Submission**: Form POST to `admin_ret_stock_issue/stock_issue/save`

---

### Navigation
- **Menu**: Inventory → Stock Issue
- **List URL**: `admin_ret_stock_issue/stock_issue/list`
- **Add URL**: `admin_ret_stock_issue/stock_issue/add`

---

### Form Fields & Mandatory Status

> **Actual UI field order (header row, left → right)**:  
> Type → Issue From → Select Employee → Issue Type → Stock Type → Select Metal → Issue to

#### Header / Common Section (visible for both Issue & Receipt)
- ✅ **Type** (Radio): `id=type_issue` (value=`1` → Issue, default selected) / `id=type_receipt` (value=`2` → Receipt)
- ✅ **Issue From** — Branch (Select2): `id=branch_select`  
  — For Head Office users, this is a dropdown. For branch users it is auto-filled (hidden `id=id_branch`).
- ⬜ **Select Employee** (Select2): `id=sel_emp` — the employee who is doing the issue (optional field visible in header).
- ✅ **Issue Type** (Select2): `id=issue_type`  
  — Loaded dynamically via `get_stock_issue_type()` AJAX call on page load.  
  — **Actual values from live system**: `Marketing` | `Photo Shoot`  
  — Each option carries an `issue_to_cus` attribute that controls downstream logic.
- ✅ **Stock Type** (Select): `id=stock_type`  
  — `1` = Taged (Tagged) | `2` = Non Taged (Non-Tagged)
- ✅ **Select Metal** (Select2): `id=metal`  
  — e.g., `GOLD`, `SILVER`. Loaded via `get_ActiveMetals()`. Visible only for Issue type (`class=tagelement`).
- ✅ **Issue to** (Select): `id=issued_to`  
  — `Customer` (value=`1`) | `Employee` (value=`2`) | `karigar` (value=`3`)  
  — Based on selection, only the matching recipient section appears below.

#### Recipient Section — Dynamic (toggled by `issued_to` value)
> Only ONE of the following three panels is shown at a time.

- **If `issued_to = Customer` (value=1)** → Shows **Customer** field:
  - Customer Name/Mobile (Typeahead): `id=est_cus_name` — type name or mobile → autocomplete → select.
  - Customer ID (Hidden): `id=cus_id`
  - Customer Mobile (Hidden): `id=cus_mobile`
  - Add New Customer Button: `id=add_new_customer` (green `+` icon)
  - Edit Customer Button: `id=edit_customer` (blue pencil icon)
  - OTP Required (Hidden): `id=otp_required` — if `1`, OTP modal fires on Save.

- **If `issued_to = Employee` (value=2)** → Shows **Select Employee** field:
  - Employee Dropdown (Select2): `id=issue_employee`, placeholder = "Select Employee"

- **If `issued_to = karigar` (value=3)** → Shows **Select karigar** field:
  - Karigar Dropdown (Select2): `id=karigar`, placeholder = "Select Karigar"

#### Issue Items Section (shown for Issue flow only, below recipient)

**Tagged Stock** (`stock_type=1`, `class=tagelement`):
- ⬜ Section/Product Select2: `id=section_select` — filters tag scan to a specific section (e.g., `GOLD CHAIN`)
- ✅ Tag Scan Code (Input): `id=issue_tag_code`, placeholder = "Tag Scan Code" → Search Button: `id=issue_tag_search`
- ⬜ OLD Tag Scan (Input): `id=issue_old_tag_code`, placeholder = "OLD Tag Scan" → Search Button: `id=issue_old_tag_search`
- ⬜ Rate Per Gram (Input): `id=rate_per_gram`, placeholder = "Rate per Gram"
- **Issue Grid**: `id=tagissue_item_detail`  
  Columns: Tag Code | Category | Purity | Section | Product | Design | Sub Design | Pcs | GWgt | NWgt | Rate | Stone | Other Metal | Taxable Amount | Tax | Tax Amount | Net Amount | Action  
  Footer row shows: Total Pcs | Total GWgt | Total NWgt | Total Stone Amt | Total Other Metal | Total Taxable | (Tax%) | Total Tax Amt | Total Net Amt

**Non-Tagged Stock** (`stock_type=2`, `class=nontagelement`):
- Search Non Tag Button: `id=search_non_tag` — opens the Non-Tag Search Modal
- **Non-Tag Modal Fields**:
  - Section (Select2)
  - Product (Select2)
  - Design (Select2)
  - Sub Design (Select2)
  - Pcs (Input)
  - Gross Wt (Input)
  - Net Wt (Input)
- **NonTag Issue Grid**: `id=nontagissue_item_detail`  
  Columns: ☐ | Section | Product | Design | Pcs | GWgt | NWgt | Taxable Amount | Tax | Tax Amount | Net Amount | Action

#### Receipt Flow (Type=2, class=`type_receipt`)
- ✅ Select Issue No (Select2): `id=select_issue_no` — loaded dynamically
- ✅ Receipt Tag Scan Code (Input): `id=receipt_tag_code` → Search Button: `id=receipt_tag_search`
- ⬜ Old Tag Scan (Input): `id=receipt_old_tag_code` → Search Button: `id=receipt_old_tag_search`
- **Receipt Tagged Grid**: `id=tag_receipt_item_detail`
  - Columns: Tag Code | Category | Purity | Product | Design | Sub Design | Pcs | GWgt | NWgt | Rate | Stone | Other Metal | Taxable Amount | Tax | Tax Amount | Net Amount | Action
- **Non-Tag Receipt Grid**: `id=nontag_receipt_item_detail`
  - Columns: ☐ | Section | Product | Design | Pcs | GWgt | NWgt | Taxable Amount | Tax | Tax Amount | Net Amount | Action

#### OTP Modal (shown when `otp_required=1` for Customer issues)
- `id=stock_otp_modal` — Bootstrap modal
- OTP Input: `id=stock_trns_otp`
- Verify Button: `id=verify_stock_otp`
- Resend OTP Button: `id=resend_stock_otp`
- Save & Submit Button: `class=submit_stock_issue` (enabled after OTP verified)

#### Action Buttons
- Save Button (non-OTP): `id=stock_issue_submit`
- Cancel Button: `class=btn-cancel`

---

#### Flow 1: Head Office Issue Flow (The primary flow for Stock Issue)

> **Scenario**: "Issue from Head Office, select employee, choose Marketing/Photo Shoot, select Stock Type (Tagged/Non-Tagged), select Metal, and issue to a Customer, Employee, or Karigar."

1. **Navigate**: Inventory → Stock Issue → Click `Add Stock Issue`.
2. **Select Type**: Radio `id=type_issue` should be selected (Issue=1).
3. **Issue From**: Select `HEAD OFFICE` from `id=branch_select`.
4. **Select Employee**: Select the designated employee from `id=sel_emp` (e.g., `111-Developer Logimax`).
5. **Issue Type**: Select relevant type from `id=issue_type`.  
   — **Available options**: `Marketing` | `Photo Shoot`.
6. **Stock Type**: Select from `id=stock_type`.  
   — `Taged` (1) for barcode items.  
   — `Non Taged` (2) for loose items/bulk.
7. **Select Metal**: Select from `id=metal` (e.g., `GOLD`).
8. **Issue to**: Select the recipient type from `id=issued_to`. This dynamically toggles the field below:
   - **If Customer** (value=1): `id=est_cus_name` appears → input name/mobile → select match.
   - **If Employee** (value=2): `id=issue_employee` appears → select employee name.
   - **If Karigar** (value=3): `id=karigar` appears → select karigar name.
9. **Issue Items (Tagged Flow)**:  
   — Optional: Select Section (`id=section_select`).  
   — Type barcode in `id=issue_tag_code` → Click `id=issue_tag_search`.  
   — **Verification**: Wait for the tag details to load in the `id=tagissue_item_detail` grid.
10. **Issue Items (Non-Tagged Flow)**:  
    — Click `id=search_non_tag` → Fill modal fields (Pcs, Weight, etc.) → Save to grid.
11. **Remark**: Enter any notes in `id=remark`.
12. **Submit**: Click `id=stock_issue_submit`.
    - Handle OTP modal if `otp_required=1`.
13. **Post-Save & ID Capture**:
    - Capture the success message (`Stock Issued successfully..`) from the initial tab.
    - **Print Tab Handling**: A new tab opens with the URL format: `.../stock_issue/issue_print/{id}` (e.g., `145`).
        1. Switch to the new tab.
        2. Extract the **Issue ID** from the URL (the trailing number).
        3. Extract the **Issue No / Invoice No** from the page content (e.g., `25-00011` — see Delivery Challan header).
        4. Close the print tab and switch back to the main window.
14. **Listing Page Verification**:
    - Navigate to `admin_ret_stock_issue/stock_issue/list`.
    - Select `Issued` from the **Status** dropdown and click **Search**.
    - Enter the captured **Issue ID** (e.g., `145`) in the table's search input.
    - **Verify**: Ensure the row appears with the correct **Issue No** (`25-00011`).
15. **Excel Synchronization**:
    - Write the captured `Issue No` to the `ActualStatus` of the current row and **store it for the next linked Receipt flow**.


#### Flow 2: Receipt Flow (Tagged & Non-Tagged)

> **Scenario**: "Select Receipt, choose branch/employee, select the original Issue No, and confirm receipt of issued items (Tagged or Non-Tagged)."

1. **Navigate**: Inventory → Stock Issue → Click `Add Stock Issue`.
2. **Select Type**: Click radio `id=type_receipt` (value=`2`).
3. **Issue From**: Select Branch via `id=branch_select`.
4. **Select Employee**: Select from `id=sel_emp`.
5. **Stock Type**: Select `Taged` (1) or `Non Taged` (2) as per the original issue.
6. **Select Issue No**: Select the **Issue No** from `id=select_issue_no` (e.g., `25-00011`).
7. **Handle Items (Tagged)**:
   - If `Stock Type` = `Taged`, the scan field `#receipt_tag_code` appears.
   - Enter tag code → Click `#receipt_tag_search`.
   - Verify row in `#tag_receipt_item_detail`.
8. **Handle Items (Non-Tagged)**:
   - If `Stock Type` = `Non Taged`, the current screenshot's list grid appears (`#nontag_receipt_item_detail`).
   - Items linked to the selected **Issue No** are automatically loaded into the grid.
   - **Select Items**: Check the checkboxes for all items (e.g., SILVER ARTICLES - KODI, KOLUSUUU).
   - **Verification**: Ensure Section, Product, Design, Pcs, GWgt, and NWgt match expectations.
9. **Submit**: Click `id=stock_issue_submit` (or the Save button shown in screenshots).
10. **Post-Save**: Capture `"Stock Receipt Added successfully.."`.

---



### Success / Failure Messages
- **Issue Success**: `"Stock Issued successfully.."` (returned as JSON `message` key)
- **Receipt Success**: `"Stock Receipt Added successfully.."` (returned as JSON `message` key)
- **Failure**: `"Unable to proceed the requested process"`
- **No items scanned**: Alert or validation block prevents submission.
- **OTP Required**: Modal `id=stock_otp_modal` opens; must verify OTP before `class=submit_stock_issue` is enabled.

---

### Excel Sheet: `StockIssue`
- **File Path**: `C:\Users\Dell\Desktop\sqrqlas\Sqarqla_Retail_data2.xlsx`
- **Sheet Name**: `StockIssue`

| Col | Header | Description |
|-----|--------|-------------|
| 1 | TestCaseId | Unique test case identifier |
| 2 | TestStatus | `Run` / `Skip` / `Done` |
| 3 | ActualStatus | Populated after run — success/failure message |
| 4 | ProcessType | `Issue` or `Receipt` (maps to radio: 1 or 2) |
| 5 | IssueFrom | Branch name (for `branch_select`) |
| 6 | SelEmp | Employee name for `sel_emp` |
| 7 | IssueType | Issue type name (e.g., `To Branch`, `To Customer`) |
| 8 | StockType | `1` = Tagged, `2` = Non Tagged |
| 9 | IssuedTo | `1` = Customer, `2` = Employee, `3` = Karigar |
| 10 | CusName | Customer name or mobile (for `est_cus_name`) — used when IssuedTo=1 |
| 11 | IssueEmployee | Employee name for `issue_employee` — used when IssuedTo=2 |
| 12 | Karigar | Karigar name for `karigar` — used when IssuedTo=3 |
| 13 | Metal | Metal name for `metal` select |
| 14 | Section | Section name for `section_select` (optional) |
| 15 | TagCode | Barcode to scan in `issue_tag_code` |
| 16 | OldTagCode | Old barcode to scan in `issue_old_tag_code` (optional) |
| 17 | RatePerGram | Rate entered in `rate_per_gram` |
| 18 | NT_Product | Non-Tag: Product name in modal |
| 19 | NT_Design | Non-Tag: Design name in modal |
| 20 | NT_SubDesign | Non-Tag: Sub Design name in modal |
| 21 | NT_Pcs | Non-Tag: Number of pieces |
| 22 | NT_GrossWt | Non-Tag: Gross weight |
| 23 | NT_NetWt | Non-Tag: Net weight |
| 24 | ReceiptIssueNo | Issue No to select in `select_issue_no` for Receipt flow |
| 25 | ReceiptTagCode | Tag code to scan in `receipt_tag_code` for Receipt flow |
| 26 | ReceiptOldTagCode | Old tag code for `receipt_old_tag_code` (optional) |
| 27 | Remark | Remarks for `id=remark` |

**Sample Rows**:

| TestCaseId | TestStatus | ActualStatus | ProcessType | IssueFrom | SelEmp | IssueType | StockType | IssuedTo | CusName | IssueEmployee | Karigar | Metal | Section | TagCode | OldTagCode | RatePerGram | NT_Product | NT_Design | NT_SubDesign | NT_Pcs | NT_GrossWt | NT_NetWt | ReceiptIssueNo | ReceiptTagCode | ReceiptOldTagCode | Remark |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC_SI_001 | Run | | Issue | Head Office | Admin | To Customer | 1 | 1 | Arun Kumar | | | Gold | | T001 | | 5000 | | | | | | | | | | Issue Tagged to Customer |
| TC_SI_002 | Run | | Issue | Head Office | Admin | To Employee | 1 | 2 | | Emp1 | | Gold | G Section | T002 | | 5500 | | | | | | | | | | Issue Tagged to Employee |
| TC_SI_003 | Run | | Issue | Head Office | Admin | To Karigar | 1 | 3 | | | Karigar1 | Silver | | T003 | | 4500 | | | | | | | | | | Issue Tagged to Karigar |
| TC_SI_004 | Run | | Issue | Head Office | Admin | To Customer | 2 | 1 | Arun Kumar | | | | | | | 5000 | Ring | Design1 | SubDes1 | 2 | 12.5 | 11.8 | | | | NonTag Issue to Customer |
| TC_SI_005 | Run | | Receipt | Head Office | Admin | | 1 | | | | | | | | | | | | | | | | ISS001 | T001 | | Receipt Tagged from Issue |
| TC_SI_006 | Run | | Receipt | Head Office | Admin | | 2 | | | | | | | | | | | | | | | | 25-00011 | | | Receipt Non-Tagged from Issue |

---

### Automation Logic — `StockIssue.py`

#### Key Patterns
- **Navigation**: Call `fc.navigate_to_url(...)` → Click Add button → `fc.click_element('#add_stock_issue')` or equivalent.
- **Type Selection**: Use `fc.click_element('#type_issue')` or `fc.click_element('#type_receipt')` based on `ProcessType`.
- **Branch**: `fc.select('#branch_select', IssueFrom)` — skip if branch user (auto-set).
- **SelEmp**: `fc.select('#sel_emp', SelEmp)`.
- **IssueType**: `fc.select('#issue_type', IssueType)` using Select2.
- **StockType**: `fc.select('#stock_type', StockType)`.
- **IssuedTo**: `fc.select('#issued_to', IssuedTo)`.
- **Customer lookup**: Type in `#est_cus_name` → wait for autocomplete suggestion → click match; or click `#add_new_customer` for new.
- **Employee**: `fc.select('#issue_employee', IssueEmployee)`.
- **Karigar**: `fc.select('#karigar', Karigar)`.
- **Metal**: `fc.select('#metal', Metal)`.
- **Section**: `fc.select('#section_select', Section)` if non-empty.
- **Tag Scan**: `fc.input_text('#issue_tag_code', TagCode)` → `fc.click_element('#issue_tag_search')` → wait for row in `#tagissue_item_detail`.
- **Old Tag Scan**: `fc.input_text('#issue_old_tag_code', OldTagCode)` → `fc.click_element('#issue_old_tag_search')`.
- **Rate**: `fc.input_text('#rate_per_gram', RatePerGram)`.
- **NonTag**: `fc.click_element('#search_non_tag')` → fill modal fields → click add → verify row in `#nontagissue_item_detail`.
- **Receipt IssueNo**: `fc.select('#select_issue_no', ReceiptIssueNo)`.
- **Receipt Tag Scan**: `fc.input_text('#receipt_tag_code', ReceiptTagCode)` → `fc.click_element('#receipt_tag_search')`.
- **Remark**: `fc.input_text('#remark', Remark)`.
- **Save**: `fc.click_element('#stock_issue_submit')`.
- **OTP Flow**: If `otp_required=1`, wait for `#stock_otp_modal` → input OTP in `#stock_trns_otp` → click `#verify_stock_otp` → click `.submit_stock_issue`.
- **Result Capture**: Read JSON response / success alert → write to `ActualStatus` via `ExcelUtils.write_actual_status(...)`.

#### Process Loop
```
for each row in StockIssue sheet where TestStatus == "Run":
    navigate to add page
    select ProcessType (Issue / Receipt)
    fill header fields
    if Issue + Tagged: scan tag(s), enter rate
    if Issue: capture Issue ID and Invoice No from print tab; verify on list page
    if Receipt: use captured Invoice No in select_issue_no, scan receipt tags
    enter remark
    click save (handle OTP if required)
    capture result
    update ActualStatus in Excel
```

---

### Test Scenarios
- **TC_SI_T01**: Issue Tagged item to Customer → Verify row in grid → Save → Success message.
- **TC_SI_T02**: Issue Tagged item to Employee → Verify row → Save → Success.
- **TC_SI_T03**: Issue Tagged item to Karigar → Verify row → Save → Success.
- **TC_SI_NT01**: Issue Non-Tagged item via Search Non Tag modal → Fill Section/Product/Design/SubDesign/Pcs/Wt → Save → Success.
- **TC_SI_R01**: Receipt — Select Issue No → Scan tag → Save → `"Stock Receipt Added successfully.."`.
- **TC_SI_OTP01**: Customer issue with OTP enabled → Fill OTP → Verify → Save → Success.
- **TC_SI_VAL01**: Try to save without scanning any tag → Expect validation block/alert.
- **TC_SI_VAL02**: Try to scan an already-issued tag → Expect error alert from server.

---

### Code Patterns & Notes
- **Show/Hide Logic**: JS toggles `type_issue` / `type_receipt` / `tagelement` / `nontagelement` divs on radio change. Selenium must wait for the correct section to be visible before interacting.
- **Issue Type AJAX**: `#issue_type` is populated after page load via `get_stock_issue_type()`. Use explicit wait before selecting.
- **Select2 fields**: Use `fc.select2(...)` or JS executor to set values for Branch, IssueType, Metal, Section, IssuedTo, IssueEmployee, Karigar, SelectIssueNo.
- **Tag Grid Verification**: After scan, verify a new row appears in `#tagissue_item_detail tbody`.
- **Consistency**: Follow `Sparqla` project structure — use `Function_Call`, `ExcelUtils`, no raw Selenium.
- **Wait Pattern**: Use explicit waits for all AJAX-driven dropdowns and grid row insertions.
