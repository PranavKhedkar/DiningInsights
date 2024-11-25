# DiningInsights

This project is a Streamlit-based web application that provides insights into student turnout trends at a dining facility. The app is integrated with a Snowflake database to fetch and manipulate data, allowing users to view visualizations, add new records, delete existing records, and update data interactively.

Synthetic data was used which was created using ChatGPT.

## Features

### Home Page: Insights Dashboard
1. **Line Chart**:   Displays student turnout trends over a selected date range.
![image](https://github.com/user-attachments/assets/95fba10e-40f4-4c2f-8196-42031f9e5976)

2. **Bar Chart**:   Shows the relationship between weather conditions and student turnout.
![image](https://github.com/user-attachments/assets/41599d10-aead-4d6a-ada0-d7527c531cd3)

3. **Pie Chart**:   Highlights the impact of campus events on student turnout.
![image](https://github.com/user-attachments/assets/48825617-d1c6-475d-b3e8-d99c382c8139)

### Record Manipulation Page
- **Add a Record**:   Allows users to insert a new record with inputs for date, day, time, academic calendar, special menu items, campus events, number of students, and weather.
  ![image](https://github.com/user-attachments/assets/b0f7eb24-cf6b-41aa-99f7-a36df3430e89)

- **Fetch Data**:   Fetches and displays records for a selected date range in a tabular format.
  ![image](https://github.com/user-attachments/assets/412c02e1-5a7d-433d-8fb6-8cab56147763)

- **Delete a Record**:   Deletes a record based on the specified date and time.
  ![image](https://github.com/user-attachments/assets/e4828edc-d4a9-4e48-8964-7ca6d9a4c770)

- **Update a Record**:   Updates an existing record's fields by specifying the date and time of the record to be updated.
  ![image](https://github.com/user-attachments/assets/01602265-97be-4c6f-810a-47b79421c735)

## Application Workflow
- **Navigate between pages**:
Use the sidebar to switch between the Home Page (Insights Dashboard) and the Record Manipulation Page (Add, Fetch, Delete, and Update records).
![image](https://github.com/user-attachments/assets/cbc5e358-849c-419b-b647-0f02889b2211)


- **Go To Section**: On the Record Manipulation Page, a "Go To" section provides quick links to specific features like adding, deleting, updating, or fetching records for ease of access.
![image](https://github.com/user-attachments/assets/10fc4f01-5e77-4b0f-a804-5a3370fcb31a)

## Future Enhancements
- Implement verification mechanisms to confirm the successful creation, deletion, and updating of records.
- Add more visualizations to provide deeper insights and enhance user understanding.
- Optimize data querying for improved performance and efficiency.


