import streamlit as st

st.title("My First App")



name = st.text_input("Enter your name")

age  = st.slider("Select age",0, 100)



if st.button("Submit"):

    st.write(f"Hello {name}, age{age}!")