from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import os
from PIL import Image

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

# Function to load gemini-pro-vision
model = genai.GenerativeModel('gemini-pro-vision')

def get_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type":uploaded_file.type, 
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title = "MultiLanguage Invoice Extracter")
st.subheader("MultiLanguage Invoice Extracter")

input = st.text_input("Input Prompt: ",key = 'input')
uploaded_file = st.file_uploader("Choose an image of the invoice ...",type=['jpg','jpeg','png'])
image=""

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption = 'Uploaded Image', use_column_width = True)

submit = st.button("Tell me about the Invoice")

input_prompt = """
you are an expert in understanding invoices. We will upload an image of incoice and you 
will have to answer any questions based on the uploaded invoice image.
"""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_response(input_prompt, image_data,input)
    st.subheader("The Response is")
    st.write(response)