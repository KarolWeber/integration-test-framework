import datetime
import string
from random import choice, randint

from dateutil.relativedelta import relativedelta
from faker import Faker
from infrastructure.config import EMAIL_DOMAIN
from pesel import Pesel
from phone_gen import PhoneNumber

fake = Faker("pl_PL")


def player_account_data(username, password):
    """
    Generuje podstawowe dane konta gracza
    :param username: (str) Nazwa konta gracza
    :param password: (str) Hasło do konta gracza
    :return: (dict) Payload z danymi konta gracza.
    """
    return {
        "password": password,
        "email": f'{username}{EMAIL_DOMAIN}',
        "termsAndConditionStatement": True,
        "adultStatement": True
    }


def player_personal_data(player_email, player_age=18):
    """
    Generuje dane osobowe gracza.
    :param player_email: (str) Adres email gracza.
    :param player_age: (int) Wiek gracza.
    :return: (dict) Payload z danymi osobowymi gracza.
    """
    today = datetime.date.today()
    birth_date = today - relativedelta(years=player_age, days=1)
    birth_date_data = f'{birth_date.year}-{birth_date.month:02}-{birth_date.day:02}'
    personal_id = Pesel.generate(year=birth_date.year, month=birth_date.month, day=birth_date.day).value

    player = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "citizenship": "PL",
        "birthCountry": "PL",
        "nickname": player_email[:12],
        "phoneNumber": {
            "prefix": "+48",
            "number": PhoneNumber("Poland").get_number(full=False)},
        "addressStreet": fake.street_name(),
        "addressHouseNumber": f'{randint(1, 999)}',
        "addressFlatNumber": f'{randint(1, 999)}a',
        "addressPostalCode": fake.postcode(),
        "addressCity": fake.city(),
        "addressCountry": "PL",
        "iban": fake.iban(),
        "currency": "PLN",
        "verificationDocumentType": "identity_card",
        "documentNumber": fake.identity_card_number(),
        "birthDayDate": birth_date_data,
        "personalId": personal_id,
    }
    return player


def player_responsible_gaming_data(dailyTimeLimit=64800, monthlyTimeLimit=2160000, dailyWagerLimit=10000000, monthlyWagerLimit=90000000):
    """
    Generuje dane limitów gracza.
    :param dailyTimeLimit: (int) Limit czasowy dzianny (w sekundach).
    :param monthlyTimeLimit: (int) Limit czasowy miesięczny (w sekundach).
    :param dailyWagerLimit: (int) Limit obrotu dzienny (w walucie gracza).
    :param monthlyWagerLimit: (int) Limit obrotu miesięczny (w walucie gracza).
    :return: (dict) Payload z limitami gracza.
    """
    return {
        "dailyTimeLimit": dailyTimeLimit,
        "monthlyTimeLimit": monthlyTimeLimit,
        "dailyWagerLimit": dailyWagerLimit,
        "monthlyWagerLimit": monthlyWagerLimit
    }


def player_consents_and_agreements(emailConsent=True, smsMessageConsent=True, phoneNumberConsent=True, pushMessageConsent=True,
                                   inboxMessageConsent=True, privateBankingStatement=False, fundsOwnerStatement=True, fundsStatement=True,
                                   fundsSource="employment_contract", pepStatement=False):
    """
    Generuje dane zgód i oświadczeń gracza.
    :param emailConsent: (bool) Zgoda na wysyłkę e-maili.
    :param smsMessageConsent: (bool) Zgoda na wysyłkę SMS-ów.
    :param phoneNumberConsent: (bool) Zgoda na kontakt telefoniczny.
    :param pushMessageConsent: (bool) Zgoda na wysyłkę wiadomości push.
    :param inboxMessageConsent: (bool) Zgoda na wiadomości inbox na platformie.
    :param privateBankingStatement: (bool) Oświadczenie o korzystaniu z bankowości prywatnej.
    :param fundsOwnerStatement: (bool) Oświadczenie gracza potwierdzające, że jest właścicielem środków.
    :param fundsStatement: (bool) Oświadczenie dotyczące własności posiadanych środków.
    :param fundsSource: (str) Źródło pochodzenia środków.
    :param pepStatement: (bool) Oświadczenie, że gracz nie jest osobą zajmującą stanowisko publiczne.
    :return: (dict) Payload ze zgodami i oświadczeniami gracza.
    """
    return {
        "emailConsent": emailConsent,
        "smsMessageConsent": smsMessageConsent,
        "phoneNumberConsent": phoneNumberConsent,
        "pushMessageConsent": pushMessageConsent,
        "inboxMessageConsent": inboxMessageConsent,
        "pepStatement": pepStatement,
        "privateBankingStatement": privateBankingStatement,
        "fundsOwnerStatement": fundsOwnerStatement,
        "fundsStatement": fundsStatement,
        "fundsSource": fundsSource
    }


def player_full_data(username=None, password=None, identity_verified=True, iban_verified=True):
    """
    Generuje wszystkie dane wymagane do utworzenia gracza.
    :param username: Nazwa konta gracza.
    :param password: Hasło do konta gracza.
    :param identity_verified: (bool) Flaga określająca czy tożsamość gracza została potwierdzona.
    :param iban_verified: (bool) Flaga określająca czy numer konta bonkowego został potwierdzony.
    :return (dict) Payload wymagany do utworzenia konta gracza zawierający dane konta, dane osobowe, zgody i oświadczenia
    oraz limity odpowiedzialnej gry.
    """
    if not username:
        username = "".join(choice(string.ascii_lowercase) for _ in range(10))
    if not password:
        password = "Test1234"
    return {"account": player_account_data(username, password),
            "personalData": player_personal_data(username),
            "consentsAndAgreements": player_consents_and_agreements(),
            "responsibleGaming": player_responsible_gaming_data(),
            "identityVerified": identity_verified,
            "ibanVerified": iban_verified}
