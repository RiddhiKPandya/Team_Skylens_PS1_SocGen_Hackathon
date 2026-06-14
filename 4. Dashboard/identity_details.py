import streamlit as st

st.title("Identity Details")

st.subheader("John Smith")

st.metric("Risk Score", "95")

st.error("Critical")

st.write("### Issues")

st.write("✓ Stale Account")
st.write("✓ Over Privileged")
st.write("✓ Toxic Combination")

st.write("### Business Impact")

st.write("✓ Customer Data")
st.write("✓ Financial Data")

st.metric("Confidence", "94%")