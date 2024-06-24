from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader

from modelo import MENU

class Cliente:
    def __init__ (self):
        self._interface :QtWidgets.QWidget = None

    @property
    def interface(self)->QtWidgets.QWidget:
        return self._interface
    
    @interface.setter
    def interface(self, interface: str):
        loader = QUiLoader()
        self._interface = loader.load(interface, None)
        self.carregarConfig()
        self.adicionarItens()
        self._interface.pages.setCurrentIndex(0)
        self._interface.show()
    
    def carregarConfig(self):
        self._interface.mainButton.clicked.connect(lambda x: self._interface.pages.setCurrentWidget(self._interface.cart))
        self._interface.cartButton.clicked.connect(self.aoClicarPagamento)
    
    def adicionarItens(self):
        for i in range(len(MENU)):
            item = MENU[i]
            widgetItem = QtWidgets.QListWidgetItem(item.get_name())
            # Adding data start
            widgetItem.setData(QtCore.Qt.UserRole, i)
            # Adding data stop
            self._interface.menuList.addItem(widgetItem)

        self._interface.menuList.itemClicked.connect(self.aoClicarItemMenu)
        self._interface.cartList.itemClicked.connect(self.aoClicarItemCarrinho)

    def aoClicarItemMenu(self, clickedItem):
        widgetItem = QtWidgets.QListWidgetItem(clickedItem.text())
        menuIndex = clickedItem.data(QtCore.Qt.UserRole)
        # Adding data start
        widgetItem.setData(QtCore.Qt.UserRole, menuIndex)
        print(menuIndex)
        # Adding data stop
        self._interface.cartList.addItem(widgetItem)
        self._interface.total.setText(f"TOTAL: {self.getTotalCarrinho():.2f}")
    
    def aoClicarItemCarrinho(self):
        index = self._interface.cartList.currentRow()
        if index >= 0:
            item = self._interface.cartList.takeItem(index) 
            del item
    
    def getListaDoCarrinho(self):
        lista = []
        for i in range(self._interface.cartList.count()):
            index = self._interface.cartList.item(i).data(QtCore.Qt.UserRole)
            lista.append(MENU[index])

        return lista
    
    def getTotalCarrinho(self):
        lista = self.getListaDoCarrinho()
        return sum(item.get_price() for item in lista)
    
    def aoClicarPagamento(self):
        print(self.getListaDoCarrinho())



        
    



        
        