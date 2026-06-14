import pandas as pd
from pathlib import Path

# =====================================
# PATHS
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    BASE_DIR /
    "Datasets" /
    "4. Model_outputs" /
    "final_risk_output.csv"
)

OUTPUT_PATH = (
    BASE_DIR /
    "Datasets" /
    "5. Final_Reports" /
    "final_soc_report.csv"
)

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv(INPUT_PATH)

print("Fusion Output Loaded:", df.shape)

# =====================================
# EXPLANATION GENERATOR
# =====================================

def generate_explanation(row):

    reasons = []

    if row["system_count"] > 5:
        reasons.append(
            f"Access across {int(row['system_count'])} systems"
        )

    if row["is_admin"] == 1:
        reasons.append(
            "Administrative privileges assigned"
        )

    if row["days_inactive"] > 30:
        reasons.append(
            f"Inactive for {int(row['days_inactive'])} days"
        )

    if row["failed_login_count"] > 3:
        reasons.append(
            f"{int(row['failed_login_count'])} failed login attempts"
        )

    if row["export_count"] > 3:
        reasons.append(
            f"{int(row['export_count'])} data export events"
        )

    if row["high_sensitivity_count"] > 3:
        reasons.append(
            "Frequent access to sensitive resources"
        )

    if row["after_hours_ratio"] > 0.30:
        reasons.append(
            "High after-hours activity"
        )

    if row["new_hire_overaccess_flag"] == 1:
        reasons.append(
            "New hire with excessive access"
        )

    if row["service_account_risk"] == 1:
        reasons.append(
            "Potential service account misuse"
        )

    if row["anomaly_flag"] == "ANOMALY":
        reasons.append(
            f"Anomaly score = {row['anomaly_score']:.2f}"
        )

    if len(reasons) == 0:
        reasons.append(
            "No significant risk indicators detected"
        )

    return " | ".join(reasons)

# =====================================
# RECOMMENDATION ENGINE
# =====================================

def generate_recommendation(row):

    level = row["final_risk_level"]

    if level == "CRITICAL":
        return (
            "Immediate investigation required. "
            "Review privileges, disable unused access, "
            "and validate account ownership."
        )

    elif level == "HIGH":
        return (
            "Investigate within 24 hours and review access rights."
        )

    elif level == "MEDIUM":
        return (
            "Schedule access review and monitor activity."
        )

    return (
        "No immediate action required."
    )

# =====================================
# CREATE EXPLANATIONS
# =====================================

df["risk_explanation"] = (
    df.apply(
        generate_explanation,
        axis=1
    )
)

df["recommended_action_detailed"] = (
    df.apply(
        generate_recommendation,
        axis=1
    )
)

# =====================================
# EXECUTIVE SUMMARY
# =====================================

df["executive_summary"] = (
    "Risk Score: "
    + df["final_risk_score"].astype(str)
    + " | Risk Level: "
    + df["final_risk_level"]
    + " | Reason: "
    + df["top_risk_reason"]
)

# =====================================
# SAVE
# =====================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nEXPLAINABILITY COMPLETE")
print(df.shape)

print("\nTop 10 Investigation Queue:")

print(
    df[
        [
            "user_id",
            "final_risk_score",
            "final_risk_level",
            "top_risk_reason",
            "risk_explanation"
        ]
    ]
    .sort_values(
        "final_risk_score",
        ascending=False
    )
    .head(10)
)

print(f"\nSaved To:\n{OUTPUT_PATH}")