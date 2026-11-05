
import streamlit as st
from modules.ai import ask_groq


def show_ai_assistant():
    st.title("🤖 SmartGaon AI Assistant")
    st.caption("Your digital helper for a smarter village.")

    st.markdown("""
    Ask questions about farming, village development, trees,
    nutrition, education, electricity and more.
    """)

    if "smartgaon_chat" not in st.session_state:
        st.session_state.smartgaon_chat = []

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.smartgaon_chat = []
        st.rerun()

    # Display chat history
    for message in st.session_state.smartgaon_chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    prompt = st.chat_input("Ask SmartGaon AI anything...")

    if prompt:
        st.session_state.smartgaon_chat.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("SmartGaon AI is thinking..."):
                answer, error = ask_groq(prompt)

                if error:
                    answer = f"⚠️ {error}"

                st.markdown(answer)

        st.session_state.smartgaon_chat.append({
            "role": "assistant",
            "content": answer
        })
