from datetime import datetime, timedelta


def calculate_expiration_date(number_of_days):
    valid_until = datetime.utcnow() + timedelta(days=number_of_days)
    return valid_until
