import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        current_date = dt.datetime.now().date()
        spent_today = 0
        for record in self.records:
            if current_date == record.date:
                spent_today += record.amount
        return spent_today

    def get_week_stats(self):
        current_date = dt.datetime.now().date()
        week_ago_date = current_date - dt.timedelta(days=6)
        whole_week = 0
        for record in self.records:
            if week_ago_date <= record.date <= current_date:
                whole_week += record.amount
        return whole_week


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        allowed_calories = self.limit - self.get_today_stats()
        if allowed_calories > 0:
            return (f"Сегодня можно съесть что-нибудь ещё, "
                    f"но с общей калорийностью не более "
                    f"{allowed_calories} кКал")
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):

    USD_RATE = 73.33
    EURO_RATE = 87.45

    def get_today_cash_remained(self, currency):
        remained_cash = self.limit - self.get_today_stats()
        cur_info = {
            "rub": (1, "руб"),
            "usd": (self.USD_RATE, "USD"),
            "eur": (self.EURO_RATE, "Euro")
        }
        cur_rate, currency = cur_info[currency]
        rounding = round(remained_cash / cur_rate, 2)
        if remained_cash == 0:
            return "Денег нет, держись"
        if remained_cash > 0:
            return f"На сегодня осталось {rounding} {currency}"
        else:
            minus = abs(rounding)
            return (f"Денег нет, держись: твой долг - "
                    f"{minus} {currency}")
