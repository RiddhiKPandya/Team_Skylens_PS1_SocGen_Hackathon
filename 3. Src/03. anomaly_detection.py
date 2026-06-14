import pandas as pd
import numpy as np

from pathlib import Path

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# =====================================
# PATHS
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    BASE_DIR /
    "Datasets" /
    "4. Model_outputs" /
    "rule_engine_output.csv"
)

OUTPUT_PATH = (
    BASE_DIR /
    "Datasets" /
    "4. Model_outputs" /
    "anomaly_output.csv"
)

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv(INPUT_PATH)

print("Rule Engine Output Loaded:", df.shape)

# =====================================
# FEATURES FOR ANOMALY DETECTION
# =====================================

anomaly_features = [

    "system_count",

    "days_inactive",

    "total_events",

    "after_hours_count",

    "high_sensitivity_count",

    "failed_login_count",

    "export_count",

    "admin_operation_count",

    "unique_resource_count",

    "blast_radius_score",

    "after_hours_ratio",

    "sensitive_access_ratio",

    "overall_risk_score"

]

# =====================================
# FEATURE MATRIX
# =====================================

X = df[anomaly_features].copy()

# =====================================
# HANDLE MISSING VALUES
# =====================================

X = X.fillna(0)

# =====================================
# SCALE FEATURES
# =====================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# =====================================
# ISOLATION FOREST
# =====================================

model = IsolationForest(

    n_estimators=200,

    contamination=0.03,

    random_state=42

)

model.fit(X_scaled)

# =====================================
# PREDICTIONS
# =====================================

df["anomaly_flag"] = model.predict(X_scaled)

# convert:
# -1 = anomaly
#  1 = normal

df["anomaly_flag"] = (
    df["anomaly_flag"]
    .map({
        -1: "ANOMALY",
         1: "NORMAL"
    })
)

# =====================================
# ANOMALY SCORE
# =====================================

scores = model.decision_function(X_scaled)

# lower = more anomalous

df["anomaly_score_raw"] = scores

# normalize 0-100

normalized_scores = (

    (scores - scores.min())

    /

    (scores.max() - scores.min())

)

# invert so:
# high score = more anomalous

df["anomaly_score"] = (
    (1 - normalized_scores) * 100
).round(2)

# =====================================
# SEVERITY LABELS
# =====================================

def get_anomaly_severity(score):

    if score >= 80:
        return "CRITICAL"

    elif score >= 60:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    return "LOW"

df["anomaly_severity"] = (
    df["anomaly_score"]
    .apply(get_anomaly_severity)
)

# =====================================
# TOP ANOMALIES
# =====================================

top_anomalies = (

    df[df["anomaly_flag"] == "ANOMALY"]

    .sort_values(
        "anomaly_score",
        ascending=False
    )

)

# =====================================
# SAVE OUTPUT
# =====================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)

# =====================================
# REPORTING
# =====================================

print("\n====================================")
print("ANOMALY DETECTION COMPLETE")
print("====================================")

print("\nDataset Shape:")
print(df.shape)

print("\nAnomaly Distribution:")
print(df["anomaly_flag"].value_counts())

print("\nAnomaly Severity:")
print(df["anomaly_severity"].value_counts())

print("\nTop 15 Anomalous Users:")

print(
    top_anomalies[
        [
            "user_id",
            "overall_risk_score",
            "anomaly_score",
            "risk_level",
            "anomaly_severity",
            "top_risk_reason"
        ]
    ]
    .head(15)
)

print(f"\nSaved To:\n{OUTPUT_PATH}")