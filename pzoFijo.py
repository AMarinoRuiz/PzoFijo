from tkinter import *
import sqlite3
from database import *
import re
from table import *
from createcalendar import *  
from graficos import *
# from PIL import ImageTk, Image

global variables
variables = getVariables()

# FUNCIONES
def on_entry_click(event):
	"""function that gets called wheneeditabilityver entry1 is clicked"""        
	if (event.widget == pf_entry['fecha_creacion'][1]):
		firstclick = pf_entry['fecha_creacion'][2]
		if firstclick: # if this is the first time they clicked it
			pf_entry['fecha_creacion'][2] = False
			pf_entry['fecha_creacion'][1].delete(0, "end") # delete all the text in the entry
			pf_entry['fecha_creacion'][1].configure(fg='black',justify = 'left')
	if (event.widget == pf_entry['fecha_acreditacion'][1]):
		firstclick = pf_entry['fecha_acreditacion'][2]
		if firstclick: # if this is the first time they clicked it
			pf_entry['fecha_acreditacion'][2] = False
			pf_entry['fecha_acreditacion'][1].delete(0, "end") # delete all the text in the entry
			pf_entry['fecha_acreditacion'][1].configure(fg='black',justify = 'left')

def formatDateToSQL(date):
	"""
		formatea para el SQL. Devuelve YYYY-MM-DD
	"""
	x = re.split("[^0123456789]", date)
	# print(date,x[0])
	# if(len(x[0])) == 4:
	x[1] = x[1].zfill(2)
	x[0] = x[0].zfill(2)
	x = x[::-1]
	return '-'.join(x)
	# else:
	# 	return date

def formatDateDisplay(date):
	"""
		formatea para el display. Devuelve DD-MM-YYYY
	"""
	x = re.split("[^0123456789]", date)
	x[1] = x[1].zfill(2)
	x[0] = x[0].zfill(2)
	return '-'.join(x)


def ingresarPF(pf_entry):
	#submit
	conn = sqlite3.connect('plazos_fijos.db')
	cursor = conn.cursor()
	sqlInsert = "INSERT INTO pzosFijos VALUES ("
	dict_insert = {}
	hasta = None
	final = None
	inicial = None
	for display_name,att_name,tipo in variables:
		if display_name == 'Ganancia':
			if(pf_entry['monto_final'][1].get() and pf_entry['monto_inicial'][1].get()):
				inicial = pf_entry['monto_inicial'][1].get()
				final = pf_entry['monto_final'][1].get()
				sqlInsert += ":{},".format(att_name)
				dict_insert[att_name] = round(float(final) - float(inicial),2)
			else:
				sqlInsert += ":{},".format(att_name)
				dict_insert[att_name] = ''
		elif 'fecha' in att_name:
			sqlInsert += ":{},".format(att_name)
			# dict_insert[att_name] = formatDateDisplay(pf_entry[att_name][1].get())
			dict_insert[att_name] = formatDateToSQL(pf_entry[att_name][1].get())
		elif display_name == 'Activo':
			desde = formatDateToSQL(pf_entry['fecha_creacion'][1].get())
			hasta = formatDateToSQL(pf_entry['fecha_acreditacion'][1].get())
			sqlInsert += "{},".format("(SELECT date('now','localtime') between '{}' and '{}')".format(desde,hasta))	
		else:
			sqlInsert += ":{},".format(att_name)
			dict_insert[att_name] = pf_entry[att_name][1].get()
	sqlInsert = sqlInsert[:-1] +")"
	cursor.execute(sqlInsert,dict_insert)

	if hasta:
		insertCalendar(pf_entry['cuenta'][1].get(),(inicial or ''),(final or ''),hasta)
	
	conn.commit()
	conn.close()
	pf_ingresar.destroy()

def abrirIngresar():
	global pf_ingresar
	global pf_entry

	pf_ingresar = Toplevel()
	pf_frame = LabelFrame(pf_ingresar)
	pf_frame.grid(
		row = 0,
		column = 0,
		padx = 10,
		pady = 10
	)
	pf_entry = {} 
	for var,index in zip(variables,range(len(variables))):	
		if var[0] not in ('Ganancia','Activo'):
			pf_entry[var[1]] = [Label(pf_frame, text = var[0]),
				Entry(pf_frame, width = 30), True ]
			pf_entry[var[1]][0].grid(
				row = index,
				column = 0,
				pady = (10,0),
				padx = (90,15),
				sticky = W
			)
			pf_entry[var[1]][1].grid(
				row = index,
				column = 1,
				pady = (10,0),
				padx = (0,90)
			)			

	pf_entry['fecha_creacion'][1].insert(0,'dd-mm-aaaa')
	pf_entry['fecha_creacion'][1].configure(fg='grey', justify='right')
	pf_entry['fecha_creacion'][1].bind('<FocusIn>', on_entry_click)

	pf_entry['fecha_acreditacion'][1].insert(0,'dd-mm-aaaa')
	pf_entry['fecha_acreditacion'][1].configure(fg='grey', justify='right')
	pf_entry['fecha_acreditacion'][1].bind('<FocusIn>', on_entry_click)

	ingresarPF_btn = Button(pf_frame, text = 'Ingresar', command = lambda: ingresarPF(pf_entry))
	ingresarPF_btn.grid(
		row = len(variables),
		column = 0,
		pady = 10,
		padx = (90,15)
	)

	cancelar_btn = Button(pf_frame, text = 'Cancelar', command = pf_ingresar.destroy)
	cancelar_btn.grid(
		row = len(variables),
		column = 1,
		pady = 10,
		padx = (0,90)
	)

def creaTabla(ubicacion,editable = False):
	global tabla_pf
	global records

	if type(tabla_pf) == Table:
		for i in tabla_pf.elements:
			i.destroy()

		for i in tabla_pf.borrar_chk:
			i.destroy()

	conn = sqlite3.connect('plazos_fijos.db')
	cursor = conn.cursor()

	sqlQuery = "SELECT *,oid FROM pzosFijos "
	where = ''

	if var_activos.get():
		where += "activo = 1 and "
	for key,value in chk_cuenta.items():
		if value.get():
			where += "cuenta = '{}' and ".format(key)

	if where: 
		where = 'where ' + where[:-4]
		sqlQuery += where 

	sqlQuery += "order by fecha_acreditacion DESC"
	cursor.execute(sqlQuery)
	records = cursor.fetchall()

	variables = getVariables()
	titulos = [x[0] for x in variables]
	visibilidad = [True] * len(variables)
	visibilidad[-1] = False #ACTIVO
	variables.append(False) #OID

	tabla_pf = Table(frame_tabla,titulos,records,visibilidad,editable)

def actualizarBase(records):
	for i in range(len(records)):
		oid = records[i][-1]
		conn = sqlite3.connect('plazos_fijos.db')
		cursor = conn.cursor()
		sqlString = "UPDATE pzosFijos SET \n" 
		sqlDict = {}
		variables = getVariables()
		for j in range(tabla_pf.total_columns -1):  #saco el índice de ACTIVO
			if variables[j][1] == 'fecha_creacion':
				desde = formatDateToSQL(tabla_pf.elements[(i+1)*(tabla_pf.total_columns-1) + j].get())
				sqlString += "{} = :{}, \n".format(variables[j][1],variables[j][1])
				sqlDict[variables[j][1]] = desde
			elif variables[j][1] == 'fecha_acreditacion':
				hasta = formatDateToSQL(tabla_pf.elements[(i+1)*(tabla_pf.total_columns-1) + j].get())
				sqlString += "{} = :{}, \n".format(variables[j][1],variables[j][1])
				sqlDict[variables[j][1]] = hasta
			else:
				sqlString += "{} = :{}, \n".format(variables[j][1],variables[j][1])
				sqlDict[variables[j][1]] = tabla_pf.elements[(i+1)*(tabla_pf.total_columns-1) + j].get()
				if variables[j][1] == 'monto_final': 
					final = tabla_pf.elements[(i+1)*(tabla_pf.total_columns-1) + j].get()
				if variables[j][1] == 'monto_inicial':
					inicial = tabla_pf.elements[(i+1)*(tabla_pf.total_columns-1) + j].get()
		if final and inicial:
			sqlString += "ganancia = :ganancia, "
			sqlDict['ganancia'] = round(float(final) - float(inicial),2)
		activo = "(SELECT date('now','localtime') between '{}' and '{}')".format(desde,hasta)
		sqlString += "activo = {} where oid = :oid".format(activo)
		sqlDict['oid'] = oid
		cursor.execute(sqlString,sqlDict)
		conn.commit()
		conn.close() 
	mostrar.destroy()

def borrarRegistros():
	conn = sqlite3.connect('plazos_fijos.db')
	cursor = conn.cursor()
	for key,value in tabla_pf.borrar_var.items():
		if value.get() == 1:
			sqlBorrar = "DELETE FROM pzosFijos where oid = {}".format(key)
			cursor.execute(sqlBorrar)
	conn.commit()
	conn.close()
	mostrar.destroy()

def abrirGraficos():
	# global ventana_graficos
	# ventana_graficos = Toplevel()
	graficos()	

def abrirMostrar(editable):
	global mostrar
	global tabla_pf
	global var_activos
	global frame_tabla
	global visibilidad
	global chk_cuenta
	chk_cuenta = {}	
	tabla_pf = None

	var_activos = IntVar()
	variables = getVariables()
	mostrar = Toplevel()
	frame_opciones = LabelFrame(mostrar,text = 'Filtros',padx=5,labelanchor ='n')
	frame_opciones.grid(
		row = 0,
		column = 0,
		sticky='n',
		padx = 10,
		pady = 10
	)

	chk_activos = Checkbutton(frame_opciones, text = 'Activos', variable = var_activos,command= lambda: creaTabla(frame_tabla,editable))
	chk_activos.grid(
		row=0,
		column = 0,
		sticky='w'
	)
	chk_activos.select()

	lbl_cuentas = Label(frame_opciones, text = 'Cuentas')
	lbl_cuentas.grid(
		row=1,
		column = 0,
		sticky='w'
	)

	if editable:
		aplicar_btn = Button(mostrar, text = 'Guardar', command = lambda: actualizarBase(records),height=1,width = 8)
		aplicar_btn.grid(
			row=1,
			column = 0,
			sticky = 's',
			pady=(10,3)
		)
		cancelar_btn = Button(mostrar, text = 'Cancelar', command = mostrar.destroy,height=1,width = 8)
		cancelar_btn.grid(
			row=2,
			column = 0,
			sticky = 's',
			pady=(3,10)
		)

		borrar_btn = Button(mostrar, text = 'Borrar Seleccionados', command = borrarRegistros, height=1,width=17)
		borrar_btn.grid(
			row=2,
			column = 1,
			sticky = 'se',
			padx = 10,
			pady=(3,10)
		)


	frame_tabla = LabelFrame(mostrar)
	frame_tabla.grid(
		row = 0,
		column = 1,
		sticky='n',
		rowspan = 2,
		padx = 10,
		pady = 10
	)

	conn = sqlite3.connect('plazos_fijos.db')
	cursor = conn.cursor()
	sqlQuery = "SELECT DISTINCT cuenta FROM pzosFijos"
	cursor.execute(sqlQuery)
	records_cuentas = cursor.fetchall()
	for index in range(len(records_cuentas)):
		var_global = globals()[records_cuentas[index][0]] = IntVar()
		b = Checkbutton(frame_opciones, text = records_cuentas[index][0],var = var_global,command= lambda: creaTabla(frame_tabla,editable))
		b.grid(
			row=index+2,
			column = 0,
			sticky='w'
		)	
		chk_cuenta[records_cuentas[index][0]] = var_global


	creaTabla(frame_tabla,editable)

# crea la base si no existe
try:
	createTable()
except:
	pass

variables = getVariables()

root = Tk()
root.title('Plazos Fijos')
root_frame = LabelFrame(root, padx = 50, pady = 50)
root_frame.grid(
	row = 0,
	column = 0,
	padx = 10,
	pady = 10
)

ingresar_btn = Button(root_frame,text = 'Ingresar Plazo Fijo', command = abrirIngresar)
ingresar_btn.grid(
	row = 0,
	column = 0,
	pady = 7
)
ingresar_btn.config(
	height=1,
	width = 20
)

visualizar_btn = Button(root_frame,text = 'Visualizar Plazos Fijos', command = lambda: abrirMostrar(False))
visualizar_btn.grid(
	row = 1,
	column = 0,
	pady = 7
)
visualizar_btn.config(
	height=1,
	width = 20
)
editar_btn = Button(root_frame,text = 'Editar Información', command = lambda: abrirMostrar(True))
editar_btn.grid(
	row = 2,
	column = 0,
	pady = 7
)
editar_btn.config(
	height=1,
	width = 20
)

graficos_btn = Button(root_frame,text = 'Gráficos', command = abrirGraficos)
graficos_btn.grid(
	row = 3,
	column = 0,
	pady = 7
)
graficos_btn.config(
	height=1,
	width = 20
)

actualizarActivos()

root.mainloop()


# conn = sqlite3.connect('plazos_fijos.db')
# cursor = conn.cursor()
# sqlQuery = "SELECT *,oid FROM pzosFijos "
# cursor.execute(sqlQuery)
# records = cursor.fetchall()
# print(records)