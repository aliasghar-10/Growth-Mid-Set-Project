import streamlit as st
import pandas as pd
import os
from io import BytesIO

def main():
    st.set_page_config(page_title="Growth Mindset Challenge", layout="wide", initial_sidebar_state="expanded")
    apply_dark_mode()

    st.title("Growth Mindset Challenge")
    st.write("Welcome to the Growth Mindset Challenge App!")

    menu = ["Home", "Upload Data", "View Data", "Convert Files", "Set Goals", "Track Progress", "Visualize Data", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        home_page()
    elif choice == "Upload Data":
        upload_data_page()
    elif choice == "View Data":
        view_data_page()
    elif choice == "Convert Files":
        convert_files_page()
    elif choice == "Set Goals":
        set_goals_page()
    elif choice == "Track Progress":
        track_progress_page()
    elif choice == "Visualize Data":
        visualize_data_page()
    elif choice == "About":
        about_page()

def apply_dark_mode():
    st.markdown(
        """
        <style>
        body {
            background-color: #0e1117;
            color: #c9d1d9;
        }
        .stButton>button {
            background-color: #21262d;
            color: #c9d1d9;
            border: 1px solid #30363d;
        }
        .stButton>button:hover {
            background-color: #30363d;
        }
        .stSidebar {
            background-color: #161b22;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def home_page():
    st.header("Home")
    st.write("This app helps you cultivate a growth mindset by tracking your progress, setting goals, and reflecting on your achievements.")

def upload_data_page():
    st.header("Upload Data")
    st.write("Upload a CSV or Excel file containing your growth mindset challenge data.")

    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)

            st.session_state['data'] = data
            st.write("Data uploaded successfully:")
            st.write(data.head())
        except Exception as e:
            st.error(f"Error reading file: {e}")

def view_data_page():
    st.header("View Data")
    if 'data' in st.session_state:
        data = st.session_state['data']
        st.write("Here is your data:")
        st.dataframe(data)

        if st.checkbox("Show Tag Description"):
            tags = data.columns.tolist()
            st.write(f"Tags: {', '.join(tags)}")

            tag_to_remove = st.text_input("Enter a tag to remove:")
            if st.button("Remove Tag"):
                if tag_to_remove in tags:
                    data = data.drop(columns=[tag_to_remove])
                    st.session_state['data'] = data
                    st.success(f"Tag '{tag_to_remove}' removed successfully!")
                    st.dataframe(data)
                else:
                    st.error("Tag not found.")
    else:
        st.warning("Please upload data first.")

def convert_files_page():
    st.header("Convert Files")
    st.write("Convert CSV to Excel or Excel to CSV.")

    uploaded_file = st.file_uploader("Choose a file to convert", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                data = pd.read_csv(uploaded_file)
                output = BytesIO()
                data.to_excel(output, index=False, engine='openpyxl')
                st.download_button(label="Download Excel File", data=output.getvalue(), file_name="converted_file.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                data = pd.read_excel(uploaded_file)
                output = BytesIO()
                data.to_csv(output, index=False)
                st.download_button(label="Download CSV File", data=output.getvalue(), file_name="converted_file.csv", mime="text/csv")
        except Exception as e:
            st.error(f"Error converting file: {e}")

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

def visualize_data_page():
    st.header("Visualize Data")
    if 'data' in st.session_state:
        data = st.session_state['data']
        numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()

        if numeric_columns:
            x_axis = st.selectbox("Choose X-axis", options=numeric_columns)
            y_axis = st.selectbox("Choose Y-axis", options=numeric_columns)

            if st.button("Generate Graph"):
                st.line_chart(data[[x_axis, y_axis]])
        else:
            st.warning("No numeric columns found in data for visualization.")
    else:
        st.warning("Please upload data first.")

def about_page():
    st.header("About")
    st.write("This app was created to inspire and help users develop a growth mindset by setting goals, tracking progress, and visualizing data.")

if __name__ == "__main__":
    main()
