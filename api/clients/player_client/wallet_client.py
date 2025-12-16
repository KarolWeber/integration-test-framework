from api.request_api import RequestApi
from urls.player import PlayerUrls


class WalletClient:
    @staticmethod
    def check_balance(context):
        """
        Zwraca salda gracza.

        :param context: Obiekt kontekstu zalogowanego gracza.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.GET, url=PlayerUrls.Wallet.check_balance, context=context)

    @staticmethod
    def pay_methods(context):
        """
        Zwraca dostępne metody płatności.

        :param context: Obiekt kontekstu zalogowanego gracza.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.GET, url=PlayerUrls.Wallet.pay_methods, context=context)

    @staticmethod
    def deposit(context, payload):
        """
        Dokonuje depozytu.

        :param context: Obiekt kontekstu zalogowanego gracza.
        :param payload: (dict) – dane wymagane do dokonania depozytu.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=PlayerUrls.Wallet.deposit, context=context, payload=payload)
