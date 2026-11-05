
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


def ask_groq_image(image_bytes, mime_type, prompt):

    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "Groq API key nahi mili. GROQ_API_KEY configure karo."
        )

    image_data = base64.b64encode(image_bytes).decode("utf-8")

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
        retry_after = response.headers.get("retry-after")

        if retry_after:
            raise Exception(
                f"Groq rate limit reached. Retry after {retry_after} seconds."
            )

        raise Exception(
            "Groq rate limit reached. Please try again later."
        )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


def show_tree_doctor():

    # FONT COLOUR
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

    st.title("🌳 TreeDoctor")

    st.write(
        "Upload a plant leaf or full tree photo "
        "to check its visible condition."
    )

    st.info(
        "TreeDoctor accepts plant leaves and full tree photos only. "
        "Human and unrelated photos are rejected."
    )

    uploaded_file = st.file_uploader(
        "Upload a plant or tree photo",
        type=["jpg", "jpeg", "png", "webp"]
    )

    tree_name = st.selectbox(
        "Select your tree (if known)",
        [
            "Unknown",
            "Neem",
            "Peepal",
            "Banyan",
            "Mango",
            "Aloe Vera",
            "Other"
        ]
    )

    extra_details = st.text_area(
        "Any symptoms you noticed? (Optional)",
        placeholder="Example: Yellow leaves, spots, drying, etc."
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
            caption="Uploaded photo",
            use_container_width=True
        )

        if st.button("🔍 Check Plant Health", type="primary"):

            prompt = f"""
You are TreeDoctor, a careful plant-health assistant.

First inspect the uploaded image.

IMPORTANT IMAGE VALIDATION:
- If the image clearly shows a plant leaf or tree, continue.
- If it shows a human, animal, unrelated object or scenery,
  do not analyze plant health.
- If the image is unclear or does not show a plant,
  politely ask the user to upload a clear plant photo.

USER DETAILS:
Selected tree: {tree_name}
User observations: {extra_details or "None"}

If the image contains a plant, use these headings:

1. Visible observations
Describe the visible leaf or tree condition.

2. Possible causes
Mention possible reasons only when supported by the image.

3. Suggested safe care steps
Give simple and practical plant-care advice.

4. When to consult an expert
Explain when the user should contact a local
agriculture or horticulture expert.

IMPORTANT:
- Do not claim a confirmed disease from an image alone.
- Do not invent plant symptoms.
- If symptoms are unclear, say so.
- If no obvious problem is visible, say that too.
- Keep the answer simple and easy to understand.
"""

            try:

                with st.spinner("🌿 Analyzing plant image..."):

                    result = ask_groq_image(
                        image_bytes,
                        mime_type,
                        prompt
                    )

                st.success("Image analysis completed!")

                st.subheader("🌿 TreeDoctor Analysis")

                st.markdown(result)

                st.caption(
                    "This is an AI-based visual assessment, "
                    "not a confirmed diagnosis. Consult a local "
                    "expert for serious plant problems."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "AI request timed out. Please try again."
                )

            except requests.exceptions.HTTPError as error:

                st.error(f"Groq API error: {error}")

            except Exception as error:

                st.error(f"Something went wrong: {error}")
