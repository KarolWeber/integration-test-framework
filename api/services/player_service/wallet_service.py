from time import sleep

import allure
from api.clients.player_client.wallet_client import WalletClient
from entities.casino.player_wallet_balance import PlayerWalletBalance
from utils.logging.logger import StepLogger
from utils.payloads import player_payloads


class WalletService:
    """
    Serwis do obsługi portfela gracza przez gracza.
    """

    def __init__(self, context):
        """
        Inicjalizuje serwis portfela gracza.

        :param context: Obiekt kontekstu zalogowanego gracza.
        """
        self._context = context

    @allure.step("Player check balance")
    def check_balance(self, step=True):
        """
        Pobiera listę portfeli gracza i zwraca obiekt.
        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        :return: Zwraca obiek portfela gracza.
        """
        resp = WalletClient.check_balance(self._context)
        if step:
            StepLogger.log_step(f"PLAYER CHECK BALANCE: {self._context.email}", response=resp)
        if resp.status_code != 200:
            return resp
        return PlayerWalletBalance.from_dict(resp.json()['balance'])

    @allure.step("Player deposit")
    def deposit(self, deposit_amount, bonus=None, payment_method='MANUAL'):
        """
        Dokonuje depozytu.

        :param deposit_amount: (int) Wysokość depozytu.
        :param bonus: Opcjonalny Obiekt bonusu w przypadku reload bonus.
        :param payment_method: (str) Nazwa metody płatności.
        """
        before_deposit_balance = self.check_balance(step=False).real_money
        after_deposit_balance = 0
        attempt = 0
        payment_methods = WalletClient.pay_methods(self._context)
        deposit_payment_method = next(
            (method for method in payment_methods.json() if method['tenantAvailablePaymentMethodName'].upper() == payment_method), None)
        if deposit_payment_method is None:
            raise ValueError(f"Payment method '{payment_method}' not found for player {self._context.email}.")

        payload = player_payloads.create_deposit_payload(
            deposit_payment_method_id=deposit_payment_method['id'],
            amount=deposit_amount,
            bonus=bonus)
        resp = WalletClient.deposit(self._context, payload=payload)
        if resp.status_code == 200:
            max_retries = 3
            for attempt in range(1, max_retries + 1):
                after_deposit_balance = self.check_balance(step=False).real_money
                if after_deposit_balance == before_deposit_balance + deposit_amount:
                    break
                sleep(1)
            if max_retries == 0 and after_deposit_balance != before_deposit_balance + deposit_amount:
                raise RuntimeError(f"Failed update balance after {attempt} attempt")
        StepLogger.log_step(f"PLAYER DEPOSIT: {self._context.email} → {deposit_amount} AMOUNT", payload=payload, response=resp)
        return resp
