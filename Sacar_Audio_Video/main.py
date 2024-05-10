import tkinter as tk # libreria de tk para que armar la aplicacion
from tkinter import filedialog, messagebox # para las alertas y buscar los archivos de video en este caso
from moviepy.editor import VideoFileClip #para tomar el archivo de video
import ttkbootstrap as ttk # para mejorar la estetica del video

#Creo la Clase
class Aplicacion: # es una costumbre mia de trabajar asi en si!
    def __init__(self,ventana) -> None:
        self.ventana = ventana
        self.ventana.title("Descargar Videos")
        self.ventana.resizable(0,0) #para que no se pueda agrandar ni achicar
        
        self.archivo_ruta = ttk.Frame(self.ventana)
        self.archivo_ruta.grid(row=0,column=0,padx=5,pady=5)
        
        self.frame_archivo = ttk.LabelFrame(master=self.archivo_ruta,text="Archivo de Video")
        self.frame_archivo.grid(row=1,column=0,columnspan=4,padx=5,pady=5,sticky="we")
        
        #Armo en entry donde va a quedar alojado la ruta del video
        self.ruta_de_video = ttk.StringVar()
        self.ruta_de_video = ttk.Entry(master=self.frame_archivo, textvariable=self.ruta_de_video,width=50)
        self.ruta_de_video.grid(row=1,column=0,padx=5,pady=5)
        self.ruta_de_video.config(state="disable") #lo deshabilito para que no se pueda escribir
        
        #boton de seleccionar el video
        btn_seleccionar_video = ttk.Button(master=self.frame_archivo,text="Seleccionar Video",width=10,command=self.seleccionar_video)
        btn_seleccionar_video.grid(row=1,column=1,padx=10,pady=10)
        
        #boton para extraer audio
        btn_extraer_audio_completo = ttk.Button(master=ventana, text="Extraer Audio COmpleto",width=60,command=self.extraer_audio)
        btn_extraer_audio_completo.grid(row=1,column=0,padx=10,pady=10)
        
        #boton para extraer audio en segundos cortado(inico/fin)
        btn_extraer_audio_cortado = ttk.Button(master=ventana,text="Seleccionar Minutos de Video",width=60,command=self.inicio_fin_extraer_audio)
        btn_extraer_audio_cortado.grid(row=2,column=0,padx=10,pady=10)
        
     #metodo para poder seleccionar el video desde una carpeta           
    def seleccionar_video(self):
        #con esto me aseguro de que pueda seleccionar videos tanto de tipo avi como mp4 x si tengo varios formatos y los detallo para que no me seleccione otra cosa
        self.archivo_video = filedialog.askopenfilename(title="Seleccionar archivo de video", filetypes=[("Archivos de video","*.mp4 *.avi")])
        
        #si seleccione uno!
        if self.archivo_video:
            self.ruta_de_video.config(state="normal")#su estado lo cambio a normal
            self.ruta_de_video.delete(0,tk.END)#borro lo que hay
            self.ruta_de_video.insert(0,self.archivo_video)#inserto la ruta del video que seleccione
            self.ruta_de_video.config(state="disabled")#lo vuelvo a colocar disable para que no se edite a mano
        else:
            messagebox.showerror("Error","No se ha seleccionado un archivo de video")
    
    def extraer_audio(self, inicio =None,fin = None): #para poder usarla tambien para el de inicio y fin de tiempo y no crear 2 funciones similares
        try:
            if not self.archivo_video:
                messagebox.showerror("Error","No se ha seleccionado ningún archivo de video")
                return
            #aca voy a guardar el clip
            video_clip = VideoFileClip(self.archivo_video)
            
            if inicio is not None:
                inicio = self.convertir_a_segundos(inicio)
                fin = self.convertir_a_segundos(fin)
                if fin <= inicio:
                    messagebox.showerror("Error","El tiempo de fin debe ser mayor que el tiempo de inicio")                
                    return
                audio = video_clip.subclip(inicio, fin).audio #tomo el timpo del video 
            else:
                audio = video_clip.audio 
            
            nombre_archivo_audio = self.archivo_video.split('.')[0]+"_audio_desde_{}_hasta_{}.mp3".format(inicio,fin) #Armo el nombre asi para identificarlo
            audio.write_audiofile(nombre_archivo_audio)
            video_clip.close
            
            messagebox.showinfo("Éxito","El audio se ha extraído correctamente puede con el nombre{}".format(nombre_archivo_audio)) 
            
        except Exception as e:
            messagebox.showerror("Error",f"se produjo un error .> {e}") # para poder leer si me da un error

    #con esto armo el formato correcto para que sea mas entendible a la hora de mostrarle
    def convertir_a_segundos(self,tiempo): #asi se entiende mejor
        try:
            partes = tiempo.split(":")
            horas = int(partes[0]) * 3600
            minutos = int(partes[1]) * 60
            segundos = int(partes[2])
            total_segundos = horas + minutos + segundos
            return total_segundos
        except ValueError: #para que sea numero
            messagebox.showerror("Error","El formato de tiempo debe ser hh:mm:ss")    
    
    #Metodo que permite elegir el tiempo que deseo obtener del video en audio, es decir si quiero solo del inicio al segundo 2 por ejemplo y no todo el audio
    def inicio_fin_extraer_audio(self):
        if self.archivo_video:
            ventana_tiempo = ttk.Toplevel(self.ventana)
            ventana_tiempo.title("Seleccionar Tiempo de Inicio y Fin")
            ventana_tiempo.grab_set() # Esto es para que no se pueda hacer nada luego de que esa ventana este por encima
            
            #label
            label_inicio = ttk.Label(master=ventana_tiempo,text="Inicio (hh:mm:ss):")
            label_inicio.grid(row=0,column=0,padx=5,pady=5)
            #entrada
            entry_inicio = ttk.Entry(ventana_tiempo)
            entry_inicio.insert(0,"00:00:00")#para q inicie asi
            entry_inicio.grid(row=0,column=1,padx=5,pady=5)
            
            #segundo label
            label_fin = ttk.Label(master=ventana_tiempo,text="Fin (hh:mm:ss):")
            label_fin.grid(row=1,column=0,padx=5,pady=5)
            #segunda entrada
            entry_fin = ttk.Entry(ventana_tiempo)
            entry_fin.insert(0,"00:00:00")#para q inicie asi
            entry_fin.grid(row=1,column=1,padx=5,pady=5)

            #boton para confirmar cambios
            btn_extraer = ttk.Button(master=ventana_tiempo,text="Extraer Audio",command=lambda: self.extraer_audio(entry_inicio.get(),entry_fin.get()))
            btn_extraer.grid(row=2,column=0,columnspan=2,padx=5,pady=10)

if __name__ == "__main__":
    ventana_principal =  ttk.Window(themename="darkly")#le aplico un tema oscuro, hay varios en la pag de ttkbooststrap
    ventana_principal.iconbitmap("musica.ico")#el icono que baje
    app = Aplicacion(ventana_principal)
    ventana_principal.mainloop()#para que se mantenga abierta
        

