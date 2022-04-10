PRICE_PER_DAY = 0.50


def get_amount(data):
    days = data['return_date'] - data['date']
    rented_days = days.days
    amount = rented_days * PRICE_PER_DAY

    return amount
