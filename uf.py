class UF:

    def __init__(self, precio, fecha):
        self._precio = precio
        self._fecha = fecha
    
    @property
    def precio(self):
        return self._precio
    
    @precio.setter
    def precio(self, precio):
        self._precio = precio
    
    @property
    def fecha(self):
        return self._fecha
    
    @fecha.setter
    def fecha(self, fecha):
        self._fecha = fecha
    
    def parsePrecio(self):
        self._precio = float(self._precio.replace('$', '').replace('.', '').replace(',', '.'))