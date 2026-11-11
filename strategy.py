from abc import ABC, abstractmethod


class ShippingStrategy(ABC):

    @abstractmethod
    def calculate(self, weight_kg, distance_km):
        pass


# Самовивіз
class PickupStrategy(ShippingStrategy):

    def calculate(self, weight_kg, distance_km):
        return 0


# Звичайна кур'єрська доставка
class CourierStrategy(ShippingStrategy):

    def calculate(self, weight_kg, distance_km):
        base_price = 70
        distance_price = 5 * distance_km
        weight_price = 2.5 * weight_kg

        return base_price + distance_price + weight_price


# Експрес-доставка
class ExpressDeliveryStrategy(ShippingStrategy):

    def calculate(self, weight_kg, distance_km):
        base_price = 150
        distance_price = 10 * distance_km

        total = base_price + distance_price

        if weight_kg > 5:
            total *= 1.3

        return total


# Доставка до поштомата
class PostMachineStrategy(ShippingStrategy):

    def calculate(self, weight_kg, distance_km):
        if weight_kg > 10:
            raise ValueError("Вага посилки не повинна перевищувати 10 кг")

        return 50


# Контекст, який використовує вибрану стратегію
class OrderShippingContext:

    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def calculate_delivery_cost(self, weight_kg, distance_km):
        return self._strategy.calculate(weight_kg, distance_km)


# Демонстрація роботи
if __name__ == "__main__":

    weight = float(input("Введіть вагу посилки (кг): "))
    distance = float(input("Введіть відстань доставки (км): "))

    context = OrderShippingContext(PickupStrategy())

    print("\nОберіть спосіб доставки:")
    print("1 — Самовивіз")
    print("2 — Кур'єрська доставка")
    print("3 — Експрес-доставка")
    print("4 — Доставка до поштомата")

    choice = input("Ваш вибір: ")

    if choice == "1":
        context.set_strategy(PickupStrategy())
    elif choice == "2":
        context.set_strategy(CourierStrategy())
    elif choice == "3":
        context.set_strategy(ExpressDeliveryStrategy())
    elif choice == "4":
        context.set_strategy(PostMachineStrategy())
    else:
        print("Невідомий спосіб доставки")
        exit()

    try:
        cost = context.calculate_delivery_cost(weight, distance)
        print(f"\nВартість доставки: {cost:.2f} грн")
    except ValueError as error:
        print(f"\nПомилка: {error}")