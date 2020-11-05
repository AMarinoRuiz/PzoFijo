from tkinter import *

class Table: 
	  
	def __init__(self,root,titles,content,visibility,editability = False): 
		"""
			titles: lista con títulos, N columnas
			content: [[record1], ... [recordM]], cada record tiene N campos
			visibility: lista de bools que marcan si el índice es visible o no
			editability: modo sólo lectura o editable
		"""
		self.total_rows = len(content) 
		# self.total_columns = len(content[0])-1
		self.total_columns = len(titles)
		self.elements = []
		self.totales = [0,0,0]
		self.borrar_chk = []
		self.borrar_var = {}

		for j in range(self.total_columns):
			if visibility[j]:
				self.e = Label(root, 
					text = titles[j],
					width = 15,
					justify = 'center',
					font=('helvetica',9,'bold'),
					borderwidth = 1.7,
					relief= 'groove',
					bg = '#FBC4A3'
					)
				self.elements.append(self.e)

				self.e.grid(row=0, column = j)
		if editability:
			self.e = Label(root, 
				text = '',
				width = 5,
				justify = 'center',
				font=('helvetica',9),
				borderwidth = 1.7,
				relief= 'groove',
				bg = '#FBC4A3'
				)
			# self.elements.append(self.e)

			self.e.grid(row=0, column = self.total_columns+1)


		for i in range(self.total_rows): 
			for j in range(self.total_columns): 
				if visibility[j]:  
					if editability:
						self.e = Entry(root,
							width=15,
							justify = 'center',
							font=('helvetica',9),
							borderwidth = 1.7,
							relief= 'groove'
							)
						self.e.insert(0,self.formatDisplay(content[i][j],j))
						# self.e.insert(0,content[i][j])
					else:
						self.e = Label(root,
							text = self.formatDisplay(content[i][j],j),
							# text = content[i][j],
							width=15,
							justify = 'center',
							font=('helvetica',9),
							borderwidth = 1.7,
							relief= 'groove'
						)
					self.elements.append(self.e)
					self.e.grid(row=i+1, column=j) 

					if i%2 == 0:
						self.e.config(bg ='#B6FF9E') 
					else:
						self.e.config(bg = '#9EFFFC')
				if j in [7,8,9]: # 7 inicial, 8 final, 9 total
					if content[i][j] != '':
						try:
								self.totales[j-7] += float(content[i][j])
						except:
							pass
			if not editability:
				self.e = Label(root,
						text = 'Totales:',
						width=15,
						justify = 'center',
						font=('helvetica',9,'bold'),
						borderwidth = 1.7,
						relief= 'groove'
					)
				self.elements.append(self.e)
				self.e.grid(row=self.total_rows+1, column=6
					)
				self.e.config(bg ='#f5d742') 
				
				for r in range(len(self.totales)):
					self.e = Label(root,
						text = round(self.totales[r],2),
						width=15,
						justify = 'center',
						font=('helvetica',9),
						borderwidth = 1.7,
						relief= 'groove'
					)
					self.elements.append(self.e)
					self.e.grid(row=self.total_rows+1, column=r+7
						)
					self.e.config(bg ='#f5d742')

			if editability: #agrego check borrar
				var_global_borrar = globals()[content[i][-1]] = IntVar()
				self.borrar_var[content[i][-1]] = var_global_borrar
				b = Checkbutton(root, var = var_global_borrar,pady=0) 
				self.borrar_chk.append(b)
				b.grid(
					row=i+1,
					column = self.total_columns+1,
					# sticky='n',
					pady = 0
				)
	def formatDisplay(self,value,index):
		"""
			formatea para el display. Devuelve DD-MM-YYYY
		"""

		if index in range(1,3):
			x = re.split("[^0123456789]", value)
			x[1] = x[1].zfill(2)
			x[0] = x[0].zfill(2)
			x = x[::-1]
			return '-'.join(x)
		else:
			return (value or '')


# lst = [(1,'Pedro','Córdoba',19), 
# (2,'Emilia','CABA',18), 
# (3,'Gonzalo','Rosario',20), 
# (4,'Carla','MDQ',21), 
# (5,'Romina','CABA',21)
# ] 

# titles = ['ID','Name','City','Age']

# root = Tk()
# t = Table(root,titles,lst,[True]*5)
# print(type('s'))
# print(type('s') == 'str')
# print(type(4))
# print(type(t))
# print(type(t) == Table)

# # for i in t.elements:
# # 	i.destroy()
# root.mainloop()

