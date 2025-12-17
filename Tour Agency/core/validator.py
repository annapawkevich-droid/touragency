import re
from datetime import date, datetime, timedelta

class SimpleValidator: #перевірка
    NAME_RE = re.compile(r"^[A-Za-zА-Яа-яЇїІіЄєҐґ'\-]{2,40}$")
    PHONE_RE = re.compile(r"^380\d{9}$")
    EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@gmail\.com$")
    CARD_RE = re.compile(r"^\d{16}$")   
    CVV_RE = re.compile(r"^\d{3}$")
    EXP_RE = re.compile(r"^(0[1-9]|1[0-2])/(\d{2})$")
    CARD_ID_RE = re.compile(r"^[A-Za-z0-9]{6,12}$")

    def validate_name(self, value): return bool(self.NAME_RE.match(value.strip())) 
    def validate_phone(self, value): return bool(self.PHONE_RE.match(value.strip()))
    def validate_email(self, value): return bool(self.EMAIL_RE.match(value.strip()))
    def validate_card_number(self, value): return bool(self.CARD_RE.match(value.strip()))
    def validate_cvv(self, value): return bool(self.CVV_RE.match(value.strip()))
    def validate_card_id(self, value): return bool(self.CARD_ID_RE.match(value.strip()))

    def validate_expiry(self, value): 
        m = self.EXP_RE.match(value.strip())
        if not m: return False
        mm, yy = int(m.group(1)), int(m.group(2))
        year_full = 2000 + yy
        first = date(year_full, mm, 1)
        next_month = date(year_full + (mm == 12), (mm % 12) + 1, 1)
        last_day = next_month - timedelta(days=1)
        return last_day >= date.today()

    def validate_date(self, value):
        for fmt in ("%Y-%m-%d", "%Y.%m.%d", "%Y/%m/%d"):
            try:
                return datetime.strptime(value.strip(), fmt).date()
            except ValueError:
                continue
        return None
