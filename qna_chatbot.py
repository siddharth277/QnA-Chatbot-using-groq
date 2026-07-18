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
            "When you get search results back, NEVER copy-paste raw snippets, titles, "
            "hashtags, links, or ads from the search results into your answer. "
            "Instead, read the search results, extract only the relevant facts, and "
            "write a short, clear, natural-language answer in your own words — as if "
            "you already knew the answer and were explaining it directly to the user. "
            "Ignore promotional content, video titles, social media handles, and "
            "unrelated links that may appear in search results. "
            "Only call the search tool ONCE per question unless the first result is "
            "clearly insufficient or irrelevant. Be concise: 2-4 sentences unless the "
            "user asks for more detail. "
            "For subjective or opinion-based questions (e.g. 'who is better', 'which is best'), "
            "clearly state that it's subjective, then briefly summarize what each side is known "
            "for based on the search results, without declaring a winner."
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
                    msg = chunk[0]
                    if getattr(msg, "type", None) == "ai" and msg.content:
                        message = message + chunk[0].content
                        space.write(message)
        except Exception as e:
            message = f"Error: {e}"
            st.error(message)
        st.session_state.history.append({"role": "ai", "content": message})
