import streamlit as st

# Page ko title ra icon set garne
st.set_page_config(page_title="Telecom Complaint Dashboard", page_icon="📞")

# Main heading
st.title("📞 Telecom Complaint Auto-Router - Dashboard")

# Subheading / description
st.write("Yo dashboard le complaint routing system ko test interface dinxa.")

# User input box - complaint text halne
complaint_text = st.text_area("Complaint ko text yaha halnuhos:")

# Category select garne dropdown
category = st.selectbox(
    "Complaint category:",
    ["Network Issue", "Billing Issue", "SIM/Recharge", "Other"]
)

# Button click bhaye pachi ko action
if st.button("Route Complaint"):
    if complaint_text:
        st.success(f"Complaint '{category}' category maa route bhayo!")
        st.write(f"**Received complaint:** {complaint_text}")
    else:
        st.error("Kripaya complaint text halnuhos.")

# Sidebar - extra info
with st.sidebar:
    st.header("System Status")
    st.metric(label="Total Complaints Today", value=42, delta=5)
    st.metric(label="Auto-Resolved", value=30, delta=-2)