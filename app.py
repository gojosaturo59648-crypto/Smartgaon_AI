
import streamlit as st

from modules.ai_assistant import show_ai_assistant
from modules.village_planner import show_village_planner
from modules.electricity import show_electricity_calculator
from modules.farming import show_farming
from modules.tree_doctor import show_tree_doctor
from modules.nutriplate import show_nutriplate
from modules.transportation import show_transportation
from modules.waste_management import show_waste_management
from modules.weather_disaster import show_weather
from modules.career_finder import show_career_finder
from modules.study_planner import show_study_planner
from modules.knowledge_hub import show_knowledge_hub


# PAGE SETTINGS
st.set_page_config(
    page_title="SmartGaon AI",
    page_icon="🏡",
    layout="wide"
)


# MAIN CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f1faf4, #eaf3ff);
}

h1, h2, h3, p, label {
    color: #174b37 !important;
}

[data-testid="stSidebar"] {
    background-color: #e0f1e7;
}

div.stButton > button {
    background: #16845b;
    color: white;
    border-radius: 10px;
    border: none;
}

.welcome-banner {
    background: linear-gradient(120deg, #174b37, #16845b);
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.welcome-banner h2 {
    color: white !important;
    font-size: 34px;
}

.welcome-banner p {
    color: #e5f5eb !important;
}

.feature-card {
    background: white;
    border: 1px solid #d8e9dd;
    border-radius: 14px;
    padding: 20px;
    min-height: 140px;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(20,70,45,0.06);
}

.feature-card h3 {
    color: #174b37 !important;
    font-size: 19px;
}

.feature-card p {
    color: #52675a !important;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# HEADER
st.title("🏡 SmartGaon AI")
st.subheader("Plan a better village, one idea at a time")


# MODULES
modules = [
    "Home",
    "Smart AI Assistant",
    "Village Development Planner",
    "Farming Assistant",
    "TreeDoctor",
    "NutriPlate",
    "Transportation & Road Safety",
    "Waste Management",
    "Light & Electricity",
    "Weather & Disaster",
    "Career Path Finder",
    "Study Planner",
    "Knowledge Hub"
]


# SIDEBAR
st.sidebar.title("🏡 SmartGaon AI")

selected = st.sidebar.selectbox(
    "Choose a Module",
    modules
)


# HOME PAGE
if selected == "Home":

    st.markdown("""
    <div class="welcome-banner">
        <h2>Welcome to SmartGaon AI 🏡</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "Technology for better villages, smarter farming and brighter futures."
    )

    st.caption("Plan a better village, one idea at a time.")

    st.markdown("---")
    st.subheader("🌿 Explore Your Smart Village")

    cards = [
        ("🤖", "Smart AI Assistant",
         "Get AI-powered assistance and information."),

        ("🏡", "Village Development Planner",
         "Plan village development and budgets."),

        ("🌾", "Farming Assistant",
         "Explore farming guidance and crop information."),

        ("🌳", "TreeDoctor",
         "Get guidance about tree health and care."),

        ("🥗", "NutriPlate",
         "Explore food and nutrition information."),

        ("🛣️", "Transportation & Road Safety",
         "Explore transportation and road safety."),

        ("♻️", "Waste Management",
         "Learn about better waste management."),

        ("💡", "Light & Electricity",
         "Calculate electricity usage and bills."),

        ("🌦️", "Weather & Disaster",
         "Explore weather and disaster awareness."),

        ("🎓", "Career Path Finder",
         "Explore career opportunities."),

        ("📅", "Study Planner",
         "Organise study schedules and tasks."),

        ("📚", "Knowledge Hub",
         "Find learning resources and information.")
    ]

    for start in range(0, len(cards), 3):

        cols = st.columns(3)

        for col, item in zip(cols, cards[start:start + 3]):

            with col:
                st.markdown(f"""
                <div class="feature-card">
                    <h3>{item[0]} {item[1]}</h3>
                    <p>{item[2]}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(
        "<h3 style='text-align:center;'>🌱 Building a Better Tomorrow</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>Smarter Villages. Empowered Farmers. Educated Communities.</p>",
        unsafe_allow_html=True
    )


# MODULE ROUTING
elif selected == "Smart AI Assistant":
    show_ai_assistant()

elif selected == "Village Development Planner":
    show_village_planner()

elif selected == "Farming Assistant":
    show_farming()

elif selected == "TreeDoctor":
    show_tree_doctor()

elif selected == "NutriPlate":
    show_nutriplate()

elif selected == "Transportation & Road Safety":
    show_transportation()

elif selected == "Waste Management":
    show_waste_management()

elif selected == "Light & Electricity":
    show_electricity_calculator()

elif selected == "Weather & Disaster":
    show_weather()

elif selected == "Career Path Finder":
    show_career_finder()

elif selected == "Study Planner":
    show_study_planner()

elif selected == "Knowledge Hub":
    show_knowledge_hub()


# SIDEBAR FOOTER
st.sidebar.divider()
st.sidebar.caption("SmartGaon AI • Development Version")
