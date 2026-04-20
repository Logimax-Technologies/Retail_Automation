from selenium import webdriver
from Utils.Excel import ExcelUtils
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from Test_login.Login import Login
from Test_master.Metal import Metal
from Test_master.Category import Category
from Test_master.Product import Product
from Test_master.Design import Design
from Test_master.Subdesign import Subdesign
from Test_master.Designmapping import Designmapping
from Test_master.Subdesignmapping import Subdesignmapping
from Test_Bill.Bill import Billing
from Test_Purchase.PurchasePO import PurchasePO
from Test_Bill.BillingIssue import BillingIssue
from Test_Purchase.GRNEntry import GRNEntry
from Test_Purchase.SupplierBillEntry import SupplierBillEntry
from Test_Purchase.HMIssueReceipt import HMIssueReceipt
from Test_Purchase.QCIssueReceipt import QCIssueReceipt
from Test_master.MCVA import McVa
from Test_lot.Lot import Lot
from Test_lot.LotGenerate import LotGenerate
from Test_Tag.Tag import Tag
from Test_vendor.Vendor import VendorRegistration
# from Test_Customer.Customer import CustomerOrderTR
from Test_Customer.CustomerOrder import CustomerOrder   
from Test_EST.EST import ESTIMATION
from Test_Purchase.PurchaseReturn import PurchaseReturn
from Test_Purchase.SmithSupplierPayment import SmithSupplierPayment
from Test_Purchase.DebitCreditEntry import DebitCreditEntry
from Test_Purchase.SmithMetalIssue import SmithMetalIssue
from Test_Purchase.RateFixGSTPurchase import RateFixGSTPurchase
from Test_vendor.VendorApproval import VendorApproval
from Test_Purchase.ApprovalRateFixing import ApprovalRateFixing
from Test_Bill.SearchBill import SearchBill
from Test_Purchase.SmithCompanyOpBal import SmithCompanyOpBal
from Test_Purchase.ApprovalToInvoice import ApprovalToInvoice
from Test_Bill.BillingReceipt import BillingReceipt
from Test_Bill.BillingDenomination import BillingDenomination
from Test_Bill.JewelNotDelivered import JewelNotDelivered
from Test_Bill.BillSplit import BillSplit
from Test_OldMetalProcess.OldMetalProcess import OldMetalProcess
from Test_StockIssue.StockIssue import StockIssue
from Test_RepairOrder.RepairOrder import RepairOrder
from Test_RepairOrder.KarigarAllotment import KarigarAllotment
from Test_RepairOrder.RepairOrderStatus import RepairOrderStatus
from Test_Inventory.BranchTransfer import BranchTransfer
from Test_Inventory.BranchTransferApproval import BranchTransferApproval
from Test_Inventory.OrderLink import OrderLink
from Test_Inventory.TagUnlink import TagUnlink
from Test_SectionTransfer.SectionTransfer import SectionTransfer
from Test_master.StoneRateSettings import StoneRateSettings
from Test_Customer.KarigarAllotment import CustomerOrderKarigarAllotment
from Test_Inventory.NonTagReceipt import NonTagReceipt
from Test_OtherInventory.InventoryCategory import InventoryCategory
from Test_OtherInventory.PackagingItemSize import PackagingItemSize
from Test_OtherInventory.OtherInventory import OtherInventory
from Test_OtherInventory.ProductMapping import ProductMapping
from Test_OtherInventory.ProductPurchaseEntry import ProductPurchaseEntry
from Test_OtherInventory.PackagingItemIssue import PackagingItemIssue
from Test_OtherInventory.OtherInventoryTagging import OtherInventoryTagging
import datetime
import os
import shutil

def create_driver():
    """Create Chrome driver. Headless when running inside Jenkins."""
    options = Options()
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Block camera popup
    options.add_argument("--use-fake-device-for-media-stream")
    options.add_argument("--use-fake-ui-for-media-stream")
    # Auto-dismiss native print dialog (prevents blocking on print popup)
    options.add_argument("--kiosk-printing")

    options.add_argument("--remote-allow-origins=*")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Enable performance logging to capture WebSocket/Network frames (for Socket.IO response parsing)
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.maximize_window()
    return driver

class main():
    @staticmethod
    def main():
        # Step 0: Clear screenshots folder
        if os.path.exists(ExcelUtils.SCREENSHOT_PATH):
            shutil.rmtree(ExcelUtils.SCREENSHOT_PATH)
        os.makedirs(ExcelUtils.SCREENSHOT_PATH, exist_ok=True)

        # ExcelUtils.ensure_copy_exists()
        FILE_PATH = ExcelUtils.file_path
        # Step 1: Initialize WebDriver
        ExcelUtils.ExcelClose(FILE_PATH)
        ct1 = datetime.datetime.now()
        print('Automation process Started',ct1)

        driver = create_driver()
        # options = Options()
        # options.add_argument("--log-level=3")
        
        
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # # Block camera popup
        # options.add_argument("--use-fake-device-for-media-stream")
        # options.add_argument("--use-fake-ui-for-media-stream")

        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # driver.maximize_window()
        # options = Options()
        try:
            sheet_names = ExcelUtils.get_sheet_names(FILE_PATH)
            print(sheet_names)
            # Step 2: Get functions to execute from the Master sheet
            functions_to_execute = ExcelUtils.get_master_sheet_data(FILE_PATH)
            print(functions_to_execute)
        
            for function_name in functions_to_execute:
                print("funct",function_name)
                if function_name in sheet_names:
                    print("sheet",sheet_names)
                    # Initialize LoginAutomation
                    match function_name:
                        case "Login":
                            print("yes")
                            login_automation = Login(driver)
                            Data = login_automation.test_login()
                        case "Metal":
                            print("yes")
                            Metal_automation = Metal(driver)
                            Data = Metal_automation.test_metal()
                        case "CategoryName":
                            print("yes")
                            Category_automation = Category(driver)
                            Data = Category_automation.test_category()    
                        case "Product":
                            print("yes")
                            Product_automation =Product(driver)
                            Data = Product_automation.test_product()
                        case "Design":
                            print("yes")
                            Design_automation =Design(driver)
                            Data = Design_automation.test_design()
                        case "SubDesign":
                            print("yes")
                            Subdesign_automation =Subdesign(driver)
                            Data = Subdesign_automation.test_subdesign()  
                        case "Designmapping":
                            print("yes")
                            designmap_automation =Designmapping(driver)
                            Data = designmap_automation.test_designmapping()      
                        case "Subdesignmapping":
                            print("yes")
                            Subdesignmap_automation =Subdesignmapping(driver)
                            Data = Subdesignmap_automation.test_subdesignmapping()
                        case "MC&VA":
                            print("yes")
                            McVa_automation =McVa(driver)
                            Data = McVa_automation.test_mc_va()    
                        case "Lot":                            
                            print("yes")
                            lot_automation = Lot(driver)
                            Data = lot_automation.test_lot()
                        case "Tag":
                            print("yes")
                            Tag_automation = Tag(driver)
                            Data = Tag_automation.test_tag(Sheet_name="Tag")
                        case "Vendor":
                            print("yes")
                            Vendor_automation = VendorRegistration(driver) 
                            Data = Vendor_automation.test_vendor_registration()
                        case "CustomerOrder":
                            print("yes")
                            Vendor_automation = CustomerOrder(driver)
                            Data = Vendor_automation.test_customer_order()  
                        case "EST":
                            print("yes")
                            EST = ESTIMATION(driver)
                            Data = EST.test_estimation() 
                        case "Billing":
                            print("yes")
                            Bill = Billing(driver)
                            Data = Bill.test_Billing()
                        case "PurchasePO":
                            print("yes")
                            PurchasePO_automation = PurchasePO(driver)
                            Data = PurchasePO_automation.test_purchase_po()
                        case "GRNEntry":
                            print("yes")
                            GRNEntry_automation = GRNEntry(driver)
                            Data = GRNEntry_automation.test_grn_entry()
                        case "SupplierBillEntry":
                            print("yes")
                            SupplierBill_automation = SupplierBillEntry(driver)
                            Data = SupplierBill_automation.test_supplier_bill_entry()
                        case "HMIssueReceipt":
                            print("yes")
                            HMIssueReceipt_automation = HMIssueReceipt(driver)
                            Data = HMIssueReceipt_automation.test_hm_issue_receipt()
                        case "QCIssueReceipt":
                            print("yes")
                            QCIssueReceipt_automation = QCIssueReceipt(driver)
                            Data = QCIssueReceipt_automation.test_qc_issue_receipt()
                        case "LotGenerate":
                            print("yes")
                            LotGenerate_automation = LotGenerate(driver)
                            Data = LotGenerate_automation.test_lot_generate()
                        case "PurchaseReturn":
                            print("yes")
                            PurchaseReturn_automation = PurchaseReturn(driver)
                            Data = PurchaseReturn_automation.test_purchase_return()
                        case "SmithSupplierPayment":
                            print("yes")
                            SmithSupplierPayment_automation = SmithSupplierPayment(driver)
                            Data = SmithSupplierPayment_automation.test_smith_supplier_payment()
                        case "DebitCreditEntry":
                            print("yes")
                            DebitCreditEntry_automation = DebitCreditEntry(driver)
                            Data = DebitCreditEntry_automation.test_debit_credit_entry()
                        case "SmithMetalIssue":
                            print("yes")
                            SmithMetalIssue_automation = SmithMetalIssue(driver)
                            Data = SmithMetalIssue_automation.test_smith_metal_issue()
                        case "RateFixGST":
                            print("yes")
                            RateFix_automation = RateFixGSTPurchase(driver)
                            Data = RateFix_automation.test_rate_fix_gst_purchase()
                        case "VendorApproval":
                            print("yes")
                            VendorApproval_automation = VendorApproval(driver)
                            Data = VendorApproval_automation.test_vendor_approval()
                        case "ApprovalRateFixing":
                            print("yes")
                            ApprovalRateFix_automation = ApprovalRateFixing(driver)
                            Data = ApprovalRateFix_automation.test_approval_rate_fixing()
                        case "SearchBill":
                            print("yes")
                            SearchBill_automation = SearchBill(driver)
                            Data = SearchBill_automation.test_search_bill()
                        case "SmithCompanyOpBal":
                            print("yes")
                            SmithCompanyOpBal_automation = SmithCompanyOpBal(driver)
                            Data = SmithCompanyOpBal_automation.test_smith_company_op_bal()
                        case "ApprovalToInvoice":
                            print("yes")
                            ApprovalToInvoice_automation = ApprovalToInvoice(driver)
                            Data = ApprovalToInvoice_automation.test_approval_to_invoice()
                        case "BillingIssue":
                            print("yes")
                            BillingIssue_automation = BillingIssue(driver)
                            Data = BillingIssue_automation.test_billing_issue()
                        case "BillingReceipt":
                            print("yes")
                            BillingReceipt_automation = BillingReceipt(driver)
                            Data = BillingReceipt_automation.test_billing_receipt()
                        case "BillingDenomination":
                            print("yes")
                            BD_automation = BillingDenomination(driver)
                            Data = BD_automation.test_cash_collection()
                        case "JewelNotDelivered":
                            print("yes")
                            JND_automation = JewelNotDelivered(driver)
                            Data = JND_automation.test_item_delivery()
                        case "BillSplit":
                            print("yes")
                            BS_automation = BillSplit(driver)
                            Data = BS_automation.test_bill_split()
                        case "OldMetalProcess":
                            print("yes")
                            OMP_automation = OldMetalProcess(driver)
                            Data = OMP_automation.test_old_metal_process()
                        case "StockIssue":
                            print("yes")
                            SI_automation = StockIssue(driver)
                            Data = SI_automation.test_stock_issue()
                        case "RepairOrder":
                            print("yes")
                            RO_automation = RepairOrder(driver)
                            Data = RO_automation.test_repair_order()
                        case "KarigarAllotment":
                            print("yes")
                            KA_automation = KarigarAllotment(driver)
                            Data = KA_automation.test_karigar_allotment()
                        case "RepairOrderStatus":
                            print("yes")
                            ROS_automation = RepairOrderStatus(driver)
                            Data = ROS_automation.test_repair_order_status()
                        case "BranchTransfer":
                            print("yes")
                            BT_automation = BranchTransfer(driver)
                            Data = BT_automation.test_branch_transfer()
                        case "BranchTransferApproval":
                            print("yes")
                            BTApp_automation = BranchTransferApproval(driver)
                            Data = BTApp_automation.test_branch_transfer_approval()
                        case "OrderLink":
                            print("yes")
                            OLRef = OrderLink(driver)
                            Data = OLRef.test_order_link()
                        case "TagUnlink":
                            print("yes")
                            TU_auto = TagUnlink(driver)
                            Data = TU_auto.test_tag_unlink()
                        case "SectionTransfer":
                            print("yes")
                            ST_auto = SectionTransfer(driver)
                            Data = ST_auto.test_section_transfer()
                        case "StoneRateSettings":
                            print("yes")
                            SRS_auto = StoneRateSettings(driver)
                            Data = SRS_auto.test_stone_rate_settings()
                        case "CustomerOrderKarigarAllotment":
                            print("yes")
                            COKA_auto = CustomerOrderKarigarAllotment(driver)
                            Data = COKA_auto.test_customer_order_allotment()
                        case "NonTagReceipt":
                            print("yes")
                            NTR_auto = NonTagReceipt(driver)
                            Data = NTR_auto.test_non_tag_receipt()
                        case "InventoryCategory":
                            print("yes")
                            IC_auto = InventoryCategory(driver)
                            Data = IC_auto.test_inventory_category()
                        case "PackagingItemSize":
                            print("yes")
                            PIS_auto = PackagingItemSize(driver)
                            Data = PIS_auto.test_packaging_item_size()
                        case "OtherInventory":
                            print("yes")
                            OI_auto = OtherInventory(driver)
                            Data = OI_auto.test_other_inventory()
                        case "ProductMapping":
                            print("yes")
                            PM_auto = ProductMapping(driver)
                            Data = PM_auto.test_product_mapping()
                        case "ProductPurchaseEntry":
                            print("yes")
                            PPE_auto = ProductPurchaseEntry(driver)
                            Data = PPE_auto.test_product_purchase_entry()
                        case "PackagingItemIssue":
                            print("yes")
                            PII_auto = PackagingItemIssue(driver)
                            Data = PII_auto.test_packaging_item_issue()
                        case "OtherInventoryTagging":
                            print("yes")
                            OIT_auto = OtherInventoryTagging(driver)
                            Data = OIT_auto.test_other_inventory_tagging()
                        case "LotGenerateTag":
                            print("yes")
                            LotGenerateTag_auto = Tag(driver)
                            Data = LotGenerateTag_auto.test_tag(Sheet_name="LotGenerateTag")

                else:
                    print("Invalid option")
        finally:
            # Close the WebDriver
            try:
                driver.quit()
            except:
                pass

            ct2 = datetime.datetime.now()
            print('Automation process completed',ct2)
            time_diff = ct2 - ct1  
            print("ct1 =", ct1.strftime("%Y-%m-%d %H:%M:%S.%f"))  # Format output
            print("ct2 =", ct2.strftime("%Y-%m-%d %H:%M:%S.%f"))  
            print("Time difference =", time_diff) 

    if __name__ == "__main__":
        print(__name__)
        main()
        
        




