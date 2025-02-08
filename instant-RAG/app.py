import streamlit as st

from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

def initialize_pinecone():
        api_key = st.secrets["PINECONE_API_KEY"]
        pc = Pinecone(api_key=api_key)
        assistant = pc.assistant.Assistant(
            assistant_name="demo1", 
        )
        return assistant

def retrieve_answer(assistant, query, json_mode):
    msg = Message(role="user", content=query)

    resp = assistant.chat(messages=[msg],
                          json_response=json_mode
                          )
    return resp.message

def main(assistant):
    st.markdown("# :blue[Pinecone Assistant]: US Constitution")

    # User query input
    user_query = st.text_input("Enter your query:")
    if st.button("Submit"):
        if user_query:
            answer = retrieve_answer(assistant, user_query, json_mode)
            if json_mode:
                st.json(answer.content)
            else:
                st.write(answer.content)
            full_response.write(answer)
        else:
            st.warning("Please enter a query.")



if __name__ == "__main__":
    
    pa = initialize_pinecone()

    st.sidebar.markdown("# :blue[Options]")
    
    json_mode = st.sidebar.radio("Select Answer Format", 
                                 ("Normal text", "JSON"),
                                 horizontal=True) == "JSON"
    
    full_response = st.sidebar.expander("Full response", expanded=False)

    main(pa)
