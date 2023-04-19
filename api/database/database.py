
import sqlite3
import pandas as pd
import datetime
import logging

connection = sqlite3.connect('weather.db')

def create_table():
  connection = sqlite3.connect('weather.db')
  connection.execute(''' CREATE TABLE IF NOT EXISTS measurements (
    id INTEGER PRIMARY KEY,
    humidity REAL NOT NULL,
    temperature REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );''')
  

  
async def add_measurement(temperature, humidity):
  thisdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
  connection = sqlite3.connect('weather.db')
  connection.execute("INSERT INTO measurements (temperature, humidity, created_at) VALUES (?, ?, ?)", (temperature, humidity, thisdate))
  connection.commit()
  connection.close()
  
  return "Measurement added successfully"

async def get_measurements():
  connection = sqlite3.connect('weather.db')
  df = pd.read_sql_query(sql="select * from measurements", con=connection)  # Convert the rows to a Pandas DataFrame
  dict1 = pd.DataFrame.to_dict(df)
  return dict1

async def get_by_date(date):
  connection = sqlite3.connect('weather.db')
  cursor =  connection.execute(f'''select temperature,
                     min(temperature) over(partition by temperature) as Temperatura_Minima_do_dia,
                     max(temperature) over(partition by temperature) as Temperatura_Maxima_do_dia,
                     avg(temperature) over(partition by temperature) as Media_da_temperatura,
                     humidity, min(humidity) over(partition by humidity) as Umidade_Minima_do_dia,
                     max(humidity) over(partition by humidity) as Umidade_Maxima_do_dia,
                     avg(humidity) over(partition by humidity) as Media_da_Umidade
                     from measurements where DATE(created_at) = '{date}' ''')
  data =  cursor.fetchall()  # Retrieve the results of the cursor
  columns = [column[0] for column in cursor.description]  # Get the column names from the cursor description
  df = pd.DataFrame(data, columns=columns)  # Convert the rows to a Pandas DataFrame
  return df

connection.close()