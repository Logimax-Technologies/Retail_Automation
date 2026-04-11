# Master Prompt: Repair Order Status Automation

Build complete Repair Order Status automation for the Retail Automation project. This module handles assigning extra custom metadata/metal (via the Item Details screen) and moving the repair order from Karigar handover to "Completed" (Ready for Delivery).

**File to create**: `c:\Retail_Automation\Sparqla\Test_RepairOrder\RepairOrderStatus.py`
**Update main.py**: Add `RepairOrderStatus` case.
**Excel Sheet**: `RepairOrderStatus`

---

### Controller & View Details
- **Module URL**: `admin_ret_order/repair_order/repair_order_status`
- **Extra Metal (Item Details) Screen**: `admin_ret_order/order/repair_item_details/{id}/{id2}`

---

### Form Fields & Technical Logic

#### 1. Filter, Search & Select on Status Grid

- **Branch**: `id="branch_select"` (Select2 / Dropdown)
- **Date Range Picker**: `id="rpt_payment_date"` (Select "Today")
- **Repair Type Dropdown**: `id="repair_type"` (1=Company, 2=Customer)
- **Repair Order Search Button**: `id="repair_order_search"`
- **Grid Search Box**: `//input[@type='search']`
- **Specific Row Checkbox**: `//table[@id='repair_order_list']/tbody/tr[contains(., '{order_no}')]//input[@type='checkbox']`
- **Action Edit / Details Trigger**: We must click the edit/add action button in the grid for the specific order. e.g., `//table[@id='repair_order_list']/tbody/tr[contains(., '{order_no}')]//a[contains(@href, 'repair_item_details')]`

#### 2. Extra Metal Screen (`Item Details` Form)
Once navigated to the `Item Details` screen, if `ExtraMetal` data exists:
- **Item Type**: `id="item_type"` (Select2 / Dropdown, Map from Excel dynamically)
- **Select Section**: `id="section"` (Select2 / Dropdown)
- **Select Category**: `id="category"` (Select2 / Dropdown)
- **Select Purity**: `id="purity"` (Select2 / Dropdown)
- **Select Product**: `id="prod_select"` (Select2 / Dropdown)
- **Select Design**: `id="des_select"` (Select2 / Dropdown)
- **Select Sub Design**: `id="sub_design_select"` (Select2 / Dropdown)
- **Pcs**: `id="pcs"` (Number Input)
- **Gross Wt**: `id="gross_wt"` (Number Input)
- **V.A(%)**: `id="wast_per"` (Number Input)
- **M.C Type**: `id="mc_type"` (Select visible text: "Per Pcs", "Per Grams", "On Price" -> Values 1, 2, 3)
- **M.C**: `id="mc_value"` (Number Input)
- **Service Charge(Rs)**: `id="service_charge"` (Number Input)

- **Add Item Button**: `id="add_repair_item"` (Green Add button)
- Wait for the item to render in the grid (`id="custrepair_item_detail"`)
- **Save Page Button**: `id="save_repair_item"` (Blue Save button at bottom)

#### 3. Action Section (Back on Status Grid)
After saving, it usually redirects back to `repair_order_status`. 
- **Mark Complete ("Ready for Delivery")**: `id="repair_order_status"` (Green button). 
- **Mark Delivered**: `id="repair_delivered"` (Green button). 

---

### Automation Flow

1. **Navigation**: 
   - Click `Toggle navigation`.
   - Click `//span[contains(text(), 'Repair Orders')]`.
   - Click `//span[contains(text(), 'Repair Order Status')]`.
   - Fallback: Navigate directly via URL to `admin_ret_order/repair_order/repair_order_status` if UI clicks fail.
2. **Search Order**: 
   - Select `Branch` (`id="branch_select"`).
   - Set Date Range to "Today" (`id="rpt_payment_date"`).
   - Select `RepairType` (Company/Customer) (`id="repair_type"`).
   - Click `Search` (`id="repair_order_search"`).
   - Enter `OrderNo` into DataTables search box.
3. **Extra Metal Logic (If provided)**:
   - Check `ExtraMetal` cell.
   - If populated, click the specific action link in the row `//a[contains(@href, 'repair_item_details')]`.
   - Wait for `Item Details` page to load.
   - Split `ExtraMetal` by `|`. Fill out ItemType, Section, Category, Purity, Product, Design, SubDesign, Pcs, GWt, VA, MCType, MC_Value, ServiceCharge using `Function_Call`.
   - Click `id="add_repair_item"`.
   - Click `id="save_repair_item"`. 
   - Wait for redirect back to the `repair_order_status` list.
4. **Select & Complete**:
   - Re-search the `OrderNo`.
   - Fill in `CompletedWeight` and `Amount` fields in the grid row if provided.
   - Check the checkbox for the specific `OrderNo`.
   - Click the **Complete** (`id="repair_order_status"`) or **Deliver** (`id="repair_delivered"`) button based on Action column.
5. **Verification**: 
   - Capture the toaster alert (`.alert-success`).

---

### Expected Excel Columns (`RepairOrderStatus`)
| Col | Name | Description |
|---|---|---|
| 1 | `TestCaseId` | Unique ID |
| 2 | `TestStatus` | Run / Option to Skip |
| 3 | `ActualStatus` | Result message |
| 4 | `OrderNo` | The specific repair order number |
| 5 | `Branch` | The branch name to filter |
| 6 | `DateRange` | E.g., "Today" |
| 7 | `RepairType` | E.g., "Company" or "Customer" |
| 8 | `ExtraMetal` | `ItemType\|Section\|Category\|Purity\|Product\|Design\|SubDesign\|Pcs\|GWt\|VA%\|MCType\|MC\|ServiceCharge` |
| 9 | `CompletedWeight` | Added to specific grid row input |
| 10 | `Amount` | Added to specific grid row input |
| 11 | `Action` | "Complete" or "Deliver" |
| 12 | `Remark` | Output message capture |
