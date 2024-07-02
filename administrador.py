from PySide6 import QtWidgets, QtCore
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox

from modelo import PEDIDOS, ItemStatus

class Administrador:

    pedidoToDeliver = []

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
        self._interface.moverButton.clicked.connect(self.aoClicarMoverButton)
        self._interface.relatorioButton.clicked.connect(lambda x:self._interface.pages.setCurrentWidget(self._interface.page_2))

        self._interface.ordersDelivered2.itemClicked.connect(self.aoClicarItemDelivered)
        self._interface.ordersPreparation2.itemClicked.connect(self.aoClicarItemPreparation)
        self._interface.deliverButton.clicked.connect(self.aoClicarDeliveredButton)

    def aoClicarHomeButton(self):
        self._interface.homeButton.clicked.connect(lambda x: self._interface.pages.setCurrentWidget(self._interface.page))
        self.atualizarPagHome()

    def aoClicarMoverButton(self):
        self._interface.moverButton.clicked.connect(lambda x: self._interface.pages.setCurrentWidget(self._interface.page_3))
        self.atualizarPagMover()
    
    def aoClicarRelatorioButton(self):
        self._interface.relatorioButton.clicked.connect(lambda x: self._interface.pages.setCurrentWidget(self._interface.page_2))


    def getPedidosPorItemStatus(self, itemstatus):
        lista = []
        for i in range(len(PEDIDOS)):
            pedido = PEDIDOS[i]
            if(itemstatus == None):
                lista.append(pedido)

            elif(pedido.get_status() == itemstatus):
                lista.append(pedido)

        return lista

    def atualizarPagMover(self):
        inPreparation = self.getPedidosPorItemStatus(ItemStatus.IN_PREPARATION)
        self._interface.ordersPreparation2.clear()
        self._interface.ordersDelivered2.clear()

        for pedido in inPreparation:
            widgetItem = QtWidgets.QListWidgetItem(pedido.get_pedido())
            widgetItem.setData(QtCore.Qt.UserRole, PEDIDOS.index(pedido))
            self._interface.ordersPreparation2.addItem(widgetItem)

    def aoClicarItemPreparation(self, clickedItem):
        widgetItem = QtWidgets.QListWidgetItem(clickedItem.text())
        pedidoIndex = clickedItem.data(QtCore.Qt.UserRole)
        self.pedidoToDeliver.append(pedidoIndex)
        self._interface.ordersDelivered2.addItem(widgetItem)
    
    def aoClicarItemDelivered(self):
        index = self._interface.ordersDelivered2.currentRow()
        if index >= 0:
            item = self._interface.ordersDelivered2.takeItem(index)
            self.pedidoToDeliver.pop(index)
            del item
    
    def aoClicarDeliveredButton(self):
        pedidosToDeliver = self.pedidoToDeliver
        if(pedidosToDeliver == []):
            warning = QMessageBox(self._interface)
            warning.setText("Você não tem nenhum pedido para ser movido")
            warning.setWindowTitle("Mais+")
            warning.setIcon(QMessageBox.Warning)
            warning.exec_()
        else:
            for i in range(len(pedidosToDeliver)):
                PEDIDOS[i].deliver_items()

            self.atualizarPagMover()

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