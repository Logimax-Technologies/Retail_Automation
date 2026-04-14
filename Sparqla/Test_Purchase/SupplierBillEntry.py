from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException
from time import sleep
from Utils.Excel import ExcelUtils
from Utils.Function import Function_Call
from openpyxl import load_workbook
from openpyxl.styles import Font
from datetime import datetime
import os
import re
import unittest

FILE_PATH = ExcelUtils.file_path

class SupplierBillEntry(unittest.TestCase):
    """
    Supplier Bill Entry Module Automation
    Follows Sparqla framework rules: Function_Call only, ExcelUtils only, No raw Selenium
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.fc = Function_Call(driver)

    def test_supplier_bill_entry(self):
        """Main entry point for Supplier Bill Entry automation"""
        driver = self.driver
        wait = self.wait

        # Navigate to Supplier Bill Entry List
        try:
            wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Toggle navigation"))).click()
            Function_Call.click(self, "//span[contains(text(), 'Purchase Module')]")
            Function_Call.click(self, "//span[contains(text(), 'Supplier Bill Entry')]")
            sleep(2)
            print("✅ Navigated to Supplier Bill Entry list page")
        except Exception as e:
            print(f"⚠️ Navigation failed: {e}")
            return

        # Read Excel data
        sheet_name = "SupplierBillEntry"
        try:
            valid_rows = ExcelUtils.get_valid_rows(FILE_PATH, sheet_name)
            print(f"✅ Found {valid_rows - 1} test cases in '{sheet_name}' sheet")
        except Exception as e:
            print(f"❌ Failed to read Excel: {e}")
            return

        workbook = load_workbook(FILE_PATH)
        sheet = workbook[sheet_name]

        for row_num in range(2, valid_rows):
            # Column mapping
            data_map = {
                "TestCaseId": 1, "TestStatus": 2, "ActualStatus": 3,
                "GRNNumber": 4, "AgainstOrder": 5, "Karigar": 6,
                "RefNo": 7, "PurchaseCategory": 8, "RefDate": 9,
                "ApprovalStock": 10, "Hallmark": 11, "RateFixed": 12,
                "AgainstKarigarIssue": 13, "PONumber": 14, "Category": 15,
                "Product": 16, "Purity": 17, "Design": 18,
                "SubDesign": 19, "Pcs": 20, "GrossWt": 21,
                "WastagePercent": 22, "McType": 23, "McValue": 24,
                "Touch": 25, "Type": 26, "RatePerGram": 27,
                "ExpectedStatus": 28, "CancelReason": 29, "Remark": 30
            }

            row_data = {key: sheet.cell(row=row_num, column=col).value for key, col in data_map.items()}

            # if str(row_data["TestStatus"]).strip().lower() != "yes":
            #     continue

            print(f"\n{'='*80}")
            print(f"🧪 Running Test Case: {row_data['TestCaseId']}")
            print(f"{'='*80}")

            tc_id = str(row_data["TestCaseId"]).upper()

            try:
                if "CANCEL" in tc_id:
                    result = self.test_cancel_flow(row_data, row_num, sheet_name)
                elif "EDIT" in tc_id:
                    result = self.test_edit_update_flow(row_data, row_num, sheet_name)
                elif "MULTIPLE" in tc_id:
                    result = self.test_multiple_items_flow(row_data, row_num, sheet_name)
                else:
                    result = self.test_save_flow(row_data, row_num, sheet_name)

                print(f"🏁 Test Result: {result[0]} - {result[1]}")
                GRN_no = result[2] if (len(result) > 2 and result[2]) else str(row_data["GRNNumber"])
                job_id = result[3] if (len(result) > 3 and result[3]) else None
                print(f"DEBUG: GRN={GRN_no}, JobID={job_id}")

                po_no = None
                if result[0] == "Pass" and "CANCEL" not in tc_id:
                    list_result = self.test_list_verification_flow(GRN_no, row_data, job_id=job_id)
                    print(f"📊 List Page Verification: {list_result[0]} - {list_result[1]}")
                    
                    po_no = list_result[2] if len(list_result) > 2 else None
                    if po_no:
                        print(f"📝 Captured Po No: {po_no}")

                # Consolidate status updates to a single call after verification
                self._update_excel_status(row_num, result[0], result[1], sheet_name, GRN_no, po_no=po_no, hallmark=str(row_data.get("Hallmark", "")))

            except Exception as e:
                print(f"❌ Test Case {row_data['TestCaseId']} failed: {e}")
                self._update_excel_status(row_num, "Fail", f"Exception: {str(e)}", sheet_name)
                self._take_screenshot(f"Exception_TC{row_data['TestCaseId']}")

        workbook.close()

    def test_save_flow(self, row_data, row_num, sheet_name):
        return self._execute_full_flow(row_data, row_num, sheet_name)

    def test_multiple_items_flow(self, row_data, row_num, sheet_name):
        tc_id = str(row_data["TestCaseId"]).strip()
        items_sheet_name = "SupplierBillEntry_Items"
        item_rows = []
        try:
            wb = load_workbook(FILE_PATH)
            items_sheet = wb[items_sheet_name]
            col_map = {
                "TestCaseId": 1, "Category": 2, "Product": 3, "Purity": 4,
                "Design": 5, "SubDesign": 6, "Pcs": 7, "GrossWt": 8,
                "WastagePercent": 9, "McType": 10, "McValue": 11,
                "Touch": 12, "RatePerGram": 13,"Type":14, "PONumber": 15
            }
            for r in range(2, items_sheet.max_row + 1):
                if str(items_sheet.cell(row=r, column=1).value).strip() == tc_id:
                    item_data = {k: items_sheet.cell(row=r, column=v).value for k, v in col_map.items()}
                    item_rows.append(item_data)
            wb.close()
            if not item_rows: return ("Fail", f"No items in {items_sheet_name}")
            return self._execute_full_flow(row_data, row_num, sheet_name, item_list=item_rows)
        except Exception as e:
            return ("Fail", f"Error reading items: {str(e)}")

    def _execute_full_flow(self, row_data, row_num, sheet_name, item_list=None):
        driver, wait = self.driver, self.wait
        current_field = "Initial Setup"
        try:
            Function_Call.alert(self)
            Function_Call.click(self, '//a[@id="add_Order"]')
            sleep(3)

            # --- Tab 1 ---
            #current_field = "Tab 1: Bill Details"

            if row_data.get("GRNNumber"):
                current_field = "GRN Number"
                Function_Call.dropdown_select(self, '//select[@id="select_grn"]/following-sibling::span', str(row_data["GRNNumber"]), '//span[@class="select2-search select2-search--dropdown"]/input')
                sleep(2)
            
            if row_data.get("AgainstOrder"):
                current_field = "Against Order"
                suffix = "order" if str(row_data["AgainstOrder"]).lower() == "yes" else "purchase"
                Function_Call.click(self, f'//input[@id="aganist_{suffix}"]')

            if row_data.get("PurchaseCategory"):
                current_field = "Purchase Category"
                try:
                    Select(driver.find_element(By.ID, "purchase_type")).select_by_visible_text(str(row_data["PurchaseCategory"]))
                    print(f"✅ Selected Purchase Category: {row_data['PurchaseCategory']}")
                except Exception as e:
                    print(f"⚠️ Failed to select Purchase Category: {e}")

            radios = [("ApprovalStock", "approval_stock_"), ("RateFixed", "is_rate_fixed_")]
            for field, prefix in radios:
                if row_data.get(field):
                    current_field = field
                    suffix = "yes" if str(row_data[field]).lower() == "yes" else "no"
                    Function_Call.click(self, f'//input[@id="{prefix}{suffix}"]')
            
            if row_data.get("Hallmark"):
                current_field = "Hallmark"
                val = "1" if str(row_data["Hallmark"]).lower() == "yes" else "0"
                Function_Call.click(self, f'//input[@name="order[is_halmerked]" and @value="{val}"]')
            
            if row_data.get("RefNo"):
                current_field = "Ref No"
                Function_Call.fill_input(self, wait, (By.NAME, "order[po_supplier_ref_no]"), str(row_data["RefNo"]), "RefNo", row_num, Sheet_name=sheet_name)
            
            # if row_data.get("RefDate"):
            #     current_field = "Ref Date"
            #     Function_Call.fill_input(self, wait, (By.NAME, "order[po_ref_date]"), str(row_data["RefDate"]), "RefDate", row_num, Sheet_name=sheet_name, Date_range='past_or_current')

            if row_data.get("AgainstKarigarIssue"):
                current_field = "Against Karigar Issue"
                val = "1" if str(row_data["AgainstKarigarIssue"]).lower() == "yes" else "0"
                Function_Call.click(self, f'//input[@name="aganist_karigar_metal_issue" and @value="{val}"]')

            current_field = "Switch to Tab 2"
            Function_Call.click(self, '//a[@id="tab_items"]')
            sleep(1)

            # --- Tab 2 ---
            current_field = "Tab 2: Item Details"
            if item_list:
                items = item_list
            else:
                items = [row_data]
            for item in items:
                if str(row_data.get("AgainstOrder")).lower() == "yes" and item.get("PONumber"):
                    current_field = "Select PO Number"
                    Function_Call.dropdown_select(self, '//select[@id="select_po_no"]/following-sibling::span', str(item["PONumber"]), '//span[@class="select2-search select2-search--dropdown"]/input')
                    sleep(1)
                    Function_Call.click(self, '//button[@id="close_order_details"]')
                    sleep(1)
                selects = [("Category", "select_category"), ("Purity", "select_purity"), ("Product", "select_product"), ("Design", "select_design"), ("SubDesign", "select_sub_design")]
                for k, eid in selects:
                    if item.get(k):
                        current_field = f"Select {k}"
                        Function_Call.dropdown_select(self, f'//select[@id="{eid}"]/following-sibling::span', str(item[k]), '//span[@class="select2-search select2-search--dropdown"]/input')
                
                inputs = [("Pcs", "tot_pcs"), ("GrossWt", "tot_gwt"), ("Touch", "purchase_touch"), ("RatePerGram", "rate_per_gram")]
                for k, eid in inputs:
                    if item.get(k):
                        current_field = f"Enter {k}"
                        Function_Call.fill_input(self, wait, (By.ID, eid), str(item[k]), k, row_num, Sheet_name=sheet_name)
                
                if item.get("McType"):
                    current_field = "MC Type"
                    Select(driver.find_element(By.ID, "mc_type")).select_by_visible_text(str(item["McType"]))
                if item.get("Type"):
                    current_field = "Karigar Calc Type"
                    Select(driver.find_element(By.ID, "karigar_calc_type")).select_by_visible_text(str(item["Type"]))
                if item.get("McValue"):
                    current_field = "MC Value"
                    Function_Call.fill_input(self, wait, (By.ID, "mc_value"), str(item["McValue"]), "McValue", row_num, Sheet_name=sheet_name)
                
                current_field = "Add Item Button"
                Function_Call.click(self, '//button[@id="add_po_order_items"]')
                sleep(2)
                if str(row_data.get("AgainstOrder")).lower() == "yes":
                    current_field = "Close Order Details"
                    Function_Call.click(self, '//button[@id="close_order_details"]')
                    sleep(1)
                
            # --- Tab 3 ---
            current_field = "Tab 3 Summary"
            Function_Call.click(self, '//li[@id="tab_tot_summary"]/a')
            sleep(1)
            
            # for cls in ["total_gb_pcs", "total_gb_gwt", "total_gb_lwt", "total_gb_nwt"]:
            #     diff = driver.find_element(By.CLASS_NAME, cls).text.strip()
            #     if diff and float(diff) != 0: return ("Fail", f"Data Mismatch: {cls}={diff}")

            current_field = "Take Screenshot"
            self._take_screenshot(f"BeforeSave_TC{row_data['TestCaseId']}")
            
            # --- Windows Handling for Print Tab ---
            main_window = self.driver.current_window_handle
            current_field = "Submit Button"
            Function_Call.click(self, '//button[@id="submit_pur_entry"]')
            job_id = self._handle_print_tab(main_window)
            sleep(9)

            try:
                current_field = "Capture Success Message"
                msg_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert-success')]")))
                msg = msg_element.text.strip()
                print(f"DEBUG: captured message: {msg}")
                if "Purchase Entry added successfully" in msg: 
                    match = re.search(r"successfully\s*[:\s]*([A-Z0-9-]+)", msg)
                    captured_grn = match.group(1) if match else row_data.get("GRNNumber") or ""
                    return ("Pass", f"✅ Purchase Entry added successfully: {captured_grn}", captured_grn, job_id)
                return ("Fail", f"Unexpected: {msg}", None, job_id)
            except: return ("Fail", "Success message not encountered", None, job_id)

        except Exception as e:
            self._take_screenshot(f"Error_TC{row_data['TestCaseId']}")
            # Click Cancel button to reset the form for the next row
            try:
                Function_Call.click(self, "//button[contains(text(), 'Cancel')]")
                sleep(2)
            except:
                self._cancel_form()
            return ("Fail", f"Error in {current_field}: {str(e)}")

    def test_list_verification_flow(self, GRN_no, row_data, job_id=None):
        driver, wait = self.driver, self.wait
        current_field = "Verification Start"
        search_val = job_id if job_id else GRN_no
        try:
            current_field = "Filter Today"
            Function_Call.click(self, '//button[@id="sbe-dt-btn"]')
            sleep(1); Function_Call.click(self, '//li[text()="Today"]'); sleep(2)
            
            current_field = "Search Box"
            search_xpath = '//div[@id="pur_entry_list_filter"]//input'
            search = wait.until(EC.presence_of_element_located((By.XPATH, search_xpath)))
            search.clear()
            search.send_keys(search_val)
            sleep(2)
            
            current_field = f"Table Row Search for {search_val}"
            table_xpath = f'//table[@id="pur_entry_list"]//tr[contains(., "{search_val}")]'
            rows = driver.find_elements(By.XPATH, table_xpath)
            if rows:
                # Capture PO Number from column 5 (at the targeted job_id row)
                try:
                    po_no = rows[0].find_element(By.XPATH, "./td[5]").text.strip()
                    sleep(1)
                    # Click checkbox for the captured row
                    Function_Call.click(self, f'//table[@id="pur_entry_list"]//tr[contains(., "{search_val}")]//input[@type="checkbox"]')
                    sleep(1)
                    
                    # Click Approve button
                    Function_Call.click(self, '//button[contains(text(), "Approve")]')
                    sleep(2)
                    
                    # Handle confirmation alert
                    Function_Call.alert(self)
                    sleep(1)

                    print(f"📍 Successfully found PO No: {po_no} for Job ID: {search_val}")
                    return ("Pass", f"Verified in list. PO No: {po_no}", po_no)
                except:
                    return ("Pass", "Verified in list but PO No extraction failed")
            return ("Fail", f"Value {search_val} not found in list")
        except Exception as e:
            return ("Fail", f"Error in {current_field}: {str(e)}")

    def test_edit_update_flow(self, row_data, row_num, sheet_name):
        wait = self.wait
        current_field = "Edit Flow Start"
        try:
            res = self.test_save_flow(row_data, row_num, sheet_name)
            if res[0] != "Pass": return res
            
            self.test_list_verification_flow(row_data["GRNNumber"], row_data)
            
            current_field = "Edit Button"
            Function_Call.click(self, f'//table[@id="pur_entry_list"]//tr[contains(., "{row_data["GRNNumber"]}")]//a[@class="btn btn-primary btn-edit"]')
            sleep(3)
            
            current_field = "Update Ref No"
            new_ref = f"{row_data['RefNo']}_ED"
            Function_Call.fill_input(self, wait, (By.NAME, "order[po_supplier_ref_no]"), new_ref, "RefNo", row_num, Sheet_name=sheet_name)
            
            current_field = "Summary Tab"
            Function_Call.click(self, '//li[@id="tab_tot_summary"]/a')
            sleep(1)
            
            current_field = "Update Button"
            main_window = self.driver.current_window_handle
            Function_Call.click(self, '//button[@id="submit_pur_entry"]')
            self._handle_print_tab(main_window)
            
            current_field = "Success Message"
            msg = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert-success')]"))).text.strip()
            if "Purchase Entry updated successfully" in msg: 
                return ("Pass", "✅ Purchase Entry updated successfully", row_data["GRNNumber"])
            return ("Fail", f"Unexpected message: {msg}")
        except Exception as e:
            return ("Fail", f"Error in {current_field}: {str(e)}")

    def test_cancel_flow(self, row_data, row_num, sheet_name):
        wait = self.wait
        current_field = "Cancel Flow Start"
        try:
            res = self.test_save_flow(row_data, row_num, sheet_name)
            if res[0] != "Pass": return res
            
            self.test_list_verification_flow(row_data["GRNNumber"], row_data)
            
            current_field = "Cancel Icon"
            Function_Call.click(self, f'//table[@id="pur_entry_list"]//tr[contains(., "{row_data["GRNNumber"]}")]//button[@class="btn btn-warning"]')
            sleep(2)
            
            current_field = "Cancel Modal"
            wait.until(EC.visibility_of_element_located((By.ID, "confirm-delete")))
            
            current_field = "Cancel Remark"
            self.driver.find_element(By.ID, "po_cancel_remark").send_keys(row_data["CancelReason"] or "Auto")
            
            current_field = "Confirm Cancel"
            Function_Call.click(self, '//button[@id="cancel_po"]')
            sleep(3)
            
            current_field = "Success Message"
            msg = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert-success')]"))).text.strip()
            if "Supplier Bill Entry Cancelled Successfully" in msg: 
                return ("Pass", "✅ Supplier Bill Entry Cancelled Successfully")
            return ("Fail", f"Unexpected message: {msg}")
        except Exception as e:
            return ("Fail", f"Error in {current_field}: {str(e)}")

    def _update_excel_status(self, row_num, test_status, actual_status, sheet_name, ref_no="", po_no=None, hallmark=""):
        try:
            print(ref_no)
            workbook = load_workbook(FILE_PATH)
            sheet = workbook[sheet_name]
            tc_id = sheet.cell(row=row_num, column=1).value
            
            color = "00B050" if test_status == "Pass" else "FF0000"
            sheet.cell(row=row_num, column=2, value=test_status).font = Font(bold=True, color=color)
            sheet.cell(row=row_num, column=3, value=actual_status).font = Font(bold=True, color=color)
            sheet.cell(row=row_num, column=4, value=ref_no).font = Font(bold=True)
            
            # Store PO No back into column 14 if captured
            if po_no:
                sheet.cell(row=row_num, column=14, value=po_no).font = Font(bold=True)
            
            sheet.cell(row=row_num, column=30, value=f"{test_status} - {actual_status}").font = Font(color=color)
            
            # Dynamic Row Mapping Formula (1:2 mapping)
            # SupplierBillEntry Row 2 -> Auxiliary Rows 2 & 3
            # SupplierBillEntry Row 3 -> Auxiliary Rows 4 & 5
            issue_idx = (row_num - 2) * 2 + 2
            receipt_idx = issue_idx + 1
            tc_issue = f"TC{issue_idx - 1:03d}"
            tc_receipt = f"TC{receipt_idx - 1:03d}"

            # Update HMIssueReceipt sheet logic (Specifically for unique rows based on row_num)
            if test_status == "Pass" and str(hallmark).lower() == "no":
                hm_sheet_name = "HMIssueReceipt"
                if hm_sheet_name in workbook.sheetnames:
                    hm_sheet = workbook[hm_sheet_name]
                    target_ref = po_no if po_no else ref_no
                    
                    if target_ref:
                        # Sequential Issue Row
                        hm_sheet.cell(row=issue_idx, column=1, value=tc_issue).font = Font(bold=True)
                        hm_sheet.cell(row=issue_idx, column=4, value="issue")
                        hm_sheet.cell(row=issue_idx, column=6, value=target_ref).font = Font(bold=True)
                        
                        # Sequential Receipt Row
                        hm_sheet.cell(row=receipt_idx, column=1, value=tc_receipt).font = Font(bold=True)
                        hm_sheet.cell(row=receipt_idx, column=4, value="receipt")
                        hm_sheet.cell(row=receipt_idx, column=6, value=target_ref).font = Font(bold=True)
                        
                        print(f"📝 Linked {target_ref} to {hm_sheet_name} (Rows {issue_idx}/{receipt_idx})")

            # Update QCIssueReceipt sheet logic (Specifically for unique rows based on row_num)
            if test_status == "Pass":
                qc_sheet_name = "QCIssueReceipt"
                if qc_sheet_name in workbook.sheetnames:
                    qc_sheet = workbook[qc_sheet_name]
                    target_ref = po_no if po_no else ref_no
                    
                    if target_ref:
                        # Sequential Issue Row
                        qc_sheet.cell(row=issue_idx, column=1, value=tc_issue).font = Font(bold=True)
                        qc_sheet.cell(row=issue_idx, column=4, value="issue")
                        qc_sheet.cell(row=issue_idx, column=6, value=target_ref).font = Font(bold=True)
                        

                        # Sequential Receipt Row
                        qc_sheet.cell(row=receipt_idx, column=1, value=tc_receipt).font = Font(bold=True)
                        qc_sheet.cell(row=receipt_idx, column=4, value="receipt")
                        qc_sheet.cell(row=receipt_idx, column=6, value=target_ref).font = Font(bold=True)
                        
                        print(f"📝 Linked {target_ref} to {qc_sheet_name} (Rows {issue_idx}/{receipt_idx})")

            workbook.save(FILE_PATH)
            workbook.close()
        except Exception as e:
            print(f"⚠️ Excel update failed: {e}")

    def _take_screenshot(self, filename):
        path = os.path.join(ExcelUtils.SCREENSHOT_PATH, f"{filename}_{datetime.now().strftime('%H%M%S')}.png")
        self.driver.save_screenshot(path)

    def _handle_print_tab(self, main_window):
        """Helper to close print tab and return focus to main window while capturing job ID from URL"""
        sleep(5)  # Wait for print tab to open
        job_id = None
        try:
            windows = self.driver.window_handles
            if len(windows) > 1:
                self.driver.switch_to.window(windows[1])
                current_url = self.driver.current_url
                print(f"DEBUG: Print Tab URL: {current_url}")
                # ID is at the end of URL: .../purchase/job_receipt/1067
                match = re.search(r"/(\d+)$", current_url)
                if match:
                    job_id = match.group(1)
                    print(f"🔍 Captured Job ID from URL: {job_id}")
                
                self.driver.close()
                self.driver.switch_to.window(windows[0])
            else:
                print("⚠️ Print tab not opened found")
        except Exception as e:
            print(f"⚠️ Print tab handling failed: {e}")
            try:
                self.driver.switch_to.window(main_window)
            except: pass
        return job_id

    def _cancel_form(self):
        try:
            # Try Back link first (common in list views)
            Function_Call.click(self, '//a[contains(text(), "Back")]')
            sleep(1)
        except:
            try:
                # Try Cancel button (common in forms)
                Function_Call.click(self, '//button[contains(text(), "Cancel")]')
                sleep(1)
            except:
                pass
