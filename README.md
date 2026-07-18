# QnA Chatbot 

You Can access this at -  [qna-chatbot-using-groq](https://qna-chatbot-using-groq-5mqvwhemgog3okkigyuzcv.streamlit.app/)



In my Gen AI journey, this is where I currently am. I built a QnA chatbot using **Groq** and **Serper**, which can search Google in real time and use those results to answer questions.

## How it works

The agent is built using:

 **LLM** — Groq (`model="llama-3.3-70b-versatile"`), chosen for its low cost and fast inference speed
 
 **Tool** — Serper's built-in search tool, `GoogleSerperAPIWrapper().run`, for real-time web search
 
 **Checkpointer** — `MemorySaver`, used as the agent's memory to maintain conversation context
 
 **System prompt** — defines the agent's role and how it should behave

Conversation history (questions and answers) is saved in Streamlit's session state:

```python
if "history" not in st.session_state:
    st.session_state.history = []
```

After building the agent, the interface was built using **Streamlit**, with `streaming=True` enabled so responses stream in as they're generated — just like a real chat experience.


You're welcome to upgrade this chatbot , just please don't change the core idea behind the code.


**Siddharth Shukla**
GitHub: [@siddharth277](https://github.com/siddharth277)
