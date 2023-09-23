from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time

coordenada = input("Ingrese la coordenada: ")
kilometros = float(input("Ingrese los kilometros: "))
kilometros = (kilometros - 0.5) * 1000

web_side = f"https://earth.google.com/web/@{coordenada},500a,{kilometros}d,35y,0h,0t,0r"
path = "chromedriver.exe"

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

print("El area del terreno es: ",area)
driver.execute_script('document.querySelector("body > earth-app").shadowRoot.querySelector("#earth-relative-elements").style.display = "none";')
# Tomar captura de pantalla
driver.get_screenshot_as_file("screenshot.png")

driver.quit()