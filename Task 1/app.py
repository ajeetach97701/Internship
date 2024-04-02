import streamlit as st
import os
import json
import smtplib
import email.message
from dotenv import load_dotenv
import streamlit.components.v1 as components

load_dotenv()
os.getenv("GOOGLE_API_KEY")

PASSWORD = "zfcgddeivxgihwux"
EMAIL = "devpalmmind@gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_PASSWORD = "zfcgddeivxgihwux"
EMAIL_TO = "ajeetacharya02@gmail.com"

def Display_form(fields, field_types):
    data = st.session_state.get('data', {})
    index = st.session_state.get('index', 0)

    for i, field_name in enumerate(fields):
        if index == i:
            if field_types[i] == 'text':
                data[field_name] = st.text_input(field_name)
            elif field_types[i] == 'dropdown':
                data[field_name] = st.selectbox(f"Select {field_name.lower()}", ["Male", "Female"])
            elif field_types[i] == 'date':
                data[field_name] = st.date_input(field_name)

    st.session_state['data'] = data

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
            st.session_state.pop("form_selected", None)
            st.session_state.pop("form_displayed", None)
            st.rerun()

def send_mail(Content, subject):
    try:
        msg = email.message.Message()
        msg['Subject'] = f"{subject}"
        msg['FROM'] = EMAIL
        msg['To'] = EMAIL_TO
        msg.add_header("Content-Type", 'text/html')
        msg.set_payload(f'{Content}')
        smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        smtp.starttls()
        smtp.login(EMAIL, EMAIL_PASSWORD)
        smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
        smtp.quit()
        print("Successfully sent")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")


def main():
    col1, col2 = st.columns(2)
    index = st.session_state.get('index', 0)
    if col1.button('Student Registration Form'):
        st.session_state['form_selected'] = 'Student Registration Form'
        fields = []
        field_types = []

        with open('form.json', 'r') as f:
            data = json.load(f)
        form_item = data.get('forms')

        form_selected = st.session_state.get('form_selected')
        if form_selected is None:
            return

        form = form_item[form_selected]
        for field in form['fields']:
            fields.append(field['label'])
            field_types.append(field['type'])

        if index < len(fields):
            Display_form(fields, field_types)

    if col2.button('Hospital Registration Form'):
        st.session_state['form_selected'] = 'Hospital Registration Form'
        fields = []
        field_types = []

        with open('form.json', 'r') as f:
            data = json.load(f)
        form_item = data.get('forms')

        form_selected = st.session_state.get('form_selected')
        if form_selected is None:
            return

        form = form_item[form_selected]
        for field in form['fields']:
            fields.append(field['label'])
            field_types.append(field['type'])

        if index < len(fields):
            Display_form(fields, field_types)


if __name__ == "__main__":
    main()
