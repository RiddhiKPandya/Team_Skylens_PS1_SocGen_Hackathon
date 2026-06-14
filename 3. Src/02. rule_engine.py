import pandas as pd
import numpy as np
from pathlib import Path

# =====================================
# PATHS
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    BASE_DIR /
    "Datasets" /
    "3. Feature_matrix" /
    "feature_matrix.csv"
)

OUTPUT_PATH = (
    BASE_DIR /
    "Datasets" /
    "4. Model_outputs" /
    "rule_engine_output.csv"
)

# =====================================
# LOAD FEATURE MATRIX
# =====================================

df = pd.read_csv(INPUT_PATH)

print("Feature Matrix Loaded:", df.shape)

# =====================================
# IDENTITY SPRAWL RISK
# =====================================

df["identity_sprawl_risk"] = 0

df.loc[df["system_count"] >= 5,
       "identity_sprawl_risk"] += 10

df.loc[df["system_count"] >= 7,
       "identity_sprawl_risk"] += 15

df.loc[df["unique_resource_count"] >= 6,
       "identity_sprawl_risk"] += 10

df.loc[df["blast_radius_score"] >= 12,
       "identity_sprawl_risk"] += 15

# =====================================
# STALE ACCOUNT RISK
# =====================================

df["stale_account_risk"] = 0

df.loc[df["days_inactive"] > 60,
       "stale_account_risk"] += 5

df.loc[df["days_inactive"] > 90,
       "stale_account_risk"] += 10

df.loc[df["privileged_inactive_flag"] == 1,
       "stale_account_risk"] += 20

# =====================================
# PRIVILEGE ABUSE RISK
# =====================================

df["privilege_abuse_risk"] = 0

df.loc[df["is_admin"] == 1,
       "privilege_abuse_risk"] += 15

df.loc[df["is_power_user"] == 1,
       "privilege_abuse_risk"] += 8

df.loc[df["blast_radius_score"] >= 15,
       "privilege_abuse_risk"] += 20

df.loc[df["new_hire_overaccess_flag"] == 1,
       "privilege_abuse_risk"] += 20

# =====================================
# SERVICE ACCOUNT RISK
# =====================================

df["service_account_risk_score"] = 0

df.loc[df["is_service_account"] == 1,
       "service_account_risk_score"] += 10

df.loc[df["service_account_risk"] == 1,
       "service_account_risk_score"] += 20

df.loc[df["after_hours_ratio"] > 0.50,
       "service_account_risk_score"] += 10

# =====================================
# BEHAVIOR RISK
# =====================================

df["behavior_risk"] = 0

df.loc[df["after_hours_ratio"] > 0.30,
       "behavior_risk"] += 10

df.loc[df["after_hours_ratio"] > 0.50,
       "behavior_risk"] += 10

df.loc[df["failed_login_count"] >= 3,
       "behavior_risk"] += 10

df.loc[df["failed_login_count"] >= 5,
       "behavior_risk"] += 10

df.loc[df["admin_operation_count"] >= 3,
       "behavior_risk"] += 10

# =====================================
# DATA ACCESS RISK
# =====================================

df["data_access_risk"] = 0

df.loc[df["export_count"] >= 3,
       "data_access_risk"] += 10

df.loc[df["export_count"] >= 5,
       "data_access_risk"] += 15

df.loc[df["high_sensitivity_count"] >= 5,
       "data_access_risk"] += 10

df.loc[df["sensitive_access_ratio"] > 0.30,
       "data_access_risk"] += 10

df.loc[df["sensitive_access_ratio"] > 0.50,
       "data_access_risk"] += 10

# =====================================
# RAW SCORE
# =====================================

raw_score = (

    df["identity_sprawl_risk"]
    + df["stale_account_risk"]
    + df["privilege_abuse_risk"]
    + df["service_account_risk_score"]
    + df["behavior_risk"]
    + df["data_access_risk"]

)

# =====================================
# RULE HIT COUNT
# =====================================

rule_hits = (

    (df["identity_sprawl_risk"] > 0).astype(int)
    + (df["stale_account_risk"] > 0).astype(int)
    + (df["privilege_abuse_risk"] > 0).astype(int)
    + (df["service_account_risk_score"] > 0).astype(int)
    + (df["behavior_risk"] > 0).astype(int)
    + (df["data_access_risk"] > 0).astype(int)

)

df["rule_hits"] = rule_hits

# =====================================
# MULTI SIGNAL BONUS
# =====================================

raw_score = raw_score + (rule_hits * 5)

# =====================================
# NORMALIZE TO 0-100
# =====================================

df["overall_risk_score"] = (
    (raw_score / raw_score.max()) * 100
).round(2)

# =====================================
# CONFIDENCE SCORE
# =====================================

df["confidence_score"] = (
    (rule_hits / 6) * 100
).round(2)

# =====================================
# TOP RISK REASON
# =====================================

def get_reason(row):

    scores = {
        "Identity Sprawl": row["identity_sprawl_risk"],
        "Stale Account": row["stale_account_risk"],
        "Privilege Abuse": row["privilege_abuse_risk"],
        "Service Account": row["service_account_risk_score"],
        "Behavior": row["behavior_risk"],
        "Data Access": row["data_access_risk"]
    }

    return max(scores, key=scores.get)

df["top_risk_reason"] = (
    df.apply(get_reason, axis=1)
)

# =====================================
# RECOMMENDED ACTIONS
# =====================================

actions = {

    "Identity Sprawl":
        "Review and remove excess access",

    "Stale Account":
        "Disable dormant account",

    "Privilege Abuse":
        "Apply least privilege review",

    "Service Account":
        "Validate automation ownership",

    "Behavior":
        "Investigate suspicious activity",

    "Data Access":
        "Review sensitive data access"
}

df["recommended_action"] = (
    df["top_risk_reason"]
    .map(actions)
)

# =====================================
# BASE RISK LEVELS
# =====================================

def get_risk_level(score):

    if score >= 85:
        return "CRITICAL"

    elif score >= 65:
        return "HIGH"

    elif score >= 35:
        return "MEDIUM"

    else:
        return "LOW"

df["risk_level"] = (
    df["overall_risk_score"]
    .apply(get_risk_level)
)

# =====================================
# CRITICAL ESCALATION RULES
# =====================================

critical_condition = (

    (
        df["is_admin"] == 1
    )

    &

    (
        df["after_hours_ratio"] > 0.50
    )

    &

    (
        df["sensitive_access_ratio"] > 0.50
    )

)

df.loc[
    critical_condition,
    "risk_level"
] = "CRITICAL"

# =====================================
# SAVE OUTPUT
# =====================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)

# =====================================
# REPORT
# =====================================

print("\nRULE ENGINE COMPLETE")
print(df.shape)

print("\nRisk Distribution:")
print(df["risk_level"].value_counts())

print("\nTop Reasons:")
print(df["top_risk_reason"].value_counts())

print("\nTop 20 Highest Risk Users:")

print(
    df[
        [
            "user_id",
            "overall_risk_score",
            "confidence_score",
            "rule_hits",
            "risk_level",
            "top_risk_reason"
        ]
    ]
    .sort_values(
        "overall_risk_score",
        ascending=False
    )
    .head(20)
)

print(f"\nSaved To:\n{OUTPUT_PATH}")