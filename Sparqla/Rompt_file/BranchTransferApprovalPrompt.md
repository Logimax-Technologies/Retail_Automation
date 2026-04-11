Build complete **Branch Transfer Approval** automation for the Retail Automation project.
Follow the **EXACT same code pattern** as `BranchTransfer.py`, `LotGenerate.py`, `QCIssueReceipt.py`, etc., using the established Selenium framework and `ExcelUtils`.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_Inventory\BranchTransferApproval.py
```

## Update main.py
Add `BranchTransferApproval` case to the module dispatcher.

---

## Navigation & URL
| Module | Menu Path | URL |
| :--- | :--- | :--- |
| **Branch Transfer Approval** | Master → Branch Transfer → Branch Transfer Approval | `admin_ret_brntransfer/branch_transfer/approval_list` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Form Fields & UI Elements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Filter/Search Section:
- ✅ **Approval Type (Radio Buttons)**: `Transit Approval` or `Stock Download`
- ✅ **From Branch (Select)**: Select the source branch (e.g., HEAD OFFICE)
- ✅ **To Branch (Select)**: Select the destination branch (e.g., LOGIMAX)
- ✅ **Trans Code (Input Text)**: The transaction code generated from Branch Transfer (e.g., 05866)
- ✅ **Type (Radio Buttons)**: Must match what was selected during Branch Transfer. Options: 
  - `Tagged`
  - `Non Tagged`
  - `Purchase Items`
  - `Packaging Items`
  - `Repair Order`
- ✅ **Product (Input Text)**: Optional product filter.
- ✅ **Date (Date Range)**: Optional date filter.
- ✅ **Other Issue (Checkbox)**: Select only if the transfer was marked as "Other Issue".
- ✅ **Filter (Button)**: Clicks to trigger the search.

### Table & Approval Section:

**For Transit Approval:**
- ✅ **Table Results**: A table displays the filtered data.
- ✅ **Row Checkbox**: A checkbox typically appears in the first column next to the Trans Code.
- ✅ **Row Input Field**: An input field inside the row to enter the `Trans Code` again for verification.
- ✅ **Approve Button**: Located at the bottom to submit the Transit Approval.
- ✅ **Success Banner**: "Branch Transfer Approval! Records updated successfully"

**For Stock Download:**
- ✅ **Table Results**: A table displays the filtered data, showing the Transit Approval status as passed.
- ✅ **Confirmation Check/Input Field**: Often an input field labeled `Tag Code` or similar appears at the bottom where the Trans Code must be re-entered, or a final checkbox must be clicked.
- ✅ **Approve Button**: Located at the bottom to submit the Stock Download.
- ✅ **Success Banner**: Confirms the Stock Download is complete.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Full Business Workflow & Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 1. Transit Approval Flow
- **Workflow**:
  1. Navigate to the `Branch Transfer Approval List` page.
  2. Select **Approval Type**: `Transit Approval`.
  3. Select **From Branch** and **To Branch**.
  4. Enter the **Trans Code** into the input field.
  5. Select the matching **Type** (e.g., Tagged, Non-Tagged).
  6. Check the **Other Issue** checkbox *only* if required by the test data.
  7. Click the **Filter** button.
  8. Wait for the table to load.
  9. In the table row, **select the checkbox** corresponding to the transaction.
  10. **Enter the Trans Code** into the input field provided in that row.
  11. Click the **Approve** button at the bottom.
  12. Verify the **Success Message** banner appears.

### 2. Stock Download Flow
- **Workflow**:
  1. **Refresh** the page (or navigate back to clear state).
  2. Select **Approval Type**: `Stock Download`.
  3. Select the same **From Branch** and **To Branch**.
  4. Enter the same **Trans Code**.
  5. Select the same **Type**.
  6. Check **Other Issue** if applicable.
  7. Click the **Filter** button.
  8. Wait for the table to load.
  9. Complete the final confirmation (e.g., enter the Trans Code in the bottom input field or select the final checkbox as prompted by the UI).
  10. Click the **Approve** button.
  11. Verify the **Success Message** banner appears.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Important Lessons Learned & Automation Gotchas
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- ⚠️ **Interactability Issues**: Floating banners and footers can intercept clicks on the `Approve` button or checkboxes. Use JavaScript scrolling (`execute_script("arguments[0].scrollIntoView(true);", element)`) or scroll to the top/bottom as needed.
- ⚠️ **XPath text() Selection**: For Radio Button labels, never use `translate(text(), ...)` because the DOM structure varies (sometimes `<label><input>Text</label>`, sometimes `<input>Text`). Use robust composites like:
  `//label[contains(normalize-space(), "Text")]//input | //input[@type="radio" and following-sibling::text()[1][contains(., "Text")]]`
- ⚠️ **Filter Field IDs**: In Approval List pages, dropdown IDs often use the `filter_` notation instead of the Add Page notation. Example: `filter_from_brn` and `filtr_to_brn` (watch out for typos in the source code like `filtr`).
- ⚠️ **Approval Type Radios**: Provide exact name locators if possible. Example: `//input[@name="bt_approval_type" and @value="1"]`.
- ⚠️ **Wait for Loaders**: Ensure explicit waits (`WebDriverWait`) are used after clicking `Filter` for the table to populate, and after clicking `Approve` for the success banner to appear. Do not just sleep.
- ⚠️ **Dictionary Access**: When reading from `row_data` in Python, ALWAYS use dictionary `get` methods (e.g., `row_data.get('TransCode')`) rather than parenthesis syntax.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Expected Excel Sheet Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Sheet: `BranchTransferApproval`**
| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **TestCaseId** | Unique ID for the test case |
| 2 | **TestStatus** | Run / Skip |
| 3 | **ApprovalType** | Transit Approval / Stock Download |
| 4 | **FromBranch** | Name of From Branch |
| 5 | **ToBranch** | Name of To Branch |
| 6 | **TransCode** | The transaction code to approve |
| 7 | **TransferType** | Tagged, Non Tagged, Purchase Items, Packaging Items, Repair Order |
| 8 | **IsOtherIssue** | Yes / No |
| 9 | **ExpectedMessage**| Success verification string |
| 10 | **ActualStatus** | Success / Fail (Updated by script) |
| 11 | **Remarks** | Error stacktrace or success details |
