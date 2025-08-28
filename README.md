# bloomeroo-microclimate
Repository created for Online Test code Submission  
My approch to the solution consist of three parts

Part 1 : Test the API, fetch data from API and print the data.
Script : fetch_data.py
Note: API only fetches 100 records

Part 2: Setup the Database to store the Data 

Part 3 :
Integrate part 1 and part2: Fetch the Data from API and Insert into DB.
Modified Script uploaded : fetch_data.py

Prerequisites & Assumptions
1.You have PostgreSQL installed and running.
2.You have created a database (e.g., bloomeroo_db) -- Add the DB details into .env File.
3.Python 3+ environment

How to Run the Program:

Download the Python script (fetch_data.py)  and .env file into a folder location.

1.Setup the Environment variable for DB Connection.
 >> Update your DB connection Details in the .env file
 >> Place the .env file in the same folder location as that of main python file (fetch_data.py)

2. Setup Python Libraries
   >> In the command Prompt, check the Python version and install the below psycopg2-binary and requests libraries for  database and HTTP calls. 
    >> pip install psycopg2-binary requests
    >> pip install python-dotenv
3. Run the Python script from command Line 
   cd <Folder Location >
   py fetch_data.py




