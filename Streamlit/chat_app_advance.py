import streamlit as st
import time
from openai import OpenAI


# ============================================
# Page Config
# ============================================
st.set_page_config(
    page_title="AI Chatbot - Ollama",
    page_icon="🤖",
    layout="wide"
)


# ============================================
# Custom CSS
# ============================================
st.markdown("""
<style>

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }

    /* Header */
    .app-header {
        text-align: center;
        padding: 10px 0 20px 0;
    }

    .app-header h1 {
        margin-bottom: 5px;
    }

    .app-header p {
        color: #888;
        margin-top: 0;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 8px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.2);
    }

    /* Status card */
    .status-card {
        padding: 12px;
        border-radius: 10px;
        background-color: rgba(128,128,128,0.08);
        margin-top: 10px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================
# Translation Dictionary
# ============================================
TRANSLATIONS = {

    "en": {
        "app_title": "🤖 AI Chatbot",
        "app_caption": "General-purpose AI assistant powered by Ollama",
        "settings": "⚙️ Settings",
        "language": "🌐 Language",
        "model": "Model",
        "temperature": "Temperature",
        "temperature_help": "0 = precise/consistent, 1 = more creative/random",
        "system_prompt": "System Prompt",
        "system_prompt_help": "Controls how the AI behaves.",
        "endpoint": "🔌 Ollama: localhost:11434/v1",
        "clear_chat": "🗑️ Clear Chat",
        "chat_placeholder": "Type your message...",
        "thinking": "Thinking...",
        "response_time": "Response time",
        "messages": "Messages",
        "ready": "Ready",
        "error": "Error",
        "error_hint": "Make sure Ollama is running with `ollama serve`.",
        "empty_chat": "Start a conversation by typing a message below.",
    },

    "ne": {
        "app_title": "🤖 AI Chatbot",
        "app_caption": "Ollama द्वारा चल्ने General-purpose AI Assistant",
        "settings": "⚙️ सेटिङ",
        "language": "🌐 भाषा",
        "model": "मोडेल",
        "temperature": "Temperature",
        "temperature_help": "0 = precise/consistent, 1 = बढी creative/random",
        "system_prompt": "System Prompt",
        "system_prompt_help": "AI ले कसरी व्यवहार गर्ने भन्ने निर्धारण गर्छ।",
        "endpoint": "🔌 Ollama: localhost:11434/v1",
        "clear_chat": "🗑️ Chat Clear गर्नुहोस्",
        "chat_placeholder": "आफ्नो message लेख्नुहोस्...",
        "thinking": "सोच्दैछ...",
        "response_time": "Response time",
        "messages": "Messages",
        "ready": "Ready",
        "error": "Error",
        "error_hint": "`ollama serve` चलिरहेको छ कि छैन जाँच गर्नुहोस्।",
        "empty_chat": "तल message लेखेर conversation सुरु गर्नुहोस्।",
    }
}


# ============================================
# Session State
# ============================================
if "lang" not in st.session_state:
    st.session_state.lang = "en"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful, accurate, and concise AI assistant. "
                "Answer the user's questions clearly and naturally. "
                "If the user asks in Nepali, respond in Nepali. "
                "If the user asks in English, respond in English."
            )
        }
    ]


# Current language
t = TRANSLATIONS[st.session_state.lang]


# ============================================
# Sidebar
# ============================================
with st.sidebar:

    st.header(t["settings"])

    # -----------------------------
    # Language
    # -----------------------------
    lang_choice = st.radio(
        t["language"],
        options=["en", "ne"],
        format_func=lambda x: "English" if x == "en" else "नेपाली",
        index=0 if st.session_state.lang == "en" else 1,
        horizontal=True
    )

    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.rerun()

    st.divider()

    # -----------------------------
    # Model
    # -----------------------------
    model = st.selectbox(
        t["model"],
        [
            "qwen2.5:7b",
            "llama3.2:3b",
            "llama3.2:latest"
        ]
    )

    # -----------------------------
    # Temperature
    # -----------------------------
    temperature = st.slider(
        t["temperature"],
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
        help=t["temperature_help"]
    )

    # -----------------------------
    # System Prompt
    # -----------------------------
    system_prompt = st.text_area(
        t["system_prompt"],
        value=(
            "You are a helpful, accurate, and concise AI assistant. "
            "Answer the user's questions clearly and naturally. "
            "If the user asks in Nepali, respond in Nepali. "
            "If the user asks in English, respond in English."
        ),
        height=150,
        help=t["system_prompt_help"]
    )

    st.divider()

    # -----------------------------
    # Ollama endpoint
    # -----------------------------
    st.caption(t["endpoint"])

    # -----------------------------
    # Chat information
    # -----------------------------
    user_message_count = sum(
        1 for m in st.session_state.messages
        if m["role"] == "user"
    )

    st.markdown(
        f"""
        <div class="status-card">
            <b>{t["messages"]}:</b> {user_message_count}<br>
            <b>Model:</b> {model}<br>
            <b>Status:</b> 🟢 {t["ready"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # -----------------------------
    # Clear Chat
    # -----------------------------
    if st.button(
        t["clear_chat"],
        use_container_width=True
    ):

        st.session_state.messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        st.rerun()


# ============================================
# Header
# ============================================
st.markdown(
    f"""
    <div class="app-header">
        <h1>{t["app_title"]}</h1>
        <p>{t["app_caption"]}</p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================
# Display Chat History
# ============================================
if len(st.session_state.messages) == 1:

    st.info(t["empty_chat"])


for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================
# Chat Input
# ============================================
user_input = st.chat_input(
    t["chat_placeholder"]
)


# ============================================
# Chat Processing
# ============================================
if user_input:

    # ----------------------------------------
    # Add system prompt
    # ----------------------------------------
    st.session_state.messages[0] = {
        "role": "system",
        "content": system_prompt
    }

    # ----------------------------------------
    # Add user message
    # ----------------------------------------
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # ----------------------------------------
    # Display user message
    # ----------------------------------------
    with st.chat_message("user"):
        st.markdown(user_input)

    # ----------------------------------------
    # Call Ollama
    # ----------------------------------------
    with st.chat_message("assistant"):

        start_time = time.time()

        with st.spinner(t["thinking"]):

            try:

                # OpenAI-compatible Ollama client
                client = OpenAI(
                    base_url="http://localhost:11434/v1",
                    api_key="ollama",
                )

                # API call
                resp = client.chat.completions.create(
                    model=model,
                    messages=st.session_state.messages,
                    temperature=temperature,
                )

                # Get response
                assistant_response = (
                    resp.choices[0].message.content
                )

                elapsed = round(
                    time.time() - start_time,
                    2
                )

                # Display response
                st.markdown(assistant_response)

                # Response time
                st.caption(
                    f"⏱️ {t['response_time']}: {elapsed}s"
                )

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_response
                    }
                )

            except Exception as e:

                st.error(
                    f"{t['error']}: {e}"
                )

                st.info(
                    t["error_hint"]
                )