import json
from openai import OpenAI
import streamlit as st

# Step 1: Client बनाउने
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

# Step 2: Model र messages लाई अलग variable मा राख्ने
model = "qwen2.5:7b"

messages = [
    {
        "role": "system",
        "content": "You are a helpful, accurate, and concise AI assistant."
    },
]

temperature = 0


# --------------------------------------------------
# Streamlit Chat UI
# --------------------------------------------------

st.title("🤖 General AI Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = messages.copy()


# पुराना messages display गर्ने
for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User बाट नयाँ message
user_input = st.chat_input("Message लेख्नुहोस्...")


if user_input:

    # User message history मा राख्ने
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # User message देखाउने
    with st.chat_message("user"):
        st.markdown(user_input)


    # Step 3: API call गर्ने
    with st.chat_message("assistant"):

        resp = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages,
            temperature=temperature,
        )

        assistant_response = resp.choices[0].message.content

        st.markdown(assistant_response)


    # AI response history मा राख्ने
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )