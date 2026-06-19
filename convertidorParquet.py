import duckdb as duck
import tkinter as tk
import tkinter.filedialog as fd
from threading import *
from pathlib import Path
import time
import random

# UI
ventana = tk.Tk()
ventana.title("Convertidor de CSV a Parquet")
ventana.geometry("1080x800")
label = tk.Label(ventana, text="Bienvenido")
label.pack()
trabajando = False
mensajes = ["¡Estoy en ello!", "No falta mucho", "Puede que esto tome un momento", "Preparando el arhivo Parquet", "¡Sigo aquí!", "Leyendo...", "Ya falta poco", "Me estoy apurando"]
inicio = 0
#Selector de archivos
def selector():
    global trabajando
    # Se seleccionan un archivo
    ruta = Path(fd.askopenfilename(filetypes=[("Archivos CSV", "*.csv")]))
    validacion = str(ruta)
    print(validacion)
    if len(validacion) > 1:
        # Marca de inicio de la operación
        inicio = time.time()
        trabajando = True
        print(ruta)
        # Se obtiene la extensión
        sufijo = ruta.suffix
        # Se obtiene el nombre, solo es para la parte visual
        nombreArchivo = ruta.stem
        # Se obtiene la ruta sin la extensión, para posteriormente cambiarsela
        archivoTransformado = ruta.with_suffix(".parquet") 

        #Validación
        if sufijo != ".csv":
            label2.config(text="Asegurese de seleccionar un archivo con el sufijo .csv")
            print("Asegurese de seleccionar un archivo con el sufijo .csv")
        else:
            label2.config(text=f"Procesando archivo: {nombreArchivo}")
            print(sufijo)
            print(f"Nuevo archivo:{archivoTransformado}")
            print("-----------------Hasta aquí llegué-----------------")

            mensaje_aleatorio()
                
            # Se usa duckdb para reescribir el archivo csv pero en formato
            duck.sql(f"COPY (SELECT * FROM read_csv_auto('{ruta}'))TO '{archivoTransformado}'(FORMAT PARQUET);")
                
            # Marca de final de la operación
            final = time.time()
            # Resta de las marcas para obtener la duración del proceso
            delta = final - inicio
                
            label2.config(text=f"El proceso ha finalizado en {round(delta,2)}s")
            trabajando = False
            
            print("Yay :D")
            
    else:
        print("No se seleccionó ningún archivo")

def hilar():
    hilo1 = Thread(target=selector)
    hilo1.start()

def mensaje_aleatorio():
    if trabajando:
        label3.config(text=random.choice(mensajes))
        ventana.after(5000, mensaje_aleatorio)
    else: 
        label3.config(text="A la orden")

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady="20px")
boton = tk.Button(frame_botones, text="Seleccionar archivo", command=hilar)
boton2 = tk.Button(frame_botones, text="Cerrar",command=ventana.destroy)
label2 = tk.Label(ventana, text="")
label3 = tk.Label(ventana, text="")

boton.pack(side="left")
boton2.pack(side="left", padx="30px")
label2.pack()
label3.pack()


ventana.mainloop()
