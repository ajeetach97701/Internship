import streamlit as st
import os
import json
import smtplib
import email.message
import streamlit.components.v1 as components

PASSWORD = "zfcgddeivxgihwux"
EMAIL = "devpalmmind@gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_PASSWORD = "zfcgddeivxgihwux"
EMAIL_TO = "ajeetacharya02@gmail.com"

def Display_form(fields, field_types, action, form):
    components.html("""
        <script>
            const inputs = window.parent.document.querySelectorAll('input');
            inputs.forEach(input => {
                input.addEventListener('keydown', function(event) {
                    if (event.key === 'Enter') {
                        event.preventDefault();
                    }
                });
            });
        </script>
        """,
        height=0
    )

    data = st.session_state.get('data', {})
    form_name = st.session_state.get('form_name', '')
    index = st.session_state.get('index', 0)
    current_index = 0

    if st.session_state.get('form_name') == None:
        st.session_state.get('form_name', action)
    if st.session_state.get('form_name') != action:
        st.session_state['data'] = {}
        data = {}
        st.session_state['index'] = 0
        st.session_state['form_name'] = action
        index = 0
    
    for i, field_name in enumerate(fields):
        if i == len(fields) - 1:
            # print("Reached the last index")
            current_index = i  
        else:
            print("")
            # print("Not the last index yet")
        
        if field_types[i] == 'text':
            value = st.text_input(field_name)
        elif field_types[i] == 'date':
            value = st.date_input(field_name, value=None)
        elif field_types[i] == 'dropdown':
            field = form['fields'][i]
            options = field.get('options', [])  # Fetch options if present, otherwise default to empty list
            value = st.selectbox(f"Select {field_name.lower()}", options)
        if value:
            print(f"Before increment index{index}")
            index += 1
            print(f"After increment index{index}")
            data[field_name] = value
            st.session_state['index'] = index
            st.session_state['data'] = data  
        else:
            st.write(data)
            break
    
    if(index < len(fields)-1):
        if st.button("Next"):
            print(f"The index{i}")
            # index += 1
    else:
                Submit(data)
            
        
        

def Submit(data):
    if st.button("Submit"):
        st.write("Data submitted successfully!", st.session_state['data'])
        json_data = st.session_state['data']
        json_data = data
        mail_data = send_mail(json_data, "Test mail")
        print(mail_data)
    if st.button("Cancel"):
        st.session_state.pop("index", None)
        st.session_state.pop("data", None)
        st.write("Data intake process canceled.")
    if st.button("Restart"):

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

def main():
    fields = []
    field_types = []
    options = []
    col1, col2 = st.columns(2)
    index = st.session_state.get('index', 0)
    with open('form.json', 'r') as f:
        data = json.load(f)
    forms_dict = data.get('forms', {})

    # Extract the names of the forms
    form_names = ["None"]
    form_data = list(forms_dict.keys())
    form_names.extend(form_data)
    action = st.selectbox("Select A form", form_names)
    if action == "None":    
        st.switch_page("app.py")
        st.rerun()
    else:
        form = data['forms'][action]
        st.write(form['form_name'])
        for field in form['fields']:
            fields.append(field['label'])
            field_types.append(field['type'])
        Display_form(fields=fields, field_types=field_types, action=action, form=form)

if __name__ == "__main__":
    main()
