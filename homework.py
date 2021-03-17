import datetime as dt
DATE_VAR = "%d.%m.%Y"


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_VAR).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        current_date = dt.date.today()
        return sum(record.amount for record in self.records
                   if current_date == record.date)

    def get_week_stats(self):
        current_date = dt.date.today()
        week_ago_date = current_date - dt.timedelta(days=6)
        return sum(record.amount for record in self.records
                   if week_ago_date <= record.date <= current_date)

    def remained(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        allowed_calories = self.remained()
        if allowed_calories > 0:
            return ("Сегодня можно съесть что-нибудь ещё, "
                    "но с общей калорийностью не более "
                    f"{allowed_calories} кКал")
        return "Хватит есть!"


class CashCalculator(Calculator):
    RUB_RATE = 1
    USD_RATE = 73.33
    EURO_RATE = 87.45

    def get_today_cash_remained(self, currency):
        remained_cash = self.remained()
        if remained_cash == 0:
            return "Денег нет, держись"
        cur_info = {
            "rub": (self.RUB_RATE, "руб"),
            "usd": (self.USD_RATE, "USD"),
            "eur": (self.EURO_RATE, "Euro")
        }
        if currency not in cur_info:
            raise ValueError("Валюта не поддерживается")
        cur_rate, currency = cur_info[currency]
        rounding = round(remained_cash / cur_rate, 2)
        if remained_cash > 0:
            return f"На сегодня осталось {rounding} {currency}"
        dept = abs(rounding)
        return (f"Денег нет, держись: твой долг - "
                f"{dept} {currency}")
