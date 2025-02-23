# # import libraries
# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO

# # set page config

# st.set_page_conig (page_title="Data Sweeper",layout = "wind", page_icon=":chart_with_upwards_trend:")

# # Custom CSS

# st.markdown (
#     """
#     <style>
#     .reportview-container .main .block-container{
#     background color: #f5f5f5;
#     color: #111;
#         max-width: 100%;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Title & Description

# st.title("Data Sweeper By Ali Asghar")
# st.write("transform your file between CSV and Excel formats with build in data cleaning and visualization tools")

# # File Upload

# uploaded_file = st.file_uploader ("Choose a file (Accepts CSV and Execl):", type = ["csv","xlsx"], accept_multiple_files = (True) )

import streamlit as st
import pandas as pd
import os
from io import BytesIO
import matplotlib.pyplot as plt
def main():
    st.title("Growth Mindset Challenge")
    st.write("Welcome to the Growth Mindset Challenge App!")

    menu = ["Home", "Upload Data", "Visualize Data", "Set Goals", "Track Progress", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        home_page()
    elif choice == "Upload Data":
        upload_data_page()
    elif choice == "Visualize Data":
        visualize_data_page()
    elif choice == "Set Goals":
        set_goals_page()
    elif choice == "Track Progress":
        track_progress_page()
    elif choice == "About":
        about_page()

def home_page():
    st.header("Home")
    st.write("This app helps you cultivate a growth mindset by tracking your progress, setting goals, and reflecting on your achievements.")


def upload_data_page():
    st.header("Upload Data")
    st.write("Upload a CSV file containing your growth mindset challenge data.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            st.session_state['data'] = data
            st.write("Data uploaded successfully:")
            st.write(data.head())
        except Exception as e:
            st.error(f"Error reading file: {e}")


def visualize_data_page():
    st.header("Visualize Data")
    if 'data' in st.session_state:
        data = st.session_state['data']
        st.write("Select a column to visualize:")

        column = st.selectbox("Columns", data.columns)
        if st.button("Generate Chart"):
            try:
                fig, ax = plt.subplots()
                data[column].value_counts().plot(kind='bar', ax=ax)
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Error generating chart: {e}")
    else:
        st.warning("Please upload data first.")


def set_goals_page():
    st.header("Set Goals")
    goal = st.text_input("Write down your growth mindset goal:")
    if st.button("Save Goal"):
        if goal:
            st.session_state['goal'] = goal
            st.success("Goal saved!")
        else:
            st.warning("Please write a goal first.")


def track_progress_page():
    st.header("Track Progress")
    if 'goal' in st.session_state:
        st.write(f"Your Goal: {st.session_state['goal']}")
        progress = st.slider("Rate your progress (0 to 100)", 0, 100, 50)
        if st.button("Save Progress"):
            st.session_state['progress'] = progress
            st.success("Progress saved!")
    else:
        st.warning("Set a goal first.")


def about_page():
    st.header("About")
    st.write("This app was created to inspire and help users develop a growth mindset by setting goals and tracking their progress.")

if __name__ == "__main__":
    main()
