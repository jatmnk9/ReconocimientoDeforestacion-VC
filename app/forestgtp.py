import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import PhotoImage
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import meshio
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mayavi import mlab
import subprocess


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

       
        # configure window
        self.title("ForestP.py")
        self.geometry(f"{1100}x{580}")
        self.iconbitmap('icono.ico')


        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="ForestP", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Ingresar imagen", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Ingresar coordenada", command=self.scrapper)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.segmentate)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Imagen Actual")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text="Reiniciar" ,fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.restart)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkScrollableFrame(self, label_text="Porcentaje de deforestación")
        self.tabview.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.optionmenu_1 = customtkinter.CTkButton(master=self.tabview, text="Area deforestada", hover=False, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.optionmenu_2 = customtkinter.CTkButton(master=self.tabview, text="Area no deforestada", hover=False, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.optionmenu_2.grid(row=3, column=0, padx=20, pady=(20, 10))
        # self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
        #                                                    command=self.open_input_dialog_event)
        # self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(1, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=7, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
        self.scrollable_frame.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        self.switch = customtkinter.CTkButton(master=self.scrollable_frame, text="Imagen 3D", command=self.Imagen3D, state="disabled")
        self.switch.grid(row=1, column=0, padx=10, pady=(0, 20))

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Elegir una opcion")
        self.appearance_mode_optionemenu.set("Dark")
        segemented_button_var = customtkinter.StringVar(value="Segmentado")
        self.seg_button_1.configure(state="disabled",values=["Original", "Segmentado", "Textura 1", "Textura 2"], variable=segemented_button_var, command = self.mostrarImagen)


    def mostrarImagen(self, value):
        if(self.seg_button_1.get() == "Original"):
            self.imagen(image)
        elif (self.seg_button_1.get() == "Segmentado"):
            self.imagen(img_segmentada)
        elif (self.seg_button_1.get() == "Textura 1"):
            self.imagen(img_binaria)
        elif (self.seg_button_1.get() == "Textura 2"):
            imagencita = cv2.imread("./image_data/textura3.png")
            self.imagen(imagencita)


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


    def sidebar_button_event(self):
        # Especificar los tipos de archivos, para elegir solo a las imágenes
        # Label donde se presentará la imagen de entrada
        self.restart()

        path_image = filedialog.askopenfilename(filetypes = [
            ("image", ".jpeg"),
            ("image", ".png"),
            ("image", ".jpg")])

        if len(path_image) > 0:
            self.imagenInput(path_image)

        self.sidebar_button_3.configure(state="enabled", text="Segmentar", hover=True)
        self.entry.configure(placeholder_text=str(path_image))


    def scrapper(self):
        global area
        self.restart()
        dialog = customtkinter.CTkInputDialog(text="Ingrese la coordenada:", title="Imagen por coordenada")
        coordenada=dialog.get_input()
        if (coordenada != ""):
            dialog2 = customtkinter.CTkInputDialog(text="Ingrese los kilometros:", title="Imagen por coordenada")
            kilometros=dialog2.get_input()
        if (coordenada != "" and kilometros!=""):
            kilometros = (float(kilometros) - 0.5) * 1000

            web_side = f"https://earth.google.com/web/@{coordenada},500a,{kilometros}d,35y,0h,0t,0r"
            path = "C:\Archivos de Programa (x86)\chromedriver.exe"

            driver = webdriver.Chrome(service=Service(path))
            driver.get(web_side)
            driver.maximize_window()

            time.sleep(8)

            # Quitar nombres en blanco
            driver.execute_script("document.querySelector('body > earth-app').shadowRoot.querySelector("
                                "'#toolbar').shadowRoot.querySelector('#map-style').shadowRoot.querySelector('#icon').click();")
            driver.execute_script('document.querySelector("body > earth-app").shadowRoot.querySelector('
                                '"#drawer-container").shadowRoot.querySelector("#mapstyle").shadowRoot.querySelector('
                                '"#header-layout > aside > paper-radio-group > earth-radio-card:nth-child('
                                '1)").shadowRoot.querySelector("#card").click();')
            driver.execute_script("document.querySelector('body > earth-app').shadowRoot.querySelector("
                                "'#toolbar').shadowRoot.querySelector('#map-style').shadowRoot.querySelector('#icon').click();")

            time.sleep(2)

            # Obtener las dimensiones de la ventana del navegador
            window_size = driver.execute_script("return [window.outerWidth, window.outerHeight];")

            #

            #CLic para medir
            driver.execute_script('document.querySelector("body > earth-app").shadowRoot.querySelector('
                                '"#toolbar").shadowRoot.querySelector("#measure").shadowRoot.querySelector("#icon").click();')
            #Ocultar barra lateral
            driver.execute_script('document.querySelector("body > earth-app").shadowRoot.querySelector("#toolbar").style.display '
                                '= "none";')

            #Ocultar barra de abajo
            driver.execute_script('document.querySelector("body > earth-app").shadowRoot.querySelector("#earth-relative-elements '
                                '> earth-view-status").style.display = "none";')

            driver.execute_script(
                "document.querySelector('body > earth-app').shadowRoot.querySelector('#earth-relative-elements "
                "> earth-view-status').style.display = 'none';")
            time.sleep(2)

            #Hacer clic en la esquina superior izquierda
            actions = ActionChains(driver)
            actions.move_by_offset(0, 0).click().perform()
            time.sleep(2)
            # Hacer clic en la esquina superior derecha
            actions = ActionChains(driver)
            actions.move_by_offset(1919, 0).click().perform()
            time.sleep(2)
            #Calcular distancia en X

            time.sleep(2)
            distanciaX = driver.execute_script('return document.querySelector("body > earth-app").shadowRoot.querySelector('
                                            '"#measure-tool").shadowRoot.querySelector("#formatted-distance").innerText;')

            distanciaX = distanciaX.replace('.', '')
            distanciaX = distanciaX.replace(',', '.')
            if "km" in distanciaX:
                distanciaX = distanciaX.replace("km", '')
            else:
                distanciaX = distanciaX.replace("m", '')
            distanciaX = float(distanciaX)

            driver.execute_script('document.querySelector("body > earth-app").shadowRoot.querySelector('
                                '"#measure-tool").shadowRoot.querySelector("#close-button").shadowRoot.querySelector('
                                '"#icon").click();')

            distanciaY = distanciaX*49/96

            area = distanciaY * distanciaX

            # Tomar captura de pantalla
            driver.get_screenshot_as_file("./image_data/screenshot.png")

            driver.quit()

            self.imagenInput("./image_data/screenshot.png")
         

            self.sidebar_button_3.configure(state="enabled", text="Segmentar")

            self.entry.configure(placeholder_text=str(coordenada))

    def imagenInput(self, ruta):
        # Label donde se presentará la imagen de entrada
        self.lblInputImage = Label(self.sidebar_frame)
        self.lblInputImage.grid(column=0, row=4)

        global image

        # Leer la imagen de entrada y la redimensionamos
        image = cv2.imread(ruta)
        image= imutils.resize(image, height=380)

        # Para visualizar la imagen de entrada en la GUI
        imageToShow= imutils.resize(image, width=150)
        imageToShow = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(imageToShow )
        img = ImageTk.PhotoImage(image=im)

        self.lblInputImage.configure(image=img)
        self.lblInputImage.image = img

        

    def segmentate(self):
        self.switch.configure(state="enabled")
        self.sidebar_button_3.configure(state="disabled", text="Segmentado")
        self.seg_button_1.configure(state="enabled")
        global image
        global img_segmentada
        global img_binaria
        global texture
        img = image

        self.lblOutputImage = Label(self, width=490)
        self.lblOutputImage.grid(column=1, row=0, rowspan=2, columnspan=2)

        # Convertimos la imagen de BGR a HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Definimos los límites inferior y superior para el color verde (bosques) en HSV
        verde_bajo = np.array([35, 0, 0])
        verde_alto = np.array([80, 255, 255])

        # Definimos los límites inferior y superior para el color marrón (zonas deforestadas) en HSV
        marron_bajo = np.array([10,0,0])
        marron_alto = np.array([28,255,255])


        # Creamos máscaras para cada rango de colores
        mask_verde = cv2.inRange(hsv, verde_bajo, verde_alto)
        mask_marron = cv2.inRange(hsv, marron_bajo, marron_alto)

        # Aplicamos operaciones morfológicas para eliminar ruido
        kernel = np.ones((3,3),np.uint8)
        mask_verde = cv2.morphologyEx(mask_verde, cv2.MORPH_OPEN, kernel)
        mask_marron = cv2.morphologyEx(mask_marron, cv2.MORPH_OPEN, kernel)

        # Sumamos las máscaras para obtener la máscara final
        mask_final = cv2.add(mask_verde, mask_marron)

        # Aplicamos la máscara final a la imagen original para obtener la imagen segmentada
        img_segmentada = cv2.bitwise_and(img, img, mask=mask_final)


        # Convertimos la imagen segmentada a escala de grises
        img_gris = cv2.cvtColor(img_segmentada, cv2.COLOR_BGR2GRAY)

        # Aplicamos umbralización para convertir los píxeles no negros a blanco
        umbral, img_binaria = cv2.threshold(img_gris, 1, 255, cv2.THRESH_BINARY)

        # Cargar la imagen binaria
        binary_image = img_binaria

        cv2.imwrite("./image_data/binario.png", img_binaria)

        # Invertir los valores de los píxeles de la imagen binaria
        inverted_image = cv2.bitwise_not(binary_image)

        # Cargar la imagen en memoria
        imagencita = Image.open("./image_data/binario.png")

        # Obtener la anchura y la altura de la imagen
        width, height = imagencita.size

        # Crear una nueva imagen para la textura
        texture = Image.new("RGB", (width, height), (0, 128, 0))

        # Iterar sobre cada píxel de la imagen binaria y asignar una textura de hojas verdes o tierra
        for x in range(width):
            for y in range(height):
                # Obtener el valor del píxel
                pixel = imagencita.getpixel((x, y))

                # Asignar una textura de hojas verdes o tierra
                if pixel == 0:
                    texture.putpixel((x, y), (49, 134, 108))  # Hojas verdes
                else:
                    texture.putpixel((x, y), (109, 68, 11))  # Tierra

        # Guardar la textura generada en un archivo
        texture.save("./image_data/textura3.png")

        # Contar el número de píxeles blancos (área de la región no deforestada)
        non_deforested_area = cv2.countNonZero(inverted_image)

        # Calcular el área total de la imagen
        total_area = binary_image.shape[0] * binary_image.shape[1]

        # Calcular el área de la región deforestada
        deforested_area = total_area - non_deforested_area

        # Calcular el área total de la imagen
        total_area = img.shape[0] * img.shape[1]

        # Calcular el porcentaje de área deforestada
        deforested_percent = deforested_area / total_area * 100

        # Calcular el porcentaje de área no deforestada
        non_deforested_percent = non_deforested_area / total_area * 100


        # Calcular el área total de la imagen
        total_area = binary_image.shape[0] * binary_image.shape[1]

        self.imagen(img_segmentada)
        try:
            self.lblinfo1 = customtkinter.CTkLabel(master=self.tabview, text="({:.2f}%)".format(deforested_percent) + " " + "{:.2f}".format(area*deforested_percent) +" km2")
            self.lblinfo1.grid(row=1, column=0)
            self.lblinfo2 = customtkinter.CTkLabel(master=self.tabview, text="({:.2f}%)".format(non_deforested_percent) + " " + "{:.2f}".format(area*non_deforested_percent) +" km2")
            self.lblinfo2.grid(row=4, column=0)
        except NameError:
            self.lblinfo1 = customtkinter.CTkLabel(master=self.tabview, text="{:.2f}%".format(deforested_percent))
            self.lblinfo1.grid(row=1, column=0)
            self.lblinfo2 = customtkinter.CTkLabel(master=self.tabview, text="{:.2f}%".format(non_deforested_percent))
            self.lblinfo2.grid(row=4, column=0)

        
        # # Imprimir los resultados
        # self.seg_button_1.configure(values=["Porcentaje de área", "Área deforestada: {:.2f}%".format(deforested_percent), "Área no deforestada: {:.2f}%".format(non_deforested_percent)])

    area = None
    image = None
    img_segmentada = None
    img_binaria = None
    texture = None

    def imagen(self,imagen):
        # Label donde se presentará la imagen de salida
        # Para visualizar la imagen en lblOutputImage en la GUI
        array = np.array(image)
        h, w, d = array.shape
        print(w)
        if(int(w)>500):
            imagen= imutils.resize(imagen, height=250)
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(imagen)
        img = ImageTk.PhotoImage(image=im)
        self.lblOutputImage.configure(image=img)
        self.lblOutputImage.image = img

    def restart(self):
        self.sidebar_button_3.configure(state="disabled", text="Elegir una opción")
        self.entry.configure(placeholder_text="Imagen Actual")
        self.seg_button_1.configure(state="disabled")
        segemented_button_var = customtkinter.StringVar(value="Segmentado")
        self.seg_button_1.configure(state="disabled",values=["Original", "Segmentado", "Textura 1", "Textura 2"], variable=segemented_button_var, command = self.mostrarImagen)
        self.switch.configure(text="Imagen 3D", state="disabled")

        try:
            self.lblInputImage.destroy()
            self.lblOutputImage.destroy()
            self.lblinfo1.destroy()
            self.lblinfo2.destroy()
        except AttributeError:
            pass
        except ValueError:
            pass

    def Imagen3D(self):
        self.sidebar_button_3.configure(state="disabled", text="Segmentado")
        self.seg_button_1.configure(state="enabled")

        # Cargar imagen
        img = image

        # Convertir imagen a matriz numpy
        imagen = np.array(img)

        # Obtener dimensiones de la imagen
        h, w, d = imagen.shape

        # Crear malla de coordenadas X, Y y Z
        x, y = np.meshgrid(np.arange(w), np.arange(h))
        z = imagen[:,:,0].astype(float) / 255

        # Crear matriz de vértices
        vertices = np.column_stack((x.flatten(), y.flatten(), z.flatten()))

        # Crear matriz de caras
        n_verts = h * w
        rows = np.tile(np.arange(w-1), (h-1,1)) + np.repeat(np.arange(h-1)[:,np.newaxis]*w, w-1, axis=1)
        faces = np.concatenate((np.column_stack((rows.flatten(), rows.flatten()+w, rows.flatten()+w+1)), np.column_stack((rows.flatten(), rows.flatten()+w+1, rows.flatten()+1)))).astype(int)

        # Crear objeto Mesh y guardar en formato .obj
        mesh = meshio.Mesh(points=vertices, cells=[("triangle", faces)])
        meshio.write('./image_data/imagen3d.obj', mesh, file_format='obj')

        # Crear figura y ejes 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Visualizar imagen utilizando la función plot_surface
        surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis', facecolors=plt.cm.viridis(z))

        # Configurar ejes y título
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Imagen en 3D')

        # Agregar barra de colores
        fig.colorbar(surf)

        #Abrir figura en Visor 3D
        os.system("./image_data/imagen3d.obj")

        # Mostrar figura
        plt.show()


if __name__ == "__main__":
    app = App()
    app.iconphoto(False, tkinter.PhotoImage(file='icono.ico'))
    app.mainloop()