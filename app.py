from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(upload_file):
    if upload_file is not None:
    ## convert pdf to image
        images=pdf2image.convert_from_bytes(upload_file.read())

        first_page=images[0]

        # convert to bytes
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("Application Tracking System")
input_text=st.text_area("Job Description: ",key="input")
upload_file=st.file_uploader("Upload your resume(PDF)....",type=["pdf"])

if upload_file is not None:
    st.write("PDF Uploaded successfully")

submit1 = st.button("Tell me about the resume")

submit2 = st.button("How Can u improvise my skills")

submit3 = st.button("Percentage match")

input_prompt1 = """You are an experienced HR with Technical Experience in the field of any one job role from  Data science, Full stack web development,Big Data Engineering, DEVOPS, Data Analyst your task is to review the provided resume against the job description for these profiles.
Please Share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weakness of the applicant in relation to the specified job requirements"""

#input_prompt2 = """You are an Technical Human Resource Manger with expertise in Data science, Full stack web development,Big Data Engineering, DEVOPS, Data Analyst you role is to scrutinize the resume in light of the job description provided. Share your insights on the candidates's suitability for the role from an HR perspective  """

input_prompt3 =""" You are skilled ATS (Applicant Tracking System) scanner with deep understanding of Data science, Full stack web development,Big Data Engineering, DEVOPS, Data Analyst and deep ATS functionality
your task is to evaluate the resume against the provided job description, give me the percentage match if the resume matches of the job description.
First the output should come as percentage and then keywords missing and last Final thoughts. """

if submit1:
    if upload_file is not None:
        pdf_content= input_pdf_setup(upload_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit3:
    if upload_file is not None:
        pdf_content= input_pdf_setup(upload_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")




