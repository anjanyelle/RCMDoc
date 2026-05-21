import os
import re

workspace_dir = r"c:\Lalataksha V Company\RCM - All Lakshya\RCMDoc"

meta_updates = {
    "Flows_Module_PROVIDER CREDENTIALING & MANAGEMENT": {
        "title": "Pre-RCM Modules 1-4: Provider Onboarding, Credentialing, Enrollment, & Contract Management",
        "h1": "Pre-RCM Modules 1-4: Provider Onboarding, Credentialing, Enrollment, & Contract Management",
        "id": "MOD-PRE-01-04",
        "category": "Pre-RCM / Foundational Flow",
        "next_title": "Module 1: Appointment Scheduling",
        "next_file": "Flows_Module_04_Appointment_Scheduling"
    },
    "Flows_Module_04_Appointment_Scheduling": {
        "title": "Module 1: Appointment Scheduling - Flow Documentation",
        "h1": "Module 1: Appointment Scheduling - Flow Documentation",
        "id": "MOD-001",
        "category": "Category 1: Patient Access Management",
        "next_title": "Module 2: Patient Registration",
        "next_file": "Flows_Module_02_Patient_Registration"
    },
    "Flows_Module_02_Patient_Registration": {
        "title": "Module 2: Patient Registration - Complete Flow Documentation",
        "h1": "Module 2: Patient Registration - Complete Flow Documentation",
        "id": "MOD-002",
        "category": "Category 1: Patient Access Management",
        "next_title": "Module 3: Insurance Eligibility Verification",
        "next_file": "Flows_Module_03_Insurance_Verification"
    },
    "Flows_Module_03_Insurance_Verification": {
        "title": "Module 3: Insurance Eligibility Verification - Flow Documentation",
        "h1": "Module 3: Insurance Eligibility Verification - Flow Documentation",
        "id": "MOD-003",
        "category": "Category 1: Patient Access Management",
        "next_title": "Module 4: Prior Authorization / Referral Management",
        "next_file": "Flows_Module_12_Prior_Authorization"
    },
    "Flows_Module_12_Prior_Authorization": {
        "title": "Module 4: Prior Authorization / Referral Management - Flow Documentation",
        "h1": "Module 4: Prior Authorization / Referral Management - Flow Documentation",
        "id": "MOD-004",
        "category": "Category 1: Patient Access Management",
        "next_title": "Module 5: Patient Check-In",
        "next_file": "Flows_Module_05_Patient_Checkin"
    },
    "Flows_Module_05_Patient_Checkin": {
        "title": "Module 5: Patient Check-In - Flow Documentation",
        "h1": "Module 5: Patient Check-In - Flow Documentation",
        "id": "MOD-005",
        "category": "Category 1: Patient Access Management",
        "next_title": "Module 6: Clinical Documentation / EMR (Encounter)",
        "next_file": "Flows_Module_14_Encounter"
    },
    "Flows_Module_14_Encounter": {
        "title": "Module 6: Clinical Documentation / EMR (Encounter) - Flow Documentation",
        "h1": "Module 6: Clinical Documentation / EMR (Encounter) - Flow Documentation",
        "id": "MOD-006",
        "category": "Category 2: Clinical & Mid-Cycle Management",
        "next_title": "Module 6 (Support): Order Management",
        "next_file": "Flows_Module_13_Order_Management"
    },
    "Flows_Module_13_Order_Management": {
        "title": "Module 6 (Support): Order Management - Flow Documentation",
        "h1": "Module 6 (Support): Order Management - Flow Documentation",
        "id": "MOD-006-SUPPORT",
        "category": "Category 2: Clinical & Mid-Cycle Management",
        "next_title": "Module 7: Medical Coding (AI-Assisted)",
        "next_file": "Flows_Module_06_Medical_Coding"
    },
    "Flows_Module_06_Medical_Coding": {
        "title": "Module 7: Medical Coding (AI-Assisted) - Flow Documentation",
        "h1": "Module 7: Medical Coding (AI-Assisted) - Flow Documentation",
        "id": "MOD-007",
        "category": "Category 2: Clinical & Mid-Cycle Management",
        "next_title": "Module 8: Charge Entry / Charge Capture",
        "next_file": "Flows_Module_07_10_Remaining",
        "next_anchor": "#module-8-charge-capture"
    },
    "Flows_Module_07_10_Remaining": {
        "title": "Modules 8-12: Charge Capture, Claim Creation, Scrubbing, Submission, & Status Tracking - Flow Documentation",
        "h1": "Modules 8-12: Charge Capture, Claim Creation, Scrubbing, Submission, & Status Tracking",
        "id": "MOD-008-012",
        "category": "Category 2 & Category 3: Clinical, Billing & Claims Management",
        "next_title": "Module 13: Insurance Adjudication Tracking",
        "next_file": "Flows_Module_Insurance Adjudication Tracking"
    },
    "Flows_Module_Insurance Adjudication Tracking": {
        "title": "Module 13: Insurance Adjudication Tracking - Flow Documentation",
        "h1": "Module 13: Insurance Adjudication Tracking",
        "id": "MOD-013",
        "category": "Category 3: Claims Management",
        "next_title": "Module 15: Payment Posting",
        "next_file": "Flows_Module_Payment_Posting"
    },
    "Flows_Module_Payment_Posting": {
        "title": "Module 15: Payment Posting - Flow Documentation",
        "h1": "Module 15: Payment Posting - Flow Documentation",
        "id": "MOD-015",
        "category": "Category 4: Payment & Revenue Management",
        "next_title": "Module 16: Denial & Appeals Management",
        "next_file": "Flows_Module_11_Denial & Appeals Management"
    },
    "Flows_Module_11_Denial & Appeals Management": {
        "title": "Module 16: Denial & Appeals Management - Flow Documentation",
        "h1": "Module 16: Denial & Appeals Management - Flow Documentation",
        "id": "MOD-016",
        "category": "Category 4: Payment & Revenue Management",
        "next_title": "Module 17: Secondary Insurance Billing",
        "next_file": "Flows_Module_20_Secondary_Billing"
    },
    "Flows_Module_20_Secondary_Billing": {
        "title": "Module 17: Secondary Insurance Billing - Flow Documentation",
        "h1": "Module 17: Secondary Insurance Billing - Flow Documentation",
        "id": "MOD-017",
        "category": "Category 4: Payment & Revenue Management",
        "next_title": "Module 18: Patient Billing",
        "next_file": "Flows_Module_18_Patient_Billing"
    },
    "Flows_Module_18_Patient_Billing": {
        "title": "Module 18: Patient Billing - Flow Documentation",
        "h1": "Module 18: Patient Billing - Flow Documentation",
        "id": "MOD-018",
        "category": "Category 4: Payment & Revenue Management",
        "next_title": "Module 19: Accounts Receivable (AR) Follow-Up",
        "next_file": "Flows_Module_Accounts Receivable (AR) Follow-Up"
    },
    "Flows_Module_Accounts Receivable (AR) Follow-Up": {
        "title": "Module 19: Accounts Receivable (AR) Follow-Up - Flow Documentation",
        "h1": "Module 19: Accounts Receivable (AR) Follow-Up",
        "id": "MOD-019",
        "category": "Category 4: Payment & Revenue Management",
        "next_title": "Module 20: Collections / Refund / Write-Off Management",
        "next_file": "Flows_Module_Collections"
    },
    "Flows_Module_Collections": {
        "title": "Module 20: Collections / Refund / Write-Off Management - Flow Documentation",
        "h1": "Module 20: Collections / Refund / Write-Off Management",
        "id": "MOD-020",
        "category": "Category 4: Payment & Revenue Management",
        "next_title": "Module 21: Reporting & Analytics",
        "next_file": "Flows_Module_Reporting_Analytics"
    },
    "Flows_Module_Reporting_Analytics": {
        "title": "Module 21: Reporting & Analytics - Flow Documentation",
        "h1": "Module 21: Reporting & Analytics",
        "id": "MOD-021",
        "category": "Category 5: Reporting, Compliance & Governance",
        "next_title": "Module 22: Compliance & Audit",
        "next_file": "Flows_Module_Compliance & Audit"
    },
    "Flows_Module_Compliance & Audit": {
        "title": "Module 22: Compliance & Audit - Flow Documentation",
        "h1": "Module 22: Compliance & Audit",
        "id": "MOD-022",
        "category": "Category 5: Reporting, Compliance & Governance",
        "next_title": "Module 23: User Login & Authentication",
        "next_file": "Flows_Module_01_User_Login"
    },
    "Flows_Module_01_User_Login": {
        "title": "Module 23: User Login & Authentication - Flow Documentation",
        "h1": "Module 23: User Login & Authentication - Flow Documentation",
        "id": "MOD-023",
        "category": "Category 6: Administration & Platform Services",
        "next_title": "Pre-RCM Modules 1-4: Provider Onboarding, Credentialing, Enrollment, & Contract Management",
        "next_file": "Flows_Module_PROVIDER CREDENTIALING & MANAGEMENT"
    }
}

def update_html(base, path, updates):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update <title>
    title_regex = re.compile(r'<title>.*?</title>', re.IGNORECASE)
    content = title_regex.sub(f"<title>{updates['title']}</title>", content)

    # 2. Update <h1>
    # Matches <h1> tag up to its closing, allowing attributes or tags inside
    h1_regex = re.compile(r'<h1[^>]*>.*?</h1>', re.IGNORECASE)
    content = h1_regex.sub(f"<h1>{updates['h1']}</h1>", content)

    # 3. Update Module ID
    id_regex = re.compile(r'(<p[^>]*><strong>\s*Module ID:\s*</strong>\s*)(?:MOD-)?[\w-]+(\s*</p>)', re.IGNORECASE)
    content = id_regex.sub(rf"\g<1>{updates['id']}\g<2>", content)

    # 4. Update Category
    cat_regex = re.compile(r'(<p[^>]*><strong>\s*Category:\s*</strong>\s*)[^<]+(\s*</p>)', re.IGNORECASE)
    content = cat_regex.sub(rf"\g<1>{updates['category']}\g<2>", content)

    # 5. Update/Insert Next Module
    # We want to match existing Next Module links
    next_html_pattern = re.compile(r'<p[^>]*>\s*<strong>\s*Next Module:\s*</strong>[\s\S]*?</p>', re.IGNORECASE)
    
    import urllib.parse
    anchor = updates.get("next_anchor", "")
    quoted_file = urllib.parse.quote(updates['next_file'])
    next_url = f"{quoted_file}.html{anchor}"
    new_next_line = f'<p><strong>Next Module:</strong> <a href="{next_url}">{updates["next_title"]}</a></p>'

    if next_html_pattern.search(content):
        content = next_html_pattern.sub(new_next_line, content)
    else:
        # If not found, insert before </body>
        body_close = re.compile(r'</body>', re.IGNORECASE)
        if body_close.search(content):
            content = body_close.sub(f"<hr>\n{new_next_line}\n\n</body>", content)
        else:
            content += f"\n<hr>\n{new_next_line}\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def update_md(base, path, updates):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update H1 (# Heading)
    # Matches the first line if it's # ...
    lines = content.splitlines()
    if lines and lines[0].startswith("#"):
        lines[0] = f"# {updates['h1']}"
    content = "\n".join(lines)

    # 2. Update Module ID
    # Handle bold or regular notation
    id_regex = re.compile(r'(\*\*Module ID:\*\*|Module ID:)\s*(?:MOD-)?[\w-]+', re.IGNORECASE)
    content = id_regex.sub(rf"\g<1> {updates['id']}", content)

    # 3. Update Category
    cat_regex = re.compile(r'(\*\*Category:\*\*|Category:)\s*[^\n]+', re.IGNORECASE)
    content = cat_regex.sub(rf"\g<1> {updates['category']}", content)

    # 4. Update/Insert Next Module
    next_md_pattern = re.compile(r'(\*\*Next Module:\*\*|Next Module:)\s*[^\n]+', re.IGNORECASE)
    
    import urllib.parse
    anchor = updates.get("next_anchor", "")
    quoted_file = urllib.parse.quote(updates['next_file'])
    next_url = f"{quoted_file}.md{anchor}"
    new_next_line = f"**Next Module:** [{updates['next_title']}]({next_url})"

    if next_md_pattern.search(content):
        content = next_md_pattern.sub(new_next_line, content)
    else:
        # Append to the end
        content = content.rstrip() + f"\n\n---\n\n{new_next_line}\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# Apply updates to all files
for base, updates in meta_updates.items():
    html_path = os.path.join(workspace_dir, base + ".html")
    md_path = os.path.join(workspace_dir, base + ".md")

    if os.path.exists(html_path):
        print(f"Updating HTML: {base}.html")
        update_html(base, html_path, updates)
    else:
        print(f"WARNING: HTML file not found: {html_path}")

    if os.path.exists(md_path):
        print(f"Updating MD: {base}.md")
        update_md(base, md_path, updates)
    else:
        print(f"WARNING: MD file not found: {md_path}")

print("All module files updated successfully!")
