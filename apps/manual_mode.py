import streamlit as st
import pandas as pd

# GUI for manual input option
def manual_input(gui, params):
    '''
    Manual input of costs, fees, tax, tips.
    '''
    if params:
        total_inputp, datap, tax_inputp, fees_inputp, tip_inputp, sharep = params
        
    else:
        total_inputp=0.0
        datap=''
        describep=''
        tax_inputp=0.0
        fees_inputp=0.0
        tip_inputp=0.0
        sharep=False
    st.title(f'Venmo Requests Calculator {gui}')
    if gui.lower() == '(alpha)':
        st.write("Let us request your friends for you!")
    else:
        st.write("Give us some info, we'll give you a personalized link!")
    with st.beta_expander(label='How To'):
        st.write(f"""
            1. Input the name and itemized money spent in a format of:
                ```
                Peter: 20.21,5.23, 3.21
                Russell: 11.01, 15.89, 1.99
                ```
                Or on a single line:
                ```
                Peter 20.21 5.23 3.21 Russell 11.01 15.89 1.99
                ```
                Or with a split cost (Peter and Russell pay 8 each)
                ```
                Peter and Russell 16
                Peter: 20.21, 5.23
                Russell 11.01 15.89 1.99
                ```
            2. Input the rest of the fees or tips as needed""")
    description = st.text_input(label="(Optional) Description, like the restaurant name", value=describep)
    receipt_input = st.text_area(label="Add name and food prices*", value=datap)
    col1, col2, col3 = st.beta_columns(3)

    with col1:
        fees_input = st.number_input("Fees in dollars",step=1.0, value=fees_inputp)
    with col2:
        tax_input = st.number_input("Tax in dollars",step=1.0, value=tax_inputp)
    with col3:
        tip_input = st.number_input("Tip in dollars",step=5.0, value=tip_inputp)

    return_me = {'description':description, 
                 'receipt_input':receipt_input, 
                 'fees_input':fees_input, 
                 'tax_input':tax_input,
                 'tip_input':tip_input}
    return return_me

def copy_to_clipboard(text):
    '''
    Copies anything in the textbox to clipboard.
    '''
    import streamlit as st
    from bokeh.models.widgets import Button
    from bokeh.models import CustomJS
    from streamlit_bokeh_events import streamlit_bokeh_events
    from io import StringIO
    import pandas as pd
    import js2py
    import streamlit.components.v1 as components
    
    # button styling, function. Textarea content, location.
    input_ =f'''<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>

    <div class="d-grid gap-2 d-md-block">
    <button type="submit" class="btn btn-outline-primary btn-sm" onclick="myFunction()">Copy</button>
    </div>
    
    <div>
    <textarea id="myInput" cols=28 style="position:absolute; left: -10000px;">{text}</textarea>
    </div>
    '''

    # f string so links can be added to textbox
    html_first = f"""<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" 
                        integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" 
                        crossorigin="anonymous"></script> 
                        {input_}
                    """

    # second part of html code, brackets wont allow it to be part of fstring
    html_second = """
    <SCRIPT LANGUAGE="JavaScript">
    function myFunction(){
    var copyText = document.getElementById("myInput");
    copyText.select();
    copyText.setSelectionRange(0, 99999); 
    document.execCommand("copy");
    }
    </SCRIPT>
    """
    # add strings together to get full html code
    html_all = html_first + html_second
    # pass it to components.html
    html_code = components.html(html_all, height=50)
    # add to page
    
    html_code

def replace_recip(my_string,venmo_user):
    "Replaces recipient with the given venmo username"
    import re
    new_string = re.sub("recipients=([A-Z])\w+&",f"recipients={venmo_user}&",my_string)
    return new_string
    
def html_table(link_output, request_money):
    '''
    Presents name, amount, and custom venmo link in a sweet table
    ASCII table source: http://www.asciitable.com/
    Use Hx column, add a % before it
    '''
    
    link_type = st.selectbox("Request payments yourself, or send payme links to your friends", options=['Request them', 'Pay me'])
    
    html_table_header = '''
    <table class="tg">
    '''
    html_table_end = '''</tr>
    </tbody>
    </table>'''
    
    html_table_data = f'''<tbody>'''    
    venmo_logo = 'https://raw.githubusercontent.com/pomkos/payme/main/images/venmo_logo_blue.png'
    
    copy_me = ''
    for key in link_output.keys():
        # append each person's rows to html table 
        html_row = f'''
        <tr>
            <td class="tg-0pky">{key}<br></td>
            <td class="tg-0pky">${request_money[key][0]}</td>
            <td class="tg-0pky"><a href="{link_output[key]}" target="_blank" rel="noopener noreferrer"><img src="{venmo_logo}" width="60" ></a><br></td>
        </tr>'''
        html_table_data += html_row
        
        copy_str = f"""**{key}**: {link_output[key]} \n"""
        copy_me += copy_str
    html_table_all = html_table_header + html_table_data + html_table_end
    
    # get the request links
    if "request" in link_type.lower():
        st.write(html_table_all, unsafe_allow_html=True)
        copied = copy_to_clipboard(copy_me) # copy button
    # get the pay links
    else:
        v_user = st.text_input("Your venmo username")
        if v_user:
            html_table_all = html_table_all.replace("charge","pay")
            html_table_all = replace_recip(html_table_all,v_user)
            
            copy_me = copy_me.replace("charge","pay")
            copy_me = replace_recip(copy_me,v_user)
            
            st.write(html_table_all, unsafe_allow_html=True)
            copied = copy_to_clipboard(copy_me) # copy button
