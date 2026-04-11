# Master Prompt: Customer Order Karigar Allotment Automation

Build complete **Karigar Allotment** automation for the **Customer Order** module. This sub-module assigns customer orders to Karigars or Employees. It follows the exact same logic and method as the `Repair Order Karigar Allotment` but operates within the Customer Order section.

**File to create**: `c:\Retail_Automation\Sparqla\Test_Customer\KarigarAllotment.py`  
**Update main.py**: Add `CustomerOrderKarigarAllotment` case.
**Excel Sheet**: `CustomerOrderKarigarAllotment`

---

### Controller Details (`admin_ret_order.php`)
- The Karigar Allotment functionality lives inside the Customer Orders module list page.
- **Menu**: Customer Orders → Karigar Allotment (or New Order List)
- **URL**: `admin_ret_order/customer_order/neworders` (Validate which one is live, usually matches `customer_order/neworders`).

---

### Form Fields & Technical Logic

This is a **List Page Bulk Action**.

#### 1. Search Section
- **Search Box**: `//input[@type='search']` (DataTables default search)
- Enter the `OrderNo` from Excel to isolate the specific record.

#### 2. Item Selection
- **Select Row Checkbox**: 
  - `//table[@id='neworder_list']/tbody/tr[contains(., '{order_no}')]//input[@type='checkbox']`
  - Fallback (if obscured): Click the associated `<label>` inside the same row.

#### 3. Assignment Section
- **Assign To (Radio)**:
  - `name="order[assign_to]" value="1"` → Karigar (Default)
  - `name="order[assign_to]" value="2"` → Employee
- **Select Worker (Select2)**:
  - Trigger: `//select[@id='karigar_sel' or @id='employee_sel']/following-sibling::span`
  - Search: `//span[@class='select2-search select2-search--dropdown']/input`
- **Smith Due Date**:
  - `//table[@id='neworder_list']/tbody/tr[contains(., '{order_no}')]//input[@type='text' or contains(@class, 'datepicker')]`
  - Use JS JS `dispatchEvent` to set value as datepickers often block direct text entry.

#### 4. Action Buttons
- **Assign/Approve**: `id="approve"` (Label/Button)
- **Reject**: `id="reject"` (Label/Button)

---

### Automation Flow

1. **Navigation**: Navigate to `Sidebar → Customer Orders → Karigar Allotment` (or direct URL).
2. **Search**: Enter `OrderNo` into the search box and `sleep(2)` for filter.
3. **Select**: Click the checkbox for the target row.
4. **Assign Role**: Select "Karigar" or "Employee" radio based on Excel `AssignTo`.
5. **Select Worker**: Pick the `AssignName` using `Function_Call.dropdown_select`.
6. **Set Date**: (Optional) Use `execute_script` to set the `SmithDueDate`.
7. **Submit**: Click the **Assign/Approve** button.
8. **Verification**: 
   - Wait for success toaster: `//div[contains(@class,'alert-success')]`.
   - Update Excel with `Pass` if message found, else `Fail`.

---

### Expected Excel Columns (`CustomerOrderKarigarAllotment`)
excel file fath : C:\Users\Dell\Desktop\sqrqlas\Sqarqla_Retail_data2.xlsx
sheet name : CustomerOrderKarigarAllotment
| Col | Field | Description |
|---|---|---|
| 1 | `TestCaseId` | Unique ID |
| 2 | `TestStatus` | Set to "Run" |
| 3 | `ActualStatus` | Script writes Pass/Fail |
| 4 | `OrderNo` | Number to search for |
| 5 | `AssignTo` | "Karigar" or "Employee" |
| 6 | `AssignName` | Exact name in Select2 |
| 7 | `SmithDueDate` | YYYY-MM-DD |
| 8 | `Action` | "Assign" (default) or "Reject" |
| 9 | `Remark` | Final message |

---

### Critical Reminders
- **Select2**: Use `//select[@id='...']/following-sibling::span`.
- **Datepicker**: Use JS `arguments[0].value = ...` to bypass overlay.
- **Table ID**: Confirm if the table ID is `neworder_list` (standard) or `customerorder_list`.
- **Framework**: Use `Function_Call` and `ExcelUtils` with `workbook = load_workbook()` inside the loop.
