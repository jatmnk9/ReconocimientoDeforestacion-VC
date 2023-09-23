from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import numpy as np

def elegir_imagen():
    # Especificar los tipos de archivos, para elegir solo a las imágenes
    path_image = filedialog.askopenfilename(filetypes = [
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg")])

    if len(path_image) > 0:
        global image

        # Leer la imagen de entrada y la redimensionamos
        image = cv2.imread(path_image)
        image= imutils.resize(image, height=380)

        # Para visualizar la imagen de entrada en la GUI
        imageToShow= imutils.resize(image, width=180)
        imageToShow = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(imageToShow )
        img = ImageTk.PhotoImage(image=im)

        lblInputImage.configure(image=img)
        lblInputImage.image = img

        # Label IMAGEN DE ENTRADA
        lblInfo1 = Label(root, text="IMAGEN DE ENTRADA:")
        lblInfo1.grid(column=0, row=1, padx=5, pady=5)

        # Al momento que leemos la imagen de entrada, vaciamos
        # la iamgen de salida y se limpia la selección de los
        # radiobutton
        # lblOutputImage.image = ""
        # selected.set(0)

        # Label ¿Qué color te gustaría resaltar?
        lblInfo2 = Label(root, text="Calcular deforestación", width=25)
        lblInfo2.grid(column=0, row=3, padx=5, pady=5)

        rad1 = Radiobutton(root, text='Segmentar imagen', width=25,value=1, variable=selected, command= deteccion_color)
        rad1.grid(column=0, row=4)

def deteccion_color():
    global image
    if selected.get() == 1:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Aplicar un filtro gaussiano para reducir el ruido
        blur = cv2.GaussianBlur(gray, (5,5), 0)

        # Aplicar un umbral adaptativo para separar las regiones de la imagen
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        cv2.imwrite('./image_data/imagen.jpg', thresh)

        #  Carga la imagen
        binary_image = cv2.imread('./image_data/imagen.jpg', cv2.IMREAD_GRAYSCALE)

        contador=0
        sumar_area_no_deforestada = 0

        # Divide la imagen en cuadrantes
        rows, cols = binary_image.shape
        n = 2 # Cantidad de cuadrantes en cada dirección
        size_r = rows // n
        size_c = cols // n

        for i in range(n):
            for j in range(n):
                contador+=1
                # Recorta el cuadrante correspondiente
                roi = binary_image[i*size_r:(i+1)*size_r, j*size_c:(j+1)*size_c]

                # Aplica la ecualización del histograma
                eq_roi = cv2.equalizeHist(roi)

                # Guarda el cuadrante como una imagen separada
                cv2.imwrite(f"./image_data/imagen{contador}.png", eq_roi)


        i=1
        while i<=4:
        
            img = cv2.imread(f'./image_data/imagen{i}.png', cv2.IMREAD_GRAYSCALE)

            # Invertir los valores de los píxeles de la imagen binaria
            inverted_image = cv2.bitwise_not(img)

            # Contar el número de píxeles blancos (área de la región no deforestada)

            non_deforested_area = cv2.countNonZero(inverted_image)

            print(non_deforested_area)

            sumar_area_no_deforestada += non_deforested_area
            i+=1

        # Calcular el área total de la imagen
        total_area = binary_image.shape[0] * binary_image.shape[1]

        # Imprimir los resultados
        lblInfo = Label(root, text="Porcentaje de deforestación", width=25)
        lblInfo.grid(column=0, row=5)
        lblInfoDef = Label(root, text="% Área deforestada: " + str(round((total_area - sumar_area_no_deforestada)*100/total_area, 2)), width=25)
        lblInfoDef.grid(column=0, row=6)
        lblInfoNoDef = Label(root, text="% Área no deforestada: " + str(round(sumar_area_no_deforestada*100/total_area, 2)), width=25)
        lblInfoNoDef.grid(column=0, row=7)

    # Para visualizar la imagen en lblOutputImage en la GUI
    im = Image.fromarray(thresh)
    img = ImageTk.PhotoImage(image=im)
    lblOutputImage.configure(image=img)
    lblOutputImage.image = img
    # Label IMAGEN DE SALIDA
    lblInfo3 = Label(root, text="IMAGEN DE SALIDA:", font="bold")
    lblInfo3.grid(column=1, row=0, padx=5, pady=5)

image = None

# Creamos la ventana principal
root = Tk()

# Label donde se presentará la imagen de entrada
lblInputImage = Label(root)
lblInputImage.grid(column=0, row=2)

# Label donde se presentará la imagen de salida
lblOutputImage = Label(root)
lblOutputImage.grid(column=1, row=1, rowspan=6)

# Creamos los radio buttons y la ubicación que estos ocuparán
selected = IntVar()

# Creamos el botón para elegir la imagen de entrada
btn = Button(root, text="Elegir imagen", width=25, command=elegir_imagen)
btn.grid(column=0, row=0, padx=5, pady=5)

root.mainloop()