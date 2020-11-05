import sqlite3
from time import *
import datetime
import matplotlib.pyplot as plt
import numpy as np
# https://www.w3schools.com/python/python_datetime.asp
 
def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def graficos():
	# Defino la fecha de inicio. 3 meses anteriores a la fecha.
	now = datetime.datetime.now()
	start = datetime.datetime(now.year +(now.month-3-1)//12, ((now.month-3-1) % 12) +1, 1)
	# print(start)

	# Busco la fecha máxima de acreditacion
	conn = sqlite3.connect('plazos_fijos.db')
	cursor = conn.cursor()
	sqlQuery = "SELECT max(fecha_acreditacion) FROM pzosFijos "
	cursor.execute(sqlQuery)
	records = cursor.fetchall()
	conn.commit()
	conn.close() 
	# max_month = records[0][0][5:7]
	max_date = datetime.datetime(int(records[0][0][0:4]),int(records[0][0][5:7]),1)
	# print(max_date)

	num_months = diff_month(max_date,start)
	dates_array = [] 
	starting_array = [] 
	earn_array = [] 
	for i in range(num_months):
		conn = sqlite3.connect('plazos_fijos.db')
		cursor = conn.cursor()
		year = start.year +(start.month+i-1)//12
		month = ((start.month+i-1) % 12) +1
		date = datetime.datetime(year,month,1)

		sqlQuery = """
			SELECT ifnull(sum(ganancia),0) from pzosFijos 
				where fecha_acreditacion between date(:date_var) and date(:date_var,'start of month','+1 month','-1 day')
		"""
		sqlDict = {
			'date_var': date.strftime("%Y-%m-%d")
		}	
		cursor.execute(sqlQuery,sqlDict)
		records = cursor.fetchall()
		earn_array.append(round(float(records[0][0]),2))
		dates_array.append(date.strftime("%b %Y"))

		conn.commit()
		conn.close()

		conn = sqlite3.connect('plazos_fijos.db')
		cursor = conn.cursor()
		year = start.year +(start.month+i-1)//12
		month = ((start.month+i-1) % 12) +1
		date = datetime.datetime(year,month,1)

		sqlQuery = """
			SELECT ifnull(sum(monto_inicial),0) from pzosFijos 
				where fecha_creacion between date(:date_var) and date(:date_var,'start of month','+1 month','-1 day')
		"""
		sqlDict = {
			'date_var': date.strftime("%Y-%m-%d")
		}	
		cursor.execute(sqlQuery,sqlDict)
		records = cursor.fetchall()
		starting_array.append(round(float(records[0][0]),2))
		conn.commit()
		conn.close()
		
	fig, axs = plt.subplots(2,1)
	axs[0].plot(dates_array,earn_array)
	axs[1].plot(dates_array,starting_array)
	plt.show()

