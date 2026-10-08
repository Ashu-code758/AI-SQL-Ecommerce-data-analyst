import streamlit as st

from agent import run_agent, SYSTEM_PROMPT



# PAGE CONFIG


st.set_page_config(
    page_title="AI E-Commerce Data Analyst",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)



# CUSTOM CSS


st.markdown(
    """
    <style>

    .stApp {
        background: #0e1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #9ca3af;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .status-card {
        background: linear-gradient(
            135deg,
            #151a24,
            #11151d
        );

        border: 1px solid #252b36;
        border-radius: 15px;
        padding: 18px 20px;
        margin-bottom: 20px;
    }

    .status-title {
        font-size: 14px;
        color: #9ca3af;
    }

    .status-value {
        font-size: 20px;
        font-weight: 700;
        margin-top: 5px;
    }

    section[data-testid="stSidebar"] {
        background: #11151c;
    }

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #303642;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# HEADER


st.markdown(
    '<div class="main-title">🤖 AI E-Commerce Data Analyst</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Ask questions about your e-commerce database using natural language.'
    '</div>',
    unsafe_allow_html=True
)


# AI MEMORY


if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


# UI CHAT HISTORY


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []



# STATUS CARDS


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">DATABASE</div>
            <div class="status-value">🗄️ MySQL</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">AI MODEL</div>
            <div class="status-value">🤖 Nemotron</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">ANALYTICS</div>
            <div class="status-value">📊 SQL Agent</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:

    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">MODE</div>
            <div class="status-value">🟢 Read Only</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DISPLAY COMPLETE CHAT HISTORY
# ============================================================

for chat in st.session_state.chat_history:

    
    # USER QUESTION
    

    with st.chat_message("user"):

        st.write(chat["question"])


    
    # AI ANSWER
    

    with st.chat_message("assistant"):

        st.markdown("### 💡 Analysis")

        st.write(chat["answer"])


        # ------------------------------------------
        # SQL
        # ------------------------------------------

        sql_queries = chat.get("sql_queries", [])

        if sql_queries:

            st.markdown("### 🔎 Generated SQL")

            for index, query in enumerate(
                sql_queries,
                start=1
            ):

                with st.expander(
                    f"SQL Query {index}",
                    expanded=False
                ):

                    st.code(
                        query,
                        language="sql"
                    )


        # ------------------------------------------
        # DATABASE RESULTS
        # ------------------------------------------

        database_results = chat.get(
            "database_results",
            []
        )

        if database_results:

            st.markdown("### 📊 Database Result")

            for index, result in enumerate(
                database_results,
                start=1
            ):

                with st.expander(
                    f"Query Result {index}",
                    expanded=False
                ):

                    st.write(result)


        
        # TOOLS USED
        

        tools_used = chat.get(
            "tools_used",
            []
        )

        if tools_used:

            unique_tools = list(
                dict.fromkeys(tools_used)
            )

            st.markdown("### 🛠️ Tools Used")

            cols = st.columns(
                len(unique_tools)
            )

            for col, tool in zip(
                cols,
                unique_tools
            ):

                with col:

                    st.info(
                        f"🔧 {tool}"
                    )


# USER INPUT


question = st.chat_input(
    "Ask something like: Which country has the highest sales?"
)


# PROCESS QUESTION


if question:


    # Add question to AI memory

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # Run AI Agent
    
    try:

        with st.spinner("🔍 Analyzing your data..."):

            result = run_agent(
                st.session_state.messages,
                return_trace=True
            )


        answer = result["answer"]

        trace = result["trace"]


    
        # Save EVERYTHING for UI history
    

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer,
                "sql_queries": trace.get(
                    "sql_queries",
                    []
                ),
                "database_results": trace.get(
                    "database_results",
                    []
                ),
                "tools_used": trace.get(
                    "tools_used",
                    []
                )
            }
        )


        # Rerun UI


        st.rerun()


    except Exception as e:

        st.error(
            "⚠️ Something went wrong while analyzing your question."
        )

        st.caption(
            f"Error: {e}"
        )


# SIDEBAR

with st.sidebar:

    st.markdown(
        "## 🤖 AI Data Analyst"
    )

    st.caption(
        "Natural Language → SQL → Business Insight"
    )

    st.divider()


    
    # PROJECT INFO
    

    st.markdown("### 📌 Project")

    st.write(
        "AI-powered e-commerce analytics agent "
        "that converts natural-language questions "
        "into SQL queries and business insights."
    )

    st.divider()


    
    # EXAMPLE QUESTIONS
    

    st.markdown("### 💬 Example Questions")

    st.caption(
        "Try these:"
    )

    st.write(
        "• Which country has the highest sales?"
    )

    st.write(
        "• Which product generates the highest profit?"
    )

    st.write(
        "• Which category has the highest sales?"
    )

    st.write(
        "• What is the average order value?"
    )

    st.write(
        "• Which country has the highest profit margin?"
    )

    st.write(
        "• Show me the monthly sales trend."
    )

    st.divider()


    # Architecture

    st.markdown("### ⚙️ Architecture")

    st.code(
        """
User Question
      ↓
AI Agent
      ↓
SQL Tool
      ↓
MySQL
      ↓
Database Result
      ↓
Business Insight
        """,
        language="text"
    )

    st.divider()


    # Clear Conversation

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        st.session_state.chat_history = []

        st.rerun()


    st.divider()

    st.caption(
        "🔒 Database access is read-only."
    )

    st.caption(
        "Python • MySQL • NVIDIA AI • Streamlit"
    )