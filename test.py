from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


#https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem.html#example-plot-tipping-problem-py

def escalas():

	#generacion de los graficos
	fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4, figsize=(8, 9))

	ax0.plot(x_qual, qual_lo, 'b', linewidth=1.5, label='Bad')
	ax0.plot(x_qual, qual_md, 'g', linewidth=1.5, label='Decent')
	ax0.plot(x_qual, qual_hi, 'r', linewidth=1.5, label='Great')
	ax0.set_title('Food quality')
	ax0.legend()

	ax1.plot(x_serv, serv_lo, 'b', linewidth=1.5, label='Poor')
	ax1.plot(x_serv, serv_md, 'g', linewidth=1.5, label='Acceptable')
	ax1.plot(x_serv, serv_hi, 'r', linewidth=1.5, label='Amazing')
	ax1.set_title('Service quality')
	ax1.legend()

	ax2.plot(x_tip, tip_lo, 'b', linewidth=1.5, label='Low')
	ax2.plot(x_tip, tip_md, 'g', linewidth=1.5, label='Medium')
	ax2.plot(x_tip, tip_hi, 'r', linewidth=1.5, label='High')
	ax2.set_title('Tip amount')
	ax2.legend()

	ax3.plot(x_tip, tip_lo, 'b', linewidth=1.5, label='Low')
	ax3.plot(x_tip, tip_md, 'g', linewidth=1.5, label='Medium')
	ax3.plot(x_tip, tip_hi, 'r', linewidth=1.5, label='High')
	ax3.set_title('Tip amount')
	ax3.legend()

	# Turn off top/right axes
	for ax in (ax0, ax1, ax2, ax3):
		ax.spines['top'].set_visible(False)
		ax.spines['right'].set_visible(False)
		ax.get_xaxis().tick_bottom()
		ax.get_yaxis().tick_left()
	plt.tight_layout()

	#creacion de la ventana
	#debido a la cantidad de graficos se crearan 2
	root = Tk()
	root.wm_title("Grafica insertada en Tkinter")
	#etiquetaMensaje = Label(root, text='El centroide es: 2')
	#etiquetaMensaje.grid(row=1, column=1)
	#------------------------------CREAR GRAFICA---------------------------------

	canvas = FigureCanvasTkAgg(fig, master=root)  # CREAR AREA DE DIBUJO DE TKINTER.
	canvas.draw()
	canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

	#ventana 2
	root2 = Tk()
	root2.wm_title("Grafica insertada en Tkinter")
	#------------------------------CREAR GRAFICA---------------------------------

	canvas = FigureCanvasTkAgg(fig, master=root2)  # CREAR AREA DE DIBUJO DE TKINTER.
	canvas.draw()
	canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)







def rendimiento():
	flag=0
	#comprobacion de los datos
	#en caso de que alguno no cumpla los datos se saldra del proceso

	refrigeracion_ = float(refrigeracion.get())
	memRam_ = float(memRam.get())
	procesador_ = float(procesador.get())
	placaMadre_ = float(placaMadre.get())
	memFisica_ = float(memFisica.get())
	grafica_ = float(grafica.get())
	fuentePoder_ = float(fuentePoder.get())
	if refrigeracion_<0 or refrigeracion_>10:
		flag=1
	if memRam_<0 or memRam_>10:
		flag=1
	if procesador_<0 or procesador_>10:
		flag=1
	if placaMadre_<0 or placaMadre_>10:
		flag=1
	if memFisica_<0 or memFisica_>10:
		flag=1
	if grafica_<0 or grafica_>10:
		flag=1
	if fuentePoder_<0 or fuentePoder_>10:
		flag=1

	#if flag==1:
	#	salida="Datos no acceptables"
	#	return (messagebox.showinfo("Error",salida))

	


	# We need the activation of our fuzzy membership functions at these values.
	# The exact values 6.5 and 9.8 do not exist on our universes...
	# This is what fuzz.interp_membership exists for!
	qual_level_lo = fuzz.interp_membership(x_qual, qual_lo, 6.5)
	qual_level_md = fuzz.interp_membership(x_qual, qual_md, 6.5)
	qual_level_hi = fuzz.interp_membership(x_qual, qual_hi, 6.5)

	serv_level_lo = fuzz.interp_membership(x_serv, serv_lo, 9.8)
	serv_level_md = fuzz.interp_membership(x_serv, serv_md, 9.8)
	serv_level_hi = fuzz.interp_membership(x_serv, serv_hi, 9.8)

	# Now we take our rules and apply them. Rule 1 concerns bad food OR service.
	# The OR operator means we take the maximum of these two.
	active_rule1 = np.fmax(qual_level_lo, serv_level_lo)

	# Now we apply this by clipping the top off the corresponding output
	# membership function with `np.fmin`
	tip_activation_lo = np.fmin(active_rule1, tip_lo)  # removed entirely to 0

	#se aplica directamente sin ncesidad de itlizar el interp
	# For rule 2 we connect acceptable service to medium tipping
	tip_activation_md = np.fmin(serv_level_md, tip_md)

	# For rule 3 we connect high service OR high food with high tipping
	active_rule3 = np.fmax(qual_level_hi, serv_level_hi)
	tip_activation_hi = np.fmin(active_rule3, tip_hi)
	tip0 = np.zeros_like(x_tip)



	aggregated = np.fmax(tip_activation_lo,
                     np.fmax(tip_activation_md, tip_activation_hi))

	# Calculate defuzzified result
	defuzz_centroid = fuzz.defuzz(x_tip, aggregated, 'centroid')
	defuzz_bisector = fuzz.defuzz(x_tip, aggregated, 'bisector')
	tip_activation = fuzz.interp_membership(x_tip, aggregated, defuzz_centroid)  # for plot
	tip_activation2 = fuzz.interp_membership(x_tip, aggregated, defuzz_bisector)  # for plot

	# Visualize this
	fig, ax0 = plt.subplots(figsize=(8, 3))

	ax0.plot(x_tip, tip_lo, 'b', linewidth=0.5, linestyle='--', )
	ax0.plot(x_tip, tip_md, 'g', linewidth=0.5, linestyle='--')
	ax0.plot(x_tip, tip_hi, 'r', linewidth=0.5, linestyle='--')
	ax0.fill_between(x_tip, tip0, aggregated, facecolor='Orange', alpha=0.7)
	ax0.vlines(defuzz_centroid, 0, tip_activation, label='centroide', color='k')
	ax0.vlines(defuzz_bisector, 0, tip_activation2, label='bisector', color='m')
	ax0.set_title('Aggregated membership and result (line)')
	ax0.legend(loc=2)

	# Turn off top/right axes
	for ax in (ax0,):
		ax.spines['top'].set_visible(False)
		ax.spines['right'].set_visible(False)
		ax.get_xaxis().tick_bottom()
		ax.get_yaxis().tick_left()
	plt.ylabel('nose')
	plt.xlabel('escala')
	plt.tight_layout()



	root = Tk()
	root.wm_title("Grafica insertada en Tkinter")
	#etiquetaMensaje = Label(root, text='El centroide es: 2')
	#etiquetaMensaje.grid(row=1, column=1)
	#------------------------------CREAR GRAFICA---------------------------------

	canvas = FigureCanvasTkAgg(fig, master=root)  # CREAR AREA DE DIBUJO DE TKINTER.
	#canvas.grid(row=3, column=1)
	canvas.draw()
	canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

	etiquetaMensaje1 = Label(root, text="bisector: "+str(round(defuzz_bisector, 3)))
	etiquetaMensaje1.pack(side=TOP)

	etiquetaMensaje2 = Label(root, text="centroide: "+str(round(defuzz_centroid, 3)))
	etiquetaMensaje2.pack(side=TOP)

	button = Button(master=root, text="cerrar", command=root.quit)
	button.pack(side=BOTTOM)



# Generate universe variables
#   * Quality and service on subjective ranges [0, 10]
#   * Tip has a range of [0, 25] in units of percentage points

#aca debemos colocar nuestras variables
x_qual = np.arange(0, 11, 1)
x_serv = np.arange(0, 11, 1)
x_tip  = np.arange(0, 26, 1)

# Generate fuzzy membership functions
qual_lo = fuzz.trimf(x_qual, [0, 0, 5])
qual_md = fuzz.trimf(x_qual, [0, 5, 10])
qual_hi = fuzz.trimf(x_qual, [5, 10, 10])
#--------------------
serv_lo = fuzz.trimf(x_serv, [0, 0, 5])
serv_md = fuzz.trimf(x_serv, [0, 5, 10])
serv_hi = fuzz.trimf(x_serv, [5, 10, 10])
#--------------------
tip_lo = fuzz.trimf(x_tip, [0, 0, 13])
tip_md = fuzz.trimf(x_tip, [0, 13, 25])
tip_hi = fuzz.trimf(x_tip, [13, 25, 25])
#--------------------


ventana=Tk()
ventana.title('Taller 2 ')
ventana.geometry("700x400+600+250")

refrigeracion = StringVar()
memRam = StringVar()
procesador = StringVar()
placaMadre = StringVar()
memFisica = StringVar()
grafica = StringVar()
fuentePoder = StringVar()


etiquetaMensaje = Label(ventana, text='Rendimiento esperado:')
etiquetaMensaje.grid(row=1, column=1)
#Generacion del contenido
#primer cosito
etiquetaMensaje1 = Label(ventana, text='Calidad del sistema de refrigeración (0-10):')
etiquetaMensaje1.grid(row=5, column=1)
entradaMensaje1 = Entry(ventana, textvariable=refrigeracion, width=10, bd=5)
entradaMensaje1.grid(row=5, column=3)
#segundo cosito
etiquetaMensaje2 = Label(ventana, text='Calidad de la memoria RAM (0-10):')
entradaMensaje2 = Entry(ventana, textvariable=memRam, width=10, bd=5)
etiquetaMensaje2.grid(row=7, column=1)
entradaMensaje2.grid(row=7, column=3)
#tercer cosito
etiquetaMensaje2 = Label(ventana, text='Calidad del procesador (0-10):')
entradaMensaje2 = Entry(ventana, textvariable=procesador, width=10, bd=5)
etiquetaMensaje2.grid(row=9, column=1)
entradaMensaje2.grid(row=9, column=3)
#cuarto cosito
etiquetaMensaje2 = Label(ventana, text='Calidad de la placa madre (0-10):')
entradaMensaje2 = Entry(ventana, textvariable=placaMadre, width=10, bd=5)
etiquetaMensaje2.grid(row=11, column=1)
entradaMensaje2.grid(row=11, column=3)
#quinto cosito
etiquetaMensaje2 = Label(ventana, text='Calidad de la memoria fisica o disco duro (0-10):')
entradaMensaje2 = Entry(ventana, textvariable=memFisica, width=10, bd=5)
etiquetaMensaje2.grid(row=13, column=1)
entradaMensaje2.grid(row=13, column=3)
#sexto cosito
etiquetaMensaje6 = Label(ventana, text='Calidad de la tarjeta gráfica (0-10):')
entradaMensaje6 = Entry(ventana, textvariable=grafica, width=10, bd=5)
etiquetaMensaje6.grid(row=15, column=1)
entradaMensaje6.grid(row=15, column=3)
#septimo cosito
etiquetaMensaje7 = Label(ventana, text='Calidad de la fuente de poder (0-10):')
entradaMensaje7 = Entry(ventana, textvariable=fuentePoder, width=10, bd=5)
etiquetaMensaje7.grid(row=17, column=1)
entradaMensaje7.grid(row=17, column=3)

#Botones
boton = Button(ventana, text="Estimar rendimiento", command=rendimiento, width=20)
boton.grid(row=23, column=3)
boton_2 = Button(ventana, text="Visualizar escalas", command=escalas, width=20)
boton_2.grid(row=25, column=3)
boton_3 = Button(ventana, text="Cerrar", command=ventana.quit)
boton_3.grid(row=27, column=3)

#Muestra de la ventana
ventana.mainloop()