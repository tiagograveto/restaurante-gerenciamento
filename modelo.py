import time
from enum import IntEnum

class ItemStatus(IntEnum):
    WAITING_PAYMENT = 1
    IN_PREPARATION = 2
    DELIVERED = 3


class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.quantity = 1

    def get_price(self):
        return self.price * self.quantity

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity = quantity
    
    def get_name(self):
        return f"{self.name} R${self.price:.2f}"

    def print_item(self):
        print(f"{self.name} R${self.price:.2f}")


class Drink(Item):
    def __init__(self, name, price, size):
        super().__init__(name, price)


class Dessert(Item):
    def __init__(self, name, price, size):
        super().__init__(name, price)


class Side(Item):
    def __init__(self, name, price, size):
        super().__init__(name, price)


class Burger(Item):
    def __init__(self, name, price, size):
        super().__init__(name, price)
        self.size = size


class Combo(Item):
    def __init__(self, name, items, discount):
        super().__init__(name, 0)
        self.items = items
        self.discount = discount
        total = sum(item.get_price() for item in items)
        self.price = total * (1 - discount / 100)

    def get_price(self):
        return self.price
    
    def get_name(self):
        name = f"{self.name} R${self.price:.2f}" + "\n"
        for item in self.items:
            name = name + " ->" + item.get_name() + "\n"

        return name.rstrip()

    def print(self):
        print(f"{self.name} R${self.price:.2f}")
        for item in self.items:
            print(" ->", end="")
            item.print_item()


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
    
    def rem_item(self, item):
        self.items.pop(item)

    def get_total_price(self):
        return sum(item.get_price() for item in self.items)

    def get_items(self):
        return self.items

    def show_cart_items(self):
        if not self.items:
            print("O carrinho está vazio.")
        else:
            print("\nSeu carrinho contém os seguintes items: \n")
            for item in self.items:
                item.print_item()


class Pedido:
    def __init__(self, cart, status):
        self.cart = cart
        self.status = status

    def deliver_items(self):
        self.set_status(ItemStatus.DELIVERED)

    def get_status(self):
        return self.status

    def get_items(self):
        return self.cart.get_items()

    def get_revenue(self):
        return sum(item.get_price() for item in self.cart.get_items())

    def set_status(self, status):
        self.status = status

PEDIDOS = []
MENU = [
        Drink("Água sem gás", 4.90, 500),
        Drink("Água com gás", 4.90, 500),
        Drink("Coca-cola", 4.90, 350),
        Drink("Coca-cola Zero", 4.90, 350),
        Drink("Guaraná", 4.90, 350),
        Burger("Hambúrguer Simples", 34.90, 80),
        Burger("Hambúrger com Bacon", 36.90, 80),
        Burger("Hambúrger com menos sal", 34.90, 80),
        Burger("Hambúrger duplo", 44.90, 160),
        Burger("Hambúrger vegano", 32.90, 70),
        Side("Batata-frita", 14.90, 150),
        Side("Anéis de cebola", 14.90, 200),
        Side("Salada verde", 10.90, 45),
        Dessert("Milkshake Ovomaltine", 24.90, 400),
        Dessert("Brownie", 12.90, 80),
        Dessert("Petit gateau", 29.90, 200),
        Combo("Combo-Mais+", [Drink("Coca-cola", 4.90, 350), Burger("Hambúrguer Simples", 34.90, 80), Side("Batata-frita", 14.90, 150), Dessert("Brownie", 12.90, 80)], 5),
        Combo("Combo-Mais+Premium", [Drink("Guaraná", 4.90, 350), Burger("Hambúrger duplo", 44.90, 160), Side("Anéis de cebola", 14.90, 200), Dessert("Milkshake Ovomaltine", 24.90, 400)], 5),
        Combo("Combo-Vegano", [Drink("Água sem gás", 4.90, 500), Burger("Hambúrger vegano", 32.90, 70), Side("Salada verde", 10.90, 45)], 5),
    ]


def in_preparation_pedidos():
    print("\nEM PREPARO")
    count_pedidos = 0
    for i, pedido in enumerate(PEDIDOS):
        if pedido.get_status() == ItemStatus.IN_PREPARATION:
            print(f"[{i + 1}] \n")
            for item in pedido.get_items():
                item.print_item()
            count_pedidos += 1

    if count_pedidos == 0:
        print("Não há pedidos sendo preparados no momento")


def in_delivered_pedidos():
    print("\nPEDIDOS ENTREGUES")
    count_pedidos = 0
    for i, pedido in enumerate(PEDIDOS):
        if pedido.get_status() == ItemStatus.DELIVERED:
            print(f"[{i + 1}]")
            for item in pedido.get_items():
                item.print_item()
            count_pedidos += 1

    if count_pedidos == 0:
        print("Não há pedidos que foram entregues no momento")


def calculate_revenue():
    return sum(pedido.get_revenue() for pedido in PEDIDOS)


def main():
    menu = -1
    cart = Cart()

    while menu == -1:
        print("\nBem-vindo a hamburgueria Mais+")
        print("\nVocê deseja entrar na opção de: \n(1) Administrador da hamburgueria\n(2) Cliente do estabelecimento\n")
        menu = int(input())

        if menu == 1:
            adm = -1
            while adm == -1:
                print("Bem-vindo Administrador da hamburgueria Mais+")
                print("Você deseja fazer que tipo de ação:\n(1) Ver faturamento de hoje\n(2) Ver pedidos para ser entregues\n(3) Mover status de um pedido")
                print("(4) Voltar para menu principal")
                adm = int(input())

                if adm == 1:
                    print(f"Seu faturamento de hoje é de: R${calculate_revenue():.2f}.\n")
                    adm = -1
                    time.sleep(3)

                elif adm == 2:
                    print("\n--Relatório do dia--\n")
                    in_preparation_pedidos()
                    print("\n")
                    in_delivered_pedidos()
                    adm = -1
                    time.sleep(3)

                elif adm == 3:
                    if not PEDIDOS:
                        print("Não há pedidos para serem movidos para ENTREGUE.")
                        adm = -1
                        time.sleep(2)
                        print()
                    else:
                        adm_1 = -1
                        while adm_1 == -1:
                            for i, pedido in enumerate(PEDIDOS):
                                print(f"({i + 1}) ", end="")
                                for item in pedido.get_items():
                                    item.print_item()
                            print()
                            adm_1 = int(input())
                            if 1 <= adm_1 <= len(PEDIDOS):
                                PEDIDOS[adm_1 - 1].set_status(ItemStatus.DELIVERED)
                                print(f"\nPedido #{adm_1} movido com sucesso para ENTREGUE.\n")
                                adm = -1

                elif adm == 4:
                    menu = -1
                    print()

        elif menu == 2:
            cl = -1
            while cl == -1:
                print("\nBem-vindo à Hamburgueria Mais+")
                print("\nVocê deseja fazer que tipo de ação:\n(1) Adicionar um item ao seu pedido\n(2) Finalizar o pagamento de seu pedido")
                print("(3) Ver seu pedido\n(4) Voltar para menu principal\n")
                cl = int(input())

                if cl == 1:
                    cl_1 = -1
                    while cl_1 == -1:
                        for i, item in enumerate(MENU):
                            print(f"({i + 1}) ", end="")
                            item.print_item()
                        print()
                        cl_1 = int(input())
                        if 1 <= cl_1 <= len(MENU):
                            cart.add_item(MENU[cl_1 - 1])
                            print("\nItem adicionado com sucesso\n")
                            time.sleep(1)
                            cl = -1

                elif cl == 2:
                    cl_2 = -1
                    while cl_2 == -1:
                        print(f"Seu pedido deu um total de R${cart.get_total_price():.2f}\n")
                        print("Qual será a forma de pagamento?\n1. Cartão de Crédito\n2. Cartão de Débito\n3. PIX\n")
                        cl_2 = int(input())

                        if 1 <= cl_2 <= 3:
                            pedido = Pedido(cart, ItemStatus.IN_PREPARATION)
                            PEDIDOS.append(pedido)
                            pedido_id = len(PEDIDOS)
                            cart = Cart()

                            if cl_2 in (1, 2):
                                print("Insira o seu cartão...")
                                time.sleep(3)
                                print("Digite a sua senha...")
                                time.sleep(5)
                                print(f"Pagamento realizado com sucesso!\n Seu pedido é o número #{pedido_id} e vai começar a ser preparado...")
                                time.sleep(2)
                                cl = -1

                            elif cl_2 == 3:
                                print("Estamos gerando o QR-Code para sua compra...")
                                time.sleep(2)
                                print("Código gerado aguardando pagamento...")
                                time.sleep(6)
                                print(f"Pagamento realizado com sucesso!\n Seu pedido é o número #{pedido_id} e vai começar a ser preparado...")
                                time.sleep(2)
                                cl = -1

                elif cl == 3:
                    cart.show_cart_items()
                    time.sleep(2)
                    cl = -1

                elif cl == 4:
                    menu = -1
                    print()
