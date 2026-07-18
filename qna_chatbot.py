from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st

from dotenv import load_dotenv
load_dotenv()


@st.cache_resource
def get_agent():
    llm = ChatGroq(model="llama-3.3-70b-versatile", streaming=True)
    search = GoogleSerperAPIWrapper()
    tools = [search.run]
    memory = MemorySaver()
    agent = create_agent(
        model=llm,
        tools=tools,
        checkpointer=memory,
        system_prompt=(
            "You are an intelligent AI agent with access to a web search tool. "
            "Be precise and concise. Only call the search tool ONCE per question "
            "unless the first result is clearly insufficient or irrelevant. "
            "After receiving search results, answer directly — do not search "
            "again for the same or a very similar query."
        )
    )
    return agent


agent = get_agent()

if "history" not in st.session_state:
    st.session_state.history = []

#### Building Web Interface
st.subheader("QNA_chatbot - By Siddharth Shukla")

for message in st.session_state.history:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)


query = st.chat_input("Ask Anything ?")
if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role": "user", "content": query})

    response = agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        {"configurable": {"thread_id": "1"}},
        stream_mode="messages"
    )

    ai_container = st.chat_message("ai")
    with ai_container:
        space = st.empty()
        message = ""

        try:
            with st.spinner("Thinking..."):
                for chunk in response:
                    if chunk[0].content:
                        message = message + chunk[0].content
                        space.write(message)
        except Exception as e:
            message = f"Error: {e}"
            st.error(message)

        st.session_state.history.append({"role": "ai", "content": message})