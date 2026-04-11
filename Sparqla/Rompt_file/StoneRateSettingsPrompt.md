# Stone Rate Settings Automation Blueprint

Build the complete **Stone Rate Settings** automation for the Retail Automation project. This module handles both single-row and **Range Flow** (multi-row) entries for stones and product configurations.

## File Hierarchy
```
C:\Retail_Automation\Sparqla\Test_master\StoneRateSettings.py
```

## Navigation & URL
| Module | Menu Path | URL |
| :--- | :--- | :--- |
| **Stone Rate Settings** | Retail catalog → Stone Rate Settings | `admin_ret_catalog/ret_stone_rate_settings/list` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Form Fields & UI Elements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Tabs
1. **Loose Stone** (Tab 1): `//a[@href='#tab_1']`
2. **Loose Products** (Tab 2): `//a[@href='#tab_2']`

### Grid Operations (Range Flow)
- **Multi-Row Logic**: Use the pipe symbol (`|`) in Excel cells to separate values for multiple rows.
- **Add Row (Stone)**: `//span[@class="add_stonerate_info"]`
- **Add Row (Product)**: `//span[@class="add_stoneproduct_info"]`
- **Logic**: For each new row, click the `(+)` icon and find the last row added by counting `tbody/tr`.

### Grid Fields (Common)
- **Branch**: Select2 dropdown (`branch_select`)
- **Quality**: Select2 dropdown (`stn_quality` or `quality_code`)
- **UOM**: Select2 dropdown (`uom_id`)
- **Calc Type**: Select2 dropdown (`stn_calc_type`)
- **From/To Cent**: Number Inputs (`from_wt`, `to_wt`). *Note: These may be read-only for non-diamond products.*
- **Min/Max Rate**: Number Inputs (`min_rate`, `max_rate`)

### Selectors (Indexed)
- Row XPath: `(//table[@id='TABLE_ID']/tbody/tr)[INDEX]`
- Select2: `//select[contains(@name, 'FIELD')]/following-sibling::span`
- Input: `//input[contains(@name, 'FIELD')]`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Full Business Workflow & Scenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Scenario 1: Single Row Entry**
1. Navigate to Add page.
2. Click `(+)` to add a single row.
3. Fill details and click **Save**.

**Scenario 2: Range Flow (Multi-Row)**
1. Navigate to Add page.
2. For each value group in Excel (split by `|`):
   - Click the green `(+)` icon.
   - Wait for the new row to appear.
   - Fill all details for that specific row index.
3. Once all rows are populated, click the blue **Save** button.
4. Catch the unified "Success" alert.

**Scenario 3: Product-Specific Settings**
1. Switch to **Loose Products** tab.
2. Fill **Product**, **Design**, and **Sub Design**.
3. If **From/To Cent** are disabled, skip them and only fill Rates.
4. Save and verify.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Expected Excel Data Structure
excel file path: C:\Users\Dell\Desktop\sqrqlas\Sqarqla_Retail_data2.xlsx
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Sheet: `StoneRateSettings`**

| Col | Field | Notes (Use `\|` for multiple rows) |
| :--- | :--- | :--- |
| **1** | **TestCaseId** | Unique identifier |
| **2** | **TestStatus** | Run / Skip |
| **3** | **ActualStatus**| Pass/Fail (Script Updated) |
| 4 | **Tab** | `Loose Stone` or `Loose Products` |
| 5 | **Branch** | `HEAD OFFICE\|HEAD OFFICE` |
| 6 | **StoneType** | (Tab 1) |
| 7 | **StoneName** | (Tab 1) |
| 8 | **Product** | `DIAMOND RING\|DIAMOND RING` |
| 11 | **Quality** | `VVS\|VVS` |
| 12 | **UOM** | `CT\|CT` |
| 14 | **FromCent** | `100\|201` |
| 15 | **ToCent** | `200\|300` |
| 16 | **MinRate** | `4000\|6000` |
| 17 | **MaxRate** | `6000\|8000` |
| 18 | **ExpectedMsg**| Success msg verification |
