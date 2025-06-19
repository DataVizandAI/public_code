import streamlit as st
import asyncio
from agents import Agent, Runner

writer_agent = Agent(
    name="Writer agent",
    instructions=f"""
                    Re-write the article so that it is suitable for kids aged around 8. 
                    Be enthusiastic about the topic - everything is an adventure! 
                    """,
    model="o4-mini",
)

researcher_agent = Agent(
    name="Research agent",
    instructions=f"""
                    You research topics and report on the results. """,
    model="o4-mini",
)

async def run_agent(input_string):
    result = await Runner.run(researcher_agent, input_string)
    result2 = await Runner.run(writer_agent, result.final_output)
    return result2

# Streamlit UI

st.title("Writer Agent")
st.write("Write stuff for kids.")

user_input = st.text_input("Enter a query and press 'Send':")

st.write("Response:")
response_container = st.container(height=300, border=True)

if st.button("Send"):
    response = asyncio.run(run_agent(user_input))
    with response_container:
        st.markdown(response.final_output)
    st.write(response)
    st.json(response.raw_responses)
    