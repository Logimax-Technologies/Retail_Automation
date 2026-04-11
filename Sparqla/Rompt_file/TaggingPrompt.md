# Master Prompt: Tagging Automation

Build complete Tagging automation for the Retail Automation project. Follow the EXACT same code pattern as `LotGenerate.py`, `QCIssueReceipt.py`, and `SupplierBillEntry.py`.

**File to create**: `c:\Retail_Automation\Sparqla\Test_Tag\Tagging.py`  
**Update main.py**: Add `Tagging` case.

### Controller Details (`admin_ret_tagging.php`)
**Function**: `tagging($type="",$id="",$tag_print_id="")`

**Switch Cases**:
- `list` → Tag List page.
- `add` → Add Tag Form.
- `save` → POST — save new tag(s).
- `tag_scan` → Barcode scan view.
- `tag_mark` → Green tag mark/unmark.

**Submission**: Form POST to `admin_ret_tagging/tagging/save`

---

### Navigation
- **Menu**: Inventory → Tagging
- **List URL**: `admin_ret_tagging/tagging/list`
- **Add URL**: `admin_ret_tagging/tagging/add`

---

### Form Fields & Mandatory Status
- **Header / Lot Section**:
    - ✅ Branch (Select2): `id=branch_select` (multi-branch accounts only)
    - ✅ Lot No (Select2): `id=tag_lot_received_id`
    - ✅ Employee (Select2): `id=emp_select`
    - ⬜ Section (Select2): `id=section_select` (shown only if `is_section_req==1`)
    - ⬜ Product (Select2): `id=tag_lt_prod`
- **Lot Summary Table (`id=lt-det`)** (auto-loaded on Lot select, read-only):
    - TD[2]: Pieces | TD[3]: Gross Wt | TD[4]: Net Wt | TD[5]: Dia Wt
    - Metal Name: `id=lt_metal` (span — e.g. `GOLD - 916.0000`)
    - Category: `id=lt_category` | Supplier: `id=lt_karigar_name`
- **Per-Tag Entry**:
    - ✅ Design (Select2): `id=des_select`
    - ✅ Sub Design (Select2): `id=sub_des_select`
    - ✅ Pieces: `id=tag_pcs`
    - ✅ No. of Items: `id=bulk_tag`
    - ✅ Gross Weight: `id=tag_gwt` (TAB triggers stone popup)
    - ⬜ Less Weight stones: Click Select2 span at row 8 → `Tag_Stone` sub-module
    - ⬜ Other Metal: Click Select2 span at row 9 → `Tag_othermetal` sub-module
    - ✅ Wastage %: `id=tag_wast_perc`
    - ✅ MC Type (Select): `id=tag_id_mc_type`
    - ✅ MC Value: `id=tag_mc_value`
    - ⬜ Size (Select2): `id=tag_size` — **Mandatory if `has_size == 1`**
    - ✅ Calc Type (Select): `id=tag_calculation_based_on`
    - ⬜ HUID 1: `id=tag_huid` | HUID 2: `id=tag_huid2`
    - ⬜ Sell Rate / MRP: `id=tag_sell_rate` — **Mandatory if `tag_sales_mode == 1` (Fixed)**
    - ⬜ Certification No: `id=cert_no` | Certification Image: `id=cert_img`
- **Computed** (read-only):
    - Net Wt: `id=tag_nwt` | Sale Value: `id=tag_sale_value`
- **Action Buttons**:
    - ✅ Add Tag: `id=addTagToPreview`
    - ✅ Add & Copy: `id=addTagToPreviewAndCopy`
    - Close Stone Popup: `(//button[@id="close_stone_details"])[1]`

---

### Full Business Workflow
1. **Add Tag Flow**
    - **Navigate**: Inventory → Tagging → Click Add (`id=add_tagging`).
    - **Board Rates**: Capture live Metal Rates from header popup (`//span[@class='header_rate']/b`) before the loop.
    - **Lot Selection**: Select Branch and Lot No. Verify lot summary table (Pieces, GWT, DWT) against `Lot.Lotdetails()`.
    - **Product/Section**: Select Product (`id=tag_lt_prod`) and Section (if applicable).
    - **Per-Tag**: Select Design, Sub Design → Enter Pieces, Bulk Items, GWT → TAB.
    - **Less Weight** (if `Less Weight == Yes`): Call `Tag_Stone.test_tagStone()` (sheet: `Tag_LWt`).
    - **Other Metal** (if `Other Metal == Yes`): Call `Tag_othermetal.test_othermetal()` (sheet: `Tag_othermetal`).
    - **Size**: Select Size conditionally if `#has_size` == 1.
    - **MC & Calc**: Enter Wastage %, MC Type, MC Value, Calc Type.
    - **Sell Rate**: If `#tag_sales_mode` == 1 (Fixed), enter MRP in `tag_sell_rate`. If 2 (Flexible), it recalculates based on weights.
    - **Verify Calculation**: Python `Tagging.calculation()` result must match `#tag_sale_value` on page.
    - **Submit**: Click `id=addTagToPreview` (more rows) or `id=addTagToPreviewAndCopy` (duplicate).
    - **Post-Save**: Call `update_Tagdetails()` — extracts tag preview table and writes Tag Nos to `Tag_EST` sheet.

2. **List Verification Flow**
    - **Navigate**: `admin_ret_tagging/tagging/list`
    - **Filter**:
        - ✅ Date Range (`id=tag-dt-btn`) → Select **Today**.
        - ✅ Lot No (`id=tag_lot_no`).
        - ✅ Karigar (`id=tag_karigar`).
        - ✅ Click Search (`id=tag_lot_search`).
    - **Search**: Enter Tag No in DataTable search box.
    - **Columns**: DataTable `id=tag_list` — Lot ID, Old Tag ID, Branch, Po-RefNo, Section, Karigar, Date, Pieces, Gross Wgt, Stn Wgt, Dia Wgt, Net Wgt.

---

### Calculation Logic (`Tagging.calculation()`)
Python re-implements all calc types:
- **Mc on Gross, Wast On Net**: `ceil((NWT + Wast%*NWT/100) * rate + MC_on_GWT + LWtAmt)`
- **Mc & Wast On Net**: `ceil((NWT + Wast%*NWT/100) * rate + MC_on_NWT + LWtAmt)`
- **Mc & Wast On Gross**: `ceil((NWT + Wast%*GWT/100) * rate + MC_on_GWT + LWtAmt)`
- **Fixed Rate based on Weight**: Same as Mc & Wast On Gross.
- MC-Type `1` = Piece (flat) | else = Per Gram (× weight).
- Board rate lookup: `GOLD - 916.0000` → 22KT rate | `GOLD - 75.0000` → 18KT | `SILVER - 92.5000` → Silver.

---

### Success / Failure Messages
- **Success**: Tag row added to preview table `#lt_item_tag_preview`.
- **Lot Completed Alert**: "Tag completed. Please click here to reload" (`div.tag_reload_div`).
- **Validation Failure**: Alert box — "Please fill mandatory fields."

---

### Excel Sheet: Tag
- **File Path**: `C:\Users\Dell\Desktop\sqrqlas\Sqarqla_Retail_data2.xlsx`
- **Sheet Name**: `Tag`

- **Col 1**: TestCaseId
- **Col 2**: TestStatus
- **Col 3**: ActualStatus
- **Col 4**: Branch
- **Col 5**: Lot No
- **Col 6**: Product
- **Col 7**: Section
- **Col 8**: Design
- **Col 9**: Sub Design
- **Col 10**: Pieces
- **Col 11**: No.of Items
- **Col 12**: GWT
- **Col 13**: Less Weight (Yes/No)
- **Col 14**: Other Metal (Yes/No)
- **Col 15**: MC&VA Available (Yes/No)
- **Col 16**: Wastage%
- **Col 17**: Mc Type
- **Col 18**: MC
- **Col 19**: Size
- **Col 20**: Calc Type
- **Col 21**: HUID1
- **Col 22**: HUID2
- **Col 23**: Rate / MRP
- **Col 24**: Attribute (Yes/No)
- **Col 25**: Attribute Name
- **Col 26**: Certification (Yes/No)
- **Col 27**: Certification No
- **Col 28**: Certification Image (path)
- **Col 29**: Button (Add/Copy)

**Sub-sheets**: `Tag_LWt` (Less Weight stones), `Tag_othermetal` (Other Metal), `Tag_EST` (populated post-tag with Tag Nos).

---

### LWT Popup Box — Sub-Module Prompt (`Tag_Stone.py`)

Build `Tag_Stone.test_tagStone()` sub-module called when `Less Weight == Yes`. Follow the EXACT same code pattern as `Tag_Stone.py`.

**File**: `c:\Retail_Automation\Sparqla\Test_Tag\Tag_Stone.py`
**Popup Table**: `id=estimation_stone_cus_item_details`
**Trigger**: Auto-opens when GWT is entered and TAB is pressed.
**Row Selector Pattern**: `est_stones_item[field][]` — all fields use index `[N]` (1-based row counter).

#### Popup Fields & Mandatory Status
- **Selection**:
    - ✅ Less Weight / Show in LWT (Select): `(//select[@name='est_stones_item[show_in_lwt][]'])[N]`
    - ✅ Stone Type (Select): `(//select[@name='est_stones_item[stones_type][]'])[N]`
    - ✅ Stone Name (Select): `(//select[@name='est_stones_item[stone_id][]'])[N]`
    - ✅ Quality / Code (Select): `(//select[@name='est_stones_item[quality_id][]'])[N]`
    - ✅ Pieces (Input): `(//input[@name='est_stones_item[stone_pcs][]'])[N]`
    - ✅ Weight (Input): `(//input[@name='est_stones_item[stone_wt][]'])[N]`
    - ✅ Weight UOM (Select): `(//select[@name='est_stones_item[uom_id][]'])[N]` — `gram` / `carat`
    - ✅ Cal. Type (Radio): `value='1'` → Wt-based | `value='2'` → Pcs-based
        - XPath: `(//input[@name='est_stones_item[cal_type][N]' and @value='1'])`
    - ✅ Rate (Input): `(//input[@name='est_stones_item[stone_rate][]'])[N]` — press TAB to auto-calc Amount
    - ⬜ Amount (computed, readonly): `(//input[@name='est_stones_item[stone_price][]'])[N]`
- **Footer Totals** (verify after all rows entered):
    - ✅ Total Wt (gram): `//table[@id='estimation_stone_cus_item_details']/tfoot/tr/td[6]`
    - ✅ Total Amount: `//table[@id='estimation_stone_cus_item_details']/tfoot/tr/td[13]`
- **Row Actions**:
    - ✅ Add Next Row: `(//button[@class='btn btn-success btn-xs create_stone_item_details'])[N]`
    - ✅ Update / Save: `(//button[@id='update_stone_details'])`
    - ⬜ Close (no save): `(//button[@id='close_stone_details'])[1]`

#### LWT Workflow
1. **Open**: Popup auto-opens on GWT TAB. Dismiss first with `close_stone_details` if needed, then open manually via Select2 span click.
2. **Per Stone Row**: Select LWT status → Stone Type → Stone Name → Quality → Enter Pcs → Enter Wt → Select UOM → Select Cal.Type → Enter Rate → TAB (Amount auto-fills).
3. **Multiple Stones**: Click `create_stone_item_details` to add next row. Increment `N`.
4. **Verify Amount**: Cal.Type `Wt` → `ceil(Wt × Rate)`. Cal.Type `Pcs` → `ceil(Pcs × Rate)`.
5. **Verify Footer**: Total Wt gram — if UOM=`carat` → `gram = carat / 5` (3 decimals). Total Amount = sum of all stone amounts.
6. **Save**: Click `update_stone_details`. Returns `(status_msg, Wt_gram, TotalAmount)`. Returns to `Tagging.py`.

#### Success / Failure Messages
- **Success**: Returns `("Less weight detail Add successfully", Wt_gram, TotalAmount)`.
- **Calc Mismatch**: Logged as print warning — does not fail the test.

#### Excel Sheet: `Tag_LWt`
- **Col 1**: Test Case Id
- **Col 2**: Less Weight (dropdown value e.g. `Yes`)
- **Col 3**: Type (Stone Type name)
- **Col 4**: XPATH (Stone Name visible text)
- **Col 5**: Code (Quality name)
- **Col 6**: Pcs
- **Col 7**: Wt
- **Col 8**: Wt Type (`gram` / `carat`)
- **Col 9**: Cal.Type (`Wt` / `Pcs`)
- **Col 10**: Rate
- **Col 11**: Amount (expected, for verification)

#### Code Patterns & Logic
- **Row loop**: Match `Test Case Id` from `Tag_LWt` sheet to `test_case_id` passed in from `Tagging.py`.
- **Count tracking**: `count = ExcelUtils.Test_case_id_count()` — if `count != 1`, click Add Row and continue; else read footer totals and break.
- **Wt_gram**: read from footer `td[6]` text (string). Passed back to `Tagging.calculation()` as `Wt_gram`.
- **TotalAmount**: read from footer `td[13]` as float. Passed back to `Tagging.calculation()` as the `LWtAmt` component.

---

### Test Scenarios
- **TC_TAG_01**: Select Lot → Select Product/Design → Enter weights → Submit → Verify tag in preview.
- **TC_TAG_CALC_01**: Enter GWT, Wastage, MC → Verify `#tag_sale_value` matches Python calculation.
- **TC_TAG_LWT_01**: Less Weight = Yes → Enter stone details → Verify deduction in Net Wt.
- **TC_TAG_HUID_01**: Enter HUID1 → Verify it is saved in preview table.
- **TC_TAG_CERT_01**: Add Certification No and Image → Submit → Verify in preview.

---

### Code Patterns & Logic
- **Board Rate Capture**: Click `//span[@class='header_rate']/b` → read rate rows before the loop starts.
- **Lot Change Detection**: Compare `row_data["Lot No"]` vs `before_Lot`; re-select only on change.
- **Stone Popup**: After entering GWT and pressing TAB, a popup auto-opens. Always dismiss with `(//button[@id="close_stone_details"])[1]` before continuing.
- **Wait Pattern**: Use explicit waits for Select2 and dynamic table loading.
- **Preview Table**: `#lt_item_tag_preview` accumulates rows; `update_Tagdetails()` reads it and writes to `Tag_EST` sheet.
- **Consistency**: Follow `Sparqla` project structure — `Function_Call`, `ExcelUtils`, no raw Selenium.
