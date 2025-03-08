import streamlit as st
import pandas as pd
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
import json

# Set the screen to wide
st.set_page_config(layout="wide")

# Initialize session state variables
if 'api_key' not in st.session_state:
    st.session_state.api_key = None
if 'dataframe' not in st.session_state:
    st.session_state.dataframe = None
if 'file_description' not in st.session_state:
    st.session_state.file_description = ""
if 'metadata' not in st.session_state:
    st.session_state.metadata = {}
if 'code_to_execute' not in st.session_state:
    st.session_state.code_to_execute = ""

# Function to load CSV file into a DataFrame
def load_csv(file):
    return pd.read_csv(file)

st.markdown("# :red[Data Analysis and Visualization with AI]")
st.markdown("*Upload and describe a file in the side bar, then enter a request for a chart below*")


with st.sidebar:
    st.markdown("### :blue[Upload Data]")
    st.markdown("*Upload a CSV file and provide a description of the data*")

    # File uploader for CSV
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        st.write(uploaded_file.name)
        # Load the CSV into a DataFrame
        st.session_state.dataframe = load_csv(uploaded_file)

        # Input for file description
        st.session_state.file_description = st.text_input("Enter a description for the file:")

        # Display DataFrame columns in an editable table
        st.subheader("Edit Column Descriptions")
        column_descriptions = {}
        for idx, column in enumerate(st.session_state.dataframe.columns):
            column_desc = st.text_input(f"Description for '{column}':", "", key=f"desc_{idx}")
            column_descriptions[column] = column_desc

        # Save button (functionality can be implemented later)
        if st.button("Save Descriptions"):
            # Create a dictionary from the column descriptions
            st.session_state.metadata = {
                "file name": uploaded_file.name,
                "file_description": st.session_state.file_description,
                "column_descriptions": column_descriptions
            }

            st.text(json.dumps(st.session_state.metadata, indent=4))
            st.success(f"Descriptions saved!")

col1, col2 = st.columns([1, 1])
with col1:

    st.markdown("### :blue[Create Chart]")
    st.markdown("*Enter a descrition of the chart you want to create, generate the code, edit it and run it*")

    request = st.text_input("Enter your request:", key="request")

    # Do not change this. This is the 'user' prompt constructed from the user request
    plotting_lib = "plotly express (use a figure size of 800 x 600)"

    prompt = f"""
    The data to be read iis in CSV format. A description of the data, including the file name, follows:

    <description>
    {json.dumps(st.session_state.metadata, indent=4)}
    </description>

    Your task is as follows:
    <task>
    {request}
    </task>

    You should generate the code to read the data file and create a {plotting_lib} chart as described.
    Display the plot using Streamlit syntax.

    The expected output is valid Python code for a {plotting_lib} chart
    """

    # System prompt
    sys_prompt = f"""
    You are an expert in writing Python code for data analysis and visualization.
    Your aim is to read and analyse data and create the code for a chart as instructed.
    Do not read the data directly. Use the metadata provided to create the a {plotting_lib} chart 
    from the data described there. Do not use Markdown fencing around the code. 
    Do not include any comments, explanations, or markdown formatting. Output plain Python code only.
    """

    #st.write(prompt)
    #st.write(sys_prompt)

    # Input for OpenAI API key

    if 'key' not in st.session_state or not st.session_state.key:
        st.header("API Key Input")
        st.session_state.key = st.text_input("Enter your OpenAI API key:", key="key_id", type="password")


    if st.button("Generate Chart Code"):
        try:
            class CodeResponse(BaseModel):
                code: str
                instructions: str

            model = OpenAIModel(model_name='gpt-4o-mini', api_key=st.session_state.key)
            agent = Agent(model, system_prompt=sys_prompt)

            result = agent.run_sync(prompt, result_type=CodeResponse)

            #st.write(result.data)
            #st.code(result.data.code, language="python")
            st.session_state.code_to_execute = result.data.code

        except Exception as e:
            st.error(f"An error occurred: {e} Did you enter the correct API key?")

    code =st.session_state.code_to_execute.replace("\\n", "\n")
    code = st.text_area("Code to Execute - edit it here hit ctrl/enter to save", code, height=500)
    
with col2:
    st.warning("""##### :red[Running AI-generated code is potentially dangerous. Review the code first.]""")
    if st.button("Run Code"):
        #code =st.session_state.code_to_execute.replace("\\n", "\n")
        #st.text(code)
        exec(code)

