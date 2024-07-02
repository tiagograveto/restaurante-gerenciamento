from PySide6 import QtWidgets, QtCore
from PySide6.QtUiTools import QUiLoader

from modelo import PEDIDOS, ItemStatus

class Administrador:

    timer = QtCore.QTimer()

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
        self._interface.homeButton.clicked.connect(self.aoClicarHomeButton)
        self._interface.moverButton.clicked.connect(lambda x:self._interface.pages.setCurrentWidget(self._interface.page_3))
        self._interface.relatorioButton.clicked.connect(lambda x:self._interface.pages.setCurrentWidget(self._interface.page_2))

    def aoClicarHomeButton(self):
        self._interface.homeButton.clicked.connect(lambda x: self._interface.pages.setCurrentWidget(self._interface.page))
        self.atualizarPagHome()

    def aoClicarMoverButton(self):
        self._interface.moverButton.clicked.connect(lambda x: self._interface.pages.setCurrentWidget(self._interface.page))
    
    def aoClicarRelatorioButton(self):
        self._interface.relatorioButton.clicked.connect(lambda x: self._interface.pages.setCurrentWidget(self._interface.page))


    def getPedidosPorItemStatus(self, itemstatus):
        lista = []
        for i in range(len(PEDIDOS)):
            pedido = PEDIDOS[i]
            if(itemstatus == None):
                lista.append(pedido)

            elif(pedido.get_status() == itemstatus):
                lista.append(pedido)

        return lista

    def atualizarPagHome(self):
        inPreparation = self.getPedidosPorItemStatus(ItemStatus.IN_PREPARATION)
        inDelivered = self.getPedidosPorItemStatus(ItemStatus.DELIVERED)

        self._interface.ordersPreparation.clear()
        self._interface.ordersDelivered.clear()

        for pedido in inPreparation:
            widgetItem = QtWidgets.QListWidgetItem(pedido.get_pedido())
            self._interface.ordersPreparation.addItem(widgetItem)
        
        for pedido in inDelivered:
            widgetItem = QtWidgets.QListWidgetItem(pedido.get_pedido())
            self._interface.ordersDelivered.addItem(widgetItem)