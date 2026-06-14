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
    "anomaly_output.csv"
)

OUTPUT_PATH = (
    BASE_DIR /
    "Datasets" /
    "4. Model_outputs" /
    "final_risk_output.csv"
)

# =====================================
# LOAD
# =====================================

df = pd.read_csv(INPUT_PATH)

print("Anomaly Output Loaded:", df.shape)

# =====================================
# FUSION SCORE
# =====================================

df["final_risk_score"] = (

    df["overall_risk_score"] * 0.70

    +

    df["anomaly_score"] * 0.30

)

# =====================================
# CRITICAL ESCALATION
# =====================================

critical_boost = (

    (
        df["risk_level"] == "CRITICAL"
    )

    |

    (
        df["anomaly_severity"] == "CRITICAL"
    )

)

critical_boost &= (

    df["confidence_score"] >= 60

)

df.loc[
    critical_boost,
    "final_risk_score"
] += 10

# =====================================
# CAP SCORE
# =====================================

df["final_risk_score"] = (
    df["final_risk_score"]
    .clip(0, 100)
    .round(2)
)

# =====================================
# FINAL RISK LEVEL
# =====================================

def get_final_level(score):

    if score >= 85:
        return "CRITICAL"

    elif score >= 65:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"

df["final_risk_level"] = (
    df["final_risk_score"]
    .apply(get_final_level)
)

# =====================================
# FINAL PRIORITY
# =====================================

def get_priority(level):

    mapping = {

        "CRITICAL": 1,
        "HIGH": 2,
        "MEDIUM": 3,
        "LOW": 4

    }

    return mapping[level]

df["investigation_priority"] = (
    df["final_risk_level"]
    .apply(get_priority)
)

# =====================================
# SAVE
# =====================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)

# =====================================
# REPORT
# =====================================

print("\nFUSION COMPLETE")
print(df.shape)

print("\nFinal Risk Distribution:")
print(
    df["final_risk_level"]
    .value_counts()
)

print("\nTop 20 Users:")

print(
    df[
        [
            "user_id",
            "final_risk_score",
            "final_risk_level",
            "investigation_priority",
            "top_risk_reason"
        ]
    ]
    .sort_values(
        "final_risk_score",
        ascending=False
    )
    .head(20)
)

print(f"\nSaved To:\n{OUTPUT_PATH}")