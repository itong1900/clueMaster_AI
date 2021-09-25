import streamlit as st

st.title("""
Welcome to the Game of Clue 
""")

st.button('Start the game')
st.radio('Radio', [1,2,3])
st.selectbox('Select', [1,2,3])
st.select_slider('Slide to select', options=[1,'2'])



add_sidebar_title = st.sidebar.title(
    "Game Configuration"
)

number_of_player = st.sidebar.number_input(
    "Enter number of player:",
    min_value = 2, max_value = 20, value = 4, step=1
)


## TODO: add input validation
suspect_myself_have = st.sidebar.text_area(
    "Enter the suspect card in your hand, seperated by ','"
)


## TODO: add input validation
weapon_myself_have = st.sidebar.text_area(
    "Enter the weapon card in your hand, seperated by ','"
)

## TODO: add input validation
room_myself_have = st.sidebar.text_area(
    "Enter the room card in your hand, seperated by ','"
)
