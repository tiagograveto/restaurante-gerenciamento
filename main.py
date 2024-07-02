from PySide6 import QtWidgets

from cliente import Cliente
from administrador import Administrador

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    adm = Administrador()
    adm.interface  = "administrador.ui"

    clt = Cliente()
    clt.interface = "cliente.ui"
    
    app.exec()