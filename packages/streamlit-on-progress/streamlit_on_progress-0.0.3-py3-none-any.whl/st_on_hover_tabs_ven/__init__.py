import os
import streamlit as st
import streamlit.components.v1 as components

_RELEASE = True

if _RELEASE:

    root_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(root_dir, "frontend/build")

    _on_hover_tabs = components.declare_component(
        "st_on_hover_tabs_ven",
        path = build_dir
    )

else:
    _on_hover_tabs = components.declare_component(
    "on_hover_tabs",
    url="http://localhost:3001"
    )

def on_hover_tabs(tabName, iconName, styles=None, default_choice=1, key=None):
    
    component_value = _on_hover_tabs(tabName=tabName, iconName=iconName, styles=styles, key=key, default=tabName[default_choice])
    
    return component_value

if not _RELEASE:
    st.subheader("Component that creates tabs corresponding with on hover sidebar")
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True) # Load the on hover side bar css file



    with st.sidebar:
         tabs = on_hover_tabs(tabName=['Dashboard', 'Money', 'Economy'], 
                              iconName=['dashboard', 'money', 'economy'], 
                              key="1") ## create tabs for on hover navigation bar

    if tabs =='Dashboard':
        st.title("Navigation Bar")
        st.write('Name of option is {}'.format(tabs))

    elif tabs == 'Money':
        st.title("Paper")
        st.write('Name of option is {}'.format(tabs))

    elif tabs == 'Economy':
        st.title("Tom")
        st.write('Name of option is {}'.format(tabs))
        logo, name = st.sidebar.columns(2)
        st.markdown(
            """
        <style>
        [data-testid='stHorizontalBlock'] {
            margin-top:-180px;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        with logo:
            image = "logo.png"  # "./images/Logo.gif"
            st.image(image, use_column_width=True)
        with name:
            st.markdown(
                """
                <style>
                [data-testid='stHorizontalBlock']{
                    gap:0!important;
                }
                [data-testid='stSidebar'] [data-testid='stVerticalBlock']{
                    background-color:#0E1117!important;
                    # gap:0!important;
                }
                [data-testid='column']{
                    background-color:#0E1117!important;
                    # gap:0!important;
                }

                [data-testid='stVerticalBlock'] .row-widget{
                   text-align: right!important;
                }
                </style>
                """,
                    unsafe_allow_html=True,
                )
            if st.button('X'):
                st.markdown(
                """
                <style>
                [data-testid='stHorizontalBlock'] {
                    display:none;
                }
                </style>
                """,
                    unsafe_allow_html=True,
                )
            st.markdown("<h1 style='text-align: left; color: grey;'> \
                            Describe</h1>", unsafe_allow_html=True)
            
        st.sidebar.write(" ")
        
