import streamlit as st
from code_utils.auth import login_st_form

st.set_page_config(page_title='Shopify Scraper', page_icon='🌶️', initial_sidebar_state="auto", menu_items=None)

st.title('🚀 Shopify Scraper')
st.markdown('Spy all your Ecommerce competitors to replicate their success...')

logged_in = login_st_form()

if logged_in:
    st.success('You are logged in!')
    st.balloons()
    st.markdown('Add Your Streamlit App Here!')
