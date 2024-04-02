import smtplib
import email.message

import streamlit as st

def Submit(data):
    action = st.radio("What would you like to do?", ("Submit", "Cancel", "Restart"))
    if st.button("Submit"):
        if action == "Submit":
            print("here submit")    
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
