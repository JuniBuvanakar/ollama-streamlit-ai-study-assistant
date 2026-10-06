import streamlit as st
import ollama

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓",
    layout="centered"
)

# ---------------- APPLICATION HEADER ----------------

st.title("🎓 AI Study Assistant")

st.markdown(
    """
    Ask questions, understand difficult concepts, and learn
    new topics with your locally running AI assistant.

    **Powered by Ollama and Qwen3 4B**
    """
)

st.divider()

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.header("About this project")

    st.write(
        "This application uses Streamlit for the user interface "
        "and Ollama to generate answers using a local AI model."
    )

    st.caption("Model: qwen3:4b")
    st.caption("AI processing: Local Ollama runtime")

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------------- DISPLAY CHAT HISTORY ----------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- USER INPUT ----------------

prompt = st.chat_input("Ask me anything...")

if prompt:
    # Display and save the user's message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the conversation for Ollama
    model_messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI study assistant. "
                "Explain concepts clearly and accurately. "
                "Use simple language and examples when useful. "
                "Organize longer answers with headings or bullet points. "
                "If you are uncertain, say so."
            )
        }
    ]

    model_messages.extend(st.session_state.messages)

    # Generate and display the AI response
    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = ollama.chat(
                    model="qwen3:4b",
                    messages=model_messages
                )

                answer = response.message.content

            st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as error:
            # Remove the unanswered user message so it can be retried
            st.session_state.messages.pop()

            st.error(
                "Sorry, I could not get a response from Ollama. "
                "Please check that Ollama is running and that "
                "the qwen3:4b model is available."
            )

            st.caption(f"Technical details: {error}")