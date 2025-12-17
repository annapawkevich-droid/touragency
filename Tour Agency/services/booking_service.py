import uuid, random
from datetime import datetime, date, timedelta
from models.client import Client, Traveler
from models.resort import SurveyAnswers
from models.booking import Booking, FlightInfo, HotelInfo


class BookingService:

    def __init__(self, validator, recommender, payments, email, repo):
        self.v = validator
        self.r = recommender
        self.p = payments
        self.mail = email
        self.repo = repo

    def create_booking(self):
        print("\n=== 🌴 Туристичне агентство — створення бронювання ===")
        client = self._input_client()
        answers = self._input_survey()

        # вибір курорту з топ3
        top_resorts = self.r.recommend_top(answers, top_n=3)
        print("\n📍 Найкращі варіанти курортів для вас:")
        for i, res in enumerate(top_resorts, 1):
            print(f"{i}) {res.name} — {res.country}. {res.desc}")

        while True:
            choice = input("Оберіть курорт (1–3): ").strip()
            if choice in ["1", "2", "3"]:
                resort = top_resorts[int(choice) - 1]
                break
            print("❌ Введіть число 1–3.")

        start, end = self._input_dates()
        travelers = self._input_travelers(client)
        total = self._calc_price(resort, start, end, len(travelers))

        print(f"\n💳 Орієнтовна вартість: {total} UAH")
        payment = self._input_payment(total)
        flight = self._generate_flight(resort, start)
        hotel = self._select_hotel(resort)

        booking = Booking(
            booking_id=str(uuid.uuid4())[:8].upper(),
            client=client,
            travelers=travelers,
            resort=resort,
            start_date=start,
            end_date=end,
            flight=flight,
            hotel=hotel,
            total_price_uah=total,
            payment=payment
        )
        self.repo.save(booking)
        self.mail.send_booking(client.email, booking)
        self._summary(booking)

    def _input_client(self):
        v = self.v

        def ask(prompt, check, msg):
            while True:
                val = input(prompt).strip()
                if check(val):
                    return val
                print(msg)

        f = ask("👤 Ім'я: ", v.validate_name, "❌ Тільки літери.")
        l = ask("👤 Прізвище: ", v.validate_name, "❌ Тільки літери.")
        c = ask("🆔 ID документа (6–12 символів): ", v.validate_card_id, "❌ Латиниця або цифри, 6–12.")
        p = ask("📞 Телефон (380XXXXXXXXX): ", v.validate_phone, "❌ Формат має бути 380XXXXXXXXX.")
        e = ask("📧 Email (@gmail.com): ", v.validate_email, "❌ Має бути @gmail.com.")
        return Client(f, l, c, p, e)

    def _input_survey(self):
        def ask(q):
            while True:
                s = input(f"{q} (1–5): ").strip()
                if s.isdigit() and 1 <= int(s) <= 5:
                    return int(s)
                print("❌ Введіть число від 1 до 5.")
        print("\n💭 Вкажіть, що для вас важливо у відпочинку:")
        return SurveyAnswers(
            ask("🏖️ Має бути море?"),
            ask("⛰️ Має бути гори?"),
            ask("🏰 Багато екскурсій?"),
            ask("🌲 Близькість до природи?"),
            ask("👨‍👩‍👧‍👦 Сімейний формат?"),
            ask("🎉 Хочете нічні розваги?")
        )

    def _input_dates(self):
        v = self.v
        today = date.today()
        while True:
            s1 = input("📅 Дата початку (YYYY-MM-DD): ").strip()
            d1 = v.validate_date(s1)
            if not d1:
                print("❌ Некоректна дата.")
                continue
            if d1 <= today:
                print("❌ Дата має бути не в минулому або сьогодні.")
                continue
            s2 = input("📅 Дата завершення (YYYY-MM-DD): ").strip()
            d2 = v.validate_date(s2)
            if not d2:
                print("❌ Некоректна дата.")
                continue
            if d2 <= d1:
                print("❌ Кінець має бути після початку.")
                continue
            return d1, d2

    def _input_travelers(self, client):
        travelers = [client]
        while True:
            try:
                count = int(input("👥 Скільки осіб їде загалом?: "))
                if count >= 1:
                    break
            except ValueError:
                pass
            print("❌ Введіть число 1 або більше.")

        for i in range(1, count):
            print(f"\n🧳 Пасажир {i + 1}:")
            f = input("Ім'я: ").strip()
            l = input("Прізвище: ").strip()
            c = input("ID документа: ").strip()
            travelers.append(Traveler(f, l, c))

        print("\n✅ Список усіх учасників поїздки:")
        for t in travelers:
            print(f"— {t.first_name} {t.last_name} ({t.card_id})")
        return travelers

    def _input_payment(self, amount):
        while True:
            print("\n💰 Спосіб оплати:")
            print("1) Apple Pay 🍎")
            print("2) Банківська картка 💳")
            c = input("Ваш вибір (1/2): ").strip()
            if c == "1":
                return self.p.pay_apple(amount)
            elif c == "2":
                pan = input("🔢 Номер картки (16 цифр): ").strip()
                if not self.v.validate_card_number(pan):
                    print("❌ Має бути рівно 16 цифр.")
                    continue
                expiry = input("📆 Строк дії (MM/YY): ").strip()
                if not self.v.validate_expiry(expiry):
                    print("❌ Некоректний строк.")
                    continue
                cvv = input("🔒 CVV (3 цифри): ").strip()
                if not self.v.validate_cvv(cvv):
                    print("❌ Некоректний CVV.")
                    continue
                return self.p.pay_card(pan, expiry, cvv, amount)
            else:
                print("❌ Некоректний вибір. Введіть 1 або 2.")

    def _calc_price(self, resort, start, end, pax):
        nights = (end - start).days or 1
        base = 1800
        coef = {
            "Україна": 0.8, "Єгипет": 1.0, "Туреччина": 1.1,
            "Індонезія": 1.7, "Чехія": 1.3, "Мальдіви": 2.2,
            "Іспанія": 1.6, "Японія": 2.0
        }.get(resort.country, 1.2)
        return int(nights * base * pax * coef)

    def _generate_flight(self, resort, start):
        dep = datetime.combine(start, datetime.min.time()) + timedelta(hours=8)
        arr = dep + timedelta(hours=random.choice([2, 3, 4, 5]))
        code = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=6))
        return FlightInfo("Київ", resort.name, dep, arr, code)

    def _select_hotel(self, resort):
        hotels = {
            "Шарм-ель-Шейх": ["Sea Paradise", "Coral Bay", "Sunrise Oasis"],
            "Анталія": ["Antalya Resort", "Golden Coast", "Lara Dream"],
            "Балі": ["Ubud Forest", "Kuta Wave", "Nusa Dua Pearl"],
            "Буковель": ["Carpathian Lodge", "Ski Inn", "Hutsul Chalet"],
            "Прага": ["Charles Bridge", "Old Town Plaza", "Bohemia Star"],
            "Мальдіви": ["Lagoon Paradise", "Ocean View", "Coco Palm"],
            "Барселона": ["Costa del Sol", "La Rambla", "Blue Horizon"],
            "Токіо": ["Shibuya Tower", "Sakura Palace", "Tokyo View"]
        }
        name = random.choice(hotels.get(resort.name, [f"Hotel {resort.name}"]))
        return HotelInfo(name, f"{resort.name}, {resort.country}", random.choice([3, 4, 5]))

    def _summary(self, b):
        print("\n=== 🧾 ПІДСУМОК БРОНЮВАННЯ ===")
        print(f"Номер: {b.booking_id}")
        print(f"Клієнт: {b.client.last_name} {b.client.first_name}")
        print(f"Кількість пасажирів: {len(b.travelers)}")
        print("👥 Пасажири:")
        for t in b.travelers:
            print(f"  — {t.first_name} {t.last_name} ({t.card_id})")
        print(f"🏝️ Курорт: {b.resort.name}, {b.resort.country}")
        print(f"📆 Період: {b.start_date} → {b.end_date}")
        print(f"✈️ Рейс: {b.flight.from_city} → {b.flight.to_city} | {b.flight.pnr}")
        print(f"🏨 Готель: {b.hotel.name} ({b.hotel.stars}⭐)")
        print(f"💰 Сума: {b.total_price_uah} UAH")
        print(f"💳 Статус оплати: {'✅ Успішно' if b.payment.approved else '❌ Відхилено'}")
        print("=====================================\n")
