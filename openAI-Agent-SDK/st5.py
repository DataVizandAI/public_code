import streamlit as st
import asyncio

from agents import Agent, Runner, handoff

adult_writer_agent = Agent(
    name="Adult Writer Agent",
    instructions=f"""Write the article based on the information given that it is suitable for adults interested in culture.
                    """, 
    model="o4-mini",
)

teen_writer_agent = Agent(
    name="Teen Writer Agent",
    instructions=f"""Write the article based on the information given that it is suitable for teenagers who want to have a cool time.
                    """, 
    model="o4-mini",
)

kid_writer_agent = Agent(
    name="Kid Writer Agent",
    instructions=f"""Write the article based on the information given that it is suitable for kids of around 8 years old. 
                    Be enthusiastic!
                    """, 
    model="o4-mini",
)

researcher_agent = Agent(
    name="Research agent",
    instructions=f"""Find information on the topic(s) given and, if a type of reader is given handoff to the appropriate writer agent""",
    
    model="o4-mini",
    handoffs = [kid_writer_agent, teen_writer_agent, adult_writer_agent]
)

async def run_agent(input_string):
    result = await Runner.run(researcher_agent, input_string)
    return result

# Streamlit UI

st.title("Writer Agent3")
st.write("Write stuff for adults, teenagers or kids.")

user_input = st.text_input("Enter a query and press 'Send':")

st.write("Response:")
response_container = st.container(height=300, border=True)

if st.button("Send"):
    response = asyncio.run(run_agent(user_input))
    with response_container:
        st.markdown(response.final_output)
    st.write(response)
    st.json(response.raw_responses)
    