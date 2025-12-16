def create_deposit_payload(deposit_payment_method_id, amount, bonus):
    """
    Generuje payload do dokonania depozytu przez gracza.
    :param deposit_payment_method_id: (uuid) Identyfikator metody płatniczej.
    :param amount: (int) Wysokość depozytu.
    :param bonus: Obiekt bonusu z którego chce skorzystać gracz.
    :return: (dict) Payload do dokonania depozytu.
    """
    return {
        "paymentMethodId": deposit_payment_method_id,
        "amount": amount,
        "currency": "PLN",
        "rulesAcceptance": True,
        "additionalProps": "",
        "returnUrl": "https://gambetsoft-stage.eu/pl/casino/all?deposit=success?deposit=success",
        "metadata": {
            "bonusDefinitionId": getattr(bonus, "bonus_definition_id", None),
            "claimId": getattr(bonus, "claim_id", None)
        }
    }
