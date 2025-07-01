import streamlit as st
import os

st.title("🕵️ Packet Monitor Viewer")

# List logs
log_dir = "docs"
logs = [f for f in os.listdir(log_dir) if f.startswith("logs_")]
selected_log = st.selectbox("Select a log file:", logs)

# Display contents
if selected_log:
    with open(os.path.join(log_dir, selected_log), "r") as file:
        content = file.read()
    st.text_area("Log Contents", content, height=400)
