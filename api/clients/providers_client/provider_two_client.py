from api.request_api import RequestApi
from faker import Faker
from urls.providers import ProviderTwoUrls

fake = Faker("pl_PL")


class ProviderTwoClient:
    @staticmethod
    def authenticate(context, payload):
        """
        Autentykuje sesję gracza.

        :param context: Obiekt kontekstu zalogowanego gracza.
        :param payload: (dict) – dane wymagane do autentykacji.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=ProviderTwoUrls.authenticate, context=context, payload=payload)

    @staticmethod
    def token_refresh(context, payload):
        """
        Odświeża token gracza.

        :param context: Obiekt kontekstu zalogowanego gracza.
        :param payload: (dict) – dane wymagane do odświeżenia.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=ProviderTwoUrls.refresh_token, context=context, payload=payload)

    @staticmethod
    def bet(context, payload):
        """
        Dokonuje zakładu.

        :param context: Obiekt zalogowanej sesji gry.
        :param payload: (dict) – dane wymagane do dokonania zakładu.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=ProviderTwoUrls.bet, context=context, payload=payload)

    @staticmethod
    def win(context, payload):
        """
        Zwraca wynik zakładu.

        :param context: Obiekt zalogowanej sesji gry.
        :param payload: (dict) – dane wymagane do zwrócenia wyniku zakładu.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=ProviderTwoUrls.win, context=context, payload=payload)

    @staticmethod
    def get_funds(context, payload):
        """
        Zwraca aktualne środki dostępne na grze.

        :param context: Obiekt zalogowanej sesji gry.
        :param payload: (dict) – dane wymagane do zwrócenia aktualnych środków.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=ProviderTwoUrls.get_funds, context=context, payload=payload)

    @staticmethod
    def rollback(context, payload):
        """
        Cofa ostatnią transakcję.

        :param context: Obiekt zalogowanej sesji gry.
        :param payload: (dict) – dane wymagane do cofnięcia transakcji.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=ProviderTwoUrls.rollback, context=context, payload=payload)
