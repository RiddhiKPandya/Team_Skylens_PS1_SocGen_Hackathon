import pandas as pd
import numpy as np

from pathlib import Path

# =====================================
# Paths
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

USERS_PATH = (
    BASE_DIR /
    "Datasets" /
    "2. Synthetic_datasets" /
    "identity_users_600_combined.csv"
)

EVENTS_PATH = (
    BASE_DIR /
    "Datasets" /
    "2. Synthetic_datasets" /
    "identity_events_1800_combined.csv"
)

OUTPUT_PATH = (
    BASE_DIR /
    "Datasets" /
    "3. Feature_matrix" /
    "feature_matrix.csv"
)

# =====================================
# Load Data
# =====================================

users = pd.read_csv(USERS_PATH)
events = pd.read_csv(EVENTS_PATH)

print(f"Users Loaded : {users.shape}")
print(f"Events Loaded: {events.shape}")

# =====================================
# User Features
# =====================================

users["system_count"] = (
    users["systems_access"]
    .fillna("")
    .apply(lambda x: len(str(x).split("|")))
)

users["is_admin"] = (
    users["privilege_level"]
    .astype(str)
    .str.lower()
    .eq("admin")
    .astype(int)
)

users["is_power_user"] = (
    users["privilege_level"]
    .astype(str)
    .str.lower()
    .eq("power-user")
    .astype(int)
)

users["is_service_account"] = (
    users["privilege_level"]
    .astype(str)
    .str.lower()
    .eq("service-account")
    .astype(int)
)

users["tenure_days"] = (
    pd.Timestamp.today()
    - pd.to_datetime(users["hire_date"])
).dt.days

# =====================================
# Event Features
# =====================================

event_features = events.groupby("user_id").agg(

    total_events=("action", "count"),

    night_access_count=(
        "time_classification",
        lambda x: (x == "night").sum()
    ),

    weekend_access_count=(
        "time_classification",
        lambda x: (x == "weekend").sum()
    ),

    after_hours_count=(
        "time_classification",
        lambda x: (
            (x == "night")
            |
            (x == "weekend")
            |
            (x == "unusual_hours")
        ).sum()
    ),

    high_sensitivity_count=(
        "resource_sensitivity",
        lambda x: (x == "high").sum()
    ),

    failed_login_count=(
        "status",
        lambda x: (x == "failure").sum()
    ),

    export_count=(
        "action",
        lambda x: (x == "export_data").sum()
    ),

    admin_operation_count=(
        "action",
        lambda x: (x == "admin_operation").sum()
    ),

    unique_resource_count=(
        "resource",
        "nunique"
    )

).reset_index()

# =====================================
# Merge
# =====================================

features = users.merge(
    event_features,
    on="user_id",
    how="left"
)

# =====================================
# ADVANCED IAM FEATURES
# =====================================

# Identity Sprawl

features["identity_sprawl_score"] = (
    features["system_count"] * 5
    +
    features["unique_resource_count"] * 2
)

# Dormant Accounts

features["stale_account_flag"] = (
    features["days_inactive"] > 30
).astype(int)

# =====================================
# NEW HIRE FEATURES
# =====================================

features["new_hire_flag"] = (
    features["tenure_days"] < 30
).astype(int)

features["new_hire_overaccess_flag"] = (
    (features["tenure_days"] < 30)
    &
    (features["system_count"] > 5)
).astype(int)

# Privileged + Inactive

features["privileged_inactive_flag"] = (
    (
        features["is_admin"] == 1
    )
    &
    (
        features["days_inactive"] > 30
    )
).astype(int)

# Very stale

features["orphaned_account_flag"] = (
    features["days_inactive"] > 90
).astype(int)


# Service account risk

features["service_account_risk"] = (
    (
        features["is_service_account"] == 1
    )
    &
    (
        features["total_events"] > 5
    )
).astype(int)

# Blast Radius

features["blast_radius_score"] = (
    features["system_count"]
    *
    (
        1
        + features["is_admin"]
        + features["is_power_user"]
    )
)

# Sensitive Access Ratio

features["sensitive_access_ratio"] = (
    features["high_sensitivity_count"]
    /
    (features["total_events"] + 1)
)

# After Hours Ratio

features["after_hours_ratio"] = (
    features["after_hours_count"]
    /
    (features["total_events"] + 1)
)

# Export Risk

features["export_risk_score"] = (
    features["export_count"] * 5
)

# Admin Activity Risk

features["admin_activity_score"] = (
    features["admin_operation_count"] * 5
)

# Failed Login Risk

features["failed_login_risk"] = (
    features["failed_login_count"] * 4
)

# =====================================
# Handle Missing Values Safely
# =====================================

numeric_cols = features.select_dtypes(
    include=["number"]
).columns

string_cols = features.select_dtypes(
    include=["object", "string"]
).columns

features[numeric_cols] = (
    features[numeric_cols]
    .fillna(0)
)

features[string_cols] = (
    features[string_cols]
    .fillna("UNKNOWN")
)

# =====================================
# Save
# =====================================

features.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n=================================")
print("FEATURE MATRIX CREATED SUCCESSFULLY")
print("=================================")

print("\nShape:")
print(features.shape)

print("\nColumns:")
print(features.columns.tolist())

print("\nPreview:")
print(features.head())

print(f"\nSaved To:\n{OUTPUT_PATH}")