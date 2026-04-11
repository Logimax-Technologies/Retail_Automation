# Section Transfer Automation Blueprint

Build complete **Section Transfer** (Section Item Transfer) automation for the Retail Automation project.
Follow the **EXACT** code pattern from recent modules (`BranchTransferApproval`, `OrderLink`, etc.), incorporating the newly learned Excel standard and locator preferences.

## File Hierarchy
```
C:\Retail_Automation\Sparqla\Test_SectionTransfer\SectionTransfer.py
```

## Navigation & URL
| Module | Menu Path | URL |
| :--- | :--- | :--- |
| **Section Transfer** | Inventory → Section Transfer List | `admin_ret_section_transfer/ret_section_transfer/list` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Form Fields & UI Elements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Search / Filter Form (Left Side)
1. **Type** (Radio Buttons): `Tagged` or `Non Tagged`
2. **Select Branch\*** (Select2 Dropdown): e.g., "HEAD OFFICE"
3. **Select Product\*** (Select2 Dropdown): e.g., "GOLD BANGLES"
4. **From Section** (Select2 Dropdown): Source section grouping.
5. **Search Tag Code** (Text Input): Optional specific tag search.
6. **Search Old Tag Id** (Text Input): Optional old tag search.
7. **Estimation No.** (Text Input): Optional estimation check.
8. **Search Button** (Blue Button): Submits filter to load the table.

### Action Form (Right Side)
1. **To Section** (Select2 Dropdown): The destination for the items being transferred.
2. **Transfer Button** (Green Button): Main submission to process the table items.

### Table Section
- **Checkbox Panel**: Standard left-side `All` checkbox or row-level checkboxes.
- **Records**: Wait for `admin_ret_section_transfer` table rows to populate.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Full Business Workflow & Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Primary Tagged Flow:**
1. Navigate directly to `ret_section_transfer/list` URL.
2. Ensure **Type** radio button matches what is needed.
3. Populate the **Branch**, **Product**, and **From Section**.
4. *(Optional)* Fill in Tag/Estimation fields if provided in Excel.
5. Click **Search**.
6. Wait for the data table and ensure the target row's checkbox is selected.
7. Fill the **To Section** in the right-side box.
8. Click the green **Transfer** button.
9. Catch the resulting Success Banner.

**Tagged Flow (Branch & Product Only):**
1. Navigate directly to `ret_section_transfer/list` URL.
2. Select **Type** radio button as `Tagged`.
3. Populate only the **Branch** and **Product** fields.
4. Click **Search** button.
5. Wait for the data table and click the checkbox dynamically.
6. Select the **To Section** in the right-side box.
7. Click the green **Transfer** button.
8. Catch the resulting Success Banner.


**Tagged Flow (Search by Old Tag Id):**
1. Navigate directly to `ret_section_transfer/list` URL.
2. Select **Type** radio button as `Tagged`.
3. Populate the **Branch** and **Product** fields.
4. Enter the specific old tag in the **Search Old Tag Id** field and wait for the tag details to show in table format.
5. Click the checkbox next to the selection dynamically.
6. Select the **To Section** in the right-side box.
7. Click the green **Transfer** button.
8. Catch the resulting Success Banner.

**Non Tagged Flow:**
1. Navigate directly to `ret_section_transfer/list` URL.
2. Select **Type** radio button as `Non Tagged`.
3. Populate the **Branch**, **Product**, and **From Section** fields.
4. Click the **Search** button.
5. Wait for the non-tagged details to show in table format.
6. Click the checkbox dynamically for the desired row.
7. Enter the pieces count in the **Pcs** field and gross weight in the **Gwt** field for the selected row.
8. Select the **To Section** in the right-side box.
9. Click the green **Transfer** button.
10. Catch the resulting Success Banner.

**Non Tagged Flow (Branch & Product Only):**
1. Navigate directly to `ret_section_transfer/list` URL.
2. Select **Type** radio button as `Non Tagged`.
3. Populate only the **Branch** and **Product** fields.
4. Click the **Search** button.
5. Wait for the non-tagged details to show in table format.
6. Click the checkbox dynamically for the desired row.
7. Enter the pieces count in the **Pcs** field and gross weight in the **Gwt** field for the selected row.
8. Select the **To Section** in the right-side box.
9. Click the green **Transfer** button.
10. Catch the resulting Success Banner.

**Post-Transfer Verification Flow (Optional Verify):**
1. After a successful transfer, reload or stay on the `ret_section_transfer/list` page.
2. Select **Type** radio button as appropriate (e.g., `Tagged`).
3. Populate the **Branch** field.
4. Set the **From Section** to the section the item was just transferred to (e.g., `HARAM SECTION`).
5. Enter the specific tag or product details in the search filters (e.g., `GBT-00440`).
6. Click the **Search** button.
7. Verify that the transferred details now show up in the data table under the new section.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Strict Framework Rules
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. **Excel Layout Rule**: `TestStatus` MUST be Column 2, and `ActualStatus` MUST be Column 3.
2. Excel Update Logic: Do not accumulate results. Use `_update_excel_status(row_num, test_status, actual_status)` via `openpyxl.styles.Font` dynamically inside the test loop directly writing to Columns 2 and 3.
3. ID Selectors: Map dropdowns using specific IDs if available instead of generic classes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Expected Excel Data Structure
excel file path:C:\Users\Dell\Desktop\sqrqlas\Sqarqla_Retail_data2.xlsx
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Sheet: `SectionTransfer`**

| Col | Field | Notes |
| :--- | :--- | :--- |
| **1** | **TestCaseId** | Unique identifier (e.g., TC_SEC_001) |
| **2** | **TestStatus** | Run / Skip |
| **3** | **ActualStatus** | Overwritten by Script (Pass/Fail) |
| 4 | **Type** | Tagged / Non Tagged |
| 5 | **Branch** | Select Branch |
| 6 | **Product** | Select Product |
| 7 | **FromSection**| From Section dropdown |
| 8 | **ToSection** | To Section dropdown (destination) |
| 9 | **TagCode** | Optional search |
| 10 | **OldTagId** | Optional search |
| 11 | **EstimationNo** | Optional search |
| 12 | **Pcs** | Pieces for Non-Tagged |
| 13 | **Gwt** | Gross weight for Non-Tagged |
| 14 | **ExpectedMsg**| Banner verification string |
| 15 | **Remarks** | Overwritten by Script (Trace) |
