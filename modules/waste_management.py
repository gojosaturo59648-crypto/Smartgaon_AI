
import streamlit as st


def show_waste_management():

    # ---------- PAGE STYLE ----------
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

    st.title("♻️ Waste Management")
    st.write(
        "Manage waste responsibly and help keep your village clean and healthy."
    )

    # ---------- SESSION STORAGE ----------
    if "waste_reports" not in st.session_state:
        st.session_state.waste_reports = []

    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Report Waste",
        "📋 Waste Reports",
        "♻️ Segregation Guide",
        "🌱 Recycling Tips"
    ])

    # ==================================================
    # TAB 1: REPORT WASTE
    # ==================================================
    with tab1:
        st.subheader("Report a Waste Problem")

        with st.form("waste_report_form"):

            location = st.text_input(
                "Village / Location",
                placeholder="Example: Near village school"
            )

            waste_type = st.selectbox(
                "Type of Waste",
                [
                    "Plastic Waste",
                    "Food / Organic Waste",
                    "Paper Waste",
                    "Glass Waste",
                    "Metal Waste",
                    "Electronic Waste",
                    "Medical / Hazardous Waste",
                    "Mixed Waste"
                ]
            )

            description = st.text_area(
                "Describe the problem",
                placeholder="Describe where the waste is and what happened..."
            )

            priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High"]
            )

            submit_report = st.form_submit_button(
                "Submit Waste Report",
                type="primary"
            )

        if submit_report:
            if location.strip() and description.strip():

                st.session_state.waste_reports.append({
                    "location": location.strip(),
                    "type": waste_type,
                    "description": description.strip(),
                    "priority": priority,
                    "status": "Pending"
                })

                st.success("Waste report submitted successfully!")

            else:
                st.error("Please enter location and problem description.")

    # ==================================================
    # TAB 2: WASTE REPORTS
    # ==================================================
    with tab2:
        st.subheader("Community Waste Reports")

        reports = st.session_state.waste_reports

        if reports:
            total = len(reports)
            pending = sum(
                1 for r in reports if r["status"] == "Pending"
            )
            completed = sum(
                1 for r in reports if r["status"] == "Completed"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Reports", total)
            col2.metric("Pending", pending)
            col3.metric("Completed", completed)

            st.divider()

            for i, report in enumerate(reports):
                with st.expander(
                    f"{report['type']} — {report['location']}"
                ):
                    st.write("**Location:**", report["location"])
                    st.write("**Waste Type:**", report["type"])
                    st.write("**Description:**", report["description"])
                    st.write("**Priority:**", report["priority"])
                    st.write("**Status:**", report["status"])

                    new_status = st.selectbox(
                        "Update Status",
                        ["Pending", "In Progress", "Completed"],
                        index=[
                            "Pending",
                            "In Progress",
                            "Completed"
                        ].index(report["status"]),
                        key=f"waste_status_{i}"
                    )

                    if st.button(
                        "Update Report",
                        key=f"update_waste_{i}"
                    ):
                        report["status"] = new_status
                        st.success("Report status updated!")
                        st.rerun()

                    if st.button(
                        "Delete Report",
                        key=f"delete_waste_{i}"
                    ):
                        reports.pop(i)
                        st.rerun()

        else:
            st.info("No waste reports yet. Submit your first report.")

        st.caption(
            "Reports are stored during the current app session only. "
            "Permanent database storage is not connected."
        )

    # ==================================================
    # TAB 3: WASTE SEGREGATION
    # ==================================================
    with tab3:
        st.subheader("Waste Segregation Guide")

        segregation = {
            "🟢 Wet / Organic Waste": (
                "Vegetable peels, leftover food and garden waste. "
                "These can often be composted."
            ),
            "🔵 Dry Recyclable Waste": (
                "Clean paper, cardboard, plastic bottles, glass "
                "and suitable metal containers."
            ),
            "🔴 Hazardous Waste": (
                "Batteries, chemicals, paint and other hazardous items. "
                "Keep them separate and use authorised collection services."
            ),
            "🟡 Electronic Waste": (
                "Old phones, chargers, wires and electronic devices. "
                "Give them to authorised e-waste collection or recycling centres."
            )
        }

        for category, detail in segregation.items():
            with st.expander(category):
                st.write(detail)

        st.warning(
            "Never mix hazardous or electronic waste with ordinary household waste."
        )

    # ==================================================
    # TAB 4: RECYCLING TIPS
    # ==================================================
    with tab4:
        st.subheader("Simple Ways to Reduce Waste")

        tips = [
            (
                "🥬 Compost Organic Waste",
                "Use suitable kitchen and garden waste to make compost."
            ),
            (
                "🛍️ Reduce Single-Use Plastic",
                "Carry reusable bags and bottles where possible."
            ),
            (
                "📦 Reuse Materials",
                "Reuse containers, boxes and other safe household items."
            ),
            (
                "♻️ Recycle Properly",
                "Keep recyclable materials clean and separated."
            ),
            (
                "🔋 Dispose of Batteries Safely",
                "Take used batteries to an authorised collection point."
            ),
            (
                "🤝 Community Cleanliness",
                "Encourage neighbours to keep public spaces clean."
            )
        ]

        for title, detail in tips:
            with st.expander(title):
                st.write(detail)

        st.success(
            "Small actions by every household can help create a cleaner village!"
        )
