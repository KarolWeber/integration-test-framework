from datetime import datetime


def create_date(date: datetime):
    """
    Konwertuje obiekt daty na format zgodny z wymaganiami systemu.
    :param date: (datetime) Obiekt daty i czasu do sformatowania.
    :return: (str) Data w formacie "YYYY-MM-DDTHH:MM:SSZ".
    """
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")
