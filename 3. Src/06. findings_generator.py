import pandas as pd
import json
from pathlib import Path

# =====================================
# PATHS
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    BASE_DIR /
    "Datasets" /
    "5. Final_Reports" /
    "final_soc_report.csv"
)

OUTPUT_JSON = (
    BASE_DIR /
    "Datasets" /
    "5. Final_Reports" /
    "findings_output.json"
)

# =====================================
# LOAD REPORT
# =====================================

df = pd.read_csv(INPUT_PATH)

print("SOC Report Loaded:", df.shape)

# =====================================
# FINDING GENERATOR
# =====================================

all_users = []

for _, row in df.iterrows():

    findings = []

    # =================================
    # STALE ACCOUNTS
    # =================================

    if row["days_inactive"] > 30:

        findings.append({
            "finding": "STALE_ACCOUNT",
            "details": f"Account inactive for {int(row['days_inactive'])} days",
            "severity": "HIGH",
            "recommendation": "Validate employment status"
        })

    if row["days_inactive"] > 90:

        findings.append({
            "finding": "ORPHANED_ACCOUNT",
            "details": f"Account inactive for {int(row['days_inactive'])} days",
            "severity": "CRITICAL",
            "recommendation": "Disable account immediately"
        })

    # =================================
    # PRIVILEGE
    # =================================

    if row["is_admin"] == 1:

        findings.append({
            "finding": "ADMIN_ACCOUNT",
            "details": "Administrative privileges assigned",
            "severity": "MEDIUM",
            "recommendation": "Review privileged access"
        })

    if row["is_power_user"] == 1:

        findings.append({
            "finding": "POWER_USER_ACCOUNT",
            "details": "Power-user privileges assigned",
            "severity": "LOW",
            "recommendation": "Validate business need"
        })

    # =================================
    # IDENTITY SPRAWL
    # =================================

    if row["system_count"] >= 6:

        findings.append({
            "finding": "IDENTITY_SPRAWL",
            "details": f"Access across {int(row['system_count'])} systems",
            "severity": "HIGH",
            "recommendation": "Review excessive access"
        })

    if row["unique_resource_count"] >= 6:

        findings.append({
            "finding": "EXCESSIVE_RESOURCE_ACCESS",
            "details": f"Accessed {int(row['unique_resource_count'])} unique resources",
            "severity": "MEDIUM",
            "recommendation": "Review resource permissions"
        })

    # =================================
    # NEW HIRE
    # =================================

    if row["new_hire_flag"] == 1:

        findings.append({
            "finding": "NEW_HIRE_ACCOUNT",
            "details": "User joined within last 30 days",
            "severity": "LOW",
            "recommendation": "Monitor onboarding access"
        })

    if row["new_hire_overaccess_flag"] == 1:

        findings.append({
            "finding": "NEW_HIRE_OVERACCESS",
            "details": f"New hire has access to {int(row['system_count'])} systems",
            "severity": "HIGH",
            "recommendation": "Review onboarding permissions"
        })

    # =================================
    # SERVICE ACCOUNT
    # =================================

    if row["is_service_account"] == 1:

        findings.append({
            "finding": "SERVICE_ACCOUNT",
            "details": "Service account detected",
            "severity": "MEDIUM",
            "recommendation": "Validate ownership"
        })

    if row["service_account_risk"] == 1:

        findings.append({
            "finding": "SERVICE_ACCOUNT_ANOMALY",
            "details": "Elevated activity observed from service account",
            "severity": "HIGH",
            "recommendation": "Investigate automation usage"
        })

    # =================================
    # FAILED LOGINS
    # =================================

    if row["failed_login_count"] >= 3:

        findings.append({
            "finding": "FAILED_LOGIN_ACTIVITY",
            "details": f"{int(row['failed_login_count'])} failed login attempts detected",
            "severity": "HIGH",
            "recommendation": "Investigate authentication activity"
        })

    # =================================
    # DATA ACCESS
    # =================================

    if row["export_count"] >= 3:

        findings.append({
            "finding": "DATA_EXPORT_ACTIVITY",
            "details": f"{int(row['export_count'])} export operations detected",
            "severity": "HIGH",
            "recommendation": "Review exported data"
        })

    if row["high_sensitivity_count"] >= 3:

        findings.append({
            "finding": "HIGH_SENSITIVITY_ACCESS",
            "details": f"{int(row['high_sensitivity_count'])} accesses to sensitive resources",
            "severity": "HIGH",
            "recommendation": "Review sensitive resource usage"
        })

    # =================================
    # AFTER HOURS
    # =================================

    if row["after_hours_ratio"] >= 0.40:

        findings.append({
            "finding": "AFTER_HOURS_ACTIVITY",
            "details": f"{round(row['after_hours_ratio']*100,2)}% activity outside business hours",
            "severity": "HIGH",
            "recommendation": "Review unusual activity"
        })

    # =================================
    # ANOMALY DETECTION
    # =================================

    if row["anomaly_flag"] == "ANOMALY":

        findings.append({
            "finding": "ML_ANOMALY_DETECTED",
            "details": f"Anomaly score {round(row['anomaly_score'],2)}",
            "severity": row["anomaly_severity"],
            "recommendation": "SOC investigation required"
        })

    # =================================
    # FINAL RISK
    # =================================

    if row["final_risk_level"] == "CRITICAL":

        findings.append({
            "finding": "CRITICAL_RISK_USER",
            "details": f"Final risk score {round(row['final_risk_score'],2)}",
            "severity": "CRITICAL",
            "recommendation": "Immediate SOC review"
        })

    elif row["final_risk_level"] == "HIGH":

        findings.append({
            "finding": "HIGH_RISK_USER",
            "details": f"Final risk score {round(row['final_risk_score'],2)}",
            "severity": "HIGH",
            "recommendation": "Prioritize investigation"
        })

    user_record = {
        "user_id": row["user_id"],
        "username": row["username"],
        "risk_level": row["final_risk_level"],
        "risk_score": float(row["final_risk_score"]),
        "findings": findings
    }

    all_users.append(user_record)

# =====================================
# SAVE JSON
# =====================================

with open(
    OUTPUT_JSON,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_users,
        f,
        indent=4
    )

print("\nFINDINGS GENERATED")
print(f"Users Processed: {len(all_users)}")
print(f"Saved To:\n{OUTPUT_JSON}")