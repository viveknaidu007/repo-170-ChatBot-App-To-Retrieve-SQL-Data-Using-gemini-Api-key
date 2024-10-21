from dotenv import load_dotenv
load_dotenv() # load all the environemnt variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load Google Gemini Model and provide queries as response
def get_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text

# function to retrieve query from the database
def read_query(query, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    connection.close()
    # print in terminal
    for student in data:
        print(student)
    return data

# default prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query 🤖📝")
st.header("ChatBot App To Retrieve SQL Data")

question = st.text_input("Input: ",key="input")

submit = st.button("Submit")

# if submit is clicked
if submit:
    response = get_response(question,prompt)
    # print in terminal
    print("Query:")
    print(response)
    data = read_query(response,"students.db")
    st.subheader("Response:")
    print("Response:")
    for student in data:
        st.write(student)
        # print in terminal
        print(student)