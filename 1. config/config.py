# ==========================================
# IAM / Identity Systems
# ==========================================

IAM_SYSTEMS = [
    "AD",
    "Azure_AD",
    "AWS_IAM",
    "Okta",
    "GCP"
]

# ==========================================
# Critical Systems
# ==========================================

CRITICAL_SYSTEMS = [
    "ADMIN_SYS",
    "PROD_DB",
    "AWS_IAM",
    "Azure_AD",
    "Okta",
    "SIEM"
]

# ==========================================
# High Risk Resources
# ==========================================

HIGH_RISK_RESOURCES = [
    "Customer_Vault",
    "PROD_DB",
    "ADMIN_SYS",
    "HRIS",
    "SIEM"
]

# ==========================================
# Departments
# ==========================================

EXECUTIVE_ROLES = [
    "Executive",
    "Director",
    "Architect"
]

SECURITY_DEPARTMENTS = [
    "Security"
]

FINANCE_DEPARTMENTS = [
    "Finance"
]

# ==========================================
# Risk Thresholds
# ==========================================

STALE_THRESHOLD = 30

HIGH_INACTIVE_THRESHOLD = 60

NEW_HIRE_DAYS = 30

IDENTITY_SPRAWL_THRESHOLD = 5

CRITICAL_SYSTEM_THRESHOLD = 3

BLAST_RADIUS_THRESHOLD = 15

