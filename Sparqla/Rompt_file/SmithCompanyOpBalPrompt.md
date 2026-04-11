Build complete **Smith / Company Opening Balance** automation for the Retail Automation project.
Follow the **EXACT same code pattern** as `SmithMetalIssue.py`, `LotGenerate.py`, `QCIssueReceipt.py`, `SupplierBillEntry.py`, `PurchaseReturn.py`, and `DebitCreditEntry.py`.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_Purchase\SmithCompanyOpBal.py
```

## Update main.py
Add `SmithCompanyOpBal` case to the module dispatcher.

---

## Controller Details (admin_ret_purchase.php)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
Function: `smith_cmpy_op_bal($type = "", $id = "", $status = "")`

Switch Cases:
- `list` → Opening Balance List Page (renders `smith_cmpy_op_bal/list`).
- `add` → Opening Balance Form (renders `smith_cmpy_op_bal/form`).
- `save` → Save Opening Balance Data.
- `ajax` → AJAX fetch for list records.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Note: This module handles entering initial stock/balance for the Company or Smith/Karigars. 
**CRITICAL**: Focus only on the **Smith Stock** flow. **Company Stock** flow should be avoided as it will be deprecated.

## Navigation
| Module | Menu Path | List URL | Add URL |
| :--- | :--- | :--- | :--- |
| **Smith Company Op Bal** | Purchase → Smith/Company Opening Balance | `admin_ret_purchase/smith_cmpy_op_bal/list` | `admin_ret_purchase/smith_cmpy_op_bal/add` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Form Fields & Mandatory Status (admin_ret_purchase/smith_cmpy_op_bal/form)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Entry Section:
- ✅ **O/P Balance For (Radio)**: `name="smth_cmpy_stk[stock_type]"`
  - 🔹 1 = Company Stock (AVOID)
  - 🔹 2 = Smith Stock (SELECT THIS)
- ✅ **Op Date (Input)**: `id="cmpy_opening_date"`
- ✅ **Smith Type (Radio)**: `name="smth_cmpy_stk[smith_type]"`
  - 🔹 1 = Supplier
  - 🔹 2 = Smith
  - 🔹 3 = Approval Supplier
  - 🔹 4 = Stone Supplier
- ✅ **Balance Type (Radio)**: `name="smth_cmpy_stk[bal_type]"`
  - 🔹 1 = Metal
  - 🔹 3 = Diamond/Stone
- ✅ **Metal Type (Radio)**: `name="smth_cmpy_stk[metal_type]"`
  - 🔹 1 = Ornament
  - 🔹 2 = Old Metal
- ✅ **Select Karigar (Select2)**: `id="select_karigar"`
- ✅ **Select Metal (Select2)**: `id="select_metal"`
- ✅ **Select Category (Select2)**: `id="select_category"` (For Ornament)
- ✅ **Select Old Metal Category (Select2)**: `id="oldcategory"` (For Old Metal)
- ✅ **Select Product (Select2)**: `id="select_product"`

**Quantity Section:**
- ✅ **Pieces**: `class="op_pcs"`
- ✅ **Gross Weight**: `class="op_wgt"`
- ✅ **UOM**: `id="op_uom"` (1=Gram, 6=Carat)
- ✅ **Net Weight**: `class="op_net_wgt"`
- ✅ **Dia Weight**: `class="op_dia_wgt"`
- ✅ **Pure Weight**: `class="op_ure_wgt"`
- ✅ **Weight Receipt Type (Radio)**: `name="smth_cmpy_stk[wt_receipt_type]"`
  - 🔹 1 = Credit
  - 🔹 2 = Debit

**Value Section:**
- ✅ **Value (Amount)**: `class="op_amt"`
- ✅ **Amount Receipt Type (Radio)**: `name="smth_cmpy_stk[amt_receipt_type]"`
  - 🔹 1 = Credit
  - 🔹 2 = Debit
- ✅ **Remark**: `name="smth_cmpy_stk[remark]"`

**Action:**
- ✅ **Save Button**: `id="smth_cmpy_bal_submit"`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Full Business Workflow & Test Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 1. Smith Stock - Metal Balance (Ornament)
- **Workflow**:
  1. Set `O/P Balance For` = **Smith Stock**.
  2. Set `Balance Type` = **Metal**.
  3. Set `Metal Type` = **Ornament**.
  4. Select `Karigar`, `Metal`, `Category`, `Product`.
  5. Enter `Pieces`, `Gross Weight`, `Net Weight`, `Pure Weight`.
  6. Set `Weight Receipt Type` = **Credit**.
  7. Enter `Remark` and click `Save`.

### 2. Smith Stock - Diamond/Stone Balance
- **Workflow**:
  1. Set `O/P Balance For` = **Smith Stock**.
  2. Set `Balance Type` = **Diamond/Stone**.
  3. Select `Karigar`, `Metal`.
  4. Enter `Value` (Amount) and `Remark`.
  5. Set `Amount Receipt Type` = **Credit**.
  6. Click `Save`.

### 3. Smith Stock - Old Metal
- **Workflow**:
  1. Set `Metal Type` = **Old Metal**.
  2. Select `Old Metal Category`.
  3. Fill weights and save.

### 4. Verification on List Page
- **Workflow**:
  1. Navigate to the Opening Balance List (`admin_ret_purchase/smith_cmpy_op_bal/list`).
  2. Search for the recorded entry by Category/Date.
  3. Verify the values match the entered data.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Advanced Logic & Constraints (from Knowledge Brain)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### technical Rules
- **Display Logic**: `old_metal_category` div is only shown when `Metal Type` is Old Metal.
- **Mandatory Fields**: Karigar and Metal are always mandatory for Smith Stock.

### UI Automation Gotchas
- **Select2**: Use `Function_Call.dropdown_select` for all Select2 elements.
- **Radios**: Ensure to click the correct radio ID or value as some might overlap in visibility.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Expected Excel Sheet Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Sheet: `SmithCompanyOpBal`**
| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **TestCaseId** | Unique ID |
| 2 | **TestStatus** | Run / Skip |
| 3 | **StockType** | 2 = Smith Stock |
| 4 | **SmithType** | 1=Supp, 2=Smith, etc. |
| 5 | **BalType** | 1=Metal, 3=Dia |
| 6 | **MetalType** | 1=Orn, 2=Old |
| 7 | **KarigarName** | Select2 text |
| 8 | **MetalName** | Select2 text |
| 9 | **CategoryName** | Select2 text |
| 10 | **ProductName** | Select2 text |
| 11 | **Pieces** | Number |
| 12 | **GrossWgt** | Number |
| 13 | **NetWgt** | Number |
| 14 | **DiaWgt** | Number |
| 15 | **PureWgt** | Number |
| 16 | **WtType** | 1=Credit, 2=Debit |
| 17 | **Amount** | Number |
| 18 | **AmtType** | 1=Credit, 2=Debit |
| 19 | **Remark** | Optional text |
| 20 | **VerifyInTable** | Yes / No |
| 21 | **ActualStatus** | Success / Fail |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Code Patterns to Follow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **Select2 Dropdowns**: Interact with the Select2 container to search and select Karigar, Metal, Category, and Product.
- **Radio Selection**: Click the radio button input matching the `@value` for StockType, SmithType, BalType, etc.
- **Weights & Amounts**: Fill numeric input fields for Pieces, Weights, and Amounts using standard input handlers.
- **Success Verification**: Monitor and accept the browser's native alert dialog to confirm successful record saving.
