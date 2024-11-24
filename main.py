# Import Python packages
import streamlit as st
import pandas as pd
import plotly.express as px
from snowflake.snowpark.context import get_active_session
from datetime import date

# Initialize Snowflake session
session = get_active_session()

# Set page configuration for wide layout
st.set_page_config(layout="wide")

# Function to fetch data from Snowflake
def fetch_data_from_snowflake(start_date, end_date):
    try:
        query = f"""
            SELECT * 
            FROM DATA
            WHERE DATE BETWEEN '{start_date}' AND '{end_date}'
        """
        dinTable = session.sql(query)
        df = dinTable.to_pandas()

        # Display the data in a table
        st.dataframe(df, use_container_width=True)

        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to fetch and plot a line chart
def fetch_and_plot_line_chart(start_date, end_date):
    try:
        t = session.table("DATA")
        df = t.to_pandas()

        # Aggregate data by date
        filtered_df = df[(df["DATE"] >= start_date) & (df["DATE"] <= end_date)]
        aggregated_data = filtered_df.groupby("DATE", as_index=False)["NUMBER_OF_STUDENTS"].sum()

        # Plot the line chart
        st.line_chart(aggregated_data.set_index("DATE")["NUMBER_OF_STUDENTS"])

    except Exception as e:
        st.error(f"Error fetching or plotting data: {e}")

# Function to plot bar chart
def plot_bar_chart():
    try:
        t = session.table("DATA")
        df = t.to_pandas()

        
        # Aggregate data by weather
        weather_effect = df.groupby("WEATHER", as_index=False)["NUMBER_OF_STUDENTS"].sum()
        st.bar_chart(weather_effect, x="WEATHER", y="NUMBER_OF_STUDENTS")

    except Exception as e:
        st.error(f"Error fetching or plotting data: {e}")

# Function to plot Pie Chart
def plot_pie_chart(start_date, end_date):

    try:

        t = session.table("DATA")
        df = t.to_pandas()
    
        # Group data by WEATHER
        weather_effect = df.groupby("CAMPUS_EVENTS", as_index=False)["NUMBER_OF_STUDENTS"].sum()
    
        # Plot a pie chart
        fig = px.pie(
            weather_effect,
            names="CAMPUS_EVENTS",  # Column for pie chart segments
            values="NUMBER_OF_STUDENTS",  # Column for segment sizes
        )

        fig.update_layout(
        width=400,
        height=400, 
        )
    
        # Display the pie chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error fetching or plotting data: {e}")




# Home page for insights
def home_page():
    st.header(":blue[DINING INSIGHTS]", divider='blue')

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date", date(2024, 1, 1))  # Default start date

    with col2:
        end_date = st.date_input("End Date", date(2024, 12, 31))    # Default end date

    if start_date > end_date:
        st.error("Start date cannot be after the end date.")
    else:
        # Line chart section
        st.subheader("Student Turnout Trend")
        fetch_and_plot_line_chart(start_date, end_date)

        # Bar and Pie chart sections
        st.markdown("---")
        bar, pie = st.columns(2)

        with bar:
            st.subheader("Student Turnout With Respect to Weather")
            plot_bar_chart()

        with pie:
            st.subheader("Student Turnout With Respect to Events")
            plot_pie_chart(start_date, end_date)
            



# Record manipulation page
def record_manipulation():

    st.subheader("Go To:")
    st.markdown("""
        <div style="font-size: 18px; color: #333;">
            <ul style="list-style-type: none; padding: 0;">
                <li style="margin: 10px 0;">
                    <a href="#add-a-record" style="text-decoration: none; color: #1E90FF; font-weight: bold;">
                        ➤ Add A Record
                    </a>
                </li>
                <li style="margin: 10px 0;">
                    <a href="#delete-a-record" style="text-decoration: none; color: #FF6347; font-weight: bold;">
                        ➤ Delete A Record
                    </a>
                </li>
                <li style="margin: 10px 0;">
                    <a href="#fetch-data" style="text-decoration: none; color: #32CD32; font-weight: bold;">
                        ➤ Fetch Data
                    </a>
                </li>
                <li style="margin: 10px 0;">
                    <a href="#update-a-record" style="text-decoration: none; color: #8A2BE2; font-weight: bold;">
                        ➤ Update Data
                    </a>
                </li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    

    
    # Add a record
    st.header("Add a Record")
    
    
    # User inputs for the new values 
    record_date = st.date_input("Date", date.today())  # Default to today's date
    day = st.text_input("Day (e.g., Monday)")  # User can input the day
    time = st.time_input("Time", value=None)  # Time field for the record
    academic_calendar = st.text_input("Academic Calendar")  # Input for Academic Calendar
    special_menu_items = st.text_input("Special Menu Items")  # Input for special menu items
    campus_events = st.text_input("Campus Events")  # Input for campus events
    number_of_students = st.number_input("Number of Students", min_value=0, step=1)  # Input for number of students
    weather = st.text_input("Weather")  # Input for weather information

    # Button to insert the record
    if st.button("Add Record"):
        if number_of_students > 0:
            # Insert the record with the provided values
            df = session.create_dataframe(
                [(record_date, day, time, academic_calendar, special_menu_items, campus_events, number_of_students, weather)],
                schema=["DATE", "DAY", "TIME", "ACADEMIC_CALENDAR", "SPECIAL_MENU_ITEMS", "CAMPUS_EVENTS", "NUMBER_OF_STUDENTS", "WEATHER"]
            )

            # Insert the record into the Snowflake table (append mode)
            df.write.save_as_table("DATA", mode="append", table_type="temporary")
            st.success("Record added successfully!")
        else:
            st.error("Please enter a valid number of students.")



    
    # Read Records
    st.header("Fetch Data")
    
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date", date(2024, 1, 1))  # Default start date

    with col2:
        end_date = st.date_input("End Date", date(2024, 12, 31))    # Default end date

    if start_date > end_date:
        st.error("Start date cannot be after the end date.")
    else:
        # Fetch data and display records
        df = fetch_data_from_snowflake(start_date, end_date)




    
    # Delete a Record
    st.header("Delete a Record")

    record_date_to_delete = st.date_input("Date", date.today(), key='delete_date')
    time_to_delete = st.time_input("Time", value=None, key='delete_time')
    if st.button("Delete Record"):
        try:
            # Get the session and reference to the table
            t = session.table("DATA")
            
            # Use filter to remove specific record based on date and time
            t = t.filter((t["DATE"] != record_date_to_delete) | (t["TIME"] != time_to_delete))
    
            # Write the modified data back to the table
            t.write.save_as_table("DATA", mode="overwrite")
    
            st.success("Record deleted successfully!")
        except Exception as e:
            st.error("Sorry, something went wrong.")
            st.text(e)
                    



    

    # Update a record
    st.header("Update a Record")

    # User inputs for selecting the record to update
    record_date_to_update = st.date_input("Date", date.today(), key='update_date')
    time_to_update = st.time_input("Time", value=None, key='update_time')

    # User inputs for the new values
    new_day = st.text_input("New Day")
    new_academic_calendar = st.text_input("New Academic Calendar")
    new_special_menu_items = st.text_input("New Special Menu Items")
    new_campus_events = st.text_input("New Campus Events")
    new_number_of_students = st.number_input("New Number of Students", min_value=0)
    new_weather = st.text_input("New Weather")

    if st.button("Update Record"):
        try:
            t = session.table("DATA")

            t.update({
            "DAY": new_day,
            "ACADEMIC_CALENDAR": new_academic_calendar,
            "SPECIAL_MENU_ITEMS": new_special_menu_items,
            "CAMPUS_EVENTS": new_campus_events,
            "NUMBER_OF_STUDENTS": new_number_of_students,
            "WEATHER": new_weather
            }, (t["DATE"] == record_date_to_update) & (t["TIME"] == time_to_update))
            # Use filter to remove specific record based on date and time
            t.write.save_as_table("DATA", mode="overwrite")
            
            st.success("Record updated successfully!")
        except Exception as e:
            st.error("Sorry, something went wrong.")
            st.text(e)
    




# Navigation
page = st.sidebar.radio("Pages:", ("Home", "Record Manipulation"))

# Display the corresponding page based on user selection
if page == "Home":
    home_page()
elif page == "Record Manipulation":
    record_manipulation()
