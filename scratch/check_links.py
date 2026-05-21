import os
import re

workspace_dir = r"c:\Lalataksha V Company\RCM - All Lakshya\RCMDoc"

# List of files we expect
files_list = [
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

all_existing_files = os.listdir(workspace_dir)

print("=== CHECKING LINKS AND CONTENT ===")

# Helper to check if a link is valid (i.e. targets an existing file or anchor)
def verify_link(source_file, target):
    import urllib.parse
    # Strip URL-encoding and file:/// prefixes
    target = target.replace("file:///", "").replace("file://", "")
    target = urllib.parse.unquote(target)
    
    # If it's a relative path, check against workspace directory
    # If absolute or has drive letter, check that too
    if "#" in target:
        base, anchor = target.split("#", 1)
    else:
        base = target
        anchor = None
        
    if not base:
        # Self link with anchor
        return True
        
    # Check if target is relative
    if not os.path.isabs(base):
        base_path = os.path.join(workspace_dir, base)
    else:
        base_path = base
        
    if not os.path.exists(base_path):
        # Maybe it's referring to something else, check if base exists in all_existing_files
        norm_base = os.path.basename(base)
        if norm_base in all_existing_files:
            return True
        return False
    return True

for f_name in all_existing_files:
    if not (f_name.endswith(".html") or f_name.endswith(".md")):
        continue
    path = os.path.join(workspace_dir, f_name)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find links
    # MD links: [text](link)
    # HTML links: href="link"
    links = []
    if f_name.endswith(".md"):
        links = re.findall(r'\[[^\]]*\]\(([^)]*)\)', content)
    else:
        links = re.findall(r'href="([^"]*)"', content)
        
    broken = []
    for link in links:
        if link.startswith("http") or link.startswith("mailto") or link.startswith("#"):
            continue
        if not verify_link(f_name, link):
            broken.append(link)
            
    if broken:
        print(f"File {f_name} has broken links:")
        for b in broken:
            print(f"  - {b}")
