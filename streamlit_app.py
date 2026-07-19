import traceback
import os
import streamlit as st
from chatbot.user_profile import UserProfile


import chatbot.llm as llm

print("LLM FILE:", llm.__file__)
print("LLM FUNCTIONS:", dir(llm))

get_ai_response = llm.get_ai_response
clear_chat = llm.clear_chat
get_token_usage = llm.get_token_usage
profile = UserProfile()


profile_data = profile.load_profile()
 


st.sidebar.markdown("---")

st.sidebar.subheader("User Profile")

if profile_data:

    st.json(profile_data)

else:

    st.info("No profile stored yet.")




# Page Configuration


st.set_page_config(
    page_title="Custom AI Chatbot",
    page_icon="🤖",
    layout="wide"
)


# Sidebar


st.sidebar.title(" AI Chatbot")

st.sidebar.markdown("---")

st.sidebar.header("Features")

st.sidebar.success(" Gemini API")

st.sidebar.success(" Memory")

st.sidebar.success(" Sessions")

st.sidebar.success(" Token Counter")

st.sidebar.success(" Prompt Engineering")

st.sidebar.success(" Memory Pruning")

st.sidebar.markdown("---")


# Token Usage


st.sidebar.subheader("Current Token Usage")

st.sidebar.metric(
    label="Tokens",
    value=get_token_usage()
)

st.sidebar.markdown("---")


# Saved Sessions


st.sidebar.subheader("Saved Sessions")

if os.path.exists("sessions"):

    files = os.listdir("sessions")

    if files:

        for file in files:

            st.sidebar.write(f" {file}")

    else:

        st.sidebar.info("No Saved Sessions")

else:

    st.sidebar.info("Sessions Folder Not Found")

st.sidebar.markdown("---")


# Clear Chat


if st.sidebar.button(" Clear Chat"):

    clear_chat()

    st.session_state.messages = []

    st.success("Conversation Cleared")

    st.rerun()

# ==========================================
# Main Page
# ==========================================

st.title(" Custom AI Chatbot with Memory")

st.markdown(
"""
### Welcome 

This chatbot supports:

- 💬 Multi-turn Conversation
- 🧠 Memory
- 💾 Session Saving
- 📊 Token Counter
- ✂ Automatic Memory Pruning
- ⚡ Gemini API
"""
)

st.divider()


# Session State


if "messages" not in st.session_state:

    st.session_state.messages = []


# Display Chat History


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# Chat Input
# ==========================================
# Chat Input
# ==========================================

prompt = st.chat_input("Ask me anything...")



if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:

        with st.spinner("Thinking..."):

            response = get_ai_response(prompt)

            st.write("DEBUG TYPE:", type(response))
            st.write("IS GENERATOR:", hasattr(response, "__next__"))

            print("TYPE:", type(response))
            print("VALUE:", response)

            with st.chat_message("assistant"):
               full_response = st.write_stream(response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )

    except Exception as e:

        st.error("Something went wrong!")

        st.write("### Exception Type")
        st.code(type(e).__name__)

        st.write("### Exception Message")
        st.code(str(e))

        st.write("### Full Traceback")
        tb = traceback.format_exc()
        st.code(tb)

        print(tb)