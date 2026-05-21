import os
import re

workspace_dir = r"C:\Lalataksha V Company\RCM - All Lakshya\RCMDoc"
files = [
    "Flows_Module_PROVIDER CREDENTIALING & MANAGEMENT",
    "Flows_Module_04_Appointment_Scheduling",
    "Flows_Module_02_Patient_Registration",
    "Flows_Module_03_Insurance_Verification",
    "Flows_Module_12_Prior_Authorization",
    "Flows_Module_05_Patient_Checkin",
    "Flows_Module_14_Encounter",
    "Flows_Module_13_Order_Management",
    "Flows_Module_06_Medical_Coding",
    "Flows_Module_07_10_Remaining",
    "Flows_Module_Insurance Adjudication Tracking",
    "Flows_Module_Payment_Posting",
    "Flows_Module_11_Denial & Appeals Management",
    "Flows_Module_20_Secondary_Billing",
    "Flows_Module_18_Patient_Billing",
    "Flows_Module_Accounts Receivable (AR) Follow-Up",
    "Flows_Module_Collections",
    "Flows_Module_Reporting_Analytics",
    "Flows_Module_Compliance & Audit",
    "Flows_Module_01_User_Login"
]

out_lines = []
out_lines.append("=== DETAILED EXTRACTION ===")

for name in files:
    md_path = os.path.join(workspace_dir, name + ".md")
    html_path = os.path.join(workspace_dir, name + ".html")
    
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        out_lines.append(f"\n--- {name}.md ---")
        first_header = re.findall(r"^#\s+(.*)", content, re.MULTILINE)
        if first_header:
            out_lines.append(f"First Header: {first_header[0]}")
            
        module_headers = re.findall(r"^#\s+(Module\s+.*)", content, re.MULTILINE)
        if module_headers:
            out_lines.append(f"Module Headers: {module_headers}")
            
        mod_ids = re.findall(r"(?:Module ID|Module\s+ID|MOD-ID|MOD_ID|MOD-PRE-\d+-\d+):\s*([^\n\r]+)", content, re.IGNORECASE)
        out_lines.append(f"Module IDs: {mod_ids}")
        
        categories = re.findall(r"(?:Category):\s*([^\n\r]+)", content, re.IGNORECASE)
        out_lines.append(f"Categories: {categories}")
        
        next_modules = re.findall(r"(?:Next Module|Next\s+Module|Next):\s*([^\n\r]+)", content, re.IGNORECASE)
        out_lines.append(f"Next Modules: {next_modules}")
        
        footer_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        out_lines.append("Footer links found in MD:")
        for text, url in footer_links:
            if "next" in text.lower() or "module" in text.lower() or "flows_module" in url.lower() or "index" in url.lower():
                out_lines.append(f"  - [{text}] -> ({url})")
                
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        html_links = re.findall(r"<a\s+[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", html_content, re.IGNORECASE)
        out_lines.append("Footer links found in HTML:")
        for url, text in html_links:
            if "next" in text.lower() or "module" in text.lower() or "flows_module" in url.lower() or "index" in url.lower():
                out_lines.append(f"  - [{text.strip()}] -> ({url})")

with open(os.path.join(workspace_dir, "scratch", "inspect_output.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
print("Done, output written to scratch/inspect_output.txt")
