# 🧠 Sparqla Retail Automation — System Brain

> Last updated: 2026-03-25 | Source: All 65 Python files, Utils, main.py, 23 prompts

---

## 1. 🏗️ Architecture Overview

```
main.py
  └─ Reads Master sheet from Excel ──► functions_to_execute[]
       └─ For each function:
            match function_name:
              case "Login": Login(driver).test_login()
              case "Billing": Billing(driver).test_Billing()
              ... (35+ cases)
```

### Key Global Constants (set in `Utils/Excel.py`)
| Constant | Value |
|---|---|
| `ExcelUtils.file_path` | `C:\Users\Dell\Desktop\sqrqlas\Sqarqla_Retail_data2.xlsx` |
| `ExcelUtils.BASE_URL` | `https://qa.retail.logimaxindia.com/admin/` |
| `ExcelUtils.SCREENSHOT_PATH` | `C:\Retail_Automation\Sparqla\Reports\screenshots` |

---

## 2. 📁 Directory & Module Map

### Utility Layer (`Utils/`)
| File | Purpose |
|---|---|
| `Excel.py` | `ExcelUtils` — file paths, `get_valid_rows()`, `get_master_sheet_data()`, `update_master_status()`, `get_column_number()` |
| `Function.py` | `Function_Call` — all UI interaction helpers (click, fill, dropdown, autocomplete, alert) |
| `Board_rate.py` | `Boardrate.Todayrate()` — fetches live gold/silver board rate from the UI |

### All Active Modules (in `main.py`)

| Master Sheet Name | Class | File | Entry Method |
|---|---|---|---|
| `Login` | `Login` | `Test_login/Login.py` | `test_login()` |
| `Metal` | `Metal` | `Test_master/Metal.py` | `test_metal()` |
| `CategoryName` | `Category` | `Test_master/Category.py` | `test_category()` |
| `Product` | `Product` | `Test_master/Product.py` | `test_product()` |
| `Design` | `Design` | `Test_master/Design.py` | `test_design()` |
| `SubDesign` | `Subdesign` | `Test_master/Subdesign.py` | `test_subdesign()` |
| `Designmapping` | `Designmapping` | `Test_master/Designmapping.py` | `test_designmapping()` |
| `Subdesignmapping` | `Subdesignmapping` | `Test_master/Subdesignmapping.py` | `test_subdesignmapping()` |
| `MC&VA` | `McVa` | `Test_master/MCVA.py` | `test_mc_va()` |
| `Lot` | `Lot` | `Test_lot/Lot.py` | `test_lot()` |
| `Tag` | `Tag` | `Test_Tag/Tag.py` | `test_tag()` |
| `Vendor` | `VendorRegistration` | `Test_vendor/Vendor.py` | `test_vendor_registration()` |
| `Customer` | `CustomerOrderTR` | `Test_Customer/Customer.py` | `test_customer_order_t_r()` |
| `EST` | `ESTIMATION` | `Test_EST/EST.py` | `test_estimation()` |
| `Billing` | `Billing` | `Test_Bill/Bill.py` | `test_Billing()` |
| `PurchasePO` | `PurchasePO` | `Test_Purchase/PurchasePO.py` | `test_purchase_po()` |
| `GRNEntry` | `GRNEntry` | `Test_Purchase/GRNEntry.py` | `test_grn_entry()` |
| `SupplierBillEntry` | `SupplierBillEntry` | `Test_Purchase/SupplierBillEntry.py` | `test_supplier_bill_entry()` |
| `HMIssueReceipt` | `HMIssueReceipt` | `Test_Purchase/HMIssueReceipt.py` | `test_hm_issue_receipt()` |
| `QCIssueReceipt` | `QCIssueReceipt` | `Test_Purchase/QCIssueReceipt.py` | `test_qc_issue_receipt()` |
| `LotGenerate` | `LotGenerate` | `Test_lot/LotGenerate.py` | `test_lot_generate()` |
| `PurchaseReturn` | `PurchaseReturn` | `Test_Purchase/PurchaseReturn.py` | `test_purchase_return()` |
| `SmithSupplierPayment` | `SmithSupplierPayment` | `Test_Purchase/SmithSupplierPayment.py` | `test_smith_supplier_payment()` |
| `DebitCreditEntry` | `DebitCreditEntry` | `Test_Purchase/DebitCreditEntry.py` | `test_debit_credit_entry()` |
| `SmithMetalIssue` | `SmithMetalIssue` | `Test_Purchase/SmithMetalIssue.py` | `test_smith_metal_issue()` |
| `RateFixGST` | `RateFixGSTPurchase` | `Test_Purchase/RateFixGSTPurchase.py` | `test_rate_fix_gst_purchase()` |
| `VendorApproval` | `VendorApproval` | `Test_vendor/VendorApproval.py` | `test_vendor_approval()` |
| `ApprovalRateFixing` | `ApprovalRateFixing` | `Test_Purchase/ApprovalRateFixing.py` | `test_approval_rate_fixing()` |
| `SearchBill` | `SearchBill` | `Test_Bill/SearchBill.py` | `test_search_bill()` |
| `SmithCompanyOpBal` | `SmithCompanyOpBal` | `Test_Purchase/SmithCompanyOpBal.py` | `test_smith_company_op_bal()` |
| `ApprovalToInvoice` | `ApprovalToInvoice` | `Test_Purchase/ApprovalToInvoice.py` | `test_approval_to_invoice()` |
| `BillingIssue` | `BillingIssue` | `Test_Bill/BillingIssue.py` | `test_billing_issue()` |
| `BillingReceipt` | `BillingReceipt` | `Test_Bill/BillingReceipt.py` | `test_billing_receipt()` |
| `BillingDenomination` | `BillingDenomination` | `Test_Bill/BillingDenomination.py` | `test_cash_collection()` |
| `JewelNotDelivered` | `JewelNotDelivered` | `Test_Bill/JewelNotDelivered.py` | `test_item_delivery()` |
| `BillSplit` | `BillSplit` | `Test_Bill/BillSplit.py` | `test_bill_split()` |
| `OldMetalProcess` | `OldMetalProcess` | `Test_OldMetalProcess/OldMetalProcess.py` | `test_old_metal_process()` |
| `StockIssue` | `StockIssue` | `Test_StockIssue/StockIssue.py` | `test_stock_issue()` |
| `RepairOrder` | `RepairOrder` | `Test_RepairOrder/RepairOrder.py` | `test_repair_order()` |

---

## 3. 🔧 Standard Module Template

Every module **must** follow this exact structure:

```python
FILE_PATH = ExcelUtils.file_path
BASE_URL  = ExcelUtils.BASE_URL

class ModuleName(unittest.TestCase):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.fc = Function_Call(driver)

    def test_module_name(self):
        # 1. Navigate (menu click with URL fallback)
        # 2. sheet_name = "SheetName"
        # 3. valid_rows = ExcelUtils.get_valid_rows(FILE_PATH, sheet_name)
        # 4. for row_num in range(2, valid_rows):
        #      workbook = load_workbook(FILE_PATH)  ← reload each row!
        #      row_data = {key: sheet.cell(row=row_num, column=col).value ...}
        #      workbook.close()
        #      result = self.test_module_flow(row_data, row_num, sheet_name)
        #      self._update_excel_status(row_num, result[0], result[1], sheet_name)

    def test_module_flow(self, row_data, row_num, sheet_name):
        # Fill form fields via Function_Call
        # Save button
        # return self.extract_id_and_verify(row_data)

    def extract_id_and_verify(self, row_data):
        # Tab or Toaster pattern (see Section 7)
        # return ("Pass", "message", captured_id)

    def _update_excel_status(self, row_num, status, message, sheet_name, captured_no=None):
        wb = load_workbook(FILE_PATH); sh = wb[sheet_name]
        color = "00B050" if status == "Pass" else "FF0000"
        sh.cell(row=row_num, column=2, value=status).font = Font(bold=True, color=color)
        sh.cell(row=row_num, column=3, value=message).font = Font(bold=True, color=color)
        if captured_no: sh.cell(row=row_num, column=LAST_COL, value=captured_no)
        wb.save(FILE_PATH)
```

---

## 4. 🛠️ Function_Call API Reference

| Method | Signature | Use For |
|---|---|---|
| `click` | `(self, xpath)` | Any element — JS fallback built in |
| `click2` | `(self, xpath)` | Scroll-heavy / sticky header areas |
| `dropdown_select` | `(self, trigger, value, search_xpath)` | Select2 (has 2s pre-pause) |
| `dropdown_select2` | `(self, trigger, value, search_xpath)` | Select2 in loops (no pre-pause) |
| `select_visible_text` | `(self, xpath, value)` | Native `<select>` by visible text |
| `select` | `(self, xpath, value)` | Native `<select>` shorthand |
| `fill_autocomplete_field` | `(self, field_id, value)` | Autocomplete by element ID |
| `fill_autocomplete_field2` | `(self, xpath, value)` | Autocomplete by XPath |
| `fill_input` | `(self, wait, locator, value, name, row, Sheet_name=)` | Validated text/number — **always pass `Sheet_name=`** |
| `fill_input2` | `(self, xpath, value)` | Quick fill, no validation |
| `Image_upload` | `(self, xpath, value)` | File input path injection |
| `get_text` | `(self, xpath)` | Read element visible text |
| `get_value` | `(self, xpath)` | Read input `.value` attribute |
| `alert` | `(self)` | Dismiss native JS alert |
| `alert1` | `(self, xpath)` | Click + capture toaster message |
| `alert2` | `(self, prefix, tc_id)` | Capture toaster with screenshot |
| `alert6` | `(self, xpath)` | Click, wait for DOM change, return toast |
| `Remark` | `(self, row_num, msg, Sheet_name)` | Write orange warning to Remark col |

---

## 5. 📊 ExcelUtils API Reference

| Method | Returns |
|---|---|
| `get_valid_rows(file_path, sheet_name)` | Row count (data rows + 2) |
| `get_master_sheet_data(file_path)` | List of function names with `Execution=yes` |
| `update_master_status(file_path, status, function_name)` | Writes to Master col 3 |
| `get_Status(file_path, function_name)` | `"Pass X, Fail Y"` string |
| `get_column_number(file_path, sheet_name)` | Column index of `Remark` header |
| `ExcelClose(file_path)` | COM-closes Excel before automation starts |

---

## 6. 🎯 XPath Patterns Quick Reference

```python
# ── Select2 ──────────────────────────────────────────────────────────────────
'//select[@id="employee_sel"]/following-sibling::span'         # trigger click
'//span[@class="select2-search select2-search--dropdown"]/input' # search box

# ── Select2 inside table row ──────────────────────────────────────────────────
prefix = f"(//table[@id='TABLE_ID']/tbody/tr)[{i+1}]"
f"{prefix}//span[contains(@id,'select2-metal-container')]/following-sibling::span"

# ── Autocomplete ──────────────────────────────────────────────────────────────
Function_Call.fill_autocomplete_field(self, "cus_name", value)
# Suggestion: //li[contains(text(),'{value}')]

# ── Date fields (JS bypass) ───────────────────────────────────────────────────
el = wait.until(EC.presence_of_element_located((By.XPATH, date_xpath)))
driver.execute_script("arguments[0].value = arguments[1];", el, "30-03-2026")
driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", el)
driver.execute_script("arguments[0].dispatchEvent(new Event('blur'));", el)

# ── Radio map pattern ────────────────────────────────────────────────────────
label_map = {"Customer": "3", "Stock": "4"}
id_map    = {"3": "cus_repair_order", "4": "stock_repair_order"}
val = label_map.get(str(row_data["Field"]).strip(), str(row_data["Field"]).strip())
Function_Call.click(self, f"//input[@id='{id_map[val]}']")

# ── Navigation ────────────────────────────────────────────────────────────────
wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Toggle navigation"))).click()
Function_Call.click(self, "//span[contains(text(), 'Module Name')]")
# Fallback:
driver.get(BASE_URL + "index.php/<controller>/<module>/list")
```

---

## 7. ✅ Post-Save Verification Patterns

### Pattern A — New Tab (RepairOrder, StockIssue-Issue, Billing)
```python
main_win = driver.current_window_handle
WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
for handle in driver.window_handles:
    if handle != main_win:
        driver.switch_to.window(handle)
        captured_id = driver.current_url.split('/')[-1]
        driver.close()
        break
driver.switch_to.window(main_win)
```

### Pattern B — Toaster Alert (HMIssueReceipt, QCIssueReceipt)
```python
msg = wait.until(EC.presence_of_element_located(
    (By.XPATH, "//div[contains(@class,'alert-success')]"))).text.strip()
if "success text" in msg:
    captured_id = driver.find_element(By.XPATH,
        '//table[@id="item_list"]/tbody/tr[1]/td[2]').text.strip()
```

### Pattern C — URL Redirect (StockIssue-Receipt)
```python
wait.until(EC.url_contains("module/list"))
return ("Pass", "Saved successfully")
```

### DataTables Verification (after any pattern)
```python
driver.get(BASE_URL + "index.php/<controller>/<module>/list")
sleep(2)
# Apply filters (branch, date, employee)
fc.click("//button[@id='search_btn_id']")
sleep(2)
sb = driver.find_element(By.XPATH, "//input[@type='search']")
sb.clear(); sb.send_keys(captured_id); sleep(2)
first_row = driver.find_element(By.XPATH, "//table[@id='TABLE_ID']/tbody/tr[1]")
if captured_id in first_row.text:
    return ("Pass", f"Verified {captured_id}", captured_id)
```

---

## 8. 📊 Excel Data Conventions

| Rule | Detail |
|---|---|
| Col 1 — `TestCaseId` | Unique ID, never None in data rows |
| Col 2 — `TestStatus` | Set `Run` to execute; script writes `Pass`/`Fail` |
| Col 3 — `ActualStatus` | Written by script as result message |
| Last col — Generated ID | e.g. `Repairorder_NO`, `HMRefNo`, `StockIssueNo` |
| `\|` separator | Multiple items in same row |
| `#` separator | Multiple stones within one item |
| `;` separator | Stone groups across different items |
| Reload per row | `load_workbook()` inside loop to pick up auto-written IDs |
| Issue→Receipt link | After Issue, write captured ID to next row's Ref col + set `TestStatus="yes"` |

---

## 9. 🔑 Module-Specific Key Facts

### Billing (`Bill.py`)
- Fetches board rate at start via `Boardrate.Todayrate()`
- 8 Bill Types: SALES, SALES & PURCHASE, PURCHASE, ORDER ADVANCE, SALES RETURN, SALES PURCHASE & RETURN, CREDIT COLLECTION, ORDER DELIVERY, Repair Order Delivery
- Delegates payment to `CreditCard`, `Cheque`, `NetBanking` sub-classes
- `_select_last_filter_bill()` auto-picks last bill for Return flows

### Tag (`Tag.py`)
- Reads live Gold 22KT/18KT/Silver rates from header rate block before loop
- Imports `Tag_Stone`, `Tag_othermetal`, `Lot` for sub-flows
- Writes tag preview back to `Tag_EST` sheet via `update_Tagdetails()`
- `calculation()` supports 4 formula types

### HMIssueReceipt & QCIssueReceipt
- Issue button class: `btn-success` | Receipt button class: `btn-primary` (both `id="add_Order"`)
- After Issue: writes new HM/QC Ref No to SAME row AND enables next receipt row
- Verification: checks `item_list` table row status column

### OldMetalProcess
- Always navigates to `add` URL directly (no list add button)
- `MELTING RECEIPT` has modal: Category, Section, Product, Design, SubDesign, Pcs, Weight
- Saves captured `ProcessNo` to next row col 10 automatically

### StockIssue
- `StockType=Taged` → scan tag code → auto-fill grid
- `StockType=Non-Tagged` → Match & Fill: iterate grid rows, match product name, fill by class name
- Issue: new tab → capture ID
- Receipt: redirect to list (no new tab)

### RepairOrder *(latest completed)*
- `OrderType`: `Customer`="3", `Stock`="4" — always use label→value map
- `WorkAt`: `In House`="1", `Out Source`="2"
- Stone modal fields (per stone): `Type,Name,Pcs,Wt,Unit,CalType,Rate` — comma separated
- `StoneData` column: `;` splits items, `#` splits stones within item
- Date fields: **must use JS bypass** — datepicker blocks input
- Post-save: new tab → URL contains repair acknowledgement ID

---

## 10. ⚡ main.py Startup Order

```
1. Clear screenshots folder (shutil.rmtree)
2. ExcelUtils.ExcelClose(FILE_PATH)  ← close Excel via COM
3. create_driver()  ← Chrome with fake cam, kiosk-print, no-sandbox
4. get_master_sheet_data()  ← which modules to run
5. Loop → match case → instantiate → run
6. finally: driver.quit() + log time diff
```

---

## 11. 🚨 Top Mistakes to Avoid

| # | Mistake | Fix |
|---|---|---|
| 1 | Click `<select>` for Select2 | `/following-sibling::span` |
| 2 | Type into datepicker | JS value + `change` + `blur` event |
| 3 | Hardcode radio value | Label→value map |
| 4 | `split('|')` on None | `if row_data["Field"]:` guard |
| 5 | No `Sheet_name=` in `fill_input` | Always pass `Sheet_name=sheet_name` |
| 6 | No sleep after modal open | `sleep(2)` after modal trigger |
| 7 | Stone row index off-by-one | `row_idx = i + 1` in prefix |
| 8 | Assume new tab after save | Verify per-module behavior first |
| 9 | Forget `.close()` on workbook | Always `workbook.close()` after read |
| 10 | Direct Selenium instead of Function_Call | Always use `Function_Call.click(self,...)` |
| 11 | XPath `text()` mismatch (whitespace) | Use `contains(normalize-space(), 'Text')` |
| 12 | Generic XPath indices `[1]`, `[2]` | Use unique parent or stable text matches |
