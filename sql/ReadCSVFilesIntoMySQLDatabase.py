# import pandas as pd
from datetime import date, timedelta
import shutil
import pymysql
import os
# from sshtunnel import SSHTunnelForwarder

# print(pymysql.__version__)

# # SSH settings
# ssh_host = 'vichogent.be'
# ssh_user = 'vicuser'
# ssh_port = 40067

# MySQL settings
db_user = 'user'
db_password = 'idjFEZmMJa*JGOYN%N1xcwGrb!)9Wr8GeRF&amp;p@hk'
db_name = 'groep8dep'
db_host = '127.0.0.1'
db_port = 3306

# server = SSHTunnelForwarder(
#     (ssh_host, 40067),
#     ssh_username="vicuser",
#     ssh_pkey="C:/Users/levim/.ssh/id_rsa",
#     remote_bind_address=('127.0.0.1', 3306)
# )
# print("voor de start")
# server.start()
# print("na de start")
conn = pymysql.connect(user=db_user, passwd=db_password, host='127.0.0.1', db=db_name, port=3306)

with conn:
    print("database is connected")
    # choose a specific start_date    
    start_date = date(2023, 4, 13)
    end_date = date.today()
    delta = timedelta(days=1) 
    while start_date <= end_date:
        print("in de while")

        date_format = start_date.strftime("%Y_%m_%d")

        # for each date and for each airline check if the file exists and copy the file to C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/
        for airline in ('Tui'): # , 'Ryanair', 'Transavia', 'BA'
            # old_path = "C:/Users/svre257/OneDrive - Hogeschool Gent/Documenten/Lesgeven Voorjaar 2023/Data Engineering Project I/Scrape/" + airline + "_" + date_format + ".csv"
            old_path_test = "C:/Users/levim/OneDrive/Documents/1 HOGENT - Toegepaste Informatica Bahelor/2 HoGent - Data Engeneering Project/project/Data-Engineering-Project/csv1/" + airline + "_" + date_format + ".csv"
            # new_path = "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/" + airline + ".csv"
            new_path_test = "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/" + airline + ".csv"
            # Remove file if it already exists
            if os.path.exists(new_path_test):
                os.remove(new_path_test)
            if os.path.exists(old_path_test):    
                shutil.copy(old_path_test, new_path_test)
        start_date += delta


    # conn.reconnect is important, otherwise error
    with conn.cursor() as cursor:

        print("database is still connected")

        # cursor.execute("SHOW TABLES;")

        # result = cursor.fetchall()

        # for i in result:
        #     print(i)

        # Execute commands in file LoadFiles.sql to import data into database airfares
        # with open('C:/Users/svre257/OneDrive - Hogeschool Gent/Documenten/Lesgeven Voorjaar 2023/Data Engineering Project I/LoadFiles.sql', 'r') as f:
        #     cursor.execute(f.read(), multi=True)
        print("trying to open the file")

        with open('C:/Users/levim/OneDrive/Documents/1 HOGENT - Toegepaste Informatica Bahelor/2 HoGent - Data Engeneering Project/project/Data-Engineering-Project/sql/LoadFilesTest.sql', 'r') as f:
            sql = f.read()
            sql_commands = sql.split(';')
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
# server.stop()