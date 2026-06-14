import streamlit as st

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Identity Risk Intelligence Dashboard",
    layout="wide"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

/* Main page spacing */
.block-container{
    padding-top:2rem;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    width:300px !important;
    background:#151824;
}

/* Sidebar Buttons */
.stButton button{
    width:100%;
    text-align:left;
    background:#1f2937;
    border:none;
    border-radius:12px;
    margin-bottom:8px;
    color:white;
    padding:12px;
    font-weight:500;
}

.stButton button:hover{
    background:#7f1d1d;
    color:white;
}

/* Metric Cards */
[data-testid="stMetric"]{
    background-color:#111827;
    border:1px solid #374151;
    padding:15px;
    border-radius:12px;
}

[data-testid="stMetric"]:hover{
    border:1px solid #60a5fa;
    box-shadow:0px 0px 10px rgba(96,165,250,0.3);
}

/* Containers */
div[data-testid="stVerticalBlockBorderWrapper"]{
    border-radius:15px;
}

/* Titles */
h1{
    font-weight:700;
}

h2{
    font-weight:600;
}

/* Investigation Status Buttons */

.green-btn button{
    background:#14532d !important;
    color:#4ade80 !important;
    border:none !important;
    border-radius:12px !important;
}

.yellow-btn button{
    background:#4d4f10 !important;
    color:#fde68a !important;
    border:none !important;
    border-radius:12px !important;
}

.red-btn button{
    background:#4c2427 !important;
    color:#ff6b6b !important;
    border:none !important;
    border-radius:12px !important;
}

.blue-btn button{
    background:#1e3a5f !important;
    color:#60a5fa !important;
    border:none !important;
    border-radius:12px !important;
}
                      
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

if "page" not in st.session_state:
    st.session_state.page = "Overview"

with st.sidebar:

    st.title("Identity Risk Intelligence")

    st.markdown("### Navigation")

    if st.button(" Overview", use_container_width=True):
        st.session_state.page = "Overview"

    if st.button(" Users and Events", use_container_width=True):
        st.session_state.page = "Users"

    if st.button(" Systems", use_container_width=True):
        st.session_state.page = "Systems"

    if st.button(" Investigations", use_container_width=True):
        st.session_state.page = "Investigations"

    st.markdown("---")
    st.caption("👩‍💻 Developed by")
    st.caption("Riya Pastay & Riddhi Pandya")

page = st.session_state.page

# =========================
# TICKET DETAILS PAGE
# =========================

if st.session_state.get("ticket_view", False):

    st.title("Investigation Ticket")

    if st.button("⬅ Back to Investigations"):
        st.session_state["ticket_view"] = False
        st.rerun()

    ticket = st.session_state["selected_ticket"]

    st.subheader(ticket["id"])

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Severity", ticket["severity"])

    with c2:
        st.metric("Status", ticket["status"])

    with c3:
        st.metric("Priority", ticket["priority"])

    st.divider()

    left, right = st.columns([2,1])

    with left:

        with st.container(border=True):

            st.markdown("### Investigation Summary")

            st.write(f"**User:** {ticket['user']}")
            st.write(f"**Finding:** {ticket['finding']}")
            st.write(f"**System:** {ticket['system']}")
            st.write(f"**Raised By:** {ticket['raised_by']}")
            st.write(f"**Assigned To:** {ticket['assigned_to']}")
            st.write(f"**Business Impact:** {ticket['impact']}")

    with right:

        with st.container(border=True):

            st.markdown("### Ticket Metadata")

            st.write(f"Created: {ticket['created']}")
            st.write(f"Last Updated: {ticket['updated']}")
            st.write(f"Department: {ticket['department']}")

    st.write("")

    with st.container(border=True):

        st.markdown("## Investigation Timeline")

        for item in ticket["timeline"]:

            st.markdown(
                f"""
### {item['time']}

**{item['title']}**

{item['description']}

---
"""
            )

    if ticket["status"] == "Resolved":

        with st.container(border=True):

            st.success("Resolution Summary")

            st.write(ticket["resolution"])

    st.stop()

# =========================
# USERS PAGE
# =========================

if page == "Users":

    if st.session_state.get("investigation_mode", False):

        st.title("Detailed Breakdown")

        if st.button("⬅ Back to Users"):
            st.session_state["investigation_mode"] = False
            st.rerun()

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button(
                "📄 Raw JSON Output",
                use_container_width=True
            ):
                st.session_state["show_json"] = True
                st.session_state["show_llm"] = False
                st.session_state["show_graph"] = False

        with c2:
            if st.button(
                "🤖 LLM Based Interpretation",
                use_container_width=True
            ):
                st.session_state["show_json"] = False
                st.session_state["show_llm"] = True
                st.session_state["show_graph"] = False

        with c3:
            if st.button(
                "🌳 Privilege Graph",
                use_container_width=True
            ):
                st.session_state["show_json"] = False
                st.session_state["show_llm"] = False
                st.session_state["show_graph"] = True

        st.divider()

        if st.session_state.get("show_json", False):

            st.code(
                """
{
        "user_id": "USR00015",
        "username": "sophia.white",
        "risk_level": "CRITICAL",
        "risk_score": 100,
        "findings": [
            {
                "finding": "ADMIN_ACCOUNT",
                "details": "Administrative privileges assigned",
                "severity": "MEDIUM",
                "recommendation": "Review privileged access"
            },
            {
                "finding": "IDENTITY_SPRAWL",
                "details": "Access across 7 systems",
                "severity": "HIGH",
                "recommendation": "Review excessive access"
            },
            {
                "finding": "EXCESSIVE_RESOURCE_ACCESS",
                "details": "Accessed 6 unique resources",
                "severity": "MEDIUM",
                "recommendation": "Review resource permissions"
            },
            {
                "finding": "HIGH_SENSITIVITY_ACCESS",
                "details": "4 accesses to sensitive resources",
                "severity": "HIGH",
                "recommendation": "Review sensitive resource usage"
            }

                """,
                language="json"
            )

        elif st.session_state.get("show_llm", False):

            st.subheader("Business Impact")

            st.warning(
                """
• The account belongs to the Security department and holds administrative privileges across 7 enterprise systems including Okta, AWS IAM, Azure AD, SIEM and ADMIN_SYS. Any misuse or compromise of this account could impact identity management, cloud access controls and security monitoring functions simultaneously.

• Access spanning 6 unique resources combined with administrative permissions creates a high blast radius. A single unauthorized action could propagate across multiple critical platforms, increasing operational disruption and reducing the ability to isolate incidents quickly.

• The account recorded 4 accesses to high-sensitivity resources despite not being a dedicated platform administrator account. Continued broad access to sensitive assets increases the risk of unauthorized configuration changes, exposure of security data, or accidental privilege misuse.
                """
            )

            st.subheader("Potential Solutions")

            st.success(
                """
• Perform an entitlement review across Okta, AWS IAM, Azure AD, SIEM, VPN, ServiceNow and ADMIN_SYS to determine whether all 7 system accesses remain necessary for the user's current responsibilities within the Security team.

• Validate the business justification for each of the 6 accessed resources and apply least-privilege controls where possible. Remove redundant permissions and restrict access to only the systems actively required for operational duties.

• Conduct a focused review of the 4 high-sensitivity resource access events, verify whether they align with approved security activities, and establish periodic access recertification to prevent future privilege accumulation.
                """
            )

        elif st.session_state.get("show_graph", False):
            st.subheader("Privilege Graph")
            st.code("""
                                    USER
                                     │
                                     ▼
                               sophia.white
                                     │
       ┌─────────────────────────────┼─────────────────────────────┐
       │                             │                             │
       ▼                             ▼                             ▼

  PRIVILEGES                  SYSTEM ACCESS                SENSITIVE ACCESS

  • Admin Account             • Okta                       • 4 Sensitive Resources
  • Elevated Permissions      • Azure AD                  • High Sensitivity Usage
                              • AWS IAM
                              • VPN
                              • SIEM
                              • ServiceNow
                              • ADMIN_SYS

                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼

             BUSINESS IMPACT                    RISK DRIVERS

     Identity Management                 ✓ Administrative Account
     Cloud Infrastructure                ✓ Access Across 7 Systems
     Security Operations                 ✓ Access To 6 Resources
     Administrative Control              ✓ 4 Sensitive Resource Events
     Resource Exposure                   ✓ Security Department User
""")

        st.stop()


    

    st.title("Users")

    st.caption(
        "Monitor stale, inactive and high-risk identities and events across the enterprise"
    )

    search = st.text_input(
        "Search users, departments, privileges..."
    )

    users = [
        ["Sophia White","USR00015","Security","Okta, SIEM, Azure_AD, ServiceNow, AWS_IAM, VPN, ADMIN_SYS",24,100,"Detailed Breakdown"],
        ["Kenneth Moore","USR00002","Sales","EMAIL, PROD_DB",13,97.4,"Detailed Breakdown"],
        ["Pooja Sullivan","USR00027","Support","VPN, Salesforce, AWS_IAM, ADMIN_SYS, SIEM, Azure_AD, ServiceNow",34,97.21,"Detailed Breakdown"],
        ["Nikhil Rao","USR00035","Executive","PROD_DB, EMAIL, ServiceNow, SIEM, Salesforce, AD",56,86.54,"Detailed Breakdown"],
        ["Paul Singh","USR00028","HR","GCP, Salesforce, EMAIL, VPN, ServiceNow, ADMIN_SYS",28,84,"Detailed Breakdown"],
        ["Nicholas Harris","USR00036","Marketing","AD, Azure_AD",40,76,"Detailed Breakdown"],
        ["George Clark","USR00047","Engineering","Azure_AD, ServiceNow",55,74.3,"Detailed Breakdown"],
        ["Robert Patel","USR00068","Support","ADMIN_SYS, PROD_DB, AWS_IAM, Salesforce, EMAIL",7,73.3,"Detailed Breakdown"],
        ["Neha Taylor","USR00077","Finance","AD, EMAIL, PROD_DB",11,70,"Detailed Breakdown"],
        ["Ryan Thomas","USR00083","Marketing","VPN, SIEM",17,62,"Detailed Breakdown"],
        ["Steven Thompson","USR00091","Support","AD, PROD_DB",28,60.6,"Detailed Breakdown"],
        ["Joseph Perez","USR00121","Security","AWS_IAM, Salesforce, ServiceNow, GCP",26,57.4,"Detailed Breakdown"],
        ["Kenneth Verma","USR00125","Marketing","SIEM, AWS_IAM, Azure_AD, EMAIL, Okta, GCP",36,56.5,"Detailed Breakdown"],
        ["Mark Patel","USR00126","Operations","ADMIN_SYS, AD, Okta, ServiceNow, GCP",43,55,"Detailed Breakdown"],
        ["Zainab Moore","USR00203","Security","SIEM, VPN, AWS_IAM, ServiceNow, EMAIL, AD, GCP",22,53,"Detailed Breakdown"],
        ["Nikhil Martinez","USR00209","Operations","SIEM, VPN",42,52,"Detailed Breakdown"],
        ["Zainab Garcia","USR00218","Sales","EMAIL, AWS_IAM, Salesforce, GCP",37,51.5,"Detailed Breakdown"],
        ["Rajesh Smith","USR00221","Engineering","Salesforce, SIEM",29,51.25,"Detailed Breakdown"],
        ["Alexander Young","USR00314","Engineering","AD, EMAIL, PROD_DB",9,50.6,"Detailed Breakdown"],
        ["Harper Walker","USR00368","Contractor","Salesforce, SIEM",10,43,"Detailed Breakdown"]
    ]

    if search:
        users = [
            user for user in users
            if search.lower() in " ".join(map(str, user)).lower()
        ]

    st.write("")

    for i in range(0, len(users), 3):

        cols = st.columns(3)

        for j in range(3):

            if i + j < len(users):

                user = users[i + j]

                with cols[j]:

                    with st.container(border=True):

                        if st.button(
                            user[0],
                            key=user[1],
                            use_container_width=True
                        ):
                            st.session_state["selected_user"] = user[0]

                        st.write(f"User ID: {user[1]}")
                        st.write(f"Department: {user[2]}")
                        st.write(f"Connected Systems: {user[3]}")
                        st.write(f"Inactive: {user[4]} Days")

                        st.metric("Risk Score", str(user[5]))

                        if st.button(
                            user[6],
                            key=f"alert_{user[1]}",
                            use_container_width=True
                        ):
                            st.session_state["investigation_mode"] = True
                            st.session_state["selected_alert"] = user[6]
                            st.session_state["selected_user"] = user[0]
                            st.rerun()


# =========================
# SYSTEMS PAGE
# =========================

elif page == "Systems":

    st.title("Systems")

    systems = [
        ["PROD_DB", "Data Engineering / Operations", "CRITICAL", "Connected"],
        ["SIEM", "Security Operations Center (SOC)", "CRITICAL", "Connected"],
        ["ADMIN_SYS", "IT Administration", "Critical", "Recent Off-Hours Access"],
        ["AWS IAM", "Cloud Security / Infrastructure", "CRITICAL", "Recent Change Activity"],
        ["GCP", "Cloud Security / Infrastructure", "CRITICAL", "Recent Off-Hours Access"],
        ["Okta", "Identity Governance Team", "High", "Operational"],
        ["VPN", "Network Security", "High", "Connected"],
        ["ServiceNow", "IT Operations", "Medium", "Operational"],
        ["Salesforce", "Sales Operations", "High", "Recent Off-Hours Access"],
        ["EMAIL", "Corporate Communications", "High", "Recent Change Activity"],
        ["AD", "IT / Infrastructure", "High", "Connected"],
        ["Azure AD", "IT / Identity & Access Management", "Medium", "Operational"]
    ]

    for i in range(0, len(systems), 3):

        cols = st.columns(3)

        for j in range(3):

            if i + j < len(systems):

                system = systems[i + j]

                with cols[j]:

                    with st.container(border=True):

                        st.subheader(system[0])

                        st.write(f"Category: {system[1]}")
                        st.write(f"Sensitivity: {system[2]}")

                        if system[3] in ["Connected", "Operational"]:
                            st.success(system[3])

                        elif "Access" in system[3]:
                            st.error(system[3])

                        else:
                            st.warning(system[3])

# =========================
# INVESTIGATIONS PAGE
# =========================

elif page == "Investigations":

    st.title("Investigations")

    investigations = [

        {
            "id":"INV-0001",
            "user":"Sophia White (USR00015)",
            "finding":"Stale_Account_Login, Overprivileged User, Credential Misuse Risk, After-Hours Activity, Suspicious Login Behavior",
            "system":"Okta, SIEM, Azure_AD, ServiceNow, AWS_IAM, VPN, ADMIN_SYS",
            "status":"Open",
            "severity":"High",
            "priority":"P1",
            "department":"HR",
            "raised_by":"SOC Alert Engine",
            "assigned_to":"Alex Johnson",
            "created":"14 Jun 2026 09:12 AM",
            "updated":"14 Jun 2026 10:48 AM",
            "impact":"Dormant account accessed after 45 days inactivity.",
            "resolution":"",
            "timeline":[
                {
                    "time":"09:12 AM",
                    "title":"Ticket Created",
                    "description":"SOC automatically generated investigation."
                },
                {
                    "time":"09:20 AM",
                    "title":"Assigned",
                    "description":"Assigned to Alex Johnson."
                },
                {
                    "time":"10:48 AM",
                    "title":"Investigation Started",
                    "description":"Identity review initiated."
                }
            ]
        },

        {
            "id":"INV-0002",
            "user":"Kenneth Verma (USR00125)",
            "finding":"Identity Sprawl,High Blast Radius,Toxic Privilege Combination,Account Compromise Indicator,High Volume Export Activity",
            "system":"SIEM, AWS_IAM, Azure_AD, EMAIL, Okta, GCP",
            "status":"Under Review",
            "severity":"Medium",
            "priority":"P2",
            "department":"Security",
            "raised_by":"Behavior Analytics Engine",
            "assigned_to":"Maria Lopez",
            "created":"13 Jun 2026 10:11 PM",
            "updated":"14 Jun 2026 08:02 AM",
            "impact":"Administrative access observed outside approved hours.",
            "resolution":"",
            "timeline":[
                {
                    "time":"10:11 PM",
                    "title":"Ticket Created",
                    "description":"After-hours login anomaly detected."
                },
                {
                    "time":"08:02 AM",
                    "title":"Security Review",
                    "description":"Analyst reviewing login legitimacy."
                }
            ]
        },

        {
            "id":"INV-0003",
            "user":"Pooja Sullivan (USR00027)",
            "finding":"Dormant Privileged Account,Privileged Inactive User,Toxic Privilege Combination,Long-Term Inactivity,Abnormal Resource Usage",
            "system":"VPN, Salesforce, AWS_IAM, ADMIN_SYS, SIEM, Azure_AD",
            "status":"Critical",
            "severity":"Critical",
            "priority":"P1",
            "department":"Database",
            "raised_by":"UEBA Engine",
            "assigned_to":"Incident Response Team",
            "created":"14 Jun 2026 12:02 AM",
            "updated":"14 Jun 2026 12:17 AM",
            "impact":"Potential unauthorized access to sensitive PII.",
            "resolution":"",
            "timeline":[
                {
                    "time":"12:02 AM",
                    "title":"Ticket Created",
                    "description":"Off-hours database access detected."
                },
                {
                    "time":"12:07 AM",
                    "title":"Escalated",
                    "description":"Escalated to Incident Response."
                },
                {
                    "time":"12:17 AM",
                    "title":"Containment",
                    "description":"Account temporarily suspended."
                }
            ]
        },

        {
            "id":"INV-0004",
            "user":"Paul Singh (USR00028)",
            "finding":"Privileged Inactive User, High Blast Radius, Cross-System Access Concentration, Access Creep",
            "system":"Salesforce, EMAIL, VPN, ServiceNow, ADMIN_SYS",
            "status":"Resolved",
            "severity":"High",
            "priority":"P2",
            "department":"Finance",
            "raised_by":"Access Governance Engine",
            "assigned_to":"Priya Shah",
            "created":"10 Jun 2026 11:41 AM",
            "updated":"11 Jun 2026 04:18 PM",
            "impact":"Unauthorized finance resource access detected.",
            "resolution":"Access request validated and permissions corrected.",
            "timeline":[
                {
                    "time":"11:41 AM",
                    "title":"Ticket Created",
                    "description":"Cross department access observed."
                },
                {
                    "time":"02:15 PM",
                    "title":"Review Started",
                    "description":"Manager approval verified."
                },
                {
                    "time":"04:18 PM",
                    "title":"Resolved",
                    "description":"Permissions corrected and ticket closed."
                }
            ]
        }
    ]

    for i in range(0, len(investigations), 2):

        cols = st.columns(2)

        for j in range(2):

            if i + j < len(investigations):

                inv = investigations[i + j]

                with cols[j]:

                    with st.container(border=True):

                        st.subheader(inv["id"])

                        st.write(f"User: {inv['user']}")
                        st.write(f"Finding: {inv['finding']}")
                        st.write(f"System: {inv['system']}")

                        if inv["status"] == "Open":

                            st.error("Recent Off-Hours Access")

                        elif inv["status"] == "Critical":

                            st.error("Critical Security Incident")

                        elif inv["status"] == "Under Review":

                            st.warning("Recent Change Activity")

                        elif inv["status"] == "Resolved":

                            st.success("Resolved")

                        if st.button(
                            "View Investigation",
                            key=f"btn_{inv['id']}",
                            use_container_width=True
                        ):
                            st.session_state["ticket_view"] = True
                            st.session_state["selected_ticket"] = inv
                            st.rerun()
                        


# =========================
# OVERVIEW PAGE
# =========================

if page == "Overview":

    st.title("Identity Risk Intelligence")

    # ==================================================
    # ENTERPRISE SNAPSHOT
    # ==================================================

    with st.container(border=True):

        st.subheader("Enterprise Snapshot")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Employees", "600")
            st.metric("Accounts", "1860")

        with c2:
            st.metric("Privileged Accounts", "120")
            st.metric("Connected Systems", "12")

        with c3:
            st.metric("Critical Assets", "42")
            st.metric("Identity Sprawl Ratio", "3.1x")

    # ==================================================
    # ENTERPRISE IDENTITY RISK
    # ==================================================

    import plotly.graph_objects as go

    with st.container(border=True):

        st.subheader("Enterprise Identity Risk")

        top_left, top_right = st.columns([3,1])

        risk_score = 83

        with top_left:

            st.markdown(
                "<h4 style='text-align:center;'>Enterprise Risk Score</h4>",
                unsafe_allow_html=True
            )

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_score,

                number={
                    "font": {"size": 50}
                },

                gauge={
                    "axis": {
                        "range": [0, 100],
                        "tickwidth": 2,
                        "tickcolor": "white"
                    },

                    "bar": {
                        "color": "white",
                        "thickness": 0.20
                    },

                    "bgcolor": "rgba(0,0,0,0)",

                    "steps": [
                        {"range": [0, 30], "color": "#22c55e"},
                        {"range": [30, 70], "color": "#facc15"},
                        {"range": [70, 100], "color": "#ef4444"}
                    ],

                    "threshold": {
                        "line": {
                            "color": "white",
                            "width": 8
                        },
                        "thickness": 0.8,
                        "value": risk_score
                    }
                }
            ))

            fig.update_layout(
                height=280,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor="#030712",
                plot_bgcolor="#030712",
                font={"color": "white"}
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with top_right:

            st.error("HIGH")

            st.caption("Last Updated: 10:32:17 AM")

            show_breakdown = st.button(
                "View Risk Breakdown",
                use_container_width=True
            )


    # ==================================================
    # RISK ANALYSIS
    # ==================================================

    if show_breakdown:

        st.write("")
        st.divider()

        st.subheader("Risk Analysis")

        col1, col2 = st.columns([2,1])

        with col1:

            st.markdown("## Risk Categories")

            st.write("Privilege Abuse - 42%")
            st.progress(42)

            st.write("Stale Accounts - 31%")
            st.progress(31)

            st.write("Compliance Violations - 18%")
            st.progress(18)

            st.write("Orphaned Accounts - 9%")
            st.progress(9)

        with col2:

            st.markdown("## Risk Summary")

            r1, r2 = st.columns(2)

            with r1:
                st.metric("High Risk", "42")
                st.metric("Stale", "31")

            with r2:
                st.metric("Compliance", "18")
                st.metric("Orphaned", "9")

    # ==================================================
    # RISK BY DEPARTMENT
    # ==================================================

    st.write("")

    with st.container(border=True):

        st.subheader("Risk By Department")

        header = st.columns([2,1,1,1,1,1,1])

        header[0].markdown("**Department**")
        header[1].markdown("**Stale**")
        header[2].markdown("**Over Priviledged**")
        header[3].markdown("**Orphaned**")
        header[4].markdown("**Compliance**")
        header[5].markdown("**Toxic**")
        header[6].markdown("**Assets**")

        st.divider()

        departments = [

            ["Engineering","🟡","🔴","🟢","🟡","🔴","🟡"],
            ["Finance","🔴","🔴","🟡","🔴","🟡","🔴"],
            ["HR","🟢","🟡","🟢","🟡","🟡","🟢"],
            ["Security","🟡","🟢","🟢","🟢","🟢","🟡"]

        ]

        for row in departments:

            cols = st.columns([2,1,1,1,1,1,1])

            cols[0].write(row[0])

            for i in range(1,7):

                if cols[i].button(
                    row[i],
                    key=f"{row[0]}_{i}"
                ):

                    st.session_state["selected_risk"] = {
                        "department": row[0],
                        "category": [
                            "Stale",
                            "Over Privileged",
                            "Orphaned",
                            "Compliance",
                            "Toxic",
                            "Assets"
                        ][i-1],
                        "status": row[i]
                    }

    # ==================================================
    # RISK DETAILS
    # ==================================================

    if "selected_risk" in st.session_state:

        risk = st.session_state["selected_risk"]

        st.write("")

        with st.container(border=True):

            st.subheader(
                f"{risk['department']} - {risk['category']}"
            )

            if risk["status"] == "🔴":
                st.error("HIGH RISK")

            elif risk["status"] == "🟡":
                st.warning("MEDIUM RISK")

            else:
                st.success("LOW RISK")

            st.write(
                """
Affected Users: 14

Finding:
Multiple user logins detected, connected to high number of systems and odd hours of access witnessed.

Recommendation:
Review authentication, access and activity logs to validate legitimacy of recent behavior and findings.
Re-certify account ownership, business justification and privileged access through the identity governance process.
                """
            )

    # ==================================================
    # ANOMALY DISTRIBUTION
    # ==================================================

    st.write("")

    with st.container(border=True):

        st.subheader("Anomaly Distribution")

        import pandas as pd

        chart_data = pd.DataFrame(
            {
                "Anomalies": [56, 21, 49, 10, 53, 24,9,67,32,11,67,87]
            },
            index=[
                "STALE_ACCOUNT_LOGIN",
                "AFTER_HOURS_ADMIN_LOGIN",
                "OFF_HOURS_DB_ACCESS",
                "CROSS_DEPARTMENT_ACCESS",
                "EXCESS_PRIVILEGE_USAGE",
                "ORPHANED_ACCOUNT_ACTIVITY",
                "Repeated_Login_Failures",
                "Repeated_sensitive_data_storage",
                "CROSS_PLATFORM_IDENTITY_EXPANSION",
                "PRIVILEGE_ACCUMULATION",
                "EXCESSIVE_NIGH_TIME_ACCESS",
                "WEEKEND_ACCESS_ACTIVITY"
            ]
        )

        st.bar_chart(chart_data)