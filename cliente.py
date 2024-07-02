from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QPropertyAnimation, QEasingCurve

from modelo import MENU, Drink, Burger, Side, Dessert, Combo, Cart, Pedido, ItemStatus, PEDIDOS

class Cliente:

    cart = Cart()

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
        self.resetar()
        self._interface.show()
    
    def carregarConfig(self):
        self._interface.mainButton.clicked.connect(lambda x: self._interface.pages.setCurrentWidget(self._interface.cart))
        self._interface.cartButton.clicked.connect(self.aoClicarPagamento)
        self._interface.menuList.itemClicked.connect(self.aoClicarItemMenu)
        self._interface.cartList.itemClicked.connect(self.aoClicarItemCarrinho)
        self._interface.burgerButton.clicked.connect(lambda x: self.adicionarPorCategoria(Burger))
        self._interface.sidesButton.clicked.connect(lambda x: self.adicionarPorCategoria(Side))
        self._interface.showAllButton.clicked.connect(lambda x: self.adicionarPorCategoria(None))
        self._interface.dessertButton.clicked.connect(lambda x: self.adicionarPorCategoria(Dessert))
        self._interface.drinkButton.clicked.connect(lambda x: self.adicionarPorCategoria(Drink))
        self._interface.comboButton.clicked.connect(lambda x: self.adicionarPorCategoria(Combo))

        self._interface.creditButton.clicked.connect(self.aoClicarMetodo)
        self._interface.debitButton.clicked.connect(self.aoClicarMetodo)
        self._interface.pixButton.clicked.connect(self.aoClicarMetodo)

    def adicionarPorCategoria(self, category):
        lista = []
        if (category == Drink):
            lista = [i for i in MENU if isinstance(i, Drink)]
        elif (category == Burger):
            lista = [i for i in MENU if isinstance(i, Burger)]
        elif (category == Side):
            lista = [i for i in MENU if isinstance(i, Side)]
        elif (category == Dessert):
            lista = [i for i in MENU if isinstance(i, Dessert)]
        elif (category == Combo):
            lista = [i for i in MENU if isinstance(i, Combo)]
        else:
            lista = MENU

        self._interface.menuList.clear()
        for i in range(len(lista)):
            item = lista[i]
            widgetItem = QtWidgets.QListWidgetItem(item.get_name())
            # Adding data start
            widgetItem.setData(QtCore.Qt.UserRole, MENU.index(item))
            # Adding data stop
            self._interface.menuList.addItem(widgetItem)

    def aoClicarItemMenu(self, clickedItem):
        widgetItem = QtWidgets.QListWidgetItem(clickedItem.text())
        menuIndex = clickedItem.data(QtCore.Qt.UserRole)
        self._interface.cartList.addItem(widgetItem)
        self.cart.add_item(MENU[menuIndex])
        self._interface.total.setText(f"TOTAL: {self.cart.get_total_price():.2f}")
    
    def aoClicarItemCarrinho(self):
        index = self._interface.cartList.currentRow()
        if index >= 0:
            item = self._interface.cartList.takeItem(index)
            self.cart.rem_item(index)
            self._interface.total.setText(f"TOTAL: {self.cart.get_total_price():.2f}")
            del item
    
    def aoClicarPagamento(self):
        total = self.cart.get_total_price()
        if(total == 0):
            warning = QMessageBox(self._interface)
            warning.setText("O seu carrinho está vazio")
            warning.setWindowTitle("Mais+")
            warning.setIcon(QMessageBox.Warning)
            warning.exec_()
        else:
            self._interface.pages.setCurrentWidget(self._interface.payment)
            self._interface.total_2.setText(f"TOTAL: {total:.2f}")
            lista = self.cart.get_items()
            for i in range(len(lista)):
                item = lista[i]
                widgetItem = QtWidgets.QListWidgetItem(item.get_name())
                self._interface.paymentList.addItem(widgetItem)
    
    def aoClicarMetodo(self):
        self._interface.animation = QPropertyAnimation(self._interface.progress_bar, b"value", self._interface.progress_bar)
        self._interface.animation.setDuration(10000)
        self._interface.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._interface.animation.setStartValue(0)
        self._interface.animation.setEndValue(100)
        self._interface.animation.start()
        self._interface.animation.finished.connect(self.enviarPedido)

        self._interface.creditButton.setEnabled(False)
        self._interface.debitButton.setEnabled(False)
        self._interface.pixButton.setEnabled(False)

        self._interface.paymentInfo.setText(f"Siga as instruções na maquininha para \nproceder com o pagamento")
    
    def enviarPedido(self):
        pedido = Pedido(self.cart, ItemStatus.IN_PREPARATION)
        PEDIDOS.append(pedido)
        self._interface.pages.setCurrentWidget(self._interface.order)
        self._interface.orderId.setText(f"#{PEDIDOS.index(pedido) + 1}")
        QtCore.QTimer.singleShot(10 * 1000, self.resetar)
        

    def resetar(self):
        self._interface.pages.setCurrentWidget(self._interface.mainpage)
        self._interface.cartList.clear()
        self.adicionarPorCategoria(None)
        self._interface.paymentList.clear()
        self._interface.total.setText(f"TOTAL: ")
        self._interface.total_2.setText(f"TOTAL: ")
        self._interface.progress_bar.setValue(0)
        self._interface.paymentInfo.setText("")
        self._interface.orderId.setText("")
        self.cart = Cart()

            

            




        
    



        
        