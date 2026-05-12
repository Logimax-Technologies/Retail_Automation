import pandas as pd
import os
import re
import json
import datetime
from Utils.Excel import ExcelUtils

# Module folder mapping
MODULE_FOLDER_MAP = {
    "Login": "Test_login",
    "Metal": "Test_master",
    "CategoryName": "Test_master",
    "Product": "Test_master",
    "Design": "Test_master",
    "SubDesign": "Test_master",
    "Designmapping": "Test_master",
    "Subdesignmapping": "Test_master",
    "MC&VA": "Test_master",
    "StoneRateSettings": "Test_master",
    "Lot": "Test_lot",
    "LotGenerate": "Test_lot",
    "Tag": "Test_Tag",
    "LotGenerateTag": "Test_Tag",
    "Vendor": "Test_vendor",
    "VendorApproval": "Test_vendor",
    "CustomerOrder": "Test_Customer",
    "CustomerOrderKarigarAllotment": "Test_Customer",
    "EST": "Test_EST",
    "Billing": "Test_Bill",
    "BillingIssue": "Test_Bill",
    "BillingReceipt": "Test_Bill",
    "BillingDenomination": "Test_Bill",
    "JewelNotDelivered": "Test_Bill",
    "BillSplit": "Test_Bill",
    "SearchBill": "Test_Bill",
    "PurchasePO": "Test_Purchase",
    "GRNEntry": "Test_Purchase",
    "SupplierBillEntry": "Test_Purchase",
    "HMIssueReceipt": "Test_Purchase",
    "QCIssueReceipt": "Test_Purchase",
    "PurchaseReturn": "Test_Purchase",
    "SmithSupplierPayment": "Test_Purchase",
    "DebitCreditEntry": "Test_Purchase",
    "SmithMetalIssue": "Test_Purchase",
    "RateFixGST": "Test_Purchase",
    "SmithCompanyOpBal": "Test_Purchase",
    "ApprovalRateFixing": "Test_Purchase",
    "ApprovalToInvoice": "Test_Purchase",
    "OldMetalProcess": "Test_OldMetalProcess",
    "StockIssue": "Test_StockIssue",
    "RepairOrder": "Test_RepairOrder",
    "KarigarAllotment": "Test_RepairOrder",
    "RepairOrderStatus": "Test_RepairOrder",
    "BranchTransfer": "Test_Inventory",
    "BranchTransferApproval": "Test_Inventory",
    "OrderLink": "Test_Inventory",
    "TagUnlink": "Test_Inventory",
    "NonTagReceipt": "Test_Inventory",
    "SectionTransfer": "Test_SectionTransfer",
    "InventoryCategory": "Test_OtherInventory",
    "PackagingItemSize": "Test_OtherInventory",
    "OtherInventory": "Test_OtherInventory",
    "ProductMapping": "Test_OtherInventory",
    "ProductPurchaseEntry": "Test_OtherInventory",
    "PackagingItemIssue": "Test_OtherInventory",
    "OtherInventoryTagging": "Test_OtherInventory",
}

FOLDER_DISPLAY_NAMES = {
    "Test_login": "Login & Authentication",
    "Test_master": "Master Data Management",
    "Test_lot": "Lot Management",
    "Test_Tag": "Tagging",
    "Test_vendor": "Vendor Management",
    "Test_Customer": "Customer Order Management",
    "Test_EST": "Estimation",
    "Test_Bill": "Billing & Receipts",
    "Test_Purchase": "Purchase Management",
    "Test_OldMetalProcess": "Old Metal Process",
    "Test_StockIssue": "Stock Issue",
    "Test_RepairOrder": "Repair Order",
    "Test_Inventory": "Inventory Management",
    "Test_SectionTransfer": "Section Transfer",
    "Test_OtherInventory": "Other Inventory",
}


def generate_test_doc():
    file_path = ExcelUtils.file_path
    output_path = os.path.join("Reports", "Test_Coverage_Document.html")
    os.makedirs("Reports", exist_ok=True)

    try:
        master_df = pd.read_excel(file_path, sheet_name="Master")
    except Exception as e:
        print(f"Error reading Master sheet: {e}")
        return

    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names

    # Build data grouped by folder
    folder_data = {}
    total_tc = 0
    total_pass = 0
    total_fail = 0

    for _, row in master_df.iterrows():
        func = str(row.get("Function", "")).strip()
        if not func or func == "nan":
            continue

        folder = MODULE_FOLDER_MAP.get(func, "Other")
        folder_label = FOLDER_DISPLAY_NAMES.get(folder, folder)

        if folder_label not in folder_data:
            folder_data[folder_label] = {"modules": {}, "folder_key": folder}

        tc_list = []
        if func in sheet_names:
            try:
                df = pd.read_excel(file_path, sheet_name=func)
                for _, r in df.iterrows():
                    tc_id = str(r.iloc[0]) if len(r) > 0 and pd.notna(r.iloc[0]) else None
                    if not tc_id or tc_id == "nan":
                        continue
                    status = str(r.iloc[1]).strip() if len(r) > 1 and pd.notna(r.iloc[1]) else "Pending"
                    remarks = str(r.iloc[2]).strip() if len(r) > 2 and pd.notna(r.iloc[2]) else ""
                    sc = "pass" if status.lower() == "pass" else ("fail" if status.lower() == "fail" else "pending")
                    tc_list.append({"id": tc_id, "status": status, "sc": sc, "remarks": remarks})
                    total_tc += 1
                    if sc == "pass": total_pass += 1
                    elif sc == "fail": total_fail += 1
            except Exception as e:
                print(f"Error reading {func}: {e}")

        folder_data[folder_label]["modules"][func] = tc_list

    coverage_pct = round((total_pass / total_tc * 100) if total_tc > 0 else 0, 1)
    now = datetime.datetime.now().strftime("%B %d, %Y — %H:%M")

    # Build module accordion HTML
    accordion_html = ""
    for folder_label, folder_info in folder_data.items():
        folder_pass = sum(tc["sc"] == "pass" for m in folder_info["modules"].values() for tc in m)
        folder_total = sum(len(m) for m in folder_info["modules"].values())
        folder_pct = round(folder_pass / folder_total * 100, 1) if folder_total > 0 else 0

        modules_html = ""
        for mod_name, tc_list in folder_info["modules"].items():
            m_pass = sum(1 for t in tc_list if t["sc"] == "pass")
            m_fail = sum(1 for t in tc_list if t["sc"] == "fail")
            rows = ""
            for i, tc in enumerate(tc_list, 1):
                rows += f"""<tr>
                    <td class="num">{i}</td>
                    <td class="tcid">{tc['id']}</td>
                    <td><span class="badge {tc['sc']}">{tc['status']}</span></td>
                    <td class="rmk">{tc['remarks'][:120] + '…' if len(tc['remarks']) > 120 else tc['remarks']}</td>
                </tr>"""

            modules_html += f"""
            <div class="module-block">
                <div class="module-header">
                    <div class="mod-left">
                        <span class="mod-icon">⚙</span>
                        <span class="mod-name">{mod_name}</span>
                        <span class="mod-count">{len(tc_list)} test cases</span>
                    </div>
                    <div class="mod-stats">
                        <span class="ms pass">✔ {m_pass}</span>
                        <span class="ms fail">✘ {m_fail}</span>
                    </div>
                </div>
                {'<table class="tc-table"><thead><tr><th>#</th><th>Test Case ID</th><th>Status</th><th>Remarks</th></tr></thead><tbody>' + rows + '</tbody></table>' if tc_list else '<p class="no-tc">No test cases recorded for this module yet.</p>'}
            </div>"""

        bar_color = "#10b981" if folder_pct >= 80 else ("#f59e0b" if folder_pct >= 50 else "#f43f5e")
        accordion_html += f"""
        <div class="folder-block">
            <div class="folder-header" onclick="toggleFolder(this)">
                <div class="fh-left">
                    <span class="folder-icon">📁</span>
                    <span class="folder-name">{folder_label}</span>
                    <span class="folder-mods">{len(folder_info['modules'])} modules · {folder_total} test cases</span>
                </div>
                <div class="fh-right">
                    <div class="prog-wrap">
                        <div class="prog-bar" style="width:{folder_pct}%; background:{bar_color};"></div>
                    </div>
                    <span class="prog-label" style="color:{bar_color};">{folder_pct}%</span>
                    <span class="chevron">▾</span>
                </div>
            </div>
            <div class="folder-body">
                {modules_html}
            </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Automation Test Coverage Document</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Inter',sans-serif;}}
body{{background:#f0f2f7;color:#1e293b;min-height:100vh;}}

/* TOP HEADER */
.doc-header{{background:linear-gradient(135deg,#1e1b4b 0%,#312e81 50%,#4338ca 100%);color:white;padding:50px 60px;position:relative;overflow:hidden;}}
.doc-header::after{{content:'';position:absolute;right:-80px;top:-80px;width:350px;height:350px;border-radius:50%;background:rgba(255,255,255,0.05);}}
.doc-header h1{{font-size:2.2rem;font-weight:700;letter-spacing:-0.5px;}}
.doc-header p{{color:rgba(255,255,255,0.7);margin-top:8px;font-size:0.95rem;}}
.doc-meta{{display:flex;gap:30px;margin-top:30px;flex-wrap:wrap;}}
.meta-item{{background:rgba(255,255,255,0.1);padding:12px 20px;border-radius:10px;border:1px solid rgba(255,255,255,0.15);}}
.meta-item .label{{font-size:0.75rem;color:rgba(255,255,255,0.6);text-transform:uppercase;letter-spacing:1px;}}
.meta-item .val{{font-size:1.5rem;font-weight:700;margin-top:4px;}}
.meta-item .val.green{{color:#34d399;}}
.meta-item .val.red{{color:#fb7185;}}

/* SUMMARY STRIP */
.summary-strip{{background:white;padding:25px 60px;border-bottom:1px solid #e2e8f0;display:flex;align-items:center;gap:40px;flex-wrap:wrap;box-shadow:0 1px 3px rgba(0,0,0,0.05);}}
.strip-label{{font-size:0.85rem;color:#64748b;font-weight:500;}}
.progress-outer{{flex:1;min-width:200px;background:#e2e8f0;border-radius:99px;height:12px;overflow:hidden;}}
.progress-inner{{height:100%;border-radius:99px;background:linear-gradient(90deg,#10b981,#059669);transition:width 0.5s;}}
.pct-big{{font-size:1.8rem;font-weight:700;color:#059669;}}

/* MAIN CONTENT */
.content{{max-width:1200px;margin:0 auto;padding:40px 30px;}}
.section-title{{font-size:1.1rem;font-weight:600;color:#374151;margin-bottom:20px;padding-bottom:10px;border-bottom:2px solid #e5e7eb;display:flex;align-items:center;gap:8px;}}

/* FOLDER ACCORDION */
.folder-block{{background:white;border-radius:14px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,0.06);overflow:hidden;border:1px solid #e5e7eb;}}
.folder-header{{padding:20px 25px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;transition:background 0.2s;user-select:none;}}
.folder-header:hover{{background:#f8fafc;}}
.fh-left{{display:flex;align-items:center;gap:12px;}}
.folder-icon{{font-size:1.3rem;}}
.folder-name{{font-weight:600;font-size:1rem;color:#1e293b;}}
.folder-mods{{font-size:0.8rem;color:#94a3b8;margin-left:6px;background:#f1f5f9;padding:3px 10px;border-radius:99px;}}
.fh-right{{display:flex;align-items:center;gap:14px;}}
.prog-wrap{{width:100px;height:8px;background:#e5e7eb;border-radius:99px;overflow:hidden;}}
.prog-bar{{height:100%;border-radius:99px;transition:width 0.4s;}}
.prog-label{{font-size:0.85rem;font-weight:600;min-width:38px;text-align:right;}}
.chevron{{font-size:1.2rem;color:#94a3b8;transition:transform 0.3s;}}
.folder-header.open .chevron{{transform:rotate(180deg);}}
.folder-body{{display:none;padding:0 25px 20px;border-top:1px solid #f1f5f9;}}
.folder-body.open{{display:block;}}

/* MODULE BLOCK */
.module-block{{margin-top:16px;background:#f8fafc;border-radius:10px;border:1px solid #e2e8f0;overflow:hidden;}}
.module-header{{padding:14px 18px;display:flex;justify-content:space-between;align-items:center;background:#f1f5f9;}}
.mod-left{{display:flex;align-items:center;gap:10px;}}
.mod-icon{{color:#6366f1;}}
.mod-name{{font-weight:600;color:#334155;font-size:0.95rem;}}
.mod-count{{font-size:0.78rem;color:#94a3b8;margin-left:4px;}}
.mod-stats{{display:flex;gap:10px;}}
.ms{{font-size:0.82rem;font-weight:600;padding:3px 10px;border-radius:99px;}}
.ms.pass{{background:#dcfce7;color:#15803d;}}
.ms.fail{{background:#fee2e2;color:#b91c1c;}}

/* TABLE */
.tc-table{{width:100%;border-collapse:collapse;font-size:0.88rem;}}
.tc-table th{{background:#e8edf5;padding:10px 14px;text-align:left;font-weight:600;color:#475569;font-size:0.78rem;text-transform:uppercase;}}
.tc-table td{{padding:10px 14px;border-bottom:1px solid #f1f5f9;vertical-align:middle;}}
.tc-table tr:last-child td{{border-bottom:none;}}
.tc-table tr:hover td{{background:#f8fafc;}}
.num{{color:#94a3b8;font-size:0.82rem;width:40px;}}
.tcid{{font-weight:600;color:#334155;width:140px;}}
.rmk{{color:#64748b;}}

/* BADGES */
.badge{{display:inline-flex;align-items:center;gap:5px;padding:4px 12px;border-radius:99px;font-size:0.78rem;font-weight:600;text-transform:uppercase;}}
.badge.pass{{background:#dcfce7;color:#15803d;}}
.badge.fail{{background:#fee2e2;color:#b91c1c;}}
.badge.pending{{background:#fef9c3;color:#a16207;}}
.no-tc{{padding:16px;color:#94a3b8;font-size:0.88rem;font-style:italic;}}

/* FOOTER */
.footer{{text-align:center;padding:30px;color:#94a3b8;font-size:0.82rem;}}
</style>
</head>
<body>

<div class="doc-header">
    <h1>📋 Automation Test Coverage Document</h1>
    <p>Module-wise test case coverage report for management review</p>
    <div class="doc-meta">
        <div class="meta-item"><div class="label">Generated On</div><div class="val" style="font-size:1rem;">{now}</div></div>
        <div class="meta-item"><div class="label">Total Test Cases</div><div class="val">{total_tc}</div></div>
        <div class="meta-item"><div class="label">Passed</div><div class="val green">{total_pass}</div></div>
        <div class="meta-item"><div class="label">Failed</div><div class="val red">{total_fail}</div></div>
        <div class="meta-item"><div class="label">Total Modules</div><div class="val">{sum(len(v['modules']) for v in folder_data.values())}</div></div>
        <div class="meta-item"><div class="label">Folders Covered</div><div class="val">{len(folder_data)}</div></div>
    </div>
</div>

<div class="summary-strip">
    <span class="pct-big">{coverage_pct}%</span>
    <span class="strip-label">Overall Pass Rate</span>
    <div class="progress-outer">
        <div class="progress-inner" style="width:{coverage_pct}%;"></div>
    </div>
</div>

<div class="content">
    <div class="section-title">📂 Module-wise Test Coverage</div>
    {accordion_html}
</div>

<div class="footer">Retail Automation QA — Test Coverage Document · Auto-generated by the Sparqla QA Framework</div>

<script>
function toggleFolder(header) {{
    header.classList.toggle('open');
    const body = header.nextElementSibling;
    body.classList.toggle('open');
}}
// Open first folder by default
document.addEventListener('DOMContentLoaded', () => {{
    const first = document.querySelector('.folder-header');
    if (first) toggleFolder(first);
}});
</script>
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Test Coverage Document generated: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    generate_test_doc()
