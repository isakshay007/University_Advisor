import os
import shutil
import streamlit as st
from PIL import Image
from lyzr import ChatBot

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

# Set Streamlit page configuration
st.set_page_config(
    page_title="Lyzr",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png",
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("University Advisor🎓")
st.markdown("### Built using Lyzr SDK🚀")
st.markdown("Welcome to the University Advisor app! Ready to explore Ivy League possibilities? Share your GRE and IELTS scores, your ambition, and your budget. We'll tailor personalized recommendations just for you! Let's find your perfect Ivy League match together!")

# Function to remove existing files in the directory
def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")

# Set the local directory
data_directory = "data"

# Create the data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Remove existing files in the data directory
remove_existing_files(data_directory)

# Function to implement RAG Lyzr Chatbot
def rag_implementation(file_path):
    _, file_extension = os.path.splitext(file_path)
    supported_extensions = [".pdf", ".docx"]

    if file_extension.lower() in supported_extensions:
        model = "gpt-4"
        if file_extension.lower() == ".pdf":
            return ChatBot.pdf_chat(input_files=[file_path], llm_params={"model": model})
        else:
            return ChatBot.docx_chat(input_files=[file_path], llm_params={"model": model})
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX files are supported.")

# Function to get Lyzr response
def advisor_response(file_path, gre, ielts, expense, ambition):
    rag = rag_implementation(file_path)
    prompt = f""" 
You are an expert university student advisor. Always Introduce yourself. Your task is to provide university recommendations by analyzing the provided GRE scores {gre}, IELTS scores {ielts}, the user's ambition {ambition}, and the average tuition fee {expense}, and suggest the most suitable universities from the uploaded document.Dont mention "uploaded document" in your responses.

Here's your step-by-step guide:

1. Begin by examining the uploaded document with detailed information on various universities to understand the options available.

2. Next, evaluate the user's GRE {gre} and IELTS {ielts} scores to gauge their academic standing.

3. Consider the user's ambition and assess their financial constraints by looking at their provided average tuition fee {expense}.

4. Compare and match the user's qualifications, goals, and financial capacity with appropriate universities from your initial analysis.

5. Compile a shortlist of universities that best align with all of the user's criteria, focusing on those that closely match their profile.

6. Present your recommendations to the user in a clear manner, explaining why each university is a strong match based on their individual needs and aspirations.

You must undertake this task with diligence as it will have a profound effect on a student's future education path.

Keep in mind that you should only display universities that closely match the user's profile in markdown , rather than showing the entire list from the uploaded document. Your recommendations should be customized to fit both academic standards and financial capabilities while supporting long-term objectives.
"""
    response = rag.chat(prompt)
    return response.response

# File path input field
file_path = "Ivy league info.docx"

# Check if file path is not empty and exists
if file_path and os.path.exists(file_path):
    # User input 
    gre = st.number_input("What's your GRE score?", step=10, min_value=260, max_value=340)
    ielts = st.number_input("What's your IELTS score?", step=0.5, min_value=5.0, max_value=9.0)
    ambition = st.text_input("What is your ambition?")
    expense = st.text_input("Your expected average tuition fee?", placeholder="$")

    # Generate advice button
    if st.button("Get Advice"):
        if not gre or not ielts or not ambition or not expense:
            st.warning("Please fill out all fields.")
        else:
            automatic_response = advisor_response(file_path, gre, ielts, expense, ambition)
            st.markdown(automatic_response)
else:
    st.info("Please enter a valid file path.")

# Footer or any additional information
with st.expander("ℹ️ - About this App"):
    st.markdown(
        """Experience the seamless integration of Lyzr's ChatBot as you refine your documents with ease. For any inquiries or issues, please contact Lyzr."""
    )
    st.link_button("Lyzr", url="https://www.lyzr.ai/", use_container_width=True)
    st.link_button(
        "Book a Demo", url="https://www.lyzr.ai/book-demo/", use_container_width=True
    )
    st.link_button(
        "Discord", url="https://discord.gg/nm7zSyEFA2", use_container_width=True
    )
    st.link_button(
        "Slack",
        url="https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw",
        use_container_width=True,
    )
