import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from dotenv import load_dotenv
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import email.message


PASSWORD="zfcgddeivxgihwux"
EMAIL="devpalmmind@gmail.com"
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
EMAIL_PASSWORD="zfcgddeivxgihwux"
EMAIL_TO="ajeetacharya02@gmail.com"


load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def ChatModel():
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)
    user_input = st.text_input("Type form to display the form.")
        
    if "form" in user_input:
        Display_form()
                               
            
def Display_form():
    fields = ["First Name", "Last Name", "Gender", "DOB", "Address"]
    index = st.session_state.get('index', 0)
    data = st.session_state.get('data', {})

    if index < len(fields):
        field_to_collect = fields[index]
        if field_to_collect == "DOB":
            data[field_to_collect] = st.date_input(field_to_collect)
        elif field_to_collect == "Gender":
            data[field_to_collect] = st.selectbox("Select gender", ["Male", "Female"])
        else:
            data[field_to_collect] = st.text_input(field_to_collect)

        if st.button("Next"):
            index += 1
            st.session_state.index = index
            if index < len(fields):
                st.empty()
        else:
            st.session_state.data = data
    else:
        action = st.radio("What would you like to do?", ("Submit", "Cancel", "Restart"))
        if st.button("Submit"):
            if action == "Submit":
                st.write("Data submitted successfully!", st.session_state['data'])
                json_data = st.session_state['data']
                mail_data = send_mail(json_data, "Test mail")
                print(mail_data)

            elif action == "Cancel":
                st.write("Data intake process canceled.")
            elif action == "Restart":
                st.session_state.pop("index", None)
                st.session_state.pop("data", None)
                st.switch_page("app.py")
                st.rerun()
                


def send_mail(Content, subject):
    try:
        msg = email.message.Message()
        msg['Subject'] = f"{subject}"
        msg['FROM'] =  EMAIL
        msg['To'] = EMAIL_TO
        msg.add_header("Content-Type", 'text/html')
        msg.set_payload(f'{Content}')
        smtp = smtplib.SMTP(SMTP_HOST,SMTP_PORT)
        smtp.starttls()
        smtp.login(EMAIL,EMAIL_PASSWORD)
        smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
        smtp.quit()
        print("Succesfully send")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")


def main():
    ChatModel()


if __name__ == "__main__":
    main()
