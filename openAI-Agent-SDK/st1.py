import streamlit as st
import asyncio
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

async def run_agent(input_string):
    result = await Runner.run(agent, input_string)
    return result.final_output


# Streamlit UI

st.title("Simple Agent SDK Query")

user_input = st.text_input("Enter a query and press 'Send':")

st.write("Response:")
response_container = st.container(height=300, border=True)

if st.button("Send"):
    response = asyncio.run(run_agent(user_input))
    with response_container:
        st.markdown(response)

