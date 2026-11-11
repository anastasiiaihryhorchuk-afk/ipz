from abc import ABC, abstractmethod


# Спільний інтерфейс для всіх платіжних систем
class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, account_identifier, amount):
        pass


# Внутрішня банківська система
class InternalBankGateway:

    def process_payment(self, account_number, amount):
        print(
            f"Оплата через внутрішній банк: "
            f"{amount:.2f} грн з рахунку {account_number}"
        )
        return True


# Адаптер для внутрішнього банку
class InternalBankProcessor(PaymentProcessor):

    def __init__(self):
        self.gateway = InternalBankGateway()

    def pay(self, account_identifier, amount):
        return self.gateway.process_payment(
            account_identifier,
            amount
        )


# Стороння платіжна система GlobalPay
class GlobalPaySDK:

    def charge_customer(self, user_email, cents_amount, currency):
        print(
            f"Оплата через GlobalPay: "
            f"{cents_amount} коп., валюта {currency}, "
            f"користувач {user_email}"
        )

        return {"status": "SUCCESS"}


# Адаптер для GlobalPay
class GlobalPayAdapter(PaymentProcessor):

    def __init__(self):
        self.sdk = GlobalPaySDK()

    def pay(self, account_identifier, amount):
        cents_amount = int(round(amount * 100))

        result = self.sdk.charge_customer(
            user_email=account_identifier,
            cents_amount=cents_amount,
            currency="UAH"
        )

        return result["status"] == "SUCCESS"


# Стороння система оплати через криптовалюту
class CryptoPayService:

    def send_crypto_invoice(self, wallet_address, uah_sum):
        print(
            f"Створено криптовалютний рахунок: "
            f"{uah_sum:.2f} грн для гаманця {wallet_address}"
        )

        return "OK"


# Адаптер для CryptoPay
class CryptoPayAdapter(PaymentProcessor):

    def __init__(self):
        self.service = CryptoPayService()

    def pay(self, account_identifier, amount):
        result = self.service.send_crypto_invoice(
            wallet_address=account_identifier,
            uah_sum=amount
        )

        return result == "OK"


# Сервіс оформлення замовлення
class CheckoutService:

    def __init__(self, payment_processor):
        self.payment_processor = payment_processor

    def checkout(self, account_identifier, amount):
        result = self.payment_processor.pay(
            account_identifier,
            amount
        )

        if result:
            print("Оплату успішно виконано!")
        else:
            print("Не вдалося виконати оплату.")

        return result


# Демонстрація роботи
if __name__ == "__main__":

    print("Оберіть платіжну систему:")
    print("1 — Внутрішній банк")
    print("2 — GlobalPay")
    print("3 — CryptoPay")

    choice = input("Ваш вибір: ")

    account = input("Введіть номер рахунку, email або адресу гаманця: ")
    amount = float(input("Введіть суму оплати (грн): "))

    if choice == "1":
        processor = InternalBankProcessor()
    elif choice == "2":
        processor = GlobalPayAdapter()
    elif choice == "3":
        processor = CryptoPayAdapter()
    else:
        print("Невідома платіжна система")
        exit()

    checkout_service = CheckoutService(processor)
    checkout_service.checkout(account, amount)