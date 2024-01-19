
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
                Example Searches: "155 Market St, Paterson, NJ" or "155 Market St".
                </li>
                </ul>
                ''', unsafe_allow_html=True)

    query = st.text_input("Search Address", 
                          placeholder="155 Market St") # clear spaces from query
    #query = query.replace("  ", "")
    query = remove_zip(query).strip()
    query = re.sub(r"\s+", " ", query)

    if query:
        with st.spinner('Please wait...'):
            res = search(query)
            if isinstance(res, pd.DataFrame):
                st.success('Address found.')
                st.dataframe(res, width=None)
            else:
                st.error("No address found.")

def remove_zip(query):
    patterns = [r"paterson(.*)$", r",(.*)$"]
    for pat in patterns:
        query = re.sub(pat, "", query)
    return query


def search(query):
    #if validate_text(query) == 2:
        #return None
        #st.error("Invalid address.")
    if validate_text(query):
        try:  
            df = pd.read_excel("Trash-Zones.xlsx")
            with st.spinner('Please wait...'):
                #res = df[df["Address_Strip"].str.contains(query, case=False,  #match case-insensitive address
                #                                regex=False)]
                #res = df[["Full_Text_Address_Strip", "Address_Strip"]].str.contains(query, 
                 #                                                                  case=False,
                 #                                                                  regex=False)
                #res = df[["Full_Text_Address_Strip", "Address_Strip"]].apply(lambda col: col.str.contains(query, 
                #                                                                   case=False,
                #                                                                   regex=False), axis=0)
                #res = df[res]
                
                # x = df["Full_Text_Address_Strip"].str.contains(query, case=False,regex=False)
                # y = df["Address_Strip"].str.contains(query, case=False,regex=False)
                # r1 = df["Raw_Address"].str.contains(query, case=False,regex=False)
                # r2 = df["Raw_Address2"].str.contains(query, case=False,regex=False)
                x1 = df["Street"].str.contains(query, case=False,regex=False)
                x2 = df["Street2"].str.contains(query, case=False,regex=False)
                x3 = df["Street3"].str.contains(query, case=False,regex=False)
                x4 = df["Street4"].str.contains(query, case=False,regex=False)
                x5 = df["Street5"].str.contains(query, case=False,regex=False)
                x6 = df["Street6"].str.contains(query, case=False,regex=False)
                logic = x1 | x2 | x3 | x4 | x5 | x6
                res = df[logic]
                #st.write(f"Debug {res}")

        except Exception as e: # raise if any query that includes symbols or invalid input
            return None
            #st.error("Invalid address.")
        else: # no errors
            if not res.empty:  # matched address
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
