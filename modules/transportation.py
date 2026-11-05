
import streamlit as st
from urllib.parse import quote


def show_transportation():

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

    st.title("🚌 Transportation & Road Safety")
    st.write("Plan safer and easier journeys in and around your village.")

    # ---------- SESSION STORAGE ----------
    if "transport_routes" not in st.session_state:
        st.session_state.transport_routes = []

    if "transport_journey" not in st.session_state:
        st.session_state.transport_journey = None

    # ---------- TABS ----------
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚍 Transport Options",
        "📍 Routes & Stops",
        "🗺️ Travel Planner",
        "🛡️ Road Safety",
        "🚨 Emergency"
    ])

    # ==================================================
    # TAB 1: TRANSPORT OPTIONS
    # ==================================================
    with tab1:
        st.subheader("Available Transport Options")

        options = {
            "🚌 Bus": "Useful for travelling between villages and nearby towns.",
            "🚆 Train": "Useful for longer-distance journeys.",
            "🛺 Auto / E-rickshaw": "Useful for short-distance local travel.",
            "🚲 Bicycle": "Useful for nearby destinations.",
            "🚶 Walking": "Suitable for short and safe routes."
        }

        for name, description in options.items():
            with st.expander(name):
                st.write(description)

        st.info(
            "Confirm transport availability and timings "
            "with your local transport provider."
        )



    # ==================================================
    # TAB 2: TRAVEL PLANNER
    # ==================================================
    with tab2:
        st.subheader("🗺️ Simple Travel Planner")

        with st.form("journey_form"):
            start = st.text_input("Starting location")
            destination = st.text_input("Destination")

            transport = st.selectbox(
                "Preferred transport",
                [
                    "Any transport",
                    "Bus",
                    "Train",
                    "Auto / E-rickshaw",
                    "Bicycle",
                    "Walking",
                    "Driving"
                ]
            )

            plan = st.form_submit_button(
                "Plan My Journey",
                type="primary"
            )

        if plan:
            if start.strip() and destination.strip():
                st.session_state.transport_journey = {
                    "start": start.strip(),
                    "destination": destination.strip(),
                    "transport": transport
                }
            else:
                st.error("Please enter both starting location and destination.")

        journey = st.session_state.transport_journey

        if journey:
            st.success("Journey details ready!")

            st.write("**From:**", journey["start"])
            st.write("**To:**", journey["destination"])
            st.write("**Transport:**", journey["transport"])

            mode = {
                "Any transport": "transit",
                "Bus": "transit",
                "Train": "transit",
                "Auto / E-rickshaw": "driving",
                "Bicycle": "bicycling",
                "Walking": "walking",
                "Driving": "driving"
            }[journey["transport"]]

            maps_url = (
                "https://www.google.com/maps/dir/?api=1"
                f"&origin={quote(journey['start'])}"
                f"&destination={quote(journey['destination'])}"
                f"&travelmode={mode}"
            )

            st.link_button("Open Route in Google Maps", maps_url)

            st.caption(
                "Google Maps will show available route information. "
                "Confirm actual road and transport conditions."
            )

    # ==================================================
    # TAB 3: ROAD SAFETY
    # ==================================================
    with tab3:
        st.subheader("🛡️ Road Safety Guide")

        safety = {
            "🪖 Helmet": "Wear a properly fitted helmet on two-wheelers.",
            "🚗 Seat Belt": "Always wear a seat belt in a car.",
            "🚦 Traffic Signals": "Follow traffic lights and road signs.",
            "🚶 Safe Crossing": "Use zebra crossings where available.",
            "📵 No Distraction": "Never use a phone while driving.",
            "🌙 Night Travel": "Use proper lights and stay alert at night.",
            "🚸 School Safety": "Slow down near schools and crowded areas."
        }

        for title, detail in safety.items():
            with st.expander(title):
                st.write(detail)

    # ==================================================
    # TAB 4: EMERGENCY
    # ==================================================
    with tab4:
        st.subheader("🚨 Emergency Travel Guidance")

        st.warning(
            "In an emergency, contact local emergency services "
            "or ask a trusted adult for immediate help."
        )

        st.markdown("### India Emergency Helpline")
        st.title("112")

        st.link_button(
            "Call Emergency Number 112",
            "tel:112"
        )

        st.caption(
            "Use emergency services only when genuinely needed."
        )
