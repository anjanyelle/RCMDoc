import os

workspace_dir = r"c:\Lalataksha V Company\RCM - All Lakshya\RCMDoc"
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
for base in files:
    for ext in [".html", ".md"]:
        path = os.path.join(workspace_dir, base + ext)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        first_15 = "".join(lines[:15])
        next_lines = [l.strip() for l in lines if "Next Module" in l or "Next:" in l or "Next Module:" in l or "Next Module Link" in l]
        
        out_lines.append(f"File: {base}{ext}")
        out_lines.append("First 15 lines:")
        out_lines.append(first_15)
        out_lines.append(f"Next lines: {next_lines}")
        out_lines.append("="*60 + "\n")

out_path = os.path.join(workspace_dir, "scratch", "all_file_metadata.txt")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print("Dumped metadata to:", out_path)
