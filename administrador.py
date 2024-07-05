from PySide6 import QtWidgets, QtCore
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox

from modelo import PEDIDOS, ItemStatus

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts, True)


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
        self._interface.relatorioButton.clicked.connect(self.aoClicarRelatorioButton)

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
        self.atualizarPagRelatorio()


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
        index = self._interface.ordersPreparation2.row(clickedItem)
        self._interface.ordersPreparation2.takeItem(index)

    
    def aoClicarItemDelivered(self):
        index = self._interface.ordersDelivered2.currentRow()
        if index >= 0:
            itemText = self._interface.ordersDelivered2.item(index).text()
            itemData = self._interface.ordersDelivered2.item(index).data(QtCore.Qt.UserRole)

            item = self._interface.ordersDelivered2.takeItem(index)
            
            newItem = QtWidgets.QListWidgetItem(itemText)
            newItem.setData(QtCore.Qt.UserRole, itemData)

            self._interface.ordersPreparation2.addItem(newItem)
            
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
            
            self.pedidoToDeliver.clear()
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


    def atualizarPagRelatorio(self):

        sold_items = self.getPedidosPorItemStatus(None)

        item_counts = {}
        for pedido in sold_items:
            for item in pedido.get_items():
                item_name = item.get_name()  
                if item_name in item_counts:
                    item_counts[item_name] += 1
                else:
                    item_counts[item_name] = 1

        self._interface.listWidget.clear()

        for item_name, count in item_counts.items():
            widgetItem = QtWidgets.QListWidgetItem(f"{item_name} - {count}")
            self._interface.listWidget.addItem(widgetItem)
            self.atualizarFaturamento()
            self.atulizarDeliveredItems()
           

    def atualizarFaturamento(self):
        
        sold_items = self.getPedidosPorItemStatus(None)

        total = 0
        for pedido in sold_items:
            for item in pedido.get_items():
                total += item.get_price()

        self._interface.label_7.setText(f"R$ {total:.2f}")

    def atulizarDeliveredItems(self):
        delivered_items = self.getPedidosPorItemStatus(ItemStatus.DELIVERED)

        count_delivered = 0
        for pedido in delivered_items:
            count_delivered += 1

        self._interface.label_6.setText(f"{count_delivered}")

            