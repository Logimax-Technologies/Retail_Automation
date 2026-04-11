# Master Prompt: Purchase Return Automation

Build complete Purchase Return automation for the Retail Automation project. Follow the EXACT same code pattern as `LotGenerate.py`, `QCIssueReceipt.py`, and `SupplierBillEntry.py`.

**File to create**: `C:\Retail_Automation\Sparqla\Test_Purchase\PurchaseReturn.py`  
**Update main.py**: Add `PurchaseReturn` case.

### Controller Details (`admin_ret_purchase.php`)
**Methods**:

- **List Page**: `purchasereturn('list')`
- **Add Form**: `purchasereturn('add')`
- **Save Function**: `returnpoitems()` — handles POST submission containing `returnitems`, `returnpuritems`, and total calculations.

### Navigation
- **Menu**: Purchase → Purchase Return
- **List URL**: `admin_ret_purchase/purchasereturn/list`
- **Add URL**: `admin_ret_purchase/purchasereturn/add`

### Form Fields & Mandatory Status -> Header Section
- ✅ **Type** (Radio): `name="purchase_type"` → Return(0) | Sales(1) | Sales Return(2)
  - *If Sales Return(2) is selected*: Receipt Type and PO Ref are hidden.
- ✅ **Stock Type** (Radio): `name="stock_type"` → Normal(0) | Suspense(1)
- ✅ **Receipt Type** (Radio): `name="purret_receipt_type"` → PO RefNO(0) | Tag(1) | NonTag(2) (Hidden if Type == Sales Return)
- ✅ **Filter by Supplier** (Select2): `id=select_karigar` (Hidden if Type == Sales)
- ✅ **Issue to Supplier** (Select2): `id=purret_to_karigar`
- ✅ **Bill No** (Select2): `id=sales_return_bill_no` (Visbile only if Type == Sales Return)
- ✅ **Purchase Return Convert To** (Radio): `name="pur_return_convert_to"` → Supplier(1) | Manufacturers(2) | Approval Ledger(3) | Stone Supplier(4) | Dia Supplier(5)
- ✅ **Return Reason** (Radio): `name="returnreason"` → Damage(1) | Excess(2)

### Form Fields -> Item Addition Workflows

#### 1. If Type == Return (0) & Receipt Type == PO RefNO (0)
- ✅ **PO Ref No** (Select2): `id=select_po_ref_no`
- *Action*: Auto-populates `#item_detail` table on selection. User must check main checkbox to load rows into `#return_item_detail`.

#### 2. If Type == Return (0) & If Type == Sales(1) &Receipt Type == Tag (1)
- ✅ **Tag Issue From** (Radio): `name="tag_issue_from"` → Available(1) | Sales Return(2) | Partly Sales(3) | H.O Other(4)
- ✅ **Tag Code** (Input): `id=tag_number`
- ⬜ **Old Tag** (Input): `id=old_tag_number`
- ⬜ **BT Code** (Input): `id=bt_number` (Visible if tag_issue_from > 1) BT Code is mandatory if Tag Issue From == Sales Return(2) | Partly Sales(3) | H.O Other(4)
- *Action*: Click `id=tag_history_search` → Auto-populates row in `#return_item_detail`.

#### 3. If Type == Return (0)  & If Type == Sales(1) & Receipt Type == NonTag (2)
- ✅ **NonTag Issue From** (Radio): `name="nontag_issue_from"` → Available(1) | Sales Return(2) | Other Issue(3)
- ✅ **Section** (Select2): `id=select_section`
- ✅ **Product** (Select2): `id=select_product`
- ✅ **Design** (Select2): `id=select_design`
- ✅ **Sub Design** (Select2): `id=select_sub_design`
- ✅ **Piece** (Input): `id=issue_pcs`
- ✅ **Weight** (Input): `id=issue_weight`
- ⬜ **BT Code** (Input): `id=nt_bt_number` (Visible if nontag_issue_from > 1) BT Code is mandatory if Non Tag Issue From == Non tag Sales Return(2) | Nontag H.O Other(3)
- *Action*: Click `id=set_non_tag_stock_list` → Adds row to `#return_item_detail`.
- *Action (If bt_number used)*: Click `id=nontag_search` → Adds row based on BT Code constraints.

#### 4. If Type == Sales Return (2)
- ✅ **Bill No** (Select2): `id=sales_return_bill_no`
- *Action*: Triggers auto-population of `#return_item_detail` via DB query without needing extra search buttons.

### Form Fields -> Per-Item Details Table (`id=return_item_detail`)
Each row contains the following modifiable fields based on class selectors:

- ✅ **Check Box**: `name="return_item_cat[catid][]"` (Must be checked to save)
- ✅ **Pcs**: `class="purreturnpcs"`
- ✅ **GWt**: `class="purreturnweight"`
- ⬜ **LWt** (Stones): Click input `class="add_less_wt"` → Opens `id=cus_stoneModal`
- ⬜ **Other MetalWt**: Click input `class="add_other_metal_wt"` → Opens `id=other_metalmodal`
- ⬜ **Other Charges**: Click input `class="add_other_charges_amt"` → Opens `id=pur_chargeModal`
- ✅ **V.A(%) / Wastage**: `class="purreturnwastper"`
- ✅ **Mc Type**: `class="purreturnmctype"` (1 = Per Gram, 2 = Flat)
- ✅ **Mc**: `class="purreturnmc"`
- ✅ **Touch / Purity**: `class="purreturntouch"`
- ✅ **Calc Type**: `class="purret_calc_type"`
- ✅ **Rate(per GRM)**: `class="purreturnrate"`
- **Readonly Computed fields**:
  - **NWt**: `class="net_wt"`
  - **Pure**: `class="purreturnpure"`
  - **Amount (Taxable)**: `class="purreturnamount"`

### Form Fields -> Data Payload / Hidden Fields (Per-Row)
These fields are hidden but captured in the UI table and sent in the final POST payload (`returnpoitems`):

- `return_item_tax_id`, `return_item_tax_type`, `return_item_tax_percent`
- `po_item_id`, `tag_id`, `ret_item_type`
- `calculation_based_on`, `bill_det_id`, `branch_trans_id`
- `id_qc_issue_details`, `pure_wt_calc_type`

### Form Fields -> Total Summary Section
- ⬜ **Taxable Amount**: `class="total_summary_taxable_amt"` (Readonly)
- ⬜ **TDS Percent**: `class="tds_percent"` / `class="tds_tax_value"` (Readonly)
- ⬜ **CGST / SGST / IGST**: `class="total_summary_cgst_amount"`, etc. (Readonly)
- ⬜ **TCS Percent**: `class="tcs_percent"` / `class="tcs_tax_value"` (Readonly)
- ⬜ **Other Charges Taxable**: `id="other_charges_taxable_amount"`
- ⬜ **Charges TDS**: `class="charges_tds_percent"` / `class="other_charges_tds_tax_value"` (Readonly)
- ⬜ **Discount** (Input): `class="return_discount"`
- ⬜ **Round Off Symbol** (Select): `class="round_off_symbol"` (+ or -)
- ⬜ **Round Off** (Input): `class="return_round_off"`
- ✅ **Narration** (Textarea): `id=returnnarration`
- **Computed Final Price**: `class="return_total_cost"` (Readonly)

### Action Buttons
- ✅ **Save**: `id=return_po_items_submit`
- ⬜ **Cancel**: `class="btn-cancel"`

---

### Full Business Workflow
#### Add Purchase Return Flow
1. **Navigate**: Purchase → Purchase Return → Click Add (`id=add_purchasereturn` or standard add btn).
2. **Setup Header**: Select Receipt Type (PO/Tag/NonTag), supplier (`select_karigar`), and Issue to (`purret_to_karigar`).
3. **Load Items**:
   - **PO Workflow**: Select `select_po_ref_no`, check items in `#item_detail`, wait for them to move to `#return_item_detail`.
   - **Tag Workflow**: Enter `tag_number`, click `tag_history_search`.
   - **NonTag Workflow**: Select Section, Product, Design, enter pcs/wt, click `set_non_tag_stock_list`.
4. **Item Level Adjustments**: Loop through `#return_item_detail` rows.
   - Adjust Wastage %, Mc Type, Mc, Touch, and Rate.
   - Interact with Sub-modals if defined in Excel (Stones, Other Metal, Charges).
5. **Footer Adjustments**: Enter discount and round off.
6. **Verify Calculation**: Call Python `PurchaseRet.calculation()` and ensure totals match UI (`purreturnamount` per row, `return_total_cost` final).
7. **Submit**: Click `id=return_po_items_submit`.
8. **Acknowledgement**: Closes/Submits and redirects to list page.

#### List Verification Flow
1. **Navigate**: `admin_ret_purchase/purchasereturn/list`
2. **Filter**: Set Date Range (Today).
3. **Verify**: Check top row contains the correct Supplier Name, Total Amount, and Status.

---

### Calculation Logic (`PurchaseRet.calculation()`)
Python must re-implement JS `calculate_purchase_return_item_cost()`:

1. **Net Wt** = `GWt - Other_Metal_Wt - Stone_Wt (LWt)`
2. **Pure Wt** (`purreturnpure`):
   - If `karigar_calc_type == 1`: `Net_Wt * ((Touch + Wastage_%) / 100)`
   - If `karigar_calc_type == 2`: `Net_Wt * (Touch / 100)`
3. **MC Value** (`total_mc_value`):
   - Based on `calculation_based_on` (0=Gross, 1=Net, 2=Gross/Net):
   - If `Mc Type == 1`: `MC * Weight_Factor`
   - If `Mc Type == 2`: `MC * Pcs`
4. **Row Amount** (`purreturnamount`):
   - `Item Cost = (Pure_Wt * Rate) + Other_Metal_Amt + Other_Charges_Amt + Total_MC_Value + Stone_Price`
5. **Final Price** (`return_total_cost`):
   - Sum of all row `Amount` values + Global Taxes + Global Total Charges - Discount +/- Round Off.

---

### Expected Excel Sheet Structure
*Since this is a new module, create the following sheets in `Purchase_Return.xlsx` (or add to `Master` file).*

#### Sheet: `PurchaseReturn`
- **Col 1**: TestCaseId
- **Col 2**: TestStatus
- **Col 3**: Select Type (Return / Sales / Sales Return) 
- **Col 4**: Stock Type (Normal Stock / Suspense Stock)
- **Col 5**: Receipt Type (PO / Tag / NonTag - Only valid if SelectType=Return)
- **Col 6**: Filter Supplier
- **Col 7**: Issue Supplier
- **Col 8**: PO Ref No (If PO)
- **Col 9**: Convert To
- **Col 10**: Return reason (Damage / Excess)
- **Col 11**: Sales Return Bill No (If Sales Return)
- **Col 12**: Issue From (1/2/3/4 for Tag/NonTag)
- **Col 13**: Tag Code (If Tag)
- **Col 14**: BT Code (Optional)
- **Col 15**: NonTag Details (Section,Prod,Des,Sub,Pcs,Wt)
- **Col 16**: Pcs
- **Col 17**: GWt
- **Col 18**: Less Weight (Yes/No) → Trigger sub-sheet `PurRet_Stones`
- **Col 19**: Other Metal (Yes/No) → Trigger sub-sheet `PurRet_OtherMetal`
- **Col 20**: Charges (Yes/No) → Trigger sub-sheet `PurRet_Charges`
- **Col 21**: Wastage %
- **Col 22**: MC Type
- **Col 23**: MC
- **Col 24**: Touch
- **Col 25**: Rate
- **Col 26**: Discount
- **Col 27**: Round Off (-10 / +50)
- **Col 28**: TDS % (Optional)
- **Col 29**: TCS % (Optional)
- **Col 30**: Charges TDS % (Optional)
- **Col 31**: Narration
- **Col 32**: Expected Row Amount
- **Col 33**: Expected Total Final Amount

#### Sub-Sheets Structure
Follow the established Tag/EST logic:
- `PurRet_Stones`: TestCaseId, Stone Type, Stone Name, Pcs, Wt, Rate, Expected Amt.
- `PurRet_OtherMetal`: TestCaseId, Metal, Purity, Pcs, Wt, MC Type, MC, Rate, Expected Amt.
- `PurRet_Charges`: TestCaseId, Charge Name, Charge Amt.

---

### Success / Failure Messages
- **Success**: `$.toaster({ priority: 'success', title: 'Success!', message: '...' })` — Alerts and redirects to `return_receipt_acknowladgement` then back to `list`.
- **Validation Failure**: "Please fill required fields." or "Please select karigar."
- **Empty Rows**: "Please select any one items." (checkbox logic).

### Code Patterns to Follow
1. **Dynamic Loading**: Use Explicit Waits for `select_po_ref_no`, `select_karigar`. Check that options load before selecting.
2. **Row Indexing**: `return_item_detail > tbody tr` (Iterate via `len()` of table rows).
3. **Checkbox Requirement**: Check `((//input[@name='return_item_cat[catid][]'])[N])` before row is considered valid for submission.
4. **Calculations**: Read strictly from the computed `input` fields, re-calculate in python, throw `logger.error` if mismatch but do not necessarily fail the test suite instantly (log logic).
