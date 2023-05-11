import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error
from datetime import date, timedelta
import time
import shutil
import os

try:
    # choose a specific start_date    
    start_date = date(2023, 4, 6)
    end_date = date.today()
    delta = timedelta(days=1) 
    while start_date <= end_date:

        date_format = start_date.strftime("%Y_%m_%d")

        # autocommit is zéér belangrijk.
        conn = mysql.connect(host='localhost', database='airfares', user='root', password='root', autocommit=True)    
        if conn.is_connected():

            old_path = "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\All_" + date_format + ".csv" 
            new_path = "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\All.csv"
            # Remove file if it already exists
            if os.path.exists(new_path):
                os.remove(new_path)
            if os.path.exists(old_path):    
                shutil.copy(old_path, new_path)

            cursor = conn.cursor()  

            # Execute commands in file LoadFiles.sql to import data into database airfares
            with open('C:\\Users\\kyana\\OneDrive - Hogeschool Gent\\Documenten\\GitHub\\Data-Engineering-Project\\sql-local\\LoadFileAll.sql', 'r') as f:
                cursor.execute(f.read(), multi=True)    
            cursor.close()
            conn.close() 
            time.sleep(5)
            
        start_date += delta
    
          


except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (conn.is_connected()):
        cursor.close()
        conn.close()
        print("MySQL connection is closed")


