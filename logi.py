from tkinter import *
from pyswip import Prolog, Functor, Variable, Query
from tkinter import messagebox

def buscaLetras(cadena):
    letras = "abcdefghijklmnopqrstuvwxyz!#$%&/()=?¡'¿+}{][-_.:;|\""
    cadena=cadena.lower()
    for s in cadena:
        if s in letras:
            print(s)
            return (1)
    return (0)

def envio():
    #primero se recibe el string proveniente de la ventana
    problemas = mensaje.get()
    salida = StringVar()
    salida = ""
    #se buscara que en la cadena solo existan numeros y comas
    #en caso de existir, se activara la bandera y se retornara un error
    flag=buscaLetras(problemas)
    if flag==1:
        salida="ERROR: letras y caracteres no aceptados"
        return (messagebox.showinfo("Resultado busqueda",salida))

    #Se eliminan todos los espacios
    problemas = problemas.replace(" ", "")
    #se separa en una lista con unicamente los numeros
    problemaList=problemas.split(",")

    #se revisara que la lista que se revisara contenga numeros y no espacio vacio
    for k in problemaList:
        if len(k)==0:
            salida="ERROR: Valores ingresados no validos"
            return (messagebox.showinfo("Resultado busqueda",salida))

    
    if len(problemaList)==5:
        for i in prolog.query("is_componente1(X,"+problemaList[0]+","+problemaList[1]+","+problemaList[2]+","+problemaList[3]+","+problemaList[4]+")"):
            salida=salida+"Mayor prioridad de cambio: "+str(i["X"])+" \n\n"    
    elif len(problemaList)==3:
    	for i in prolog.query("is_componente2(X,"+problemaList[0]+","+problemaList[1]+","+problemaList[2]+")"):
            salida=salida+"Mayor prioridad de cambio: "+str(i["X"])+" \n\n"


    for k in problemaList:
        for i in prolog.query("is_componente3(X,"+k+")"):            
            if i["X"] not in salida:
            	salida=salida+str(i["X"])+" \n\n"
            else:
            	bus1="Dar prioridad a: "+str(i["X"])
            	bus2="Mayor prioridad de cambio: "+str(i["X"])
            	if bus2 not in salida:
            		if bus1 not in salida:
            			salida = salida.replace(i["X"],"Dar prioridad a: "+str(i["X"]))+" \n\n"

    if len(salida)==0:
        salida="Sin conocimiento"

    return (messagebox.showinfo("Resultado busqueda",salida))






prolog = Prolog()




#HECHOS

prolog.assertz("componente(sistema_de_refrigeracion,2,4)")
prolog.assertz("componente(memoria_ram,1,2,7,8,11)")
prolog.assertz("componente(procesador,1,2,5,10,8)")
prolog.assertz("componente(placa_madre,1,2,4)")
prolog.assertz("componente(tarjeta_grafica,1,2,3,8,9)")
prolog.assertz("componente(disco_duro,5,6,10,11,8)")
prolog.assertz("componente(fuente_de_poder,1,2)")

"""
1-No enciende (ram, procesador, placa madre, grafica)
2-Apagado/Reinicio repentino (ram, procesador, placa madre, grafica, refrigeracion)
3-Monitor no muestra imagen (grafica)
4-Sobrecalentamiento(refrigeracion, placa madre)
5-Lentitud en el equipo (discoduro, procesador)
6-Imposibilidad de instalar programas (discoduro)
7-Error al acceder a un archivo  (disco duro,ram)
8-El ordenador pita al intentar encenderlo(grafica, ram, placa madre, procesador, disco duro)
9-Rayas verticales en el monitor(grafica)
10-Pantalla Azul(discoduro, ram, procesador)
11-Archivos corruptos (disco duro, ram)
"""

#REGLAS

prolog.assertz("is_componente1(X,Y,Z,A,B,C):-(componente(X,Y,_,_,_,_);componente(X,_,Y,_,_,_);componente(X,_,_,Y,_,_);componente(X,_,_,_,Y,_);componente(X,_,_,_,_,Y)),(componente(X,Z,_,_,_,_);componente(X,_,Z,_,_,_);componente(X,_,_,Z,_,_);componente(X,_,_,_,Z,_);componente(X,_,_,_,_,Z)),(componente(X,A,_,_,_,_);componente(X,_,A,_,_,_);componente(X,_,_,A,_,_);componente(X,_,_,_,A,_);componente(X,_,_,_,_,A)),(componente(X,B,_,_,_,_);componente(X,_,B,_,_,_);componente(X,_,_,B,_,_);componente(X,_,_,_,B,_);componente(X,_,_,_,_,B)),(componente(X,C,_,_,_,_);componente(X,_,C,_,_,_);componente(X,_,_,C,_,_);componente(X,_,_,_,C,_);componente(X,_,_,_,_,C))")
prolog.assertz("is_componente2(X,Y,Z,A):-(componente(X,Y,_,_);componente(X,_,Y,_);componente(X,_,_,Y)),(componente(X,Z,_,_);componente(X,_,Z,_);componente(X,_,_,Z)),(componente(X,A,_,_);componente(X,_,A,_);componente(X,_,_,A))")
prolog.assertz("is_componente3(X,Y):-componente(X,Y,_);componente(X,_,Y);componente(X,Y,_,_);componente(X,_,Y,_);componente(X,Y,_,_,_,_);componente(X,_,Y,_,_,_);componente(X,_,_,Y,_,_);componente(X,_,_,_,Y,_);componente(X,_,_,_,_,Y)")


#Propiedades de la ventana
#creacion ventana
ventana=Tk()
ventana.title('Taller 1 ')
ventana.geometry("700x400+600+250")

#Varialbles a ultizar en ventana
mensaje = StringVar()
errores="\t1-No enciende \n\t2-Apagado/Reinicio repentino\n\t3-Monitor no muestra imagen \n\t4-Sobrecalentamiento\n\t5-Lentitud en el equipo \n\t6-Imposibilidad de instalar programas\n\t7-Error al acceder a un archivo\n\t8-El ordenador pita al intentar encenderlo\n\t9-Rayas verticales en el monitor\n\t10-Pantalla Azul\n\t11-Internet lento\n\t12-Archivos corruptos\n\t13-Ventanas emergentes"

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