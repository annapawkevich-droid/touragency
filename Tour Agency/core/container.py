from core.validator import SimpleValidator
from services.recommender import StaticRecommendationService
from services.payment_gateway import RandomPaymentGateway
from services.email_service import ConsoleEmailService
from services.booking_repo import InMemoryBookingRepo
from services.booking_service import BookingService

class ServiceContainer:

    def __init__(self):
        self._singletons = {}#словник

    def validator(self): return self._get('validator', SimpleValidator())
    def recommender(self): return self._get('recommender', StaticRecommendationService())
    def payment(self): return self._get('payment', RandomPaymentGateway())
    def email(self): return self._get('email', ConsoleEmailService())
    def repo(self): return self._get('repo', InMemoryBookingRepo())

    def booking_service(self):
        return BookingService(
            validator=self.validator(),
            recommender=self.recommender(),
            payments=self.payment(),
            email=self.email(),
            repo=self.repo()
        )

    def _get(self, name, instance):
        if name not in self._singletons:
            self._singletons[name] = instance
        return self._singletons[name]
