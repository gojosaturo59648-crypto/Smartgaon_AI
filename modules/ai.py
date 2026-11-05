
import os
import requests
import streamlit as st


def ask_groq(prompt):
    try:
        api_key = st.secrets.get(
            "GROQ_API_KEY",
            os.getenv("GROQ_API_KEY", "")
        )

        if not api_key:
            return None, "Groq API key nahi mili. Pehle API key configure karo."

        url = "https://api.groq.com/openai/v1/chat/completions"

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are SmartGaon AI, a helpful assistant for "
                            "village development, farming, trees, nutrition, "
                            "education, electricity, waste management and "
                            "rural communities. Give clear, practical and "
                            "easy-to-understand answers."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            },
            timeout=60
        )

        if response.status_code != 200:
            return None, f"Groq API error ({response.status_code}): {response.text}"

        data = response.json()
        answer = data["choices"][0]["message"]["content"]

        return answer, None

    except requests.Timeout:
        return None, "Request timeout. Dobara try karo."
    except (KeyError, IndexError, ValueError):
        return None, "Groq se valid response nahi mila."
    except Exception as e:
        return None, f"Error: {e}"
