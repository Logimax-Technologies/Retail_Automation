# Master Prompt: Karigar Allotment Automation

Build complete Karigar Allotment automation for the Retail Automation project. This module assigns new orders to Karigars or Employees. Follow the project's standard code pattern using `Function_Call` and `ExcelUtils`.

**File to create**: `c:\Retail_Automation\Sparqla\Test_RepairOrder\KarigarAllotment.py`  
**Update main.py**: Add `KarigarAllotment` case.
**Excel Sheet**: `KarigarAllotment`

---

### Controller Details (`admin_ret_order.php`)
- The Karigar Allotment functionality lives inside the repair/new orders module list page.
- **Menu**: Order → New Order
- **URL**: `admin_ret_order/neworder/list` or `admin_ret_order/repair_order/neworders` (Validate which one is the actual live one in the app, usually `repair_order/neworders`).

---

### Form Fields & Technical Logic

Unlike standard add forms, this is a **List Page Bulk Action**. 

#### 1. Filter Section (Optional based on Excel)
If we need to search for a specific `Order No` before assigning:
- **Search Box**: `//input[@type='search']` (DataTables default search)

#### 2. Item Selection
- The script must select the checkbox for the specific `Order No` or click `Select All`.
- **Select All Checkbox**: `id="select_all"`
- **Specific Row Checkbox**: `//table[@id='neworder_list']/tbody/tr[contains(., '{order_no}')]//input[@type='checkbox']`

#### 3. Assignment Section
- **Assign To (Radio)**: 
  - `name="order[assign_to]" value="1"` → Karigar (Default)
  - `name="order[assign_to]" value="2"` → Employee
- **Select Worker (Select2)**:
  - If Karigar: `id="karigar_sel"` (Container `id="karigar_assign"`)
  - If Employee: `id="employee_sel"` (Container `id="emp_assign"`)
- **Action Buttons**:
  - **Assign/Approve**: `id="approve"` (Label containing `<input type="radio" name="upd_status_btn" value="1">`) Validate standard click.
  - **Reject**: `id="reject"` (Label containing `<input type="radio" name="upd_status_btn" value="2">`)

---

### Automation Flow

1. **Navigation**: Go to New Orders (`repair_order/neworders` or via Menu).
2. **Search**: Enter `Order No` into DataTables search box.
3. **Select**: Click the checkbox for the loaded row.
4. **Assign Role**: 
   - Read `AssignTo` value from Excel (e.g., "Karigar" or "Employee").
   - Click the corresponding radio button map.
5. **Select Person**: 
   - Click the Select2 dropdown for `karigar_sel` or `employee_sel`.
   - Enter the name (from `AssignName` column) in the search box.
   - Press Enter to select.
6. **Submit**: Click the **Assign** button (`id="approve"`).
7. **Verification**: 
   - Capture the success toaster alert: `//div[contains(@class,'alert-success')]`.
   - Ensure the message confirms the assignment.

---

### Expected Excel Columns (`KarigarAllotment`)
| Column | Name | Description |
|---|---|---|
| 1 | `TestCaseId` | Unique ID |
| 2 | `TestStatus` | Run / Pass / Fail |
| 3 | `ActualStatus` | Result message |
| 4 | `OrderNo` | The specific order number to assign |
| 5 | `AssignTo` | Role: "Karigar" or "Employee" |
| 6 | `AssignName` | The name of the Karigar or Employee |
| 7 | `Action` | "Assign" or "Reject" |
| 8 | `Remark` | Execution details |

---

### Critical Reminders (From Brain)
- **Select2 clicking**: Always click `//select[@id='karigar_sel']/following-sibling::span`.
- **Checkboxes**: Do not click the `<input>` directly if it's hidden; click the parent `<label>` or wrapper if needed, or use JS `click()`.
- **Toaster Alert**: Use `Function_Call.alert2` or explicit wait for `.alert-success`.
- **Row Reloading**: Remember to use `workbook = load_workbook(...)` inside the loop. 
