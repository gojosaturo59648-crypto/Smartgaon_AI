
import streamlit as st
from datetime import date, timedelta


def show_study_planner():

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

    st.title("📚 Smart Study Planner")
    st.write("Plan your studies, manage tasks and track your progress.")

    # ---------- SESSION STATE ----------
    if "study_tasks" not in st.session_state:
        st.session_state.study_tasks = []

    if "study_timetable" not in st.session_state:
        st.session_state.study_timetable = []

    tab1, tab2, tab3 = st.tabs([
        "📝 Daily Tasks",
        "🗓️ Timetable",
        "📊 Progress"
    ])

    # ---------- DAILY TASKS ----------
    with tab1:
        st.subheader("Add a Study Task")

        with st.form("study_task_form"):
            subject = st.selectbox(
                "Select Subject",
                [
                    "Mathematics",
                    "Science",
                    "English",
                    "Social Science",
                    "Computer Science",
                    "Hindi",
                    "Other"
                ]
            )

            task = st.text_input(
                "What do you need to study?",
                placeholder="Example: Complete Chapter 3"
            )

            task_date = st.date_input(
                "Study Date",
                value=date.today()
            )

            priority = st.selectbox(
                "Priority",
                ["High", "Medium", "Low"]
            )

            submitted = st.form_submit_button(
                "Add Task",
                type="primary"
            )

            if submitted:
                if task.strip():
                    st.session_state.study_tasks.append({
                        "subject": subject,
                        "task": task.strip(),
                        "date": task_date,
                        "priority": priority,
                        "completed": False
                    })
                    st.success("Study task added!")
                else:
                    st.warning("Please enter a task.")

        st.divider()
        st.subheader("Your Study Tasks")

        selected_date = st.date_input(
            "Show tasks for",
            value=date.today(),
            key="task_filter_date"
        )

        tasks = [
            (i, item)
            for i, item in enumerate(st.session_state.study_tasks)
            if item["date"] == selected_date
        ]

        if not tasks:
            st.info("No tasks for this date. Add a new task above.")
        else:
            for index, item in tasks:
                col1, col2 = st.columns([5, 1])

                with col1:
                    checked = st.checkbox(
                        f"{item['subject']} — {item['task']}",
                        value=item["completed"],
                        key=f"task_done_{index}"
                    )

                    st.caption(
                        f"Priority: {item['priority']} | "
                        f"Date: {item['date']}"
                    )

                    if checked != item["completed"]:
                        st.session_state.study_tasks[index]["completed"] = checked
                        st.rerun()

                with col2:
                    if st.button("🗑️", key=f"delete_task_{index}"):
                        st.session_state.study_tasks.pop(index)
                        st.rerun()

    # ---------- TIMETABLE ----------
    with tab2:
        st.subheader("Create Your Study Timetable")

        with st.form("timetable_form"):
            day = st.selectbox(
                "Select Day",
                [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday"
                ]
            )

            timetable_subject = st.text_input(
                "Subject",
                placeholder="Example: Mathematics"
            )

            study_time = st.text_input(
                "Study Time",
                placeholder="Example: 5:00 PM - 6:00 PM"
            )

            timetable_task = st.text_input(
                "Topic / Activity",
                placeholder="Example: Practice Algebra"
            )

            timetable_submit = st.form_submit_button(
                "Add to Timetable",
                type="primary"
            )

            if timetable_submit:
                if timetable_subject.strip() and study_time.strip():
                    st.session_state.study_timetable.append({
                        "day": day,
                        "subject": timetable_subject.strip(),
                        "time": study_time.strip(),
                        "activity": timetable_task.strip()
                    })
                    st.success("Timetable entry added!")
                else:
                    st.warning("Please enter subject and study time.")

        st.divider()
        st.subheader("Weekly Timetable")

        selected_day = st.selectbox(
            "View Day",
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ],
            key="view_timetable_day"
        )

        day_entries = [
            (i, item)
            for i, item in enumerate(st.session_state.study_timetable)
            if item["day"] == selected_day
        ]

        if not day_entries:
            st.info("No timetable entries for this day.")
        else:
            for index, item in day_entries:
                with st.container(border=True):
                    st.write(f"**{item['time']}**")
                    st.write(f"📘 {item['subject']}")
                    if item["activity"]:
                        st.write(item["activity"])

                    if st.button(
                        "Delete",
                        key=f"delete_timetable_{index}"
                    ):
                        st.session_state.study_timetable.pop(index)
                        st.rerun()

    # ---------- PROGRESS ----------
    with tab3:
        st.subheader("Your Learning Progress")

        all_tasks = st.session_state.study_tasks
        total = len(all_tasks)
        completed = sum(
            1 for item in all_tasks if item["completed"]
        )
        pending = total - completed

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Tasks", total)
        col2.metric("Completed", completed)
        col3.metric("Pending", pending)

        progress = completed / total if total else 0

        st.write("Overall Completion")
        st.progress(progress)
        st.write(f"{progress * 100:.1f}% completed")

        st.divider()
        st.subheader("Study Tips")

        tips = [
            "Break large chapters into smaller tasks.",
            "Take short breaks between study sessions.",
            "Revise previously studied topics regularly.",
            "Keep your phone away during focused study time.",
            "Get enough sleep and maintain a balanced routine."
        ]

        for tip in tips:
            st.write("•", tip)

        if st.button("Reset All Study Tasks"):
            st.session_state.study_tasks = []
            st.session_state.study_timetable = []
            st.rerun()

        st.caption(
            "Your tasks and timetable are stored in the current "
            "Streamlit session. They are not permanently saved."
        )
