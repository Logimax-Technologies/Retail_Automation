# Master Prompt: Repair Order Automation

Build complete Repair Order (Create Order) automation for the Retail Automation project. Follow the project's standard code pattern using `Function_Call`, `ExcelUtils`, and `DataTable` verification.

**File to create**: `c:\Retail_Automation\Sparqla\Test_RepairOrder\RepairOrder.py`  
**Update main.py**: Add `RepairOrder` case.

---

### Controller Details (`admin_ret_order.php`)
**Functions**: 
- `repair_order/list` → Repair Order List page.
- `repair_order/add`  → Create Repair Order Form.
- `repair_order/save` → POST — save Repair Order.

---

### Navigation
- **Menu**: Order → Repair Order
- **List URL**: `admin_ret_order/repair_order/list`
- **Add URL**: `admin_ret_order/repair_order/add`

---

### Form Fields & Technical Logic

#### 1. Header Section
- ✅ **Type** (Radio): `id=cus_repair_order` (value=`3` → Customer, default) / `id=stock_repair_order` (value=`4` → Stock)
- ✅ **Work At** (Radio): `id=cus_repair_at_inhouse` (value=`1` → In House, default) / `id=cus_repair_at_outsource` (value=`2` → Out Source)
- ✅ **Employee** (Select2): `id=employee_sel` — Select employee taking the order.
- ✅ **Order From** — Branch (Select2): `id=branch_select` — Dropdown for HO users.

#### 2. Recipient Section (Dynamic)
- **If Type = Customer**: `id=cus_name` — Autocomplete lookup (type name/mobile → keyup match).
- **If Type = Stock**: `id=issue_tag_code` (Input) → `id=issue_tag_search` (Button).

#### 3. Customer Order Items Table (`#custrepair_item_detail`)
- **Fields per row**:
  - **Metal** (Select2): e.g., GOLD.
  - **Product** (Select2): e.g., GOLD BANGLES.
  - **Design** (Select2): e.g., KERALA.
  - **Sub Design** (Select2): e.g., LK BANGLE.
  - **Gross Wt** (Input): Enter total weight.
  - **Less Wt** (Modal Trigger): Click the `+` button next to the Less Wt field to open the **Add Stone Modal**.
  - **Net Wt** (Read-only): Automatically calculated as `Gross Wt - Less Wt`.
  - **Pcs** (Input): Total pieces.
  - **C.Due** (Datepicker): Delivery due date.
  - **Repair Type** (Select2): e.g., POLISH.
  - **Image** (Icon `+`): Click to open upload dialog.
  - **Description** (Icon `+`): Click to open text modal.
  - **Action**: 
    - `+` (Green button): Add new item row.
    - `🗑️` (Red button): Delete current row.

#### 4. Add Stone Modal (`#cus_stoneModal`)
- **Action**: Opened by clicking the `+` next to `Less Wt` in the main grid.
- **Fields in Stone Table**:
  - **LWT** (Checkbox): Link to less weight.
  - **Type** (Select): Stone type.
  - **Name** (Select): Stone name.
  - **Pcs** (Input): Number of stones.
  - **Wt** (Input) + **Unit Select**: e.g., `5` and `gram` or `carat`.
  - **Cal.Type** (Radio): `By Wt` or `By Pcs`.
  - **Rate** (Input): Price per unit.
  - **Amount** (Input): Calculated total.
- **Buttons**:
  - `+ Add`: Append a new stone row.
  - `Save`: Writes total stone weight to the `Less Wt` field in the main grid and closes modal.

#### 5. Stock Repair Items Table (`#tagissue_item_detail`)
- **Trigger**: Type barcode in `issue_tag_code` → Search.
- **Auto-filled Fields**: Image, Tag Code, Old Tag, Category, Purity, Product, Design, Sub Design, Pcs, GWgt, NWgt, LWgt.
- **Manual Input**:
  - **Repair Type** (Select).
  - **Image** (`+` button).
  - **Narration/Description** (`+` button).

#### 6. Submission
- **Save Button**: `id=create_repair_order` — Submits the entire form.
- **Cancel Button**: `class=btn-cancel`.

---

### Automation Flow Sequence

#### Flow 1: Customer Repair (Multi-Item + Stones)
1. **Header**: Select "Customer", "In House", Employee, and "HEAD OFFICE".
2. **Customer**: Lookup and select "KUMAR".
3. **Main Grid Row 1**:
   - Select Metal, Product, Design, Sub Design.
   - Enter `Gross Wt` (e.g., 10.000).
   - **Stones**: Click `+` next to Less Wt.
     - In modal: Select Type, Name, enter Pcs, Wt (gram), Cal Type (By Wt), Rate.
     - Click `Add` for another stone if needed.
     - Click `Save` (Modal closes, Less Wt populates, Net Wt updates).
   - Enter `Pcs` (e.g., 10).
   - Select `C.Due` date from calendar.
   - Select `Repair Type` (e.g., POLISH).
   - Add Image and Description via `+` icons.
4. **Additional Rows**: Click green `+` in Action column → Fill second row → Delete if added wrongly.
5. **Final**: Click `Save` button at bottom.

#### Flow 2: Stock Repair
1. **Header**: Select "Stock", "Out Source", etc.
2. **Scan**: Enter Tag Code → Click Search (item details populate grid).
3. **Fill**: Select `Repair Type` in the populated row.
4. **Final**: Click `Save`.

---

### Post-Submission Verification Flow
1. **Tab Handling**:
   - After clicking **Save**, wait for a new tab to open automatically.
   - Switch to the newly opened tab (Repair Order Proforma Invoice).
   - **ID Extraction**: Get the `Repair Order ID` from the URL (e.g., extract `711` from `.../repair_acknowledgement/711`).
   - Close the proforma invoice tab.
   - Switch back to the main application window.
2. **Listing Page Search**:
   - Navigate to the **Repair Order Listing** page.
   - **Set Filters**:
     - **Branch**: Select the branch used in the order.
     - **Date Range**: Select "Today".
     - **Employee**: Select the employee who took the order.
   - Click **Search** button.
3. **Detail Validation**:
   - In the listing table search box, enter the `Repair Order ID` extracted from the URL.
   - Verify the data in the 1st row of the results matches the expected customer name, metal, weight, and pieces.



---

### Excel Sheet: `RepairOrder`

> [!IMPORTANT]
> **Multi-Item & Multi-Stone Logic**:
> - Use Pipe (`|`) to separate different items in an order (e.g., `GOLD|SILVER`).
> - Use Hash (`#`) to separate multiple stones *within* a single item.
> - Use Semicolon (`;`) to separate stone groups for different items in the `StoneData` column.

| Col | Header | Description |
|---|---|---|
| 1 | TestCaseId | Unique ID |
| 2 | TestStatus | Run/Skip/Done |
| 3 | ActualStatus | Result message |
| 4 | OrderType | 3 (Customer) or 4 (Stock) |
| 5 | WorkAt | 1 (In House) or 2 (Out Source) |
| 6 | Employee | Employee name |
| 7 | OrderFrom | Branch name |
| 8 | CusName | Customer name (for autocomplete) |
| 9 | Metal | Pipe-separated metals: `GOLD|GOLD` |
| 10 | Product | Pipe-separated products: `BANGLES|RINGS` |
| 11 | Design | Pipe-separated designs |
| 12 | SubDesign | Pipe-separated sub-designs |
| 13 | GrossWt | Pipe-separated gross weights: `10.500|5.200` |
| 14 | StoneData | Multi-level data: `Item1Stone1#Item1Stone2 | Item2Stone1`. <br>Stone Format: `Type,Name,Pcs,Wt,Unit,Cal,Rate` (e.g., `Stone,Diamond,1,0.05,carat,By Wt,5000`) |
| 15 | Pcs | Pipe-separated pieces: `1|1` |
| 16 | DueDate | Pipe-separated dates: `30-03-2026|31-03-2026` |
| 17 | RepairType | Pipe-separated types: `POLISH|REPAIR` |
| 18 | TagCode | For Stock Type: Tag to scan (Pipe-separated if multiple) |
| 19 | Narration | Pipe-separated remarks |
| 20 | ItemImage | Pipe-separated image paths |
| 21 | ItemDesc | Pipe-separated description texts |



---

### Technical Notes
- **Select2**: Use `fc.select2` for Employee, Branch, Metal, Product, etc.
- **Grids**: Use `wait.until` to ensure rows appear after adding items or scanning tags.
- **Success Capture**: Success alert logic should be consistent with `main.py` patterns.
