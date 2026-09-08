import streamlit as st
import json
import time
from openai import OpenAI

# ============================================
# Page Config
# ============================================
st.set_page_config(
    page_title="NLP Extractor - Ollama",
    page_icon="🧠",
    layout="wide"
)

# ============================================
# Custom CSS
# ============================================
st.markdown("""
    <style>
    .result-card {
        background-color: #1e1e1e;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# TRANSLATION DICTIONARY - Yehi core part ho
# Sabai UI text yaha centralize gareko
# ============================================
TRANSLATIONS = {
    "en": {
        "app_title": "🧠 NLP Extractor",
        "app_caption": "Extract structured data using Ollama (Local LLM)",
        "total_extractions": "Total Extractions",
        "settings_header": "⚙️ Settings",
        "language_label": "🌐 Language",
        "model_label": "Model",
        "temperature_label": "Temperature",
        "temperature_help": "0 = precise/consistent output, 1 = creative/random output",
        "system_prompt_label": "System Prompt",
        "endpoint_caption": "🔌 Endpoint: `localhost:11434/v1`",
        "clear_history_btn": "🗑️ Clear History",
        "tab_extract": "✨ Extract",
        "tab_history": "📜 History",
        "input_header": "📝 Input",
        "input_placeholder": "Enter text here:",
        "extract_btn": "🚀 Extract",
        "output_header": "📤 Output",
        "error_empty": "Please enter some text!",
        "spinner_text": "Processing with '{model}'...",
        "error_api": "Error: {error}",
        "error_hint": "Check if `ollama serve` is running.",
        "time_taken": "⏱️ Time Taken",
        "model_used": "🤖 Model",
        "not_json_warning": "Not pure JSON, raw output:",
        "raw_output_expander": "📋 Raw Output (Copy)",
        "empty_output_hint": "👈 Enter text on the left and click 'Extract'",
        "history_header": "📜 Extraction History",
        "history_empty": "No extractions yet.",
        "history_input_label": "**Input Text:**",
        "history_model_label": "**Model:**",
        "history_output_label": "**Output:**",
        "footer_note": "💡 This pattern can be used in the Telecom Complaint Router to extract category/urgency.",
        "extract_task_instruction": 'Extract the name and city. Respond with JSON only.\nText: "{text}"',
    },
    "ne": {
        "app_title": "🧠 NLP एक्स्ट्र्याक्टर",
        "app_caption": "Ollama (Local LLM) प्रयोग गरेर structured data निकाल्ने Tool",
        "total_extractions": "जम्मा Extraction",
        "settings_header": "⚙️ सेटिङ",
        "language_label": "🌐 भाषा",
        "model_label": "मोडेल",
        "temperature_label": "Temperature",
        "temperature_help": "0 = precise/consistent output, 1 = creative/random output",
        "system_prompt_label": "System Prompt",
        "endpoint_caption": "🔌 Endpoint: `localhost:11434/v1`",
        "clear_history_btn": "🗑️ History Clear गर्नुहोस्",
        "tab_extract": "✨ Extract",
        "tab_history": "📜 History",
        "input_header": "📝 Input",
        "input_placeholder": "यहाँ Text हाल्नुहोस्:",
        "extract_btn": "🚀 Extract गर्नुहोस्",
        "output_header": "📤 Output",
        "error_empty": "कृपया text हाल्नुहोस्!",
        "spinner_text": "'{model}' ले Process गर्दैछ...",
        "error_api": "Error भयो: {error}",
        "error_hint": "जाँच्नुहोस्: `ollama serve` चालु छ कि छैन?",
        "time_taken": "⏱️ लागेको समय",
        "model_used": "🤖 मोडेल",
        "not_json_warning": "Pure JSON होइन, Raw Output:",
        "raw_output_expander": "📋 Raw Output (Copy गर्न)",
        "empty_output_hint": "👈 बायाँतिर Text हालेर 'Extract गर्नुहोस्' थिच्नुहोस्",
        "history_header": "📜 Extraction History",
        "history_empty": "अहिलेसम्म कुनै Extraction गरिएको छैन।",
        "history_input_label": "**Input Text:**",
        "history_model_label": "**Model:**",
        "history_output_label": "**Output:**",
        "footer_note": "💡 यो Pattern लाई Telecom Complaint Router मा category/urgency निकाल्न प्रयोग गर्न सकिन्छ।",
        "extract_task_instruction": 'Extract the name and city. Respond with JSON only.\nText: "{text}"',
    }
}

# ============================================
# Session State Initialize
# ============================================
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "lang" not in st.session_state:
    st.session_state.lang = "en"   # Default language: English

# Current language ko translation dictionary lai 't' short-name diyeko
t = TRANSLATIONS[st.session_state.lang]

# ============================================
# Header
# ============================================
col_title, col_status = st.columns([3, 1])
with col_title:
    st.title(t["app_title"])
    st.caption(t["app_caption"])
with col_status:
    st.metric(t["total_extractions"], len(st.session_state.history))

st.divider()

# ============================================
# Sidebar - Settings + Language Toggle
# ============================================
with st.sidebar:
    st.header(t["settings_header"])

    # ---- Language Selector (Yehi naya feature ho) ----
    lang_choice = st.radio(
        t["language_label"],
        options=["en", "ne"],
        format_func=lambda x: "English" if x == "en" else "नेपाली",
        index=0 if st.session_state.lang == "en" else 1,
        horizontal=True
    )

    # Language change bhaye rerun garne (UI turant update huna)
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.rerun()

    st.divider()

    model = st.selectbox(
        t["model_label"],
        ["qwen2.5:7b", "llama3.2:3b", "llama3.2:latest"]
    )

    temperature = st.slider(
        t["temperature_label"], min_value=0.0, max_value=1.0, value=0.0, step=0.1,
        help=t["temperature_help"]
    )

    system_prompt = st.text_area(
        t["system_prompt_label"],
        value="You are a terse travel assistant for Nepal.",
        height=80
    )

    st.divider()
    st.caption(t["endpoint_caption"])

    if st.button(t["clear_history_btn"]):
        st.session_state.history = []
        st.rerun()

# ============================================
# Tabs
# ============================================
tab1, tab2 = st.tabs([t["tab_extract"], t["tab_history"]])

# ---------- TAB 1: Extract ----------
with tab1:
    col_input, col_output = st.columns(2)

    with col_input:
        st.subheader(t["input_header"])
        user_text = st.text_area(
            t["input_placeholder"],
            value='Ram Thapa runs a trekking shop in Pokhara.',
            height=150,
            key="input_text"
        )

        extract_btn = st.button(t["extract_btn"], type="primary", use_container_width=True)

    with col_output:
        st.subheader(t["output_header"])

        if extract_btn:
            if not user_text.strip():
                st.error(t["error_empty"])
            else:
                start_time = time.time()

                with st.spinner(t["spinner_text"].format(model=model)):
                    try:
                        client = OpenAI(
                            base_url="http://localhost:11434/v1",
                            api_key="ollama",
                        )

                        messages = [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": t["extract_task_instruction"].format(text=user_text)},
                        ]

                        resp = client.chat.completions.create(
                            model=model,
                            messages=messages,
                            temperature=temperature,
                        )

                        result_text = resp.choices[0].message.content
                        elapsed = round(time.time() - start_time, 2)

                        st.session_state.last_result = {
                            "text": user_text,
                            "output": result_text,
                            "model": model,
                            "time": elapsed
                        }
                        st.session_state.history.insert(0, st.session_state.last_result)

                    except Exception as e:
                        st.error(t["error_api"].format(error=e))
                        st.info(t["error_hint"])

        if st.session_state.last_result:
            r = st.session_state.last_result

            m1, m2 = st.columns(2)
            m1.metric(t["time_taken"], f"{r['time']}s")
            m2.metric(t["model_used"], r['model'])

            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            try:
                parsed = json.loads(r["output"])
                st.json(parsed)
            except json.JSONDecodeError:
                st.warning(t["not_json_warning"])
                st.code(r["output"], language="text")
            st.markdown('</div>', unsafe_allow_html=True)

            with st.expander(t["raw_output_expander"]):
                st.code(r["output"], language="json")
        else:
            st.info(t["empty_output_hint"])

# ---------- TAB 2: History ----------
with tab2:
    st.subheader(t["history_header"])

    if not st.session_state.history:
        st.info(t["history_empty"])
    else:
        for i, item in enumerate(st.session_state.history):
            with st.expander(f"#{len(st.session_state.history)-i} — \"{item['text'][:50]}...\"  ({item['time']}s)"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(t["history_input_label"])
                    st.write(item["text"])
                    st.write(f"{t['history_model_label']} {item['model']}")
                with col_b:
                    st.write(t["history_output_label"])
                    try:
                        st.json(json.loads(item["output"]))
                    except json.JSONDecodeError:
                        st.code(item["output"])

# ============================================
# Footer
# ============================================
st.divider()
st.caption(t["footer_note"])