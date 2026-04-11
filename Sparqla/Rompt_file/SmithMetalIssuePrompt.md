Build complete **Smith Metal Issue** automation for the Retail Automation project.
Follow the **EXACT same code pattern** as `LotGenerate.py`, `QCIssueReceipt.py`, `SupplierBillEntry.py`, `PurchaseReturn.py`, and `DebitCreditEntry.py`.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_Purchase\SmithMetalIssue.py
```

## Update main.py
Add `SmithMetalIssue` case to the module dispatcher.

---

## Controller Details (admin_ret_purchase.php)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
Function: `karigarmetalissue($type="")`

Switch Cases:
- `list` → Smith Metal Issue List Page.
- `add` → Smith Metal Issue Form.
- `save` → Save Metal Issue.
- `karigarmetalissue_acknowladgement` → Print/Acknowledgment.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Note: This module handles issuing metal (Tag or Non-Tag) to Karigars (Smiths), potentially against Orders (PO) or Supplier Bills.

## Navigation
| Module | Menu Path | List URL | Add URL |
| :--- | :--- | :--- | :--- |
| **Smith Metal Issue** | Purchase → Smith Metal Issue | `admin_ret_purchase/karigarmetalissue/list` | `admin_ret_purchase/karigarmetalissue/add` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Form Fields & Mandatory Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Main Form: Smith Metal Issue (metalissue/form.php)
**Header Section:**
- ✅ **Branch (Select2)**: `id="select_branch"` (If applicable/visible)
- ✅ **Karigar (Select2)**: `id="select_karigar"`, `name="issue[id_karigar]"`
- ✅ **Metal (Select2)**: `id="select_metal"`, `name="issue[id_metal]"`
- ✅ **Metal Issue Type (Radio)**: `name="issue[metal_issue_type]"` (1 = Normal issue, 2 = Appr Issue)
- ✅ **Against Opening (Radio)**: `name="issue[is_against_opening]"` (1 = Yes, 0 = No)
  - 🔹 If **Yes**: Show `id="karigar_select"` (Search Karigar) + Button `id="search_kar_opening_det"`.
- ✅ **Against Order (Radio)**: `name="issue[issue_aganist]"` (1 = Yes, 0 = No)
  - 🔹 If **Yes**: Enable/Show `id="select_po_no"` (Select PO No).
- ✅ **Against Supplier Bill (Radio)**: `name="issue[issue_against_po]"` (1 = Yes, 0 = No)
  - 🔹 If **Yes**: 
    1. Select Financial Year: `id="po_fin_year"` (Dropdown).
    2. Select Supplier's Po No: `id="select_supplier_po_no"` (Select2).
  - 🔹 If **No**: Show `Issue From` and `NonTag Issue From` options.

**Source Selection:**
- ✅ **Issue From (Radio)**: `name="issue[issue_from]"` (1 = Tag, 2 = Non Tag)
- ✅ **Tag Issue From (Radio)**: `name="issue[tag_issue_from]"`
  - 1 = Available Stock, 2 = Sales Return, 3 = Partly Sales, 4 = H.O OtherIssue
- ✅ **NonTag Issue From (Radio)**: `name="issue[nontag_issue_from]"`
  - 1 = Available Stock, 2 = NonTag Sales Return, 3 = NonTag Other Issue

**Code Injection:**
- 🔹 **Tag Code**: `id="tag_code"` + Click `id="tag_history_search"`.
- 🔹 **BT Code**: `id="bt_number"`.

**Item Selection (Table: `id="metal_details"`):**
- ✅ **Select All Checkbox**: `id="select_all"`
- ✅ **Individual Checkboxes**: Within the table body.

**Footer Section:**
- ✅ **Remark (Textarea)**: `id="remark"`, `name="issue[remark]"`

**Action Buttons:**
- ✅ **Save (Button)**: `id="submit_metal_issue"`
- ✅ **Cancel (Button)**: `class="btn-cancel"`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Full Business Workflow & Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 1. Normal Issue (Against Tag/Non-Tag)
- **Context**: Standard metal movement from stock to Karigar.
- **Workflow**: 
  1. Select Branch (if visible) & Karigar & Metal.
  2. Choose `Normal Issue`.
  3. Set `Against Order` = **No**.
  4. Ensure `Against Supplier Bill` = **No** to reveal stock sources.
  5. Select **Issue From** (Tag/Non-Tag) and **Condition** (Available/Sales Return/etc).
  6. Search Tag or Enter BT.
  7. Save.

### 2. Issue Against Order (PO)
- **Rule (RULE-PUR-002)**: Order type determines source.
- **Workflow**:
  1. `Against Order` = **Yes**.
  2. Select `PO No` from `id="select_po_no"`.
  3. Form dynamically loads items.

### 3. Issue Against Supplier Bill (Approval Stock)
- **Workflow**:
  1. `Against Supplier Bill Entry` = **Yes**.
  2. Select `Supplier's PO No` (`id="select_supplier_po_no"`).

### 4. Against Opening Stock
- **Workflow**:
  1. `Against Opening` = **Yes**.
  2. Use `id="karigar_select"` to search and click `id="search_kar_opening_det"`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Advanced Logic & Constraints (from Knowledge Brain)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Technical Rules
- **RULE-PUR-028 (FY Requirement)**: Ensure active Financial Year exists.
- **Pure Weight Calculation (RULE-PUR-029)**: Pure Weight = (Weight * Touch) / 100.
- **Pure Weight Limit (RULE-PUR-030)**: Total issued pure weight must NOT exceed Karigar's Outstanding Pure Balance (visible in `.availablepurebalance`).
- **Data Flow**: Updates `ret_karigar_metal_issue` and `ret_taging` (status 17).

### UI Automation Gotchas
- **Visibility Checks**: Use `is_displayed()` before interacting with `select_po_no` or `karigar_select` as they are context-dependent.
- **Select2 AJAX**: Wait for outstanding balances to populate in `.availableamtbalance`.
- **Radio Selection**: Click the `label[for='...']` to ensure interaction triggers JS events.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Expected Excel Sheet Structure (Refined)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Sheet: `SmithMetalIssue`**
| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **TestCaseId** | Unique ID for each test case |
| 2 | **TestStatus** | Run / Skip |
| 3 | **ActualStatus** | Pass / Fail (Result populated by script) |
| 4 | **Branch** | Branch name |
| 5 | **Karigar** | Karigar name |
| 6 | **Metal** | Metal type |
| 7 | **IssueType** | Normal / Appr |
| 8 | **AgainstOpening**| Yes / No |
| 9 | **SearchKarigar** | Yes / No |
| 10 | **AgainstOrder** | Yes / No |
| 11 | **AgainstBill** | Yes / No |
| 12 | **SupplierFY** | Financial Year (e.g., FY 25-26) |
| 13 | **RefOrderNo** | PO number or Bill Ref |
| 14 | **SourceType** | Tag / Non Tag |
| 15 | **StockSource** | Available / Sales Return / Partly / HO |
| 16 | **Code** | Tag Number or BT Number |
| 17 | **Touch** | Touch value (e.g., 91.6) |
| 18 | **UOM** | UOM name (e.g., Gms) |
| 19 | **Remark** | Remark |
| 20 | **VerifyList** | Yes / No |

**Sheet: `SmithMetalIssueItems`**
| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **TestCaseId** | Matches Header Sheet |
| 2 | **RefOrderNo** | PO number or Bill Ref (To identify row) |
| 3 | **Purity** | Purity name (e.g., 22KT) |
| 4 | **Touch** | Touch value (e.g., 91.6) |
| 5 | **Pcs** | Pieces count |
| 6 | **Weight** | Issue weight |
| 7 | **UOM** | UOM name (e.g., Gms) |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Code Patterns to Follow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- **Wait for Visibility**: `WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "select_po_no")))`.
- **Radio Logic**:
  - `tag_issue_from`: 1=Available, 2=Sales Return, 3=Partly Sales, 4=H.O OtherIssue.
  - `nontag_issue_from`: 1=Available, 2=Sales Return, 3=Other Issue.
