import streamlit as st
import asyncio
from agents import Agent, Runner, function_tool
import wikipedia

@function_tool
def wikipedia_lookup(q: str) -> str:
    """Look up a query in Wikipedia and return the result"""
    return wikipedia.page(q).summary

research_agent = Agent(
    name="Research agent",
    instructions="""You research topics using Wikipedia and report on 
                    the results. You may need to use Wikipedia more than once
                    to find the answer to a query.""",
    model="o4-mini",
    tools=[wikipedia_lookup],
)

async def run_agent(input_string):
    result = await Runner.run(research_agent, input_string)
    return result

# Streamlit UI

st.title("Simple Tool-using Agent")
st.write("This agent uses Wiipedia to look up information.")

user_input = st.text_input("Enter a query and press 'Send':")

st.write("Response:")
response_container = st.container(height=300, border=True)

if st.button("Send"):
    response = asyncio.run(run_agent(user_input))
    with response_container:
        st.markdown(response.final_output)
    st.write(response)
    st.json(response.raw_responses)
    