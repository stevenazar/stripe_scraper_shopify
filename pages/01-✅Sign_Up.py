import streamlit as st
from code_utils.auth import create_account_st_form
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title='ScrapStore', page_icon=':bar_chart:', initial_sidebar_state="auto", menu_items=None)

if create_account_st_form():
    switch_page('ScrapShop')

#presentation in synthetic forms of data from numerous e-commerce stores with 
#some success and constantly updated according to monthly results.