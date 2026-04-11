Build complete **Order Link** automation for the Retail Automation project.
Follow the **EXACT same code pattern** as `BranchTransferApproval.py` and other modules, using the established Selenium framework and `ExcelUtils`.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_Tagging\OrderLink.py
*(Note: It may be under Test_Inventory or Test_Tagging. We'll use Test_Inventory if requested, though breadcrumb shows Tagging)*
```

## Update main.py
Add `OrderLink` case to the module dispatcher.

---

## Navigation & URL
| Module | Menu Path | URL |
| :--- | :--- | :--- |
| **Order Link** | Tagging → Order Link | `admin_ret_tagging/...` or similar *(Script should navigate via menu or URL fallback)* |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Form Fields & UI Elements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Filter/Search Section:
- ✅ **Select Branch** (Select2 Dropdown): Sets the source branch (e.g., HEAD OFFICE).
- ✅ **Search Order** (Select2 Dropdown): Multi-select or single-select to search for the specific order (e.g., ATM25-OR-00001).
- ✅ **Select Financial Year** (Select2 Dropdown): Usually defaults to the current active year, but may need explicit setting.

### Table & Processing Section:
- ✅ **Table Row Identification**: Row appears after an order is selected.
- ✅ **Row Checkbox**: A checkbox in the first column (often has an ID/text next to it).
- ✅ **Tag No (Input Box)**: A text input field in the table row to assign a tag.
- ✅ **Old Tag No (Input Box)**: A text input field in the table row to assign an old tag.
- ✅ **Delete Button**: A red trash icon to remove the row from the preview.
- ✅ **Save All Button**: Submits the form.
- ✅ **Cancel Button**: Clears the form.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Full Business Workflow & Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 1. Primary Flow (Order Linking)
- **Workflow**:
  1. Navigate to the Order Link page.
  2. Select the **Branch** and **Financial Year** (if they differ from default/test data).
  3. Enter the target order number in **Search Order** and select it.
  4. Wait for the data table to populate.
  5. In the generated table row, ensure the **checkbox** is checked.
  6. Fill in the **Tag No** (or **Old Tag No**) as provided by the test data.
  7. Click **Save All**.
  8. Verify the **Success Message** banner appears.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Important Lessons Learned & Automation Gotchas
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- ⚠️ **Interactability Issues**: Floating banners and footers can intercept clicks. Use JavaScript scrolling (`execute_script("arguments[0].scrollIntoView({block:'center'});", element)`).
- ⚠️ **Table Locators**: When injecting input into table rows, do not assume all inputs are text fields (exclude checkboxes, hidden elements).
- ⚠️ **Explicit Waits**: Do not use `sleep()` for page/table loads. Always wait for the specific table element or success banner to be visible.
- ⚠️ **Dictionary Access**: Always use `.get('ColumnName')` when accessing `row_data` to prevent script crashes on missing data.
- ⚠️ **Select2 Loading**: Searching the order might trigger an AJAX call. Allow brief time for the Select2 results to populate before selecting.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Expected Excel Sheet Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Sheet: `OrderLink`**
| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **TestCaseId** | Unique ID for the test case |
| 2 | **TestStatus** | Run / Skip |
| 3 | **Branch** | Branch selection |
| 4 | **FinYear** | Financial year selection (if needed) |
| 5 | **OrderNo** | E.g. ATM25-OR-00001 |
| 6 | **TagNo** | The Tag number to assign |
| 7 | **OldTagNo** | The Old Tag number to assign |
| 8 | **ExpectedMsg**| Success verification string |
| 9 | **ActualStatus** | Success / Fail (Updated by script) |
| 10 | **Remarks** | Error stacktrace or success details |
