import pandas as pd
import os
import re
import datetime
from openpyxl import load_workbook

# Update this import if the path is different, assuming this is run from Sparqla directory
from Utils.Excel import ExcelUtils

def generate_html_report():
    file_path = ExcelUtils.file_path
    screenshots_dir = ExcelUtils.SCREENSHOT_PATH
    output_html_path = os.path.join("Reports", "Execution_Report.html")

    print(f"Generating HTML report from {file_path}...")
    
    # Ensure Reports dir exists
    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

    # 1. Read Master sheet to get executed modules
    try:
        master_df = pd.read_excel(file_path, sheet_name="Master")
    except Exception as e:
        print(f"Failed to read Master sheet: {e}")
        return

    executed_modules = []
    for index, row in master_df.iterrows():
        if pd.notna(row.get("Execution")) and re.match(r"yes", str(row["Execution"]), re.IGNORECASE):
            func_name = str(row.get("Function")).strip()
            executed_modules.append(func_name)

    # 2. Gather data for each module
    all_data = {}
    total_pass = 0
    total_fail = 0
    total_cases = 0

    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names

    for module in executed_modules:
        if module in sheet_names:
            try:
                # Read the sheet for the module
                df = pd.read_excel(file_path, sheet_name=module)
                module_data = []
                
                # In the test scripts, data is written starting from row 2
                # df.columns will represent row 1 headers.
                # Assuming standard format: Col 0: Test Case Id, Col 1: Status, Col 2: Message/Remarks
                # We'll use positional indexing just in case headers differ.
                for idx, row in df.iterrows():
                    tc_id = str(row.iloc[0]) if len(row) > 0 and pd.notna(row.iloc[0]) else None
                    if not tc_id or tc_id == "nan" or tc_id.strip() == "":
                        continue # Skip empty rows
                        
                    status = str(row.iloc[1]).strip() if len(row) > 1 and pd.notna(row.iloc[1]) else "Pending/Unknown"
                    remarks = str(row.iloc[2]).strip() if len(row) > 2 and pd.notna(row.iloc[2]) else ""
                    
                    # Check for screenshot
                    screenshot_name = f"{tc_id}.png"
                    screenshot_path = os.path.join(screenshots_dir, screenshot_name)
                    has_screenshot = os.path.exists(screenshot_path)
                    
                    # Convert to relative path for HTML
                    rel_screenshot_path = f"screenshots/{screenshot_name}" if has_screenshot else ""

                    # Normalize status
                    if status.lower() == "pass":
                        total_pass += 1
                        status_class = "pass"
                    elif status.lower() == "fail":
                        total_fail += 1
                        status_class = "fail"
                    else:
                        status_class = "unknown"

                    total_cases += 1
                    
                    module_data.append({
                        "tc_id": tc_id,
                        "status": status,
                        "status_class": status_class,
                        "remarks": remarks,
                        "screenshot": rel_screenshot_path
                    })
                
                all_data[module] = module_data

            except Exception as e:
                print(f"Error reading sheet {module}: {e}")

    # 3. Generate HTML
    import json
    json_data = json.dumps(all_data)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Advanced Automation Report</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root {{
                --bg-main: #0f1015;
                --bg-panel: #1a1b23;
                --bg-card: #232531;
                --text-main: #f3f4f6;
                --text-muted: #9ca3af;
                --accent: #6366f1;
                --accent-hover: #4f46e5;
                --pass: #10b981;
                --fail: #f43f5e;
                --unknown: #f59e0b;
                --border: #2e303d;
            }}
            * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }}
            body {{ background-color: var(--bg-main); color: var(--text-main); display: flex; height: 100vh; overflow: hidden; }}
            
            /* Sidebar */
            .sidebar {{ width: 280px; background-color: var(--bg-panel); border-right: 1px solid var(--border); display: flex; flex-direction: column; z-index: 10; }}
            .sidebar-header {{ padding: 25px 20px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 10px; }}
            .sidebar-header h2 {{ font-size: 1.2rem; font-weight: 600; background: linear-gradient(90deg, #6366f1, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .module-list {{ flex: 1; overflow-y: auto; padding: 15px 10px; }}
            .module-item {{ padding: 12px 15px; margin-bottom: 5px; border-radius: 8px; cursor: pointer; transition: all 0.3s; display: flex; justify-content: space-between; align-items: center; color: var(--text-muted); font-size: 0.95rem; }}
            .module-item:hover {{ background-color: rgba(99, 102, 241, 0.1); color: var(--text-main); }}
            .module-item.active {{ background-color: var(--accent); color: white; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3); }}
            .module-badge {{ background: rgba(0,0,0,0.2); padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; }}

            /* Main Content */
            .main-content {{ flex: 1; display: flex; flex-direction: column; overflow-y: auto; overflow-x: hidden; position: relative; }}
            .main-content::before {{ content: ''; position: absolute; top: -100px; right: -100px; width: 300px; height: 300px; background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, rgba(0,0,0,0) 70%); border-radius: 50%; pointer-events: none; }}
            
            .header-bar {{ padding: 20px 30px; display: flex; justify-content: space-between; align-items: center; background: rgba(26, 27, 35, 0.8); backdrop-filter: blur(10px); border-bottom: 1px solid var(--border); z-index: 5; position: sticky; top: 0; }}
            .header-title h1 {{ font-size: 1.5rem; font-weight: 600; }}
            .timestamp {{ font-size: 0.85rem; color: var(--text-muted); margin-top: 5px; }}
            
            .dashboard-grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr 300px; gap: 20px; padding: 30px; }}
            .stat-card {{ background-color: var(--bg-panel); padding: 25px; border-radius: 16px; border: 1px solid var(--border); position: relative; overflow: hidden; transition: transform 0.3s; }}
            .stat-card:hover {{ transform: translateY(-5px); }}
            .stat-card::before {{ content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; }}
            .stat-card.total::before {{ background-color: var(--accent); }}
            .stat-card.pass::before {{ background-color: var(--pass); }}
            .stat-card.fail::before {{ background-color: var(--fail); }}
            
            .stat-title {{ font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; font-weight: 500; }}
            .stat-value {{ font-size: 2.5rem; font-weight: 700; margin-top: 10px; }}
            .stat-card.pass .stat-value {{ color: var(--pass); }}
            .stat-card.fail .stat-value {{ color: var(--fail); }}
            
            .chart-card {{ background-color: var(--bg-panel); border-radius: 16px; border: 1px solid var(--border); padding: 15px; display: flex; justify-content: center; align-items: center; grid-row: span 2; grid-column: 4; }}
            .chart-container {{ width: 100%; max-width: 200px; aspect-ratio: 1; }}

            /* Controls */
            .controls {{ display: flex; justify-content: space-between; padding: 0 30px 15px; }}
            .search-box {{ background: var(--bg-panel); border: 1px solid var(--border); padding: 10px 15px; border-radius: 8px; width: 300px; color: var(--text-main); font-family: 'Poppins', sans-serif; outline: none; transition: border-color 0.3s; }}
            .search-box:focus {{ border-color: var(--accent); }}

            /* Table Area */
            #tablesContainer {{ padding-bottom: 30px; }}
            .table-container {{ padding: 0 30px; display: none; }}
            .table-container.active {{ display: block; }}
            
            table {{ width: 100%; border-collapse: separate; border-spacing: 0 8px; table-layout: fixed; }}
            th {{ background-color: transparent; font-weight: 600; color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase; padding: 10px 20px; text-align: left; white-space: nowrap; }}
            th:nth-child(1) {{ width: 15%; }}
            th:nth-child(2) {{ width: 20%; }}
            th:nth-child(3) {{ width: 50%; }}
            th:nth-child(4) {{ width: 15%; }}
            
            tbody tr {{ background-color: var(--bg-panel); box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: all 0.2s; }}
            tbody tr:hover {{ transform: scale(1.005); background-color: var(--bg-card); }}
            td {{ padding: 15px 20px; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); vertical-align: middle; }}
            td:first-child {{ border-left: 1px solid var(--border); border-top-left-radius: 8px; border-bottom-left-radius: 8px; font-weight: 500; }}
            td:last-child {{ border-right: 1px solid var(--border); border-top-right-radius: 8px; border-bottom-right-radius: 8px; }}
            
            .remarks-content {{ max-height: 100px; overflow-y: auto; word-wrap: break-word; font-size: 0.9rem; line-height: 1.5; color: var(--text-muted); padding-right: 10px; }}
            
            .status-badge {{ padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; display: inline-flex; align-items: center; gap: 6px; }}
            .status-badge::before {{ content: ''; width: 8px; height: 8px; border-radius: 50%; }}
            .status-badge.pass {{ background-color: rgba(16, 185, 129, 0.1); color: var(--pass); }}
            .status-badge.pass::before {{ background-color: var(--pass); }}
            .status-badge.fail {{ background-color: rgba(244, 63, 94, 0.1); color: var(--fail); }}
            .status-badge.fail::before {{ background-color: var(--fail); }}
            .status-badge.unknown {{ background-color: rgba(245, 158, 11, 0.1); color: var(--unknown); }}
            .status-badge.unknown::before {{ background-color: var(--unknown); }}

            .screenshot-btn {{ background: transparent; border: 1px solid var(--accent); color: var(--accent); padding: 8px 16px; border-radius: 6px; cursor: pointer; transition: all 0.3s; font-size: 0.85rem; font-weight: 500; display: inline-flex; align-items: center; justify-content: center; gap: 8px; width: 100%; }}
            .screenshot-btn:hover {{ background: var(--accent); color: white; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4); }}
            
            /* Modal */
            .modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.9); backdrop-filter: blur(5px); justify-content: center; align-items: center; }}
            .modal.active {{ display: flex; animation: fadeIn 0.3s; }}
            @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
            .modal-content {{ position: relative; max-width: 95%; max-height: 95%; display: flex; flex-direction: column; align-items: center; }}
            .modal-content img {{ max-width: 100%; max-height: 85vh; border-radius: 12px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); object-fit: contain; }}
            .close-modal {{ position: absolute; top: -40px; right: 0; color: white; font-size: 35px; font-weight: 300; cursor: pointer; transition: color 0.2s; }}
            .close-modal:hover {{ color: var(--fail); }}
            
            /* Scrollbar */
            ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
            ::-webkit-scrollbar-track {{ background: var(--bg-main); border-radius: 4px; }}
            ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 4px; }}
            ::-webkit-scrollbar-thumb:hover {{ background: var(--text-muted); }}
            
            .remarks-content::-webkit-scrollbar {{ width: 4px; }}
            .remarks-content::-webkit-scrollbar-track {{ background: transparent; }}
            .remarks-content::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}
        </style>
    </head>
    <body>
        <div class="sidebar">
            <div class="sidebar-header">
                <h2>⚡ QA Analytics</h2>
            </div>
            <div class="module-list" id="moduleList">
                <!-- Modules injected via JS -->
            </div>
        </div>
        
        <div class="main-content">
            <div class="header-bar">
                <div class="header-title">
                    <h1>Test Execution Dashboard</h1>
                    <div class="timestamp">Report Generated: {datetime.datetime.now().strftime("%B %d, %Y - %H:%M:%S")}</div>
                </div>
            </div>
            
            <div class="dashboard-grid">
                <div class="stat-card total">
                    <div class="stat-title">Total Test Cases</div>
                    <div class="stat-value">{total_cases}</div>
                </div>
                <div class="stat-card pass">
                    <div class="stat-title">Passed Tests</div>
                    <div class="stat-value">{total_pass}</div>
                </div>
                <div class="stat-card fail">
                    <div class="stat-title">Failed Tests</div>
                    <div class="stat-value">{total_fail}</div>
                </div>
                <div class="chart-card">
                    <div class="chart-container">
                        <canvas id="statusChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="controls">
                <input type="text" id="searchInput" class="search-box" placeholder="Search Test Case ID or Remarks..." onkeyup="filterTable()">
            </div>

            <div id="tablesContainer"></div>
        </div>

        <div class="modal" id="imageModal">
            <div class="modal-content">
                <span class="close-modal" onclick="closeModal()">&times;</span>
                <img id="modalImg" src="" alt="Screenshot">
            </div>
        </div>

        <script>
            // Safely inject JSON data
            const reportData = {json_data};
            const totalPass = {total_pass};
            const totalFail = {total_fail};
            const totalCases = {total_cases};
        </script>
        
        <script>
            // Initialize Chart
            const ctx = document.getElementById('statusChart').getContext('2d');
            const unknownCount = totalCases - totalPass - totalFail;
            
            new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: ['Pass', 'Fail', 'Unknown'],
                    datasets: [{{
                        data: [totalPass, totalFail, unknownCount],
                        backgroundColor: ['#10b981', '#f43f5e', '#f59e0b'],
                        borderWidth: 0,
                        hoverOffset: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: true,
                    cutout: '75%',
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            backgroundColor: 'rgba(26, 27, 35, 0.9)',
                            titleFont: {{ family: 'Poppins' }},
                            bodyFont: {{ family: 'Poppins' }},
                            padding: 12,
                            cornerRadius: 8
                        }}
                    }}
                }}
            }});

            const moduleList = document.getElementById('moduleList');
            const tablesContainer = document.getElementById('tablesContainer');
            let isFirst = true;
            let currentModule = '';

            for (const [moduleName, testCases] of Object.entries(reportData)) {{
                // Sidebar Item
                const moduleItem = document.createElement('div');
                moduleItem.className = `module-item ${{isFirst ? 'active' : ''}}`;
                moduleItem.innerHTML = `<span>${{moduleName}}</span> <span class="module-badge">${{testCases.length}}</span>`;
                moduleItem.onclick = () => showModule(moduleName, moduleItem);
                moduleList.appendChild(moduleItem);

                // Table Container
                const tableContainer = document.createElement('div');
                tableContainer.className = `table-container ${{isFirst ? 'active' : ''}}`;
                tableContainer.id = `module-${{moduleName}}`;
                
                if (isFirst) currentModule = moduleName;

                let tableHTML = `
                    <table>
                        <thead>
                            <tr>
                                <th>Test Case ID</th>
                                <th>Execution Status</th>
                                <th>Remarks / Details</th>
                                <th style="text-align:center;">Screenshot</th>
                            </tr>
                        </thead>
                        <tbody id="tbody-${{moduleName}}">
                `;

                testCases.forEach(tc => {{
                    let screenshotHTML = '';
                    if (tc.screenshot) {{
                        screenshotHTML = `<button class="screenshot-btn" onclick="openModal('${{tc.screenshot}}')">
                            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg> View
                        </button>`;
                    }} else {{
                        screenshotHTML = '<span style="color: var(--text-muted); font-size: 0.85rem;">N/A</span>';
                    }}

                    tableHTML += `
                        <tr class="tc-row">
                            <td class="tc-id">${{tc.tc_id}}</td>
                            <td><span class="status-badge ${{tc.status_class}}">${{tc.status}}</span></td>
                            <td class="tc-remarks"><div class="remarks-content">${{tc.remarks}}</div></td>
                            <td style="text-align:center;">${{screenshotHTML}}</td>
                        </tr>
                    `;
                }});

                tableHTML += `
                        </tbody>
                    </table>
                `;
                tableContainer.innerHTML = tableHTML;
                tablesContainer.appendChild(tableContainer);

                isFirst = false;
            }}

            function showModule(moduleName, element) {{
                currentModule = moduleName;
                document.querySelectorAll('.module-item').forEach(el => el.classList.remove('active'));
                element.classList.add('active');

                document.querySelectorAll('.table-container').forEach(el => el.classList.remove('active'));
                document.getElementById(`module-${{moduleName}}`).classList.add('active');
                
                // Re-apply filter if exists
                filterTable();
            }}

            function filterTable() {{
                const input = document.getElementById('searchInput').value.toLowerCase();
                if (!currentModule) return;
                
                const rows = document.querySelectorAll(`#module-${{currentModule}} .tc-row`);
                rows.forEach(row => {{
                    const id = row.querySelector('.tc-id').innerText.toLowerCase();
                    const remarks = row.querySelector('.tc-remarks').innerText.toLowerCase();
                    
                    if (id.includes(input) || remarks.includes(input)) {{
                        row.style.display = '';
                    }} else {{
                        row.style.display = 'none';
                    }}
                }});
            }}

            // Modal logic
            const modal = document.getElementById('imageModal');
            const modalImg = document.getElementById('modalImg');

            function openModal(imgSrc) {{
                modalImg.src = imgSrc;
                modal.classList.add('active');
            }}

            function closeModal() {{
                modal.classList.remove('active');
            }}

            window.onclick = function(event) {{
                if (event.target == modal) {{
                    closeModal();
                }}
            }}
            
            // Allow Esc key to close modal
            document.addEventListener('keydown', function(event) {{
                if (event.key === "Escape" && modal.classList.contains('active')) {{
                    closeModal();
                }}
            }});
        </script>
    </body>
    </html>
    """

    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML Report generated successfully at: {os.path.abspath(output_html_path)}")

if __name__ == "__main__":
    generate_html_report()
