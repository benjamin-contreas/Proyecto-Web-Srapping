# Librerías
import time                                             # Para control de pausas
from bs4 import BeautifulSoup                           # Para hermosear HTMLs
from selenium import webdriver                          # Para realizar web scraping
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

def printProducto(producto):
    print(producto.patronBusqueda)
    print(producto.multitienda)
    print(producto.descripcion)
    print(producto.precioPesos)
    print(producto.precioUf)

def menorPrecio(sPrices):
    # Find all the price elements within sPrices
    precio_tarjeta = sPrices.find_all('li', class_='catalog-prices__card-price')
    precio_oferta = sPrices.find_all('li', class_='catalog-prices__offer-price')
    precio_normal = sPrices.find_all('li', class_='catalog-prices__list-price')

    # Check if any price elements are found and extract the lowest price
    if precio_tarjeta:
        return int(precio_tarjeta[0].text.replace('$', '').replace('.', ''))
    elif precio_oferta:
        return int(precio_oferta[0].text.replace('$', '').replace('.', ''))
    elif precio_normal:
        return int(precio_normal[0].text.replace('$', '').replace('.', ''))
    else:
        return None  # Return None if no prices are found




if (__name__ == '__main__'):

    # 1: Encontrar el valor de la UF
    # Driver y carga de página
    driver = iniciarDriver()
    driver.get('https://www.bcentral.cl')

    weUFContent = driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[1]/section/div/div[2]/div/div/div/div/div[1]/div/div')
    htmlData = weUFContent.get_attribute('innerHTML')
    lxmlData = BeautifulSoup(htmlData, 'lxml')

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

    # 2.2 Ripley
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

        if (bOkExistData):
            try:
                mySleep(2)
                sXpath = '/html/body/div[9]/div[2]/div/div[2]/div[3]/section/div/div' 
                contentData = driver.find_element(By.XPATH, sXpath)
                htmlData = contentData.get_attribute('innerHTML')
                lxmlData = BeautifulSoup(htmlData, 'lxml')
                outputHtml('ripley.html', lxmlData)
            except:
                print("No hay mas paginas")

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
                contentData = driver.find_element(By.XPATH, sXpath)
                htmlData = contentData.get_attribute('innerHTML')
                lxmlData = BeautifulSoup(htmlData, 'lxml')

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
                
            except:
                if (B_VERBOSE_DEBUG):
                    print('Caída al capturar contenedor')
                    #print('ClassError: {} - NameError: {}'.format(sys.exc_info()[0], sys.exc_info()[1]))
                bOkExistData = False

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
        print('Proceso finalizado')