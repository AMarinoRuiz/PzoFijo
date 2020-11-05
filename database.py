import sqlite3

# var type: text, integer, real, null, blob
# Create Table
# var type: text, integer, real, null, blob
# esto lo quiero ejecutar una única vez, no es necesario que la cree cada vez.
# dp ver cómo hacer que sucesivas ejecuciones no lo corran, por ahora lo comento

def getVariables():
	# (display_name, table_name, type)
	return 	[ 
		['Cuenta','cuenta','text'],
		['Creación','fecha_creacion','text'],
		['Acreditación','fecha_acreditacion','text'],
		['Porcentaje','porcentaje','real'],
		['UVAS','uvas','real'],
		['Valor Inicial UVA','uva_inicial','real'],
		['Valor Final UVA','uva_final','real'],
		['Monto Inicial','monto_inicial','real'],
		['Monto Final','monto_final','real'],
		['Ganancia','ganancia','real'],
		['Activo','activo','text']
	]

def createTable():
	conn = sqlite3.connect('plazos_fijos.db')
	cursor = conn.cursor()
	variables = getVariables()
	sqlQuery = "CREATE TABLE pzosFijos ("
	for nombre,att,tipo in variables:
		sqlQuery += "{} {},".format(att,tipo)
	sqlQuery = sqlQuery[:-1] + ")"
	cursor.execute(sqlQuery)
	conn.commit()
	conn.close()

def actualizarActivos():
	conn = sqlite3.connect('plazos_fijos.db')
	cursor = conn.cursor()
	variables = getVariables()
	sqlQuery = """
		update pzosFijos set activo = (fecha_creacion<=date('now','localtime') and date('now','localtime')<fecha_acreditacion)
	"""
	# sqlQuery = """
	# 	select fecha_creacion, fecha_acreditacion, date('now','localtime'), fecha_creacion<=date('now','localtime'),date('now','localtime')<fecha_acreditacion from pzosFijos

	# """
	cursor.execute(sqlQuery)
	records = cursor.fetchall()
	# print(records)
	conn.commit()
	conn.close()	

actualizarActivos()