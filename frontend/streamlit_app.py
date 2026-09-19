# import requests
# import streamlit as st


# API_URL = "http://backend:8000/ask"


# st.set_page_config(
#     page_title="Medical Coding AI Assistant",
#     page_icon="🏥",
#     layout="wide",
# )


# st.title("🏥 Medical Coding AI Assistant")
# st.write(
#     "Ask questions about medical coding using the available coding documents."
# )


# question = st.text_input(
#     "Enter your medical coding question:",
#     placeholder="Example: What is CPT code 99213?",
# )


# if st.button("Ask"):
#     if not question.strip():
#         st.warning("Please enter a question.")
#     else:
#         try:
#             with st.spinner("Searching coding documents..."):

#                 response = requests.post(
#                     API_URL,
#                     json={"question": question},
#                     timeout=120,
#                 )

#             if response.status_code == 200:
#                 result = response.json()

#                 st.subheader("Answer")
#                 st.write(result["answer"])

#                 sources = result.get("sources", [])

#                 if sources:
#                     st.subheader("Sources")

#                     for source in sources:
#                         document_name = source.get(
#                             "source",
#                             "Unknown",
#                         )

#                         page = source.get(
#                             "page",
#                             "Unknown",
#                         )

#                         score = source.get(
#                             "score",
#                             "Unknown",
#                         )

#                         st.write(
#                             f"- **{document_name}** "
#                             f"| Page: **{page}** "
#                             f"| Rerank Score: **{score}**"
#                         )

#             else:
#                 st.error(
#                     f"API request failed: "
#                     f"{response.status_code} - {response.text}"
#                 )

#         except requests.exceptions.RequestException as exc:
#             st.error(
#                 f"Could not connect to the backend API: {exc}"
#             )



import requests
import streamlit as st


# ============================================================
# Configuration
# ============================================================

API_URL = "http://backend:8000/ask"


st.set_page_config(
    page_title="Medical Coding AI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Custom CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background-color: #f7f7f8;
    }

    /* Remove excessive top spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1100px;
    }

    /* Header */
    .app-header {
        text-align: center;
        padding: 10px 0 20px 0;
    }

    .app-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 5px;
        color: #202123;
    }

    .app-subtitle {
        font-size: 15px;
        color: #6b7280;
    }

    /* User message */
    .user-message {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 14px 18px;
        margin: 15px 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }

    /* Assistant message */
    .assistant-message {
        background: #f0fdf4;
        border: 1px solid #dcfce7;
        border-radius: 12px;
        padding: 18px;
        margin: 15px 0;
        line-height: 1.6;
    }

    /* Avatar */
    .avatar {
        font-size: 22px;
        margin-right: 8px;
    }

    /* Source card */
    .source-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 12px 15px;
        margin: 8px 0;
    }

    .source-title {
        font-weight: 600;
        color: #202123;
        margin-bottom: 5px;
    }

    .source-meta {
        color: #6b7280;
        font-size: 13px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #202123;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Input */
    div[data-testid="stChatInput"] {
        padding-bottom: 20px;
    }

    /* Example buttons */
    .example-title {
        font-size: 14px;
        font-weight: 600;
        color: #6b7280;
        margin-bottom: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Session State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:15px 0;">
            <div style="font-size:45px;">🏥</div>
            <h2>Medical Coding AI</h2>
            <p style="font-size:13px;">
                AI-powered medical coding assistant
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### About")

    st.write(
        "Ask questions about medical coding, CPT, "
        "ICD-10-CM, HCPCS and related coding guidelines."
    )

    st.divider()

    st.markdown("### RAG Pipeline")

    st.markdown(
        """
        🔎 Semantic Search  
        
        🔤 Keyword Search  
        
        🔀 Hybrid Retrieval  
        
        📊 RRF Fusion  
        
        🎯 FlashRank Reranking  
        
        🤖 LLM Generation
        """
    )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# Header
# ============================================================

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">
            🏥 Medical Coding AI Assistant
        </div>
        <div class="app-subtitle">
            Ask questions about medical coding and get
            answers grounded in your coding documents.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Welcome Screen
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:35px 20px;
            color:#6b7280;
        ">
            <div style="font-size:50px;">🩺</div>

            <h3 style="color:#202123;">
                How can I help you today?
            </h3>

            <p>
                Ask a question about medical coding,
                coding guidelines, CPT, ICD-10-CM or HCPCS.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="example-title">Example questions</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "What is CPT code 99213?",
            use_container_width=True,
        ):
            st.session_state.pending_question = (
                "What is CPT code 99213?"
            )

    with col2:
        if st.button(
            "Explain ICD-10-CM coding",
            use_container_width=True,
        ):
            st.session_state.pending_question = (
                "Explain ICD-10-CM coding"
            )

    with col3:
        if st.button(
            "What is HCPCS?",
            use_container_width=True,
        ):
            st.session_state.pending_question = (
                "What is HCPCS?"
            )


# ============================================================
# Display Conversation
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message(
            "user",
            avatar="👤",
        ):
            st.markdown(message["content"])

    else:

        with st.chat_message(
            "assistant",
            avatar="🏥",
        ):
            st.markdown(message["content"])

            sources = message.get("sources", [])

            if sources:

                with st.expander(
                    f"📚 Sources ({len(sources)})",
                    expanded=False,
                ):

                    for index, source in enumerate(
                        sources,
                        start=1,
                    ):

                        document_name = source.get(
                            "source",
                            "Unknown document",
                        )

                        page = source.get(
                            "page",
                            "Unknown",
                        )

                        score = source.get(
                            "score",
                            None,
                        )

                        # Safely format score
                        if isinstance(
                            score,
                            (int, float),
                        ):
                            score_text = f"{float(score):.4f}"
                        else:
                            score_text = str(score)

                        st.markdown(
                            f"""
                            <div class="source-card">

                                <div class="source-title">
                                    📄 {index}. {document_name}
                                </div>

                                <div class="source-meta">
                                    Page: <b>{page}</b>
                                    &nbsp;&nbsp;|&nbsp;&nbsp;
                                    Rerank Score:
                                    <b>{score_text}</b>
                                </div>

                            </div>
                            """,
                            unsafe_allow_html=True,
                        )


# ============================================================
# Handle Example Question
# ============================================================

pending_question = st.session_state.pop(
    "pending_question",
    None,
)


# ============================================================
# Chat Input
# ============================================================

question = st.chat_input(
    "Ask a medical coding question..."
)


if pending_question:
    question = pending_question


# ============================================================
# Send Question
# ============================================================

if question:

    question = question.strip()

    if not question:
        st.warning("Please enter a question.")

    else:

        # ----------------------------------------------------
        # Add user message
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        # Display user message immediately
        with st.chat_message(
            "user",
            avatar="👤",
        ):
            st.markdown(question)

        # ----------------------------------------------------
        # Backend request
        # ----------------------------------------------------

        with st.chat_message(
            "assistant",
            avatar="🏥",
        ):

            try:

                with st.spinner(
                    "🔎 Searching coding documents..."
                ):

                    response = requests.post(
                        API_URL,
                        json={
                            "question": question
                        },
                        timeout=120,
                    )

                # ------------------------------------------------
                # Successful response
                # ------------------------------------------------

                if response.status_code == 200:

                    result = response.json()

                    answer = result.get(
                        "answer",
                        "I couldn't generate an answer.",
                    )

                    sources = result.get(
                        "sources",
                        [],
                    )

                    st.markdown(answer)

                    # --------------------------------------------
                    # Sources
                    # --------------------------------------------

                    if sources:

                        with st.expander(
                            f"📚 Sources ({len(sources)})",
                            expanded=False,
                        ):

                            for index, source in enumerate(
                                sources,
                                start=1,
                            ):

                                document_name = source.get(
                                    "source",
                                    "Unknown document",
                                )

                                page = source.get(
                                    "page",
                                    "Unknown",
                                )

                                score = source.get(
                                    "score",
                                    None,
                                )

                                if isinstance(
                                    score,
                                    (int, float),
                                ):
                                    score_text = (
                                        f"{float(score):.4f}"
                                    )
                                else:
                                    score_text = str(score)

                                st.markdown(
                                    f"""
                                    <div class="source-card">

                                        <div class="source-title">
                                            📄 {index}. {document_name}
                                        </div>

                                        <div class="source-meta">
                                            Page:
                                            <b>{page}</b>
                                            &nbsp;&nbsp;|&nbsp;&nbsp;
                                            Rerank Score:
                                            <b>{score_text}</b>
                                        </div>

                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                    # --------------------------------------------
                    # Save assistant response
                    # --------------------------------------------

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                        }
                    )

                # ------------------------------------------------
                # API error
                # ------------------------------------------------

                else:

                    error_message = (
                        f"Backend returned "
                        f"{response.status_code}: "
                        f"{response.text}"
                    )

                    st.error(error_message)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": (
                                "❌ I couldn't process your "
                                "question because the backend "
                                "returned an error."
                            ),
                            "sources": [],
                        }
                    )

            # ----------------------------------------------------
            # Connection error
            # ----------------------------------------------------

            except requests.exceptions.ConnectionError:

                message = (
                    "❌ I couldn't connect to the backend. "
                    "Please make sure the backend container "
                    "is running."
                )

                st.error(message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": message,
                        "sources": [],
                    }
                )

            # ----------------------------------------------------
            # Timeout
            # ----------------------------------------------------

            except requests.exceptions.Timeout:

                message = (
                    "⏳ The request took too long. "
                    "The backend may still be processing "
                    "the document search."
                )

                st.error(message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": message,
                        "sources": [],
                    }
                )

            # ----------------------------------------------------
            # Other request errors
            # ----------------------------------------------------

            except requests.exceptions.RequestException as exc:

                message = (
                    f"❌ Backend request failed: {exc}"
                )

                st.error(message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": message,
                        "sources": [],
                    }
                )

            # ----------------------------------------------------
            # Unexpected errors
            # ----------------------------------------------------

            except Exception as exc:

                message = (
                    f"❌ Unexpected error: {exc}"
                )

                st.error(message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": message,
                        "sources": [],
                    }
                )

