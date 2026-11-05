
import streamlit as st
from modules.ai import ask_groq


def show_career_finder():

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

    st.title("🎯 Career Finder")
    st.write(
        "Discover career paths based on your interests, "
        "education and favourite subjects."
    )

    tab1, tab2, tab3 = st.tabs([
        "🔍 Find My Career",
        "📘 Career Information",
        "🧭 My Career Roadmap"
    ])

    # ---------- CAREER FINDER ----------
    with tab1:
        st.subheader("Tell us about yourself")

        name = st.text_input(
            "Your Name (Optional)",
            placeholder="Enter your name"
        )

        education = st.selectbox(
            "Current Education Level",
            [
                "Class 6",
                "Class 7",
                "Class 8",
                "Class 9",
                "Class 10",
                "Class 11",
                "Class 12",
                "College Student",
                "Graduate",
                "Other"
            ]
        )

        subjects = st.multiselect(
            "Which subjects do you enjoy?",
            [
                "Science",
                "Mathematics",
                "Computer Science",
                "English",
                "Social Science",
                "Arts",
                "Commerce",
                "Agriculture",
                "Biology"
            ]
        )

        interests = st.multiselect(
            "What are you interested in?",
            [
                "Technology & Computers",
                "Science & Research",
                "Teaching & Education",
                "Medicine & Healthcare",
                "Defence & Navy",
                "Farming & Agriculture",
                "Business & Entrepreneurship",
                "Art & Designing",
                "Sports & Fitness",
                "Government Services",
                "Environment & Nature",
                "Engineering",
                "Law & Public Service"
            ]
        )

        skills = st.multiselect(
            "What skills do you enjoy using?",
            [
                "Problem Solving",
                "Communication",
                "Creativity",
                "Leadership",
                "Teamwork",
                "Logical Thinking",
                "Practical Work",
                "Helping Others"
            ]
        )

        extra = st.text_area(
            "Anything else you want us to know? (Optional)",
            placeholder="Write about your goals or interests..."
        )

        if st.button("Find My Career 🚀", type="primary"):
            if not interests:
                st.warning("Please select at least one interest.")
            elif not subjects:
                st.warning("Please select at least one favourite subject.")
            else:
                prompt = f"""
You are the Career Guidance Assistant inside SmartGaon AI.

Give beginner-friendly and realistic career guidance to a student.

Student details:
Name: {name or "Not provided"}
Education: {education}
Favourite subjects: {", ".join(subjects)}
Interests: {", ".join(interests)}
Skills: {", ".join(skills) if skills else "Not provided"}
Additional information: {extra or "Not provided"}

Please provide:

1. Five suitable career options based on the student's interests.
2. For each career, explain what the person does.
3. Mention relevant school subjects and skills.
4. Explain the general education or training path.
5. Mention possible entrance exams or eligibility requirements
   only when you are confident. Otherwise say to verify current rules.
6. Give three practical steps the student can start taking now.
7. Include different options, not just high-paying careers.

Important:
- Do not guarantee a job, salary or admission.
- Do not decide the student's future for them.
- Use simple language and clear headings.
- Remind the student that eligibility and exam rules can change.
- For Indian career routes, recommend checking official websites
  for the latest requirements.
"""

                with st.spinner("Finding suitable career paths..."):
                    try:
                        answer, error = ask_groq(prompt)

                        if error:
                            st.error(str(error))
                        elif answer:
                            st.session_state["career_finder_result"] = answer
                        else:
                            st.warning("No response received. Please try again.")

                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

        if st.session_state.get("career_finder_result"):
            st.divider()
            st.subheader("✨ Your Career Suggestions")
            st.markdown(st.session_state["career_finder_result"])

    # ---------- CAREER INFORMATION ----------
    with tab2:
        st.subheader("📘 Explore Career Fields")

        career_info = {
            "💻 Technology": (
                "Software Developer, Web Developer, "
                "Cybersecurity Analyst, Data Scientist"
            ),
            "🩺 Healthcare": (
                "Doctor, Nurse, Pharmacist, Physiotherapist"
            ),
            "🛡️ Defence Services": (
                "Army, Navy, Air Force and other defence careers"
            ),
            "🌾 Agriculture": (
                "Agricultural Scientist, Agronomist, "
                "Food Technology and related careers"
            ),
            "🏗️ Engineering": (
                "Civil, Mechanical, Electrical and Computer Engineering"
            ),
            "🎨 Design & Creativity": (
                "Graphic Designer, Animator, UI/UX Designer"
            ),
            "📚 Education": (
                "Teacher, Lecturer, Researcher and Education Specialist"
            ),
            "🏛️ Government Services": (
                "Civil Services and other government career paths"
            )
        }

        for field, careers in career_info.items():
            with st.expander(field):
                st.write(careers)

        st.info(
            "These are examples of career fields, not personalised "
            "recommendations. Explore different options before deciding."
        )

    # ---------- CAREER ROADMAP ----------
    with tab3:
        st.subheader("🧭 Build Your Career Roadmap")

        goal = st.text_input(
            "Which career do you want to explore?",
            placeholder="Example: Software Developer, Navy Officer"
        )

        current_class = st.selectbox(
            "Your Current Class / Level",
            [
                "Class 6–8",
                "Class 9–10",
                "Class 11–12",
                "College",
                "Graduate"
            ],
            key="roadmap_education"
        )

        roadmap_notes = st.text_area(
            "What do you already know or want to improve?",
            placeholder="Example: I enjoy computers and want to learn coding."
        )

        if st.button("Create My Roadmap 🗺️", type="primary"):
            if not goal.strip():
                st.warning("Please enter a career goal.")
            else:
                prompt = f"""
You are a student career roadmap assistant.

Create a realistic beginner-friendly roadmap for:
Career goal: {goal}
Current education: {current_class}
Student's notes: {roadmap_notes or "Not provided"}

Include:
1. What this career involves.
2. Subjects and skills to focus on.
3. A step-by-step education and preparation path.
4. Free or low-cost learning activities.
5. A small action plan for the next 30 days.
6. Official sources to verify current eligibility and requirements.

Do not invent current exam dates, application openings,
cut-offs, salaries or eligibility rules.
Use simple language and encourage the student to explore
multiple paths.
"""

                with st.spinner("Creating your roadmap..."):
                    try:
                        answer, error = ask_groq(prompt)

                        if error:
                            st.error(str(error))
                        elif answer:
                            st.session_state["career_roadmap_result"] = answer
                        else:
                            st.warning("No response received. Please try again.")

                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

        if st.session_state.get("career_roadmap_result"):
            st.divider()
            st.subheader("🗺️ Your Career Roadmap")
            st.markdown(st.session_state["career_roadmap_result"])
