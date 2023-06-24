class Producto:
    def __init__(self, patronBusqueda, multitienda, descripcion, precioPesos, precioUf):
        self._patronBusqueda = patronBusqueda
        self._multitienda = multitienda
        self._descripcion = descripcion
        self._precioPesos = precioPesos
        self._precioUf = precioUf
    
    @property
    def patronBusqueda(self):
        return self._patronBusqueda
    
    @patronBusqueda.setter
    def patronBusqueda(self, patronBusqueda):
        self._patronBusqueda = patronBusqueda

    @property
    def multitienda(self):
        return self._multitienda
    
    @multitienda.setter
    def multitienda(self, multitienda):
        self._multitienda = multitienda
    
    @property
    def descripcion(self):
        return self._descripcion
    
    @descripcion.setter
    def descripcion(self, descripcion):
        self._descripcion = descripcion
    
    @property
    def precioPesos(self):
        return self._precioPesos
    
    @precioPesos.setter
    def precioPesos(self, precioPesos):
        self._precioPesos = precioPesos

    @property
    def precioUf(self):
        return self._precioUf
    
    @precioUf.setter
    def precioUf(self, precioUf):
        self._precioUf = precioUf