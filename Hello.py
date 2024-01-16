
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
from streamlit.logger import get_logger
import re

LOGGER = get_logger(__name__)



st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            a {display:none; visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


st.markdown(
    """
    <style>
    .st-emotion-cache-zq5wmm, .st-emotion-cache-zq5wmm.ezrtsby0,
    #MainMenu
    {
        display: none;
        visibility: hidden;
    }
    footer{
        display:none;
        visibility:hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)



def run():

    st.title("Search Bulk Pickup Zones by Address")

    st.markdown('''
                <p style="color:red">Important Note:</p>
                <ul>
                <li>
                <b>Supported Browsers:</b> Google Chrome, Microsoft Edge, or Safari.
                </li>
                <li> 
                Please <u>do not</u> include apartment, floor, 
                or unit information in your search. 
                </li>
                <li>
                Please use prefixes, suffixes, and/or abbreviations when applicable. For example, if 
                your address is located on 1234 East 18 Avenue, please search <i><b>"1234 E 18th Ave, Paterson, NJ".</b></i> 
                </li>
                <li>
                Example Searches: "155 Market St, Paterson, NJ" or "155 Market St".
                </li>
                </ul>
                ''', unsafe_allow_html=True)

    query = st.text_input("Search Address", 
                          placeholder="155 Market St") # clear spaces from query
    query = query.replace(" ", "")

    if query:
        with st.spinner('Please wait...'):
            res = search(query)
            if isinstance(res, pd.DataFrame):
                st.success('Address found.')
                st.dataframe(res, width=None)
            else:
                st.error("No address found.")


def search(query):
    #if validate_text(query) == 2:
        #return None
        #st.error("Invalid address.")
    if validate_text(query):
        try:  
            df = pd.read_excel("Trash-Zones.xlsx")
            with st.spinner('Please wait...'):
                res = df[df["Address_Strip"].str.contains(query, case=False,  #match case-insensitive address
                                                regex=False)]
        except Exception as e: # raise if any query that includes symbols or invalid input
            return None
            #st.error("Invalid address.")
        else:
            if not res.empty:  
                with st.spinner('Wait for it...'):
                    #st.success('Address found.')
                    res = res[["Address", "Zone"]]
                    res = res.set_index("Address")
                    res = res.head(3)
                    return res  
            else:
                return None
                #st.error("Address not found.") 

def validate_text(q): # checks for empty string, 
    #valid_pattern = r"^[a-zA-Z0-9,]+$"
    #valid_pattern = r"[\w,]+"
    comma_pattern = r"^[,]*$"
    #just_st_name = r"^[st|ave|ter|ln|pl|brg|run|dr|ct|pkwy|mall|plz|way|rd|trl|blvd]$"
    just_st_name = r"^(st|ave|ter|ln|pl|brg|run|dr|ct|pkwy|mall|plz|way|rd|trl|blvd|st\.|ave\.|ter\.|ln\.|pl\.|brg\.|rd\.|blvd\.|dr\.|pl\.)$"
    #st|ave|ter|ln|pl|brg|run|dr|ct|pkwy|mall|plz|way|rd|trl|blvd|st\.|ave\.|ter\.|ln\.|pl\.|brg\.|rd\.|blvd\.|dr\.|pl\.
    #if re.search(valid_pattern, q) and not re.fullmatch(r"^[,]*$", q):
    if re.fullmatch(comma_pattern, q) or re.fullmatch(just_st_name, q):
    # if not q or re.fullmatch(comma_pattern, q) or re.fullmatch(just_st_name, q):
        return False
    return True



if __name__ == "__main__":
    run()
