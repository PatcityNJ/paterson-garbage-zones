
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


st.markdown(
    """
    <style>
    .st-emotion-cache-zq5wmm, .st-emotion-cache-zq5wmm.ezrtsby0,
    #MainMenu
    {
        display: none;
        visibility: hidden;
    }
    </style>
    """
)



def run():

    st.title("Search Bulk Pickup Zones by Address")

    st.markdown('''
                :red[Important note:] Please do not include apartment, floor, 
                or unit information in your search.''')

    query = st.text_input("Search Address", 
                          placeholder="155 Market St") # clear spaces from query
    query = query.replace(" ", "")

    #if query and validate_text(query):
    if validate_text(query) == 2:
        st.error("Invalid address.")
    elif validate_text(query):
        try:  
            df = pd.read_excel("Trash-Zones.xlsx")
            res = df[df["Address_Strip"].str.contains(query, case=False,  #match case-insensitive address
                                                regex=False)]
        except Exception as e: # raise if any query that includes symbols or invalid input
            st.error("Invalid address.")
        else:
            if not res.empty:  
                st.success('Address found.')
                res = res[["Address", "Zone"]]
                res = res.set_index("Address")
                res = res.head(3)
                st.dataframe(res, width=None)
            else:
                st.error("Address not found.") 


def validate_text(q): # checks for empty string, 
    #valid_pattern = r"^[a-zA-Z0-9,]+$"
    #valid_pattern = r"[\w,]+"
    comma_pattern = r"^[,]*$"
    #if re.search(valid_pattern, q) and not re.fullmatch(r"^[,]*$", q):
    if not q:
        return False
    elif re.fullmatch(comma_pattern, q):
        return 2
    else:
        return True



if __name__ == "__main__":
    run()
