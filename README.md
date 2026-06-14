This is Team Skylens final submission for the Societe Generale Hackathon for the PS-1 : Identity Sprawl & Privilege Abuse Detection.
The following is the complete codebase structure: 
Team_Skylens_PS1_SocGen_Hackathon/
│
├── 1. config/
│   ├── __init__.py
│   ├── config.py
│   └── __pycache__/
│
├── 2. Datasets/
│   │
│   ├── 1. Raw_Original_datasets/
│   │   ├── identity_events.csv
│   │   └── identity_users.csv
│   │
│   ├── 2. Synthetic_datasets/
│   │   ├── identity_events_1800_combined.csv
│   │   └── identity_users_600_combined.csv
│   │
│   ├── 3. Feature_matrix/
│   │   └── feature_matrix.csv
│   │
│   ├── 4. Model_outputs/
│   │   ├── anomaly_output.csv
│   │   ├── final_risk_output.csv
│   │   └── rule_engine_output.csv
│   │
│   ├── 5. Final_Reports/
│   │   ├── final_soc_report.csv
│   │   └── findings_output.json
│   │
│   └── 6. LLM_reports/
│       └── USR00002.json
│
├── 3. Src/
│   ├── 01. feature_engineering.py
│   ├── 02. rule_engine.py
│   ├── 03. anomaly_detection.py
│   ├── 04. risk_fusion.py
│   ├── 05. explainability.py
│   ├── 06. findings_generator.py
│   └── 07. llm_analyst.py
│
├── 4. Dashboard/
│   ├── app.py
│   ├── identity_details.py
│   └── requirements.txt
│
├── notebook/
│
└── Outputs/
