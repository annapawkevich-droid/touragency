class ConsoleEmailService:

    def send_booking(self, to_email: str, booking):
        print("\n—— Лист надіслано ——")
        print(f"До: {to_email}")
        print(f"Тема: Підтвердження бронювання №{booking.booking_id}")
        if booking.payment.approved:
            print("✅ Оплату підтверджено.")
        else:
            print("❌ Оплата не пройшла, бронювання очікує підтвердження.")
        print(f"Курорт: {booking.resort.name}, {booking.resort.country}")
        print(f"Готель: {booking.hotel.name} ({booking.hotel.stars}⭐)")
        print(f"Рейс: {booking.flight.from_city} → {booking.flight.to_city}")
        print("Документи надіслані на електронну адресу.")
        print("——————————————\n")
