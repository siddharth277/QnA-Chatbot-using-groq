You Can access this at - https://qna-chatbot-using-groq-5mqvwhemgog3okkigyuzcv.streamlit.app/

In my Gen AI Journey , 
Now i am here in this phase , i made a qna chatbot using groq and serper , which can search on realtime from google and give us answer .

Agent is made up using LLM - Groq ( model="llama-3.3-70b-versatile" )(used because of low cost and groq is fast as well) , tool is inbuilt in serper i.e. GoogleSerperAPIWrapper().run , checkpointer = memory for memory saver , 
and system prompt to address the agent their work. 

-> if "history" not in st.session_state:
    st.session_state.history = [] 
--- this is for saving the answer and question 

Then after making agent , we moved on making the interface using Streamlit . 
Used Streaming = True , to see the result streaming 


You Are welcomed to upgrade this chatbot without changing the core idea of code .

Siddharth Shukla 
github.com/siddharth277
