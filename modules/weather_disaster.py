
import streamlit as st
import requests


def show_weather():

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

    st.title("🌦️ Weather & Disaster Management")
    st.write(
        "Check weather conditions, forecasts and important disaster safety guidance."
    )

    # ---------- WEATHER CODE ----------
    def weather_description(code):
        descriptions = {
            0: "Clear Sky ☀️",
            1: "Mainly Clear 🌤️",
            2: "Partly Cloudy ⛅",
            3: "Overcast ☁️",
            45: "Fog 🌫️",
            48: "Depositing Rime Fog 🌫️",
            51: "Light Drizzle 🌦️",
            53: "Moderate Drizzle 🌦️",
            55: "Dense Drizzle 🌧️",
            61: "Light Rain 🌧️",
            63: "Moderate Rain 🌧️",
            65: "Heavy Rain ⛈️",
            71: "Light Snow ❄️",
            73: "Moderate Snow ❄️",
            75: "Heavy Snow ❄️",
            80: "Rain Showers 🌦️",
            81: "Moderate Rain Showers 🌧️",
            82: "Violent Rain Showers ⛈️",
            95: "Thunderstorm ⛈️",
            96: "Thunderstorm with Hail ⛈️",
            99: "Severe Thunderstorm with Hail ⛈️"
        }
        return descriptions.get(code, "Weather information unavailable")

    # ---------- TABS ----------
    tab1, tab2, tab3 = st.tabs([
        "🌤️ Live Weather",
        "📅 Forecast",
        "🚨 Disaster Safety"
    ])

    # ---------- LOCATION INPUT ----------
    with tab1:
        st.subheader("Check Weather in Your Area")

        city = st.text_input(
            "Enter Village / City / District",
            placeholder="Example: Patna, Bihar"
        )

        if st.button("Get Weather", type="primary"):
            if not city.strip():
                st.error("Please enter a location.")
            else:
                try:
                    with st.spinner("Fetching weather information..."):

                        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

                        geo_response = requests.get(
                            geo_url,
                            params={
                                "name": city.strip(),
                                "count": 1,
                                "language": "en",
                                "format": "json"
                            },
                            timeout=15
                        )

                        geo_response.raise_for_status()
                        geo_data = geo_response.json()

                        results = geo_data.get("results", [])

                        if not results:
                            st.error("Location not found. Check the spelling.")
                        else:
                            place = results[0]
                            latitude = place["latitude"]
                            longitude = place["longitude"]

                            weather_url = "https://api.open-meteo.com/v1/forecast"

                            weather_response = requests.get(
                                weather_url,
                                params={
                                    "latitude": latitude,
                                    "longitude": longitude,
                                    "current": (
                                        "temperature_2m,"
                                        "relative_humidity_2m,"
                                        "apparent_temperature,"
                                        "is_day,"
                                        "precipitation,"
                                        "weather_code,"
                                        "wind_speed_10m"
                                    ),
                                    "daily": (
                                        "temperature_2m_max,"
                                        "temperature_2m_min,"
                                        "precipitation_sum,"
                                        "precipitation_probability_max,"
                                        "wind_speed_10m_max"
                                    ),
                                    "forecast_days": 3,
                                    "timezone": "auto"
                                },
                                timeout=20
                            )

                            weather_response.raise_for_status()
                            data = weather_response.json()

                            st.session_state.weather_data = data
                            st.session_state.weather_place = place

                            st.success(
                                f"Weather found for {place['name']}, "
                                f"{place.get('admin1', '')}, "
                                f"{place.get('country', '')}"
                            )

                except requests.RequestException:
                    st.error(
                        "Weather service is unavailable. "
                        "Please check your internet connection and try again."
                    )
                except (KeyError, ValueError, IndexError):
                    st.error("Could not read weather data. Please try again.")

        # Show saved result
        if "weather_data" in st.session_state:
            data = st.session_state.weather_data
            place = st.session_state.weather_place
            current = data["current"]

            st.divider()
            st.subheader(
                f"Weather in {place['name']}, {place.get('country', '')}"
            )

            st.caption(
                "Updated: " + current.get("time", "Time unavailable")
            )

            st.markdown(
                f"### {weather_description(current['weather_code'])}"
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Temperature",
                f"{current['temperature_2m']} °C"
            )
            c2.metric(
                "Feels Like",
                f"{current['apparent_temperature']} °C"
            )
            c3.metric(
                "Humidity",
                f"{current['relative_humidity_2m']}%"
            )

            c4, c5 = st.columns(2)

            c4.metric(
                "Wind Speed",
                f"{current['wind_speed_10m']} km/h"
            )
            c5.metric(
                "Precipitation",
                f"{current['precipitation']} mm"
            )

            st.caption(
                "Weather data provided by Open-Meteo. "
                "Forecasts are estimates and may change."
            )

    # ---------- FORECAST ----------
    with tab2:
        st.subheader("📅 3-Day Weather Forecast")

        if "weather_data" not in st.session_state:
            st.info("First check a location in the Live Weather tab.")
        else:
            daily = st.session_state.weather_data["daily"]

            for i in range(len(daily["time"])):
                with st.expander(f"📅 {daily['time'][i]}"):
                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Maximum Temperature",
                        f"{daily['temperature_2m_max'][i]} °C"
                    )

                    col2.metric(
                        "Minimum Temperature",
                        f"{daily['temperature_2m_min'][i]} °C"
                    )

                    st.write(
                        "**Expected Rainfall:**",
                        f"{daily['precipitation_sum'][i]} mm"
                    )

                    st.write(
                        "**Rain Probability:**",
                        f"{daily['precipitation_probability_max'][i]}%"
                    )

                    st.write(
                        "**Maximum Wind Speed:**",
                        f"{daily['wind_speed_10m_max'][i]} km/h"
                    )

    # ---------- DISASTER SAFETY ----------
    with tab3:
        st.subheader("🚨 Disaster Preparedness & Safety")

        safety_guides = {
            "🌊 Flood Safety": [
                "Move to higher ground when flooding threatens.",
                "Stay away from flowing floodwater.",
                "Never walk or drive through flooded roads.",
                "Follow official evacuation instructions."
            ],
            "⛈️ Thunderstorm Safety": [
                "Move indoors when thunder is heard.",
                "Stay away from trees and open fields.",
                "Avoid contact with electrical equipment during storms.",
                "Wait until the storm has passed before going outside."
            ],
            "🔥 Heatwave Safety": [
                "Drink water regularly.",
                "Avoid strenuous outdoor activity during peak heat.",
                "Wear light, comfortable clothing.",
                "Stay in a cool or shaded place."
            ],
            "🌪️ Strong Wind / Storm Safety": [
                "Stay indoors and away from windows.",
                "Keep away from damaged trees and electric wires.",
                "Secure loose outdoor objects when safe to do so.",
                "Follow official weather warnings."
            ],
            "🌍 Earthquake Safety": [
                "Drop, Cover and Hold On during shaking.",
                "Stay away from windows and heavy objects.",
                "After shaking stops, move carefully to an open area if safe.",
                "Do not use elevators."
            ]
        }

        for title, instructions in safety_guides.items():
            with st.expander(title):
                for instruction in instructions:
                    st.write("•", instruction)

        st.divider()

        st.subheader("Official Weather Information")

        st.write(
            "For official weather warnings and alerts in India, "
            "check the India Meteorological Department."
        )

        st.link_button(
            "Open IMD Weather Website",
            "https://mausam.imd.gov.in/"
        )

        st.error(
            "For immediate emergencies in India, call 112. "
            "Follow local authorities' instructions."
        )
