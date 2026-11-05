
import streamlit as st


def show_electricity():

    # ---------- FONT STYLING ----------
    st.markdown("""
    <style>
    .stApp h1, .stApp h2, .stApp h3,
    .stApp p, .stApp label,
    .stApp span, .stApp li,
    .stApp [data-testid="stMarkdownContainer"] {
        color: #000000 !important;
    }

    .stApp input, .stApp textarea,
    .stApp [data-baseweb="select"] * {
        color: #ffffff !important;
    }

    .stApp [data-testid="stRadio"] label,
    .stApp [data-testid="stCheckbox"] label {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("💡 Light & Electricity Management")
    st.write(
        "Monitor electricity issues, report streetlight problems "
        "and learn how to save energy."
    )

    # ---------- SESSION STORAGE ----------
    if "electricity_reports" not in st.session_state:
        st.session_state.electricity_reports = []

    if "streetlight_reports" not in st.session_state:
        st.session_state.streetlight_reports = []

    # ---------- TABS ----------
    tab1, tab2, tab3, tab4 = st.tabs([
        "⚡ Electricity Issues",
        "💡 Streetlights",
        "📋 Reports",
        "🌱 Energy Saving"
    ])

    # ==================================================
    # TAB 1: ELECTRICITY ISSUES
    # ==================================================
    with tab1:
        st.subheader("Report Electricity Problems")

        with st.form("electricity_report_form"):

            location = st.text_input(
                "Village / Area",
                placeholder="Example: Near village school"
            )

            issue = st.selectbox(
                "Problem Type",
                [
                    "Power Cut",
                    "Low Voltage",
                    "Electricity Fluctuation",
                    "Damaged Electric Pole",
                    "Exposed / Damaged Wire",
                    "Other"
                ]
            )

            description = st.text_area(
                "Problem Description",
                placeholder="Describe the electricity problem..."
            )

            priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High", "Urgent"]
            )

            submitted = st.form_submit_button(
                "Submit Electricity Report",
                type="primary"
            )

        if submitted:
            if location.strip() and description.strip():

                st.session_state.electricity_reports.append({
                    "location": location.strip(),
                    "issue": issue,
                    "description": description.strip(),
                    "priority": priority,
                    "status": "Pending"
                })

                st.success("Electricity report submitted successfully!")

            else:
                st.error("Please enter location and problem description.")

        st.warning(
            "Never touch damaged wires, electric poles or electrical equipment. "
            "Keep away and inform a trusted adult and electricity authorities."
        )

    # ==================================================
    # TAB 2: STREETLIGHT MANAGEMENT
    # ==================================================
    with tab2:
        st.subheader("Streetlight Problem Reporting")

        with st.form("streetlight_form"):

            light_location = st.text_input(
                "Streetlight Location",
                placeholder="Example: Main village road"
            )

            light_issue = st.selectbox(
                "Streetlight Problem",
                [
                    "Light Not Working",
                    "Light Flickering",
                    "Damaged Streetlight",
                    "Pole Damage",
                    "Other"
                ]
            )

            light_description = st.text_area(
                "Additional Details"
            )

            light_submit = st.form_submit_button(
                "Submit Streetlight Report",
                type="primary"
            )

        if light_submit:
            if light_location.strip():

                st.session_state.streetlight_reports.append({
                    "location": light_location.strip(),
                    "issue": light_issue,
                    "description": light_description.strip(),
                    "status": "Pending"
                })

                st.success("Streetlight report submitted!")

            else:
                st.error("Please enter the streetlight location.")

    # ==================================================
    # TAB 3: REPORT MANAGEMENT
    # ==================================================
    with tab3:
        st.subheader("Electricity Reports")

        reports = st.session_state.electricity_reports
        lights = st.session_state.streetlight_reports

        total = len(reports) + len(lights)

        pending = sum(
            1 for r in reports + lights
            if r["status"] == "Pending"
        )

        completed = sum(
            1 for r in reports + lights
            if r["status"] == "Completed"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Reports", total)
        col2.metric("Pending", pending)
        col3.metric("Completed", completed)

        st.divider()

        st.markdown("### Electricity Complaints")

        if reports:
            for i, report in enumerate(reports):

                with st.expander(
                    f"{report['issue']} — {report['location']}"
                ):
                    st.write("**Location:**", report["location"])
                    st.write("**Problem:**", report["description"])
                    st.write("**Priority:**", report["priority"])
                    st.write("**Status:**", report["status"])

                    new_status = st.selectbox(
                        "Update Status",
                        ["Pending", "In Progress", "Completed"],
                        index=[
                            "Pending", "In Progress", "Completed"
                        ].index(report["status"]),
                        key=f"electricity_status_{i}"
                    )

                    if st.button(
                        "Update Report",
                        key=f"update_electricity_{i}"
                    ):
                        report["status"] = new_status
                        st.rerun()

                    if st.button(
                        "Delete Report",
                        key=f"delete_electricity_{i}"
                    ):
                        reports.pop(i)
                        st.rerun()
        else:
            st.info("No electricity complaints yet.")

        st.divider()
        st.markdown("### Streetlight Complaints")

        if lights:
            for i, report in enumerate(lights):

                with st.expander(
                    f"{report['issue']} — {report['location']}"
                ):
                    st.write("**Location:**", report["location"])
                    st.write("**Details:**", report["description"])
                    st.write("**Status:**", report["status"])

                    new_status = st.selectbox(
                        "Update Status",
                        ["Pending", "In Progress", "Completed"],
                        index=[
                            "Pending", "In Progress", "Completed"
                        ].index(report["status"]),
                        key=f"streetlight_status_{i}"
                    )

                    if st.button(
                        "Update Status",
                        key=f"update_light_{i}"
                    ):
                        report["status"] = new_status
                        st.rerun()

                    if st.button(
                        "Delete Report",
                        key=f"delete_light_{i}"
                    ):
                        lights.pop(i)
                        st.rerun()
        else:
            st.info("No streetlight complaints yet.")

        st.caption(
            "Reports are stored during the current app session only. "
            "Permanent database storage is not connected."
        )

    # ==================================================
    # TAB 4: ENERGY SAVING
    # ==================================================
    with tab4:
        st.subheader("Save Electricity, Save Energy")

        tips = {
            "💡 Use LED Bulbs": (
                "LED bulbs generally use less electricity "
                "than traditional incandescent bulbs."
            ),
            "🔌 Switch Off Appliances": (
                "Switch off lights, fans and appliances when not needed."
            ),
            "☀️ Use Solar Energy": (
                "Solar panels can provide renewable electricity "
                "where suitable."
            ),
            "🌬️ Use Fans Efficiently": (
                "Use fans when needed and switch them off "
                "when leaving a room."
            ),
            "🏠 Natural Daylight": (
                "Use sunlight during daytime instead of unnecessary lighting."
            ),
            "🔋 Energy Efficient Appliances": (
                "Choose energy-efficient appliances when possible."
            )
        }

        for title, detail in tips.items():
            with st.expander(title):
                st.write(detail)

        st.success(
            "Saving electricity helps households and communities."
        )

        st.info(
            "For electrical repairs, always contact a qualified electrician."
        )
