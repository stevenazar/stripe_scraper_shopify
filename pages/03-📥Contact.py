import streamlit as st 

st.set_page_config(page_title='ScrapStore', page_icon=':bar_chart:', initial_sidebar_state="auto", menu_items=None)

st.header(":mailbox: Get In Touch With Us !")

contact_form = """
<form action="https://formsubmit.co/tony.azrk@gmail.com" method="POST">
    <input type="hidden" name="_captcha" value="False">
    <input type="text" name="name", placeholder="Enter your name" required>
    <input type="email" name="email" placeholder="Enter your email" required>
    <textarea name="message" placeholder="Details of your query"></textarea>
    <button type="submit">Send</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)

#use o local css file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("pages/style.css")
