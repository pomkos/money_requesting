# core app. Redirects to appropriate apps.

# libraries
import streamlit as st
st.set_page_config(page_title = 'Venmo Calculator')
import pandas as pd
import numpy as np
import re
import sys

# files
from apps import calculator as calc
from apps import manual_mode as mm

# arguments
us_pw = sys.argv[1]  # user input: "my_user:password"
db_ip = sys.argv[2]  # user input: 192.168.1.11
port = sys.argv[3]   # user input: 5432
db_info = [us_pw, db_ip, port]

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
<script src="https://cdn.jsdelivr.net/npm/darkmode-js@1.5.7/lib/darkmode-js.min.js"></script>
<script>
  function addDarkmodeWidget() {
    new Darkmode().showWidget();
  }
  window.addEventListener('load', addDarkmodeWidget);
</script>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def start(button=None): # button arg doesnt do anything
    '''
    Thalamus. Creates the GUI and redirects requests to the appropriate scripts. The Thalamus.
    '''
#     if st.experimental_get_query_params():
#         params = use_params()
#         st.write(params)
#         if params[-1] == True: # if the link is shared
#             st.info("Looks like this is a shared link, so we filled in the info for you!")
#             select_input = params[-2]
    params = None
    
    select_input = 'release' # disabled user section of payme ('alpha' to activate)
    service_chosen = st.select_slider("",options=['Delivery App','Manual Mode'])
    
    if 'Manual' not in service_chosen:
        gui = 'doordelivery'
        user_output = mm.manual_input(gui, params)
    else:
        gui = 'Manual'
        user_output = mm.manual_input(gui, params)
        
    total_input, data = calc.total_calculator(**user_output)
    # dictionary of kwargs for venmo_calc()
    user_modified = {
        'tax':user_output['tax_input'],
        'tip':user_output['tip_input'],
        'misc_fees':user_output['fees_input'],
        'description':user_output['description'],
        'total':total_input,
        'discount':user_output['discount'],
        'contribution':user_output['contribution'],
        'my_dic':data
    }
    try:
        calc_message = calc.venmo_calc(**user_modified, clean=False)
        mm.html_table(calc_message["messages"], calc_message["request_money"])

    except ZeroDivisionError:
        st.info("See the how to for more information!")
        calc_message={'request_money':None}
        st.stop()
    # add parameters to url for easy sharing
    if st.button("Ping Pete some love!"):
        st.balloons()
        st.success("Thanks for using payme! <3")
        send_webhook() # notify Pete that someone used payme!
        st.stop()
        
    ###################
    # TESTING GROUNDS #
    ###################
    if ('alpha' in select_input) and calc_message['request_money']:
        from apps import alpha_users
        st.write()
        alpha_users.app(my_dic = calc_message['request_money'], total=total_input, 
                        messages = calc_message['messages'],db_info=db_info)
        st.write("_________________________")
    
def image_rec_logic():
    '''
    Image recognition is moot, but saving for posterity and funsies
    '''
    ################
    # MORE OPTIONS #
    ################
    options = ['Copy-Paste','Auto Request (Alpha)', 'Image Recognition (Beta)']
    if 'door' in service_chosen:
        website = 'doordash'
        select_input = st.sidebar.selectbox("How would you like to analyze the receipt?", options = options)

    elif 'uber' in service_chosen:
        website = 'ubereats'
        select_input = st.sidebar.selectbox("How would you like to analyze the receipt?", options = options)
        if ('beta' in select_input.lower()) or ('alpha' in select_input.lower()):
            st.warning('Not yet implemented.')
            st.stop()
    select_input = select_input.lower()
    if 'beta' in select_input:
        from apps import beta_image_rec as ir
        gui = '(Beta)'
        user_output = ir.auto_input(gui)
    elif 'alpha' in select_input:
        gui = '(Alpha)'
        user_output = mm.manual_input(gui, params)
        
    # gets a dictionary of total spent, dictionary of spent on food, percent tip, percent tax, and misc fees per person
    if "alpha" in select_input:
        calc_message = calc.venmo_calc(**user_modified, clean=True)
    else:
        # if manual or orc, then show the html table
        calc_message = calc.venmo_calc(**user_modified, clean=False)
        mm.html_table(calc_message["messages"], calc_message["request_money"])
            
def send_webhook():
    '''
    Sends a hook to zapier, which emails me.
    '''
    import json
    import requests
    from apps import secret
    
    webhook_url = secret.app()
    response = requests.get(webhook_url)
    
    if response.status_code != 200:
        raise ValueError(
        'Request to zapier returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )
        
def app():
    '''
    Only purpose is to start the app from bash script. Own function so the rest of the functions can be organized in a logical way.
    '''
    start(button='start')

app()