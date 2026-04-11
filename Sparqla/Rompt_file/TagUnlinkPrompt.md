Build complete **Tag Unlink** (referred to as Order Unlink) automation for the Retail Automation project.
Follow the **EXACT same code pattern** as `OrderLink.py`, using the established Selenium framework and `ExcelUtils`.

---

## File to Create
```
C:\Retail_Automation\Sparqla\Test_Tagging\TagUnlink.py
```

## Update main.py
Add `TagUnlink` case to the module dispatcher.

---

## Navigation & URL
| Module | Menu Path | URL |
| :--- | :--- | :--- |
| **Tag Unlink** | Tagging → Tag Unlink | `admin_ret_tagging/tagging/tag_unlink` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Form Fields & UI Elements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Filter/Search Section:
- ✅ **Select Branch** (Select2 Dropdown): Sets the source branch (e.g., HEAD OFFICE).
- ✅ **Search Tag Code** (Text Input): To search for the specific tag being unlinked (e.g., GBT-LJXNH).
- ✅ **Search Old Tag Code** (Text Input): Alternatively, search by old tag code.

### Table & Processing Section:
- ✅ **Table Row Identification**: Row appears after searching a tag code.
- ✅ **Row Checkbox**: A checkbox in the first column to select the item for unlinking.
- ✅ **Table Verification Data**: Includes `Tag Code`, `Order No`, ` status`.
- ✅ **Save All Button**: Submits the form to execute the unlink process.
- ✅ **Cancel Button**: Clears the form.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Full Business Workflow & Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 1. Primary Flow (Tag Unlinking)
- **Workflow**:
  1. Navigate to the Tag Unlink page.
  2. Select the **Branch**.
  3. Enter the target tag in **Search Tag Code** (or Old Tag Code).
  4. Wait for the data table to populate with the matching record.
  5. In the generated table row, ensure the **leftmost checkbox** is checked.
  6. Click the blue **Save All** button at the bottom.
  7. Verify the **Success Message** banner appears.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Important Lessons Learned & Automation Gotchas
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- ⚠️ **Interactability Issues**: Floating banners and footers can intercept clicks. Use JavaScript scrolling (`execute_script("arguments[0].scrollIntoView({block:'center'});", element)`).
- ⚠️ **Search Inputs**: Unlike `OrderLink` where the search was a select2 dropdown, the `Search Tag Code` here appears to be a standard text input field. Use standard `send_keys()`.
- ⚠️ **Explicit Waits**: Do not use `sleep()` for page/table loads. Always wait for the specific table element or success banner to be visible.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Expected Excel Sheet Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Sheet: `TagUnlink`**
| Col | Field | Notes |
| :--- | :--- | :--- |
| 1 | **TestCaseId** | Unique ID for the test case |
| 2 | **TestStatus** | Run / Skip |
| 3 | **Branch** | Branch selection |
| 4 | **TagCode** | E.g. GBT-LJXNH |
| 5 | **OldTagCode** | Alternative search |
| 6 | **ExpectedMsg**| Success verification string |
| 7 | **ActualStatus** | Success / Fail (Updated by script) |
| 8 | **Remarks** | Error stacktrace or success details |
