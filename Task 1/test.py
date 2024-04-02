import streamlit as st

fields = ['First Name', 'Last Name', 'Gender']
item_types = ['text', 'text', 'dropdown']

def display_next_field(current_index):
    if current_index < len(fields):
        field_label = fields[current_index]
        field_type = item_types[current_index]

        if field_type == 'text':
            user_input = st.text_input(field_label)
        elif field_type == 'dropdown':
            options = ['Male', 'Female', 'Other']
            user_input = st.selectbox(field_label, options)
        
        return user_input

def main():
    st.title('Dynamic Form')

    form_data = []
    current_index = st.session_state.get('current_index', 0)

    if st.button('Give Form'):
        user_input = display_next_field(current_index)
        if user_input is not None:
            form_data.append(user_input)
            current_index += 1
            st.session_state['current_index'] = current_index

    st.write('Form Data:', form_data)

if __name__ == "__main__":
    main()
