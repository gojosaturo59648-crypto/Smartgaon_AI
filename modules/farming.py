
import streamlit as st
from modules.ai import ask_groq


def show_farming():

    # BLACK FONT COLOUR
    st.markdown("""
    <style>
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp p,
    .stApp label,
    .stApp span,
    .stApp li,
    .stApp [data-testid="stMarkdownContainer"] {
        color: #000000 !important;
    }

    .stApp input,
    .stApp textarea,
    .stApp [data-baseweb="select"] * {
        color: #000000 !important;
    }

    .stApp [data-testid="stRadio"] label,
    .stApp [data-testid="stCheckbox"] label {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🌱 SmartGaon Farming Assistant")
    st.write("Get crop guidance and farming support for your village.")

    st.subheader("1. Farm Details")

    col1, col2 = st.columns(2)

    with col1:
        location = st.text_input(
            "Village / District",
            placeholder="Example: Ranchi, Jharkhand"
        )

        crop = st.selectbox(
            "Select Crop",
            [
                "Rice (Paddy)",
                "Wheat",
                "Maize",
                "Potato",
                "Tomato",
                "Mustard",
                "Pulses",
                "Vegetables",
                "Other"
            ]
        )

        soil = st.selectbox(
            "Soil Type",
            [
                "Alluvial Soil",
                "Red Soil",
                "Black Soil",
                "Sandy Soil",
                "Clay Soil",
                "Loamy Soil",
                "Unknown"
            ]
        )

    with col2:
        season = st.selectbox(
            "Growing Season",
            ["Kharif", "Rabi", "Zaid", "Not Sure"]
        )

        irrigation = st.selectbox(
            "Irrigation Source",
            [
                "Rainwater",
                "Borewell",
                "Tube Well",
                "Canal",
                "River",
                "Other"
            ]
        )

        land = st.number_input(
            "Farm Area (acres)",
            min_value=0.0,
            step=0.1
        )

    st.subheader("2. Describe Your Farming Problem")

    problem = st.text_area(
        "What help do you need?",
        placeholder="Example: My rice crop leaves are turning yellow..."
    )

    photo = st.file_uploader(
        "Upload crop photo (optional)",
        type=["jpg", "jpeg", "png"]
    )

    if photo:
        st.image(
            photo,
            caption="Uploaded Crop Photo",
            use_container_width=True
        )

    if st.button("Get Farming Advice", type="primary"):

        if not location.strip() or not problem.strip():
            st.warning(
                "Please enter your location and farming problem."
            )

        else:
            prompt = f"""
You are SmartGaon AI Farming Assistant.

Give practical, easy-to-understand farming guidance.
Never invent pesticide doses or guarantee crop results.
For serious crop disease, recommend local agricultural experts.

Village/District: {location}
Crop: {crop}
Soil: {soil}
Season: {season}
Irrigation: {irrigation}
Farm Area: {land} acres

Farmer's Problem:
{problem}

Give your answer with these sections:

1. Understanding the farming problem
2. Possible causes
3. Recommended next steps
4. Water and soil care
5. Prevention advice
6. When to contact an agricultural expert

Use simple language and practical suggestions.
Do not assume facts that the farmer has not provided.
"""

            with st.spinner(
                "SmartGaon AI is analysing your farming question..."
            ):
                try:
                    answer, error = ask_groq(prompt)

                    if error:
                        st.error(error)

                    elif answer:
                        st.divider()
                        st.subheader("🌾 Groq AI Farming Advice")
                        st.markdown(answer)

                    else:
                        st.error(
                            "AI returned an empty response. Please try again."
                        )

                except Exception as error:
                    st.error(f"AI request failed: {error}")

    st.caption(
        "AI guidance is informational. Confirm important crop "
        "treatment decisions with a qualified agricultural expert."
    )
