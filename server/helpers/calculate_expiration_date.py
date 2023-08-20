from datetime import datetime, timedelta


class DateTimeProvider:  # Add DateTimeProvider to enable easier testing
    @staticmethod
    def get_utc_now():
        """Returns current UTC timestamp"""
        return datetime.utcnow()


def calculate_expiration_date(number_of_days, datetime_provider=None):
    """Calculates a date X days from date of function call"""
    if datetime_provider is None:
        datetime_provider = DateTimeProvider()

    valid_until = datetime_provider.get_utc_now() + timedelta(days=number_of_days)
    return valid_until
