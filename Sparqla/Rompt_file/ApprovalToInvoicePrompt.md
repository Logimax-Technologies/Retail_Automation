Build complete **Approval To Invoice Conversion** (Supplier Rate Cut) automation for the Retail Automation project.
Follow the **EXACT same code pattern** as `SmithCompanyOpBal.py`, `SmithMetalIssue.py`, `LotGenerate.py`, `QCIssueReceipt.py`, `SupplierBillEntry.py`, `PurchaseReturn.py`, and `DebitCreditEntry.py`.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_Purchase\ApprovalToInvoice.py
```

## Update main.py
Add `ApprovalToInvoice` case to the module dispatcher.

---

## Controller Details (admin_ret_purchase.php)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
Function: `supplier_rate_cut($type = "", $id = "", $status = "")`

Switch Cases:
- `list` → Pure Weight to Amount Conversion List Page (renders `amt_weight_conversation/list`).
- `add` → Conversion Form (renders `amt_weight_conversation/form`).
- `save` → Save Rate Cut Data.
- `ajax` → AJAX fetch for list records.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Note: This module handles converting a Supplier's Pure Weight or Amount balance into a fixed or unfixed invoice.

## Navigation
| Module | Menu Path | List URL | Add URL |
| :--- | :--- | :--- | :--- |
| **Approval To Invoice** | Purchase → Pure Weight to Amount Conversion | `admin_ret_purchase/supplier_rate_cut/list` | `admin_ret_purchase/supplier_rate_cut/add` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Form Fields & Mandatory Status (admin_ret_purchase/supplier_rate_cut/form)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Entry Section:
- ✅ **Opening Balance (Radio)**: `name="supplier_rate_cut[is_opening_blc]"`
  - 🔹 1 = Yes
  - 🔹 0 = No (Default)
- ✅ **Rate Cut Type (Radio)**: `name="supplier_rate_cut[rate_cut_type]"`
  - 🔹 1 = Amount
  - 🔹 2 = Pure to Amount (Default)
  - 🔹 3 = Amount to Pure
- ✅ **Convert Bill To (Radio)**: `name="supplier_rate_cut[convert_to]"`
  - 🔹 1 = Supplier, 2 = Manufacturer, 3 = Stone, 4 = Diamond, 5 = Approval
- ✅ **Conversion Type (Radio)**: `name="supplier_rate_cut[conversion_type]"`
  - 🔹 1 = Fix (Default)
  - 🔹 2 = Unfix
- ✅ **Supplier (Select2)**: `id="select_karigar"`
- ✅ **PO Section (Visible if Opening=No)**:
  - Financial Year: `id="pur_fin_year_select"`
  - PO No (Select2): `id="select_po_ref_no"`
- ✅ **Opening Section (Visible if Opening=Yes)**:
  - O/p Ref No (Select2): `id="opening_ref_no"`
- ✅ **Select Metal (Select2)**: `id="select_metal"`
- ✅ **Select Category (Select2)**: `id="select_category"`
- ✅ **Select Product (Select2)**: `id="select_product"`

### Quantity & Value Section:
- ✅ **To Pay (Input)**: `class="charges_amount"` (For Amount type)
- ✅ **Pure Weight (Input)**: `class="src_weight"` (For Pure to Amount type)
- ✅ **Rate (Input)**: `class="src_rate"`
- ✅ **Remark (Textarea)**: `name="supplier_rate_cut[src_remark]"`

### Payment Section (Visible if Rate Cut Type = 1):
- ✅ **Cash (Input)**: `name="billing[cash_amount]"`
- ✅ **Net Banking (Button/Modal)**: `id="net_bank_modal"`

### Action:
- ✅ **Save Button**: `id="submit_rate_cut"` (or generic submit within form)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Full Business Workflow & Test Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 1. Pure Weight to Amount Conversion (Against PO)
- **Workflow**:
  1. Set `Opening Balance` = **No**.
  2. Set `Rate Cut Type` = **Pure to Amount**.
  3. Select `Supplier` and `PO No`.
  4. Select `Metal`, `Category`, `Product`.
  5. Enter `Pure Weight` and `Rate`.
  6. Enter `Remark` and click `Save`.

### 2. Pure Weight to Amount Conversion (Against Opening)
- **Workflow**:
  1. Set `Opening Balance` = **Yes**.
  2. Select `O/p Ref No`.
  3. Fill weight/rate and save.

### 3. Verification on List Page
- **Workflow**:
  1. Navigate to List page.
  2. Search by Date/Supplier.
  3. Verify record status and amounts.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Advanced Logic & Constraints
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### technical Rules
- **Tax Calculation**: GST (3%) is automatically calculated based on Rate * Weight.
- **Pure Balance**: The `wt_balance` field shows available pure metal weight for the supplier.
- **Amount Balance**: The `amt_balance` field shows available credit/debit balance.

### UI Automation Gotchas
- **Select2**: Use `Function_Call.dropdown_select` for all Select2 elements.
- **JS Triggers**: Entering Weight/Rate triggers AJAX for GST and Net Amount calculation; wait for these fields to update.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Expected Excel Sheet Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Sheet: `ApprovalToInvoice`**
| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **TestCaseId** | Unique ID |
| 2 | **TestStatus** | Run / Skip |
| 3 | **OpeningBal** | 1=Yes, 0=No |
| 4 | **RateCutType** | 1=Amt, 2=Pure, 3=AmtToPure |
| 5 | **ConvertTo** | 1=Supp, etc. |
| 6 | **ConvType** | 1=Fix, 2=Unfix |
| 7 | **SupplierName** | Select2 text |
| 8 | **RefNo** | PO No or Op Ref No |
| 9 | **Metal** | Select2 text |
| 10 | **Category** | Select2 text |
| 11 | **Product** | Select2 text |
| 12 | **PureWeight** | Number |
| 13 | **Amount** | Number |
| 14 | **Rate** | Number |
| 15 | **Remark** | Optional text |
| 16 | **ActualStatus** | Success / Fail |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Code Patterns to Follow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **Select2 Dropdowns**: Interact with the Select2 container to search and select Supplier, PO, and items.
- **Radio Selection**: Click the radio button matching the `@value` for conversion types.
- **Numeric Inputs**: Fill Weight and Rate and wait for dynamic calculations.
- **Success Verification**: Accept the browser alert after saving.
