# roxiler_task

running the server
python app.py

To initialize the database, access http://localhost:5000/api/initialize using a GET request.
To get statistics for a specific month, access http://localhost:5000/api/statistics?month=January using a GET request.
To get bar chart data for a specific month, access http://localhost:5000/api/bar_chart?month=January using a GET request.
To get pie chart data for a specific month, access http://localhost:5000/api/pie_chart?month=January using a GET request.
To get the final combined response, access http://localhost:5000/api/final_response?month=January using a GET request.

Remember to replace "January" in the URL with the desired month. The APIs will filter the data for the given month, regardless of the year.
