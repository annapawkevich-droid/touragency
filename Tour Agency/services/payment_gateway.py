import random
import uuid #створення унікальних цифр
from models.booking import PaymentInfo

class RandomPaymentGateway:

    def _result(self, method: str, masked: str, amount: int) -> PaymentInfo:
        approved = random.random() >= 0.2 
        return PaymentInfo(
            method=method,
            masked_pan=masked,
            transaction_id=str(uuid.uuid4()),
            approved=approved
        )

    def pay_apple(self, amount_uah: int) -> PaymentInfo:
        return self._result("APPLE_PAY", "APPLE-PAY", amount_uah)

    def pay_card(self, pan: str, expiry: str, cvv: str, amount_uah: int) -> PaymentInfo:
        masked = f"{pan[:6]}******{pan[-4:]}"
        return self._result("CARD", masked, amount_uah)
