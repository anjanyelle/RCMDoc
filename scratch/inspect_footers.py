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

output_file = os.path.join(workspace_dir, "scratch", "footers_inspection.txt")

with open(output_file, "w", encoding="utf-8") as out:
    for base in files:
        for ext in [".html", ".md"]:
            path = os.path.join(workspace_dir, base + ext)
            if not os.path.exists(path):
                continue
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            out.write(f"File: {base}{ext} (Total lines: {len(lines)})\n")
            out.write("Last 10 lines:\n")
            last_lines = lines[-10:]
            for idx, l in enumerate(last_lines):
                line_num = len(lines) - len(last_lines) + idx + 1
                out.write(f"  L{line_num}: {l.strip()}\n")
            out.write("="*60 + "\n\n")

print("Footers inspection completed. Output saved to:", output_file)
