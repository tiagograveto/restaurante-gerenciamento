from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader

from modelo import PEDIDOS

class Administrador:
    def __init__ (self):
        self._interface :QtWidgets.QWidget = None

    @property
    def interface(self)->QtWidgets.QWidget:
        return self._interface
    
    @interface.setter
    def interface(self, interface: str):
        loader = QUiLoader()
        self._interface = loader.load(interface, None)
        self.carregarBotoes()
        self._interface.pages.setCurrentIndex(0)
        self._interface.show()
    
    def carregarBotoes(self):
        self._interface.homeButton.clicked.connect(lambda x: self._interface.pages.setCurrentWidget(self._interface.page))
        self._interface.moverButton.clicked.connect(lambda x:self._interface.pages.setCurrentWidget(self._interface.page_3))
        self._interface.relatorioButton.clicked.connect(lambda x:self._interface.pages.setCurrentWidget(self._interface.page_2))