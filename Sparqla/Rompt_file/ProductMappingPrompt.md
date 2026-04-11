# Master Prompt: Other Inventory Product Mapping Automation

Build complete **Product Mapping** automation for the Retail Automation project. This module is used to link "Other Inventory Items" (e.g., Packaging Boxes) to specific "Products" (e.g., Ring, Necklace) so they can be issued together.

**File to create**: `c:\Retail_Automation\Sparqla\Test_OtherInventory\ProductMapping.py`
**Update main.py**: Add `ProductMapping` case.

---

### Controller Details (`admin_ret_other_inventory.php`)
**Functions**:
- `product_mapping/list` → Main mapping page.
- `update_product_mapping` → Save mapping between item and products.
- `delete_product_mapping` → Remove mapping.

---

### Navigation
- **Menu**: Other Inventory -> Product Mapping
- **URL**: `admin_ret_other_inventory/product_mapping/list`

---

### UI Elements (Main Page)
#### Mapping Details Section
- **Select Item (Dropdown)**: `id=select_item`
- **Select Product (Multi-select)**: `id=select_product`
- **Update Button**: `id=update_product_mapping`
- **Delete Button**: `id=delete_product_mapping`

#### Filter Section
- **Product Filter**: `id=prod_filter`
- **Item Filter**: `id=item_filter`
- **Search Button**: `id=search_design_maping`

---

### Full Business Workflow
1. **Create Product Mapping Flow**
    - **Navigate**: Other Inventory -> Product Mapping.
    - **Select Item**: Select the item name from `id=select_item` (e.g., "Gift Box").
    - **Select Product**: Select one or more products from `id=select_product` (e.g., "Gold Ring").
    - **Save**: Click the **Update** button (`id=update_product_mapping`).
    - **Verify**: Confirm success alert: "Product Mapped successfully".

2. **List Verification Flow**
    - **Navigate**: Other Inventory -> Product Mapping List.
    - **Filter**: 
        - Select product in `id=prod_filter`.
        - Select item in `id=item_filter`.
        - Click **Search** (`id=search_design_maping`).
    - **Verify Table**: Confirm the mapping appears in the `mapping_list` table.

---

### Success / Failure Messages
- **Success (Map)**: "Product Mapped successfully"
- **Success (Delete)**: "Product Mapped Deleted successfully"
- **Failure**: "Unable to Proceed Your Request"

---

### Excel Sheet: ProductMapping
- **Sheet Name**: `ProductMapping`
- **Columns**:
    - **Col 1**: TestCaseId
    - **Col 2**: TestStatus
    - **Col 3**: ActualStatus
    - **Col 4**: ItemName
    - **Col 5**: ProductName
    - **Col 6**: ExpectedStatus

---

### Code Patterns & Logic
- **Multi-select Handling**: The `select_product` field is a multi-select dropdown. Ensure the script handles selecting single or multiple items using the standard Sparqla Select2/Dropdown utility.
- **Search Logic**: After mapping, use the filter section (Product/Item filters) and Search button to verify the record exists in the table.
- **Consistency**: Follow the `Sparqla` project structure.
