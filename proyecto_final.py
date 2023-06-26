# Librerías
import time                                             # Para control de pausas
from bs4 import BeautifulSoup                           # Para hermosear HTMLs
from selenium import webdriver                          # Para realizar web scraping
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from itertools import groupby
from operator import itemgetter
from itertools import product
import csv                                              # Para exportar a CSV
import uf
import producto


# Constantes
B_VERBOSE_DEBUG = True                                  # Para debug
B_VERBOSE_RESULT = True                                # Para mostrar resultados de capturas de datos

# Generar archivo HTML de salida
def outputHtml(sFile, lxmlData):
    fOutputHtml = open (sFile,'w')
    fOutputHtml.write(lxmlData.prettify())
    fOutputHtml.close()

def iniciarDriver():
    # Driver y carga de página
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

# Hacer click con espera MÁXIMA. Devuelve True si hizo click
def clickWithWait(nTimeOut, driver, sXpath):
    nTimeInit = time.time()
    nTimeDifference = time.time() - nTimeInit 
    bContinuar = True
    bClickDone = False
    while (nTimeDifference < nTimeOut) and (bContinuar):
        nTimeDifference = time.time() - nTimeInit
        try:
            btnToBeClick = driver.find_element(By.XPATH, sXpath)
            btnToBeClick.click()
            bContinuar = False # Sino se cae la línea anterior es porque ya hizo el click
            bClickDone = True
        except:
            #print(f'error click {nTimeDifference}')
            pass
    return (bClickDone)

# Hacer una pausa MÁXIMA en segundos o hasta que aparezca sXpath
def mySleepUntilObject(nTimeOut, driver, sXpath):
    nTimeInit = time.time()
    nTimeDifference = time.time() - nTimeInit 
    bContinuar = True
    while (nTimeDifference < nTimeOut) and (bContinuar):
        nTimeDifference = time.time() - nTimeInit
        try:
            contentData = driver.find_element(By.XPATH, sXpath)
            bContinuar = False # Sino se cae la línea anterior es porque ya apareció el objeto, por lo que salimos del while de pausa
        except:
            #print('Error en sleep')
            #print('ClassError: {} - NameError: {}'.format(sys.exc_info()[0], sys.exc_info()[1]))
            pass


# Hacer una pausa en segundos para saltarse sleep de Python (le causa problemas al web driver)
def mySleep(nTimeOut):
    nTimeInit = time.time()
    nTimeDifference = time.time() - nTimeInit 
    while (nTimeDifference < nTimeOut):
        nTimeDifference = time.time() - nTimeInit

# Leer archivo de patrones de búsqueda
def listaBusqueda(fname):
    file_path = fname
    file = open(file_path, "r")
    lines = file.readlines()
    file.close()
    
    elements_list = []
    for line in lines:
        elements_list.append(line.strip())

    print(elements_list)
    return elements_list

# Imprimir atributos de un objeto Producto
def printProducto(producto):
    print(producto.patronBusqueda)
    print(producto.multitienda)
    print(producto.descripcion)
    print(producto.precioPesos)
    print(producto.precioUf)

# Obtener el menor precio de un contenedor de precios de Ripley
def menorPrecio(sPrices):
    precio_tarjeta = sPrices.find_all('li', class_='catalog-prices__card-price')
    precio_oferta = sPrices.find_all('li', class_='catalog-prices__offer-price')
    precio_normal = sPrices.find_all('li', class_='catalog-prices__list-price')

    # Revisamos si existe el precio en tarjeta, oferta o normal
    if precio_tarjeta:
        return int(precio_tarjeta[0].text.replace('$', '').replace('.', ''))
    elif precio_oferta:
        return int(precio_oferta[0].text.replace('$', '').replace('.', ''))
    elif precio_normal:
        return int(precio_normal[0].text.replace('$', '').replace('.', ''))
    else:
        return None
    
# Exportar a CSV
def resultadosCsv(listaResultados, nombresColumnas, filename):
  with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(nombresColumnas)
    for objeto in listaResultados:
      fila = [getattr(objeto, columna) for columna in nombresColumnas]
      writer.writerow(fila)

# Parsear HTML con lxml
def lxmlParse(sXpath):
    contentData = driver.find_element(By.XPATH, sXpath)
    htmlData = contentData.get_attribute('innerHTML')
    lxmlData = BeautifulSoup(htmlData, 'lxml')
    return lxmlData

#Función para leer csv usando open csv
def lectura_csv(archivo_csv):
  resultado = []
  with open(archivo_csv, "r") as archivo_csv:
    lector = csv.reader(archivo_csv, delimiter = ";")
    resultado = list(lector)
  return resultado
todosolo = lectura_csv("todosolo.csv")

#----------Funciones-------Auxiliares-----------Para---------PArte-------------4
#Función para tener lista de tiendas unicos
def tiendas_unicos(todosolo):
  tiendas = set(multitiendas[1] for multitiendas in todosolo[1:])#Selecciono solo lo importante, los titulos no
  return list(tiendas) #Función list nos entrega datos no repetidos 

#Función para tener lista de patrones unicos
def patrones_unicos(todosolo):
  patrones = set(patron[0] for patron in todosolo[1:])#Selecciono solo lo importante, los titulos no
  return list(patrones) #Función list nos entrega datos no repetidos 

#Función para obtener los precios 
#Minimo_Patron_tienda
def precioMinimo_Patron_Multitienda(data,patron,tienda):
  #Lista con todos los precios por combinación seleccionada
  preciosUF = (float(precios[4].replace(",",".")) for precios in data[1:] if precios[0] == patron and precios[1] == tienda)
  #Extraemos el minimo
  PMin = min(preciosUF)
  #Extraemos el presio minimo en pesos y UF
  precios_pesos_uf = ((precios[3],precios[4]) for precios in data[1:] if float(precios[4].replace(",",".")) == PMin)
  precios = list(precios_pesos_uf)
  return precios

#Maximo_PAtron_tienda
def precioMaximo_Patron_Multitienda(data,patron,tienda):
  #Lo mismo que el anterior pero con el maximo
  preciosUF = (float(precios[4].replace(",",".")) for precios in data[1:] if precios[0] == patron and precios[1] == tienda)
  PMax = max(preciosUF)
  precios_pesos_uf = ((precios[3],precios[4]) for precios in data[1:] if float(precios[4].replace(",",".")) == PMax)
  precios = list(precios_pesos_uf)
  return precios

#Minimo_Patron
def precioMinimo_Patron(data,patron):
  #Lista con todos los precios por combinación seleccionada
  preciosUF = (float(precios[4].replace(",",".")) for precios in data[1:] if precios[0] == patron)
  #Extraemos el minimo
  PMin = min(preciosUF)
  #Extraemos el presio minimo en pesos y UF
  precios_pesos_uf = ((precios[3],precios[4]) for precios in data[1:] if float(precios[4].replace(",",".")) == PMin)
  precio = list(precios_pesos_uf)
  return precio

#Maximo_Patron
def precioMaximo_Patron(data,patron):
  #Lista con todos los precios por combinación seleccionada
  preciosUF = (float(precios[4].replace(",",".")) for precios in data[1:] if precios[0] == patron)
  #Extraemos el maximo
  PMax = max(preciosUF)
  #Extraemos el presio maximo en pesos y UF
  precios_pesos_uf = ((precios[3],precios[4]) for precios in data[1:] if float(precios[4].replace(",",".")) == PMax)
  precios = list(precios_pesos_uf)
  return precios


#Promedio PATRON Y MULTITIENDA
#UF
def Promedio_Patron_Multitienda_UF(data,patron,tienda):
  precio = (float(precios[4].replace(",",".")) for precios in data[1:] if precios[0] == patron and precios[1] == tienda)
  precios = list(precio)
  suma = sum(precios)
  largo_lista = len(precios)
  promedio = suma/largo_lista
  return promedio

#Pesos
def Promedio_Patron_Multitienda_pesos(data,patron,tienda):
  precio = (float(precios[3].replace(",",".")) for precios in data[1:] if precios[0] == patron and precios[1] == tienda)
  precios = list(precio)
  suma = sum(precios)
  largo_lista = len(precios)
  promedio = suma/largo_lista
  return promedio

#Promedio PATRON
#UF
def Promedio_Patron_UF(data,patron):
  precio = (float(precios[4].replace(",",".")) for precios in data[1:] if precios[0] == patron)
  precios = list(precio)
  suma = sum(precios)
  largo_lista = len(precios)
  promedio = suma/largo_lista
  return promedio

#Pesos
def Promedio_Patron_pesos(data,patron):
  precio = (float(precios[3].replace(",",".")) for precios in data[1:] if precios[0] == patron)
  precios = list(precio)
  suma = sum(precios)
  largo_lista = len(precios)
  promedio = suma/largo_lista
  return promedio

#Combinaciones
def combinaciones_patrones_tiendas(patrones,tiendas):
  Comb_Pat_Tiend = list(product(patrones,tiendas))
  return Comb_Pat_Tiend
#---------------------------FUNCIONES-----PEDIDAS-----EN--------PARTE------------4
#PRECIOS MINIMOS POR PATRON DE BUSQUEDA  Y MULTITIENDA
def Precios_MIN_PATRON_MULT(todosolo):
  #Sacamos todas las combinaciones
  combinaciones=combinaciones_patrones_tiendas(patrones_unicos(todosolo),tiendas_unicos(todosolo))
  #Obtenemos los minimos de las combinaciones
  Precios_minimos = ((fila[0],fila[1],precioMinimo_Patron_Multitienda(todosolo,fila[0],fila[1])[0][0],precioMinimo_Patron_Multitienda(todosolo,fila[0],fila[1])[0][1]) for fila in combinaciones)
  #Lo convertimos en una lista
  lista_precios_minimos = list(Precios_minimos)
  return lista_precios_minimos

#PRECIOS MAXIMOS POR PATRON DE BUSQUEDA  Y MULTITIENDA
def Precios_MAX_PATRON_MULT(todosolo):
  #Este codigo hace lo mismo que el anterior pero para los maximos precios en UF
  combinaciones=combinaciones_patrones_tiendas(patrones_unicos(todosolo),tiendas_unicos(todosolo))
  Precios_maximos = ((fila[0],fila[1],precioMaximo_Patron_Multitienda(todosolo,fila[0],fila[1])[0][0],precioMaximo_Patron_Multitienda(todosolo,fila[0],fila[1])[0][1]) for fila in combinaciones)
  lista_precios_maximos = list(Precios_maximos)
  return lista_precios_maximos

#PRECIOS PROMEDIO POR PATRON DE BUSQUEDA Y MULTITIENDA
def PRECIOS_PROMEDIO_PESOS_UF(todosolo):
  #Este codigo hace lo mismo que el anterior pero para los maximos precios en UF
  combinaciones=combinaciones_patrones_tiendas(patrones_unicos(todosolo),tiendas_unicos(todosolo))
  Precios_promedios = ((fila[0],fila[1],Promedio_Patron_Multitienda_pesos(todosolo,fila[0],fila[1]),Promedio_Patron_Multitienda_UF(todosolo,fila[0],fila[1])) for fila in combinaciones)
  precios_promedios = list(Precios_promedios)
  return precios_promedios

#PRECIOS MINIMOS POR PATRON DE BUSQUEDA
def Precios_MIN_PATRON(todosolo):
  #Sacamos todos los patrones
  patrones=patrones_unicos(todosolo)
  #Obtenemos los minimos de las combinaciones
  Precios_minimos = ((fila,precioMinimo_Patron(todosolo,fila)[0][0],precioMinimo_Patron(todosolo,fila)[0][1]) for fila in patrones)
  #Lo convertimos en una lista
  lista_precios_minimos = list(Precios_minimos)
  return lista_precios_minimos

#PRECIOS MAXIMOS POR PATRON DE BUSQUEDA
def Precios_MAX_PATRON(todosolo):
  #Sacamos todos los patrones
  patrones=patrones_unicos(todosolo)
  #Obtenemos los minimos de las combinaciones
  Precios_maximos = ((fila,precioMaximo_Patron(todosolo,fila)[0][0],precioMaximo_Patron(todosolo,fila)[0][1]) for fila in patrones)
  #Lo convertimos en una lista
  lista_precios_maximos = list(Precios_maximos)
  return lista_precios_maximos

#PRECIOS PROMEDIO POR PATRON DE BUSQUEDA
def PRECIOS_PROMEDIO_PATRONES_PESOS_UF(todosolo):
  #Este codigo hace lo mismo que el anterior pero para los maximos precios en UF
  patrones=patrones_unicos(todosolo)
  Precios_promedios = ((fila,Promedio_Patron_pesos(todosolo,fila),Promedio_Patron_UF(todosolo,fila)) for fila in patrones)
  precios_promedios = list(Precios_promedios)
  return precios_promedios

#Minimo_bulto
def precioMinimo_bulto(data):
  #Lista con todos los precios por combinación seleccionada
  preciosUF = (float(precios[4].replace(",",".")) for precios in data[1:])
  #Extraemos el minimo
  PMin = min(preciosUF)
  #Extraemos el presio minimo en pesos y UF
  precios_pesos_uf = (precios for precios in data[1:] if float(precios[4].replace(",",".")) == PMin)
  precio = list(precios_pesos_uf)
  return precio

#Maximo_bulto
def precioMaximo_bulto(data):
  #Lista con todos los precios por combinación seleccionada
  preciosUF = (float(precios[4].replace(",",".")) for precios in data[1:])
  #Extraemos el maximo
  PMax = max(preciosUF)
  #Extraemos el presio maximo en pesos y UF
  precios_pesos_uf = (precios for precios in data[1:] if float(precios[4].replace(",",".")) == PMax)
  precios = list(precios_pesos_uf)
  return precios

#Función para imprimir las listas
def print_lista(lista):
  for file in lista:
    print(file)
  print("")

if (__name__ == '__main__'):

    # 1: Encontrar el valor de la UF
    # Driver y carga de página
    driver = iniciarDriver()
    driver.get('https://www.bcentral.cl')

    lxmlData = lxmlParse('/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]')

    sTipoCambio= lxmlData.find_all("p", class_= "basic-text fs-2 f-opensans-bold text-center c-blue-nb-2")[0].text
    ufHoy = uf.UF(sTipoCambio, time.strftime("%d/%m/%Y"))

    ufHoy.parsePrecio()
    print(ufHoy.precio)

    # Cierre del driver
    driver.close()
    driver.quit()

    # 2: Lectura del paquete de datos (patrones de búsqueda)
    patronesBusqueda = listaBusqueda("patrones_busqueda.txt")

    # Lista de resultados
    listResult = []

    # 2.1 Falabella
    for S_FIND in patronesBusqueda:

        if (B_VERBOSE_DEBUG):
            print('=' * len('Patrón de búsqueda: {}'.format(S_FIND)))
            print('Patrón de búsqueda: {}'.format(S_FIND))
            print('=' * len('Patrón de búsqueda: {}'.format(S_FIND)))
        
        # Driver y carga de página
        driver = iniciarDriver()
        driver.get('https://www.falabella.com/falabella-cl')
        mySleep(2)

        try:
            # Cierre de ventana emergente
            sXpath = '/html/body/div[4]/div[2]/div/div[1]'
            btnAccept = driver.find_element(By.XPATH, sXpath)
            btnAccept.click()
        except:
            print('No hay ventana emergente')
            pass

        # Ingresar producto en la barra de búsqueda
        inputText = driver.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/div[3]/div/div/input')
        inputText.send_keys(S_FIND)
        inputText.send_keys(Keys.ENTER)
        mySleep(3)

        # Verificar si hay datos
        bOkExistData = False
        try:
            sXpath = '/html/body/div[1]/div/div[2]/div[2]/section[2]/div/div[3]' 
            btnPage1 = driver.find_element(By.XPATH, sXpath)
            bOkExistData = True
            print('Hay datos')
        except: 
            # Si no hay datos, intentamos con otro XPATH
            try:
                sXpath = '/html/body/div[1]/div/div/div[2]/section[2]/div/div[3]' 
                btnPage1 = driver.find_element(By.XPATH, sXpath)
                bOkExistData = True
                print('Hay datos')
            except:
                if (B_VERBOSE_DEBUG):
                    print('No hay datos')   
                pass

        # Iterar en todas las páginas
        nPage = 1
        while (bOkExistData):
            if (B_VERBOSE_DEBUG):
                print('{}: Página {}'.format(S_FIND, nPage))

            # Capturar datos desde el contenedor
            try:
                # Esperamos a que termine de cargar 
                # Luego de carga inicial para primera pasada
                # O luego de páginación para siguientes pasadas
                if (S_FIND == 'impresora 3d'):
                    sXpath = '/html/body/div[1]/div/div/div[2]/section[2]/div/div[3]'
                else:
                    sXpath = '/html/body/div[1]/div/div[2]/div[2]/section[2]/div/div[3]'
                mySleepUntilObject(20, driver, sXpath)
                mySleep(4)

                # Capturamos HTML del contenedor de productos tecnológicos
                if (S_FIND == 'impresora 3d'):
                    sXpath = '/html/body/div[1]/div/div/div[2]/section[2]/div/div[3]'
                else:
                    sXpath = '/html/body/div[1]/div/div[2]/div[2]/section[2]/div/div[3]'

                lmxlData = lxmlParse(sXpath)
                
                
                # Generamos HTML
                outputHtml('falabella_{}_{}.html'.format(S_FIND, nPage), lxmlData)
            
                # Determinamos el tipo de contenedor
                # 0: No reconocido
                # 1: Multiples productos por línea
                # 2: Un producto por línea
                nContentType = 0
                sNames = lxmlData.find_all('div', class_= 'jsx-1833870204 jsx-3831830274 pod-details pod-details-4_GRID has-stickers')

                if len(sNames) > 0:
                    nContentType = 1
                else:
                    sNames = lxmlData.find_all('b', class_= 'jsx-1576191951 title2 primary jsx-2889528833 bold pod-subTitle subTitle-rebrand')
                    if len(sNames) > 0:
                        nContentType = 2
                    else:
                        if (B_VERBOSE_DEBUG):
                            print('Contenedor no reconocido')
                if (B_VERBOSE_DEBUG):
                    print('Tipo contenedor: {}'.format(nContentType))

                # Capturamos datos del contenedor
                if (nContentType == 1):
                    sNames = lxmlData.find_all('div', class_= 'jsx-1833870204 jsx-3831830274 pod-details pod-details-4_GRID has-stickers')
                    sPrices = lxmlData.find_all('a', class_= 'jsx-1833870204 jsx-3831830274 pod-summary pod-link pod-summary-4_GRID')
                elif (nContentType == 2):
                    sNames = lxmlData.find_all('b', class_= 'jsx-1576191951 title2 primary jsx-2889528833 bold pod-subTitle subTitle-rebrand')
                    sPrices = lxmlData.find_all('div', class_= 'jsx-2112733514 prices prices-4_GRID') 

                # Recorremos el contenedor para llenar lista
                for i in range(len(sNames)):
                    # Capturamos según tipo de contenedor
                    if (nContentType == 1):
                        nPrecio = sPrices[i].div.ol.li.div.span.string.replace('$', '').replace(' ', '').replace('.', '')
                        print(int(nPrecio))
                        precioUF = float(nPrecio) / ufHoy.precio
                        miProducto = producto.Producto(S_FIND, "Falabella" ,sNames[i].a.span.b.string, int(nPrecio), precioUF)
                        listResult.append(miProducto)
                    else: # elif (nContentType == 2):
                        nPrecio = sPrices[i].ol.li.div.span.string.replace('$', '').replace(' ', '').replace('.', '')
                        nPrecio = nPrecio.split("-")[0]
                        precioUF = float(nPrecio) / ufHoy.precio
                        miProducto = producto.Producto(S_FIND, "Falabella" ,sNames[i].string, int(nPrecio), precioUF)
                        listResult.append(miProducto)
                    
                    # Imprimimos
                    if (B_VERBOSE_DEBUG):
                        printProducto(miProducto)

                # Capturamos HTML de la botonera de paginación
                '''
                sXpath = '//*[@id="testId-searchResults-actionBar-bottom"]/div[2]'
                contentData = driver.find_element(By.XPATH, sXpath)
                htmlData = contentData.get_attribute('innerHTML')
                lxmlData = BeautifulSoup(htmlData, 'lxml')

                # Generamos HTML
                outputHtml('falabella_{}_{}_buttons.html'.format(S_FIND, nPage), lxmlData)
                '''

                # Dar click a la siguiente página
                try:
                    # Obtenemos botón próxima página, sino se caerá y será capturado en except
                    if (nPage == 1):
                        sXpath = '/html/body/div[1]/div/div/div[2]/section[2]/div/div[1]/div/div[2]/div/div/button'
                    else:
                        sXpath = '/html/body/div[1]/div/div/div[2]/section[2]/div/div[1]/div/div[2]/div/div[2]/button'
                    contentData = driver.find_element(By.XPATH, sXpath)
                    
                    # Intentamos click por espera para próxima página
                    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    bOkExistData = clickWithWait(4, driver, sXpath)

                    # Si retorna en False es porque existe el botón siguiente pero no quedó clickleable
                    if not (bOkExistData):
                        if (B_VERBOSE_DEBUG):
                            print('Reintento con scroll fin + F5')
                        
                        # Hacemos scroll hasta el final y luego F5 para refrescar
                        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        driver.get(driver.current_url)

                        # Intentamos NUEVAMENTE click por espera para próxima página
                        bOkExistData = clickWithWait(4, driver, sXpath)
                        if not (bOkExistData):
                            if (B_VERBOSE_DEBUG):
                                print('No se logró hacer click a la siguiente página')  
                except:
                    if (B_VERBOSE_DEBUG):
                        print('No hay más páginas de información')
                        #print('ClassError: {} - NameError: {}'.format(sys.exc_info()[0], sys.exc_info()[1]))
                    bOkExistData = False          
            except:
                if (B_VERBOSE_DEBUG):
                    print('Caída al capturar contenedor')
                    #print('ClassError: {} - NameError: {}'.format(sys.exc_info()[0], sys.exc_info()[1]))
                bOkExistData = False

            # Incrementamos página
            nPage = nPage + 1
    
    # Cierre del driver
    driver.close()
    driver.quit()

    # Imprimir capturas de datos
    if (B_VERBOSE_RESULT):
        print('=' * len('Lista total:'))
        print('Lista total:')       
        print('=' * len('Lista total:'))
        #print(*listResult, sep='\n')
        [print('"{}";"{}";{}'.format(item.patronBusqueda, item.descripcion, item.precioPesos)) for item in listResult]
    
    # Proceso finalizado
    if (B_VERBOSE_DEBUG):
        print('Proceso Falabella finalizado')

    # 2.2 Búsqueda en Ripley
    for S_FIND in patronesBusqueda:

        if (B_VERBOSE_DEBUG):
            print('=' * len('Patrón de búsqueda: {}'.format(S_FIND)))
            print('Patrón de búsqueda: {}'.format(S_FIND))
            print('=' * len('Patrón de búsqueda: {}'.format(S_FIND)))
        
        # Driver y carga de página
        driver = iniciarDriver()
        driver.get('https://simple.ripley.cl/')
        mySleep(2)

        # Ingresar producto en la barra de búsqueda
        inputText = driver.find_element(By.XPATH, '/html/body/div[5]/header/section/nav/ul/li[1]/div/div[1]/input')
        inputText.send_keys(S_FIND)
        inputText.send_keys(Keys.ENTER)
        mySleep(3)

        # Verificar si hay datos
        bOkExistData = False
        try:
            sXpath = '/html/body/div[9]/div[2]/div/div[2]/div[3]/section/div/div' 
            btnPage1 = driver.find_element(By.XPATH, sXpath)
            bOkExistData = True
            print('Hay datos')
        except: 
            print('No hay datos')
            pass

        # Iterar en todas las páginas
        nPage = 1
        while (bOkExistData):
            if (B_VERBOSE_DEBUG):
                print('{}: Página {}'.format(S_FIND, nPage))

            # Capturar datos desde el contenedor
            try:
                # Esperamos a que termine de cargar 
                # Luego de carga inicial para primera pasada
                # O luego de páginación para siguientes pasadas
                sXpath = '/html/body/div[9]/div[2]/div/div[2]/div[3]/section/div/div'
                mySleepUntilObject(20, driver, sXpath)
                mySleep(4)

                # Capturamos HTML del contenedor de productos tecnológicos
                sXpath = '/html/body/div[9]/div[2]/div/div[2]/div[3]/section/div/div'
                lmxlData = lxmlParse(sXpath)

                # Capturamos datos del contenedor
                sNames = lxmlData.find_all('div', class_= 'catalog-product-details__name')
                sPrices = lxmlData.find_all('div', class_ = 'catalog-product-details__prices')
                # Recorremos el contenedor para llenar lista
                for i in range(len(sNames)):
                    nPrecio = menorPrecio(sPrices[i])
                    print(nPrecio)
                    precioUF = float(nPrecio) / ufHoy.precio
                    miProducto = producto.Producto(S_FIND, "Ripley" ,sNames[i].string, nPrecio, precioUF)
                    listResult.append(miProducto)                    
                    # Imprimimos
                    if (B_VERBOSE_DEBUG):
                        printProducto(miProducto)
                
                # Dar click a la siguiente página
                # Obtenemos botón próxima página, sino se caerá y será capturado en except
                if (S_FIND == 'notebook hp'):
                    link_element = driver.find_element(By.XPATH, '/html/body/div[9]/div[2]/div/div[2]/div[4]/nav/ul/li[5]/a')
                    link_url = link_element.get_attribute('href')
                    # Aplicar esta solución al resto de los casos.
                    if link_url == driver.current_url + "#":
                        print('No hay más páginas')
                        bOkExistData = False      
                    driver.get(link_url)              
                if (S_FIND == 'impresora 3d'):
                    link_element = driver.find_element(By.XPATH,'/html/body/div[9]/div[2]/div/div[2]/div[4]/nav/ul/li[13]/a')
                    link_url = link_element.get_attribute('href')
                    if link_url == driver.current_url + "#":
                        print('No hay más páginas')
                        bOkExistData = False
                    driver.get(link_url)
                if (S_FIND == 'tablet samsung'):
                    link_element = driver.find_element(By.XPATH,'/html/body/div[9]/div[2]/div/div[2]/div[4]/nav/ul/li[3]/a')
                    link_url = link_element.get_attribute('href')
                    if link_url == driver.current_url + "#":
                        print('No hay más páginas')
                        bOkExistData = False                                     
            except:
                if (B_VERBOSE_DEBUG):
                    print('Caída al capturar contenedor')
                    #print('ClassError: {} - NameError: {}'.format(sys.exc_info()[0], sys.exc_info()[1]))
                bOkExistData = False

            # Incrementamos página
            nPage = nPage + 1

    # Cierre del driver
    driver.close()
    driver.quit()

    # Imprimir capturas de datos
    if (B_VERBOSE_RESULT):
        print('=' * len('Lista total:'))
        print('Lista total:')       
        print('=' * len('Lista total:'))
        #print(*listResult, sep='\n')
        [print('"{}";"{}";{}'.format(item.patronBusqueda, item.descripcion, item.precioPesos)) for item in listResult]
    
    # Proceso finalizado
    if (B_VERBOSE_DEBUG):
        print('Proceso Ripley finalizado')

    # 3: Exportar a CSV
    resultadosCsv(listResult, ['patronBusqueda', 'multitienda', 'descripcion', 'precioPesos', 'precioUf'], 'todosolo.csv')

    # 4: Obtener los precios mínimos, máximos y promedios por patrón de búsqueda y multitienda
    Minimos_PAT_MULT =Precios_MIN_PATRON_MULT(todosolo)
    Maximos_PAT_MULT =Precios_MAX_PATRON_MULT(todosolo)
    Promedios_PAT_MULT = PRECIOS_PROMEDIO_PESOS_UF(todosolo)
    Minimos_PAT = Precios_MIN_PATRON(todosolo)
    Maximos_PAT = Precios_MAX_PATRON(todosolo)
    Promedios_PAT = PRECIOS_PROMEDIO_PATRONES_PESOS_UF(todosolo)
    Minimo_Bulto = precioMinimo_bulto(todosolo)
    Maximo_Bulto = precioMaximo_bulto(todosolo)


    print("PRECIOS MINIMOS POR PATRON Y BUSQUEDA")
    print_lista(Minimos_PAT_MULT)
    
    print("PRECIOS MAXIMOS POR PATRON Y BUSQUEDA")
    print_lista(Maximos_PAT_MULT)

    print("PROMEDIO DE PRECIOS POR PATRON Y BUSQUEDA EN UF Y PESOS") 
    print_lista(Promedios_PAT_MULT)

    print("PRECIOS MINIMOS POR PATRON")
    print_lista(Minimos_PAT)

    print("PRECIOS MAXIMOS POR PATRON")
    print_lista(Maximos_PAT)

    print("PROMEDIO DE PRECIOS POR PATRON EN UF Y PESOS") 
    print_lista(Promedios_PAT)

    print("PRECIOS MINIMOS BULTO")
    print_lista(Minimo_Bulto)

    print("PRECIOS MAXIMOS BULTO")
    print_lista(Maximo_Bulto)
        
