from tkinter import *
from pyswip import Prolog
from tkinter import messagebox


def envio():		
	problema = mensaje.get()
	salida = StringVar()
	salida = ""	
	for i in prolog.query("is_componente(X,"+problema+")"):
		print("se encontro \n",i["X"])
		salida=salida+str(i["X"])+" \n"
	if len(salida)==0:
		salida="Sin conocimiento"
		
	return (messagebox.showinfo("Resultado busqueda",salida))	





print("inicio")
prolog = Prolog()




#HECHOS
prolog.assertz("componente(sistema_de_refrigeracion,4,7)")
prolog.assertz("componente(memoria_ram,3,2)")
prolog.assertz("componente(procesador,2,1)")
prolog.assertz("componente(placa_madre,7,7)")
prolog.assertz("componente(memoria_fisica,5,6)")
prolog.assertz("componente(tarjeta_grafica,1,3)")
prolog.assertz("componente(fuente_de_poder,1,2)")

"""
a-1-No enciende  (fuente de poder,tarjeta grafica )
b-2-Apagado repentino (fuente de poder, procesador)
c-3-Monitor no muestra imagen(tarjeta grafica, )
d-4-Sobrecalentamiento (tarjeta grafica, procesador )
e-5-Lentitud en el equipo (disco duro)
f-6-Imposibilidad de instalar programas (disco duro)
g-7-Relleno
"""

#REGLAS
prolog.assertz("is_componente(X,Y):-componente(X,Y,_);componente(X,_,Y)")

#Propiedades de la ventana
#creacion ventana
ventana=Tk()
ventana.title('Taller 1 ')
ventana.geometry("600x600+600+250")

#Varialbles a ultizar en ventana
mensaje = StringVar()
errores="\t1-No enciende \n\t2-Apagado repentino\n\t3-Monitor no muestra imagen \n\t4-Sobrecalentamiento\n\t5-Lentitud en el equipo \n\t6-Imposibilidad de instalar programas\n\t7-Relleno"

#Generacion del contenido
etiquetaMensaje1 = Label(ventana, text='Errores:')
etiquetaMensaje2 = Label(ventana, text=errores)
entradaMensaje = Entry(ventana, textvariable=mensaje, width=40, bd=5)
etiquetaMensaje1.grid(row=1, column=1)
etiquetaMensaje2.grid(row=2, column=1)
entradaMensaje.grid(row=2, column=3)

#Boton
boton = Button(ventana, text="Buscar Origen", command=envio, width=20)
boton.grid(row=8, column=3)
boton_2 = Button(ventana, text="Cerrar", command=ventana.quit)
boton_2.grid(row=15, column=3)

#Muestra de la ventana
ventana.mainloop()