import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title='ScrapStore', page_icon=':bar_chart:', initial_sidebar_state="auto", menu_items=None)

st.title('ScrapStore :bar_chart:')


st.markdown(    
    """
### Price scraping to optimize your marketing strategy
ScrapStore is a formidable price scraping tool that will allow you to obtain information at your disposal...
    """)


sign_up = st.button('Sign Up', type='primary')
if sign_up:
    switch_page('sign up')