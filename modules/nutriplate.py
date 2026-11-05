
import streamlit as st
import requests
import base64
import os


MODEL = "qwen/qwen3.8-27b"
API_URL = "https://api.groq.com/openai/v1/chat/completions"


def get_api_key():
    try:
        return st.secrets.get(
            "GROQ_API_KEY",
            os.getenv("GROQ_API_KEY", "")
        )
    except Exception:
        return os.getenv("GROQ_API_KEY", "")


def analyze_food_image(image_bytes, mime_type):

    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "Groq API key nahi mili. GROQ_API_KEY configure karo."
        )

    image_data = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
You are NutriPlate, a nutrition estimation assistant.

Analyze the visible meal in the uploaded plate photograph.

Do not perform a separate food-identification or image-validation
step. Directly estimate the nutritional content of the visible meal.

Use these headings:

1. Estimated Calories
Give approximate total calories for the visible meal.

2. Macronutrients
Estimate:
- Carbohydrates (grams)
- Protein (grams)
- Fat (grams)
- Fibre (grams), if reasonably estimable

3. Important Nutrients
Mention relevant vitamins and minerals that may be present.

4. Nutritional Benefits
Explain the general nutritional benefits of the meal.

5. Suggestions
Suggest foods that could improve the nutritional balance
if something appears limited.

IMPORTANT:
- Focus only on nutrition estimates.
- Do not claim exact calorie or nutrient values from a photo.
- Do not invent ingredients or portion sizes.
- State when portion size or ingredients are unclear.
- Do not diagnose nutritional deficiencies.
- Keep the response simple and easy to understand.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        "temperature": 0.3,
        "max_completion_tokens": 1200
    }

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=90
    )

    if response.status_code == 429:
        raise Exception(
            "Groq rate limit reached. Please try again later."
        )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


def show_nutriplate():

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
        color: #ffffff !important;
    }

    .stApp [data-testid="stRadio"] label,
    .stApp [data-testid="stCheckbox"] label {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🍽️ NutriPlate")

    st.write(
        "Upload your food plate photo to understand its nutrition."
    )

    st.info(
        "Upload a clear photo of your meal to get "
        "estimated calories and nutrients."
    )

    uploaded_file = st.file_uploader(
        "📸 Upload your food plate",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file:

        image_bytes = uploaded_file.getvalue()

        if len(image_bytes) > 5 * 1024 * 1024:
            st.error(
                "Image is too large. Please upload an image below 5 MB."
            )
            return

        mime_type = uploaded_file.type

        if mime_type not in [
            "image/jpeg",
            "image/png",
            "image/webp"
        ]:
            st.error("Please upload a valid JPG, PNG or WEBP image.")
            return

        st.image(
            image_bytes,
            caption="Your uploaded food plate",
            use_container_width=True
        )

        if st.button("🔍 Analyze Nutrition", type="primary"):

            try:
                with st.spinner("🍎 Estimating plate nutrition..."):

                    result = analyze_food_image(
                        image_bytes,
                        mime_type
                    )

                st.success("Nutrition analysis completed!")

                st.subheader("🥗 Your NutriPlate Report")
                st.markdown(result)

                st.caption(
                    "All nutrition values are approximate visual "
                    "estimates. Actual values depend on ingredients "
                    "and portion sizes."
                )

            except requests.exceptions.Timeout:
                st.error("AI request timed out. Please try again.")

            except requests.exceptions.HTTPError as error:
                st.error(f"Groq API error: {error}")

            except Exception as error:
                st.error(f"Something went wrong: {error}")

    else:
        st.info("No food photo uploaded yet.")
