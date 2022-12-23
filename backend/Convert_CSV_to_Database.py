import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error


data = pd.read_csv ('sample_covid_data.csv')
df = pd.DataFrame(data)

try:
    conn = mysql.connect(host='localhost', user='root',
                        password='root1234')           # Enter your Database username, password here
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE CovidProject1")

except Error as e:
    print("Error while connecting to MySQL", e)
# table created and importing CSV file to database
try:
    conn = mysql.connect(host='localhost', database='CovidProject1', user='root', password='root1234')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()

        cursor.execute('DROP TABLE IF EXISTS sample_covid_data;')

# in the below line we need to pass the #create table statement which we want to create
        cursor.execute("CREATE TABLE sample_covid_data(id int,Subsection varchar(255),BusinessType varchar(255),Quantity int,AvgPop int,OpCapacity float,RelRisk float,RelChange float,SubsectionCount int)")

        for i,row in df.iterrows():
            #here %S means string values
            sql = "INSERT INTO CovidProject1.sample_covid_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))

            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)
