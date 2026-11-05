
import streamlit as st
from datetime import datetime
from uuid import uuid4

from modules.database import (
    initialize_database,
    save_report,
    get_all_reports,
    delete_report
)

from modules.ai import ask_groq


def show_village_planner():

    # Black font styling for this module
    st.markdown("""
    <style>
    .st-key-village_planner_page {
        color: #000000 !important;
    }

    .st-key-village_planner_page h1,
    .st-key-village_planner_page h2,
    .st-key-village_planner_page h3,
    .st-key-village_planner_page p,
    .st-key-village_planner_page label,
    .st-key-village_planner_page span,
    .st-key-village_planner_page li {
        color: #000000 !important;
    }

    .st-key-village_planner_page input,
    .st-key-village_planner_page textarea {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container(key="village_planner_page"):

        initialize_database()

        st.title("🏡 Village Development Planner")
        st.write(
            "Report village problems, save them and explore AI-powered solutions."
        )

        st.subheader("1. Report a Village Problem")

        report_method = st.radio(
            "How would you like to report?",
            ["Manual Report", "Map Location"],
            horizontal=True,
            key="planner_report_method"
        )

        problem_types = [
            "Road Damage",
            "Water Shortage",
            "Drainage Problem",
            "Electricity Problem",
            "Waste Management",
            "Flooding",
            "School / Hospital Need",
            "Other"
        ]

        with st.form("village_problem_form", clear_on_submit=True):

            problem = st.selectbox(
                "Problem Category",
                problem_types
            )

            description = st.text_area(
                "Describe the problem",
                placeholder="Example: The village road gets flooded during rain..."
            )

            location = st.text_input(
                "Village / Area Name",
                placeholder="Enter village and area name"
            )

            photo = st.file_uploader(
                "Upload a problem photo (optional)",
                type=["jpg", "jpeg", "png"]
            )

            map_note = ""

            if report_method == "Map Location":
                map_note = st.text_input(
                    "Map location or coordinates",
                    placeholder="Enter location or coordinates"
                )

            submitted = st.form_submit_button(
                "Save Village Problem",
                type="primary"
            )

        if submitted:

            if not description.strip() or not location.strip():
                st.warning(
                    "Please enter the problem description and location."
                )

            elif report_method == "Map Location" and not map_note.strip():
                st.warning(
                    "Please enter the map location or coordinates."
                )

            else:
                report = {
                    "id": str(uuid4())[:8],
                    "category": problem,
                    "description": description.strip(),
                    "location": location.strip(),
                    "report_method": report_method,
                    "map_location": map_note.strip(),
                    "photo_name": photo.name if photo else None,
                    "photo_bytes": photo.getvalue() if photo else None,
                    "submitted_at": datetime.now().isoformat(
                        timespec="seconds"
                    )
                }

                try:
                    save_report(report)
                    st.success("Village problem saved successfully!")
                    st.rerun()

                except Exception as error:
                    st.error(f"Could not save report: {error}")

        st.divider()
        st.subheader("2. Saved Village Reports")

        try:
            reports = get_all_reports()

        except Exception as error:
            st.error(f"Could not load reports: {error}")
            reports = []

        st.metric("Total Reports", len(reports))

        if not reports:
            st.info("No reports saved yet.")

        for report in reports:

            with st.expander(
                f"{report['category']} — {report['location']} ({report['id']})"
            ):

                st.write("**Report ID:**", report["id"])
                st.write("**Category:**", report["category"])
                st.write("**Village / Area:**", report["location"])
                st.write("**Description:**", report["description"])
                st.write("**Report Method:**", report["report_method"])
                st.write("**Submitted:**", report["submitted_at"])

                if report["map_location"]:
                    st.write(
                        "**Map Location:**",
                        report["map_location"]
                    )

                if report["photo_name"]:
                    st.write("**Photo:**", report["photo_name"])

                    if report["photo_bytes"]:
                        st.image(
                            report["photo_bytes"],
                            caption="Uploaded problem photo",
                            use_container_width=True
                        )

                if st.button(
                    "Delete This Report",
                    key=f"delete_{report['id']}"
                ):
                    try:
                        delete_report(report["id"])
                        st.success("Report deleted.")
                        st.rerun()

                    except Exception as error:
                        st.error(f"Could not delete report: {error}")

        # GROQ AI ANALYSIS
        st.divider()
        st.subheader("3. 🤖 AI Problem Analysis")

        st.write(
            "Select a saved village report to get practical suggestions "
            "from SmartGaon AI."
        )

        if reports:

            report_options = {
                f"{r['category']} — {r['location']} ({r['id']})": r
                for r in reports
            }

            selected_report_name = st.selectbox(
                "Choose a report for AI analysis:",
                list(report_options.keys()),
                key="planner_ai_report"
            )

            selected_report = report_options[selected_report_name]

            if st.button(
                "🤖 Analyze Village Problem",
                type="primary",
                use_container_width=True
            ):

                prompt = f"""
You are SmartGaon AI, a helpful village development assistant.

Analyze this reported village problem.

Category: {selected_report['category']}
Village or area: {selected_report['location']}
Problem description: {selected_report['description']}
Report method: {selected_report['report_method']}
Map location: {selected_report['map_location'] or 'Not provided'}

Give your response in simple, practical language.

Include:
1. Understanding of the problem.
2. Possible causes.
3. Practical solutions.
4. Suggested priority: Low, Medium or High, with reason.
5. Which local authorities or qualified professionals may need to be contacted.
6. Affordable steps the community can consider.

Do not invent facts about the village.
Mention when an on-site inspection or expert advice is needed.
"""

                with st.spinner(
                    "SmartGaon AI is analyzing the report..."
                ):

                    try:
                        answer, error = ask_groq(prompt)

                        if error:
                            st.error(error)

                        elif answer:
                            st.session_state["planner_ai_result"] = answer
                            st.session_state["planner_ai_result_id"] = (
                                selected_report["id"]
                            )

                        else:
                            st.error(
                                "AI returned an empty response. Please try again."
                            )

                    except Exception as error:
                        st.error(f"AI analysis failed: {error}")

            if (
                st.session_state.get("planner_ai_result")
                and st.session_state.get("planner_ai_result_id")
                == selected_report["id"]
            ):
                st.markdown("### AI Analysis Result")
                st.markdown(
                    st.session_state["planner_ai_result"]
                )

        else:
            st.info(
                "Save a village report first to use AI Problem Analysis."
            )
