import json
import requests
from pathlib import Path

# =====================================
# CONFIG
# =====================================

SELECTED_USERS = [
    "USR00002",
    "USR00015",
    "USR00027",
    "USR00028",
    "USR00035",
    "USR00036",
    "USR00047",
    "USR00068",
    "USR00077",
    "USR00083",
    "USR00091",
    "USR00121",
    "USR00125",
    "USR00126",
    "USR00203",
    "USR00209",
    "USR00218",
    "USR00221",
    "USR00314",
    "USR00368"
]

# =====================================
# PATHS
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    BASE_DIR
    / "Datasets"
    / "5. Final_Reports"
    / "findings_output.json"
)

OUTPUT_DIR = (
    BASE_DIR
    / "Datasets"
    / "6. LLM_Reports"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =====================================
# LOAD FINDINGS
# =====================================

with open(
    INPUT_PATH,
    "r",
    encoding="utf-8"
) as f:
    users = json.load(f)

# =====================================
# FILTER USERS
# =====================================

selected_users = [
    user
    for user in users
    if user["user_id"] in SELECTED_USERS
]

print("\n=================================")
print("SELECTED USERS FOUND")
print("=================================")
print(f"Found {len(selected_users)} users")

# =====================================
# PROCESS USERS
# =====================================

for selected_user in selected_users:

    print("\n=================================")
    print(f"PROCESSING {selected_user['user_id']}")
    print("=================================")

    print("Risk Level:", selected_user["risk_level"])
    print("Risk Score:", selected_user["risk_score"])

    # =====================================
    # BUILD EVIDENCE
    # =====================================

    finding_text = ""

    print("\n=================================")
    print("EVIDENCE SENT TO OLLAMA")
    print("=================================")

    for finding in selected_user["findings"]:

        finding_name = finding.get(
            "finding",
            "UNKNOWN_FINDING"
        )

        details = finding.get(
            "details",
            "No Details"
        )

        severity = finding.get(
            "severity",
            "UNKNOWN"
        )

        recommendation = finding.get(
            "recommendation",
            "No Recommendation"
        )

        print(f"\n{finding_name}")
        print(f"Details: {details}")
        print(f"Severity: {severity}")

        finding_text += f"""
Finding: {finding_name}
Details: {details}
Severity: {severity}
Recommendation: {recommendation}

"""

    # =====================================
    # PROMPT
    # =====================================

    prompt = f"""
You are SOCGen AI.

You are a Senior Identity Security Analyst.

You are NOT a cybersecurity teacher.

You are NOT generating findings.

The findings are already validated by the detection engine.

Your ONLY job is to generate:

1. business_impact
2. future_investigation

====================================================

STRICT RULES

1. Use ONLY supplied evidence.

2. Never speculate.

3. Never mention ransomware.

4. Never mention widespread breaches.

5. Never mention compromise unless directly supported.

6. Do not invent facts.

7. Reference actual findings.

8. Reference actual evidence.

9. Business impact should be 2-3 sentences.

10. Future investigation should be 2-3 sentences.

11. Sound like a SOC analyst.

12. Be specific.

====================================================

INTERPRETATION GUIDANCE

FAILED_LOGIN_ACTIVITY
→ Authentication misuse risk.

HIGH_SENSITIVITY_ACCESS
→ Sensitive business information exposure risk.

AFTER_HOURS_ACTIVITY
→ Unusual access behavior.

IDENTITY_SPRAWL
→ Excessive permissions.

EXCESSIVE_RESOURCE_ACCESS
→ Broad resource exposure.

SERVICE_ACCOUNT_ANOMALY
→ Unexpected account activity.

DATA_EXPORT_ACTIVITY
→ Potential data exposure.

STALE_ACCOUNT
→ Dormant access risk.

ORPHANED_ACCOUNT
→ Account should be reviewed for deactivation.

ADMIN_ACCOUNT
→ Privileged access increases business impact.

POWER_USER_ACCOUNT
→ Elevated access requires validation.

ML_ANOMALY_DETECTED
→ Behavior differs from baseline.

CRITICAL_RISK_USER
→ Immediate review required.

HIGH_RISK_USER
→ Prioritized review required.

====================================================

EXAMPLE

Evidence:

Finding: FAILED_LOGIN_ACTIVITY
Details: 5 failed login attempts detected

Finding: AFTER_HOURS_ACTIVITY
Details: 78% activity outside business hours

Output:

{{
    "business_impact":
    "Repeated failed authentication attempts combined with significant after-hours activity increase the risk of unauthorized access to enterprise resources. The observed behavior deviates from expected access patterns and may affect the integrity of business operations if not reviewed promptly.",

    "future_investigation":
    "Review authentication logs associated with the failed login attempts and validate whether the activity originated from legitimate sources. Investigate the business justification for access occurring outside standard operating hours."
}}

====================================================

REAL USER

User ID:
{selected_user["user_id"]}

Risk Level:
{selected_user["risk_level"]}

Risk Score:
{selected_user["risk_score"]}

Evidence:

{finding_text}

====================================================

Generate ONLY:

{{
    "business_impact":"",
    "future_investigation":""
}}

Return VALID JSON ONLY.
"""

    # =====================================
    # SEND TO OLLAMA
    # =====================================

    print("\nSending To Ollama...\n")

    try:

        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "gemma3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.05
                }
            },
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        output = result.get(
            "response",
            ""
        )

        print("\n=================================")
        print("OLLAMA OUTPUT")
        print("=================================\n")

        print(output)

        # =====================================
        # SAVE INDIVIDUAL FILE
        # =====================================

        output_file = (
            OUTPUT_DIR
            / f"{selected_user['user_id']}.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(output)

        print(f"\nSaved To:")
        print(output_file)

    except Exception as e:

        print(
            f"\nError processing {selected_user['user_id']}: {e}"
        )

print("\n=================================")
print("ALL USERS COMPLETED")
print("=================================")