import random
import uuid
from datetime import datetime, timedelta

from utils.converters.date_converter import create_date


def create_custom_game_payload(provider, game_reporting_group_id, game_type, name, free_spins_supported):
    """
    Generuje payload wymagany do utworzenia gry technicznej.
    :param provider: Obiekt dostawcy gry.
    :param game_reporting_group_id: (uuid) Identyfikator grupy raportowej gry.
    :param game_type: (str) Typ gry.
    :param name: (str) Nazwa gry.
    :param free_spins_supported: (bool) Flaga wskazująca, czy gra obsługuje free spiny.
    :return: (dict) Payload wymagany do utworzenia gry technicznej.
    """
    base_name = f"AUTOMAT {game_type} {provider.name}"
    if name:
        game_name = f"{base_name} - {name} - {random.randint(1000, 9999)}"
    else:
        game_name = f"{base_name} - {random.randint(1000, 9999)}"
    return {
        "providerId": provider.id,
        "providerGameId": str(uuid.uuid4()),
        "name": game_name,
        "thumbs": [],
        "rtp": 95,
        "freeRoundsSupported": free_spins_supported,
        "reportingGameGroup": game_reporting_group_id,
        "order": 1,
        "hasJackpot": False,
        "hasDemo": True,
        "gameType": game_type,
        "visible": True
    }


def create_free_spins_template_payload(provider_integration, free_spin_mode, name, active_from_now, active_from, active_days):
    """
    Generuje payload wymagany do utworzenia szablonu free spinów.
    :param provider_integration: (str) Typ integracji dostawcy free spinów.
    :param free_spin_mode: (str) Tryb free spinów np z enuma BonusType.
    :param name: (str, opcjonalny) Nazwa szablonu.
    :param active_from_now: (bool) Flaga wskazująca, czy szablon ma być aktywny od teraz.
    :param active_from: (str) Data aktywacji.
    :param active_days: (int) Liczba dni, przez które szablon ma być aktywny.
    :return: (dict) Payload wymagany do utworzenia szablonu free spin.
    """
    now = datetime.now()
    return {
        "name": f'AUTOMAT: {name}' if name else "AUTOMAT FREE SPINS TEMPLATE",
        "description": "TEST DESCRIPTION",
        "activeFromNow": active_from_now,
        "activeFrom": active_from if active_from is not None else create_date(now),
        "activeTo": create_date((now + timedelta(days=active_days))),
        "freeSpinsMode": free_spin_mode,
        "freeSpinsProviderId": None,
        "freeSpinsProviderType": provider_integration,
        "freeSpinsProviderTemplateId": "",
        "quantity": 5,
        "stakes": {'PLN': 1}
    }


def create_deposit_interval(min_deposit=None, max_deposit=None, amount=None, free_spin_template_data_id=None):
    """
    Generuje payload wymagany do przedziałów depozytów.
    :param min_deposit: (int) Minimalna kwota depozytu.
    :param max_deposit: (int, opcjonalny) Maksymalna kwota depozytu.
    :param amount: (int) Wartość bonusu albo ilość free spinów jeśli został przekazany identyfikator szablonu free spin.
    :param free_spin_template_data_id: (uuid, opcjonalny) Identyfikator szablonu free spin.
    :return: (dict) Payload wymagany przy przedziałach depozytów podczas tworzenia bonusów.
    """
    payload = {
        "minDepositAmount": min_deposit if min_deposit is not None else 0,
        "maxDepositAmount": max_deposit
    }
    if free_spin_template_data_id:
        payload.update({"freeSpinsTemplateId": free_spin_template_data_id,
                        "freeSpinsQuantity": amount if amount else 10})
    else:
        payload.update({"bonusAmount": amount if amount else 100})
    return payload


def create_bonus_payload(bonus_type_enum, bonus_name=None, campaign=False, games=None, deposit_intervals: list = None, free_spin_template=None):
    """
    Generuje payload do utworzenia bonusu.
    :param bonus_type_enum: (BonusType) Typ bonusu z enuma BonusType zawierający konfigurację.
    :param bonus_name: (str, opcjonalny) Nazwa bonusu.
    :param campaign: (bool) Flaga określająca czy bonus jest kampanijny.
    :param games: (list) Lista obiektów gry.
    :param deposit_intervals: (list) Lista przedziałów depozytów generowanych przez 'create_deposit_interval'.
    :param free_spin_template: Obiekt szablonu free spinów.
    :return: (dict) Payload do utworzenia bonusu.
    """
    bonus_type = bonus_type_enum.value
    if bonus_name:
        name = f"AUTOMAT: {bonus_name} {bonus_type['bonusType']} {bonus_type['offeringMethod']} {bonus_type['claimContext']}"
    else:
        name = f"AUTOMAT {bonus_type['bonusType']} {bonus_type['offeringMethod']} {bonus_type['claimContext']}"
    if games is None and free_spin_template is None:
        if free_spin_template is not None:
            games = [game.id for game in free_spin_template.games]
        else:
            games = []
    now = datetime.now()
    active_from = create_date(now)
    active_to = create_date((now + timedelta(days=30)))
    payload = {
        "product": 'CASINO',
        "bonusType": bonus_type['bonusType'],
        "offeringMethod": "CAMPAIGN" if campaign else bonus_type['offeringMethod'],
        "claimContext": bonus_type['claimContext'],
        "name": name,
        "description": "Automat description",
        "reportingCategory": 'CASINO',
        "activeFromNow": True,
        "activeFrom": active_from,
        "activeTo": active_to,
        "isEnabled": True,
        "requireAcceptation": False,
        "freeSpinsTemplateId": free_spin_template.id if free_spin_template else None,
        "freeSpinsQuantity": 1,
        "bonusSettings": [
            {
                "currency": "PLN",
                "freeSpinsTemplateId": free_spin_template.id if free_spin_template else None,
                "freeSpinsQuantity": free_spin_template.quantity if free_spin_template else None,
                "presentationSettings": [
                    {
                        "locale": "pl",
                        "bonusPresentationName": name,
                        "shortTermsAndConditions": f"Short T&C {name}",
                        "termsAndConditionsUrl": f"Short T&C {name}",
                    }
                ],
                "isBonusAmountFixed": True if bonus_type['bonusType'] == "BONUS_MONEY" or bonus_type['bonusType'] == "FREE_SPINS" else False,
                "maxBonusAmount": None,
                "bonusDepositIntervals": deposit_intervals if deposit_intervals is not None else [
                    create_deposit_interval(free_spin_template_data_id=free_spin_template.id if free_spin_template else None)],
                "bonusAmount": 100,
                "maxBet": None,
                "maxWin": None,
                "isWageringAmountFixed": False,
                "wageringAmount": 1,
                "wageringCalculatedOn": 'BONUS_AND_DEPOSIT' if bonus_type['claimContext'] == "DEPOSIT_CONTEXT" and bonus_type[
                    'bonusType'] != 'FREE_SPINS' else 'BONUS_ONLY',
                "onBonusWageringCompletion": 'REDEEM_ALL',
                "redemptionThreshold": 1,
                "redemptionThresholdTrigger": "INSTANT",
            }
        ],
        "bonusAvailableOnDepositNumbers": None,
        "maxTimesPlayerCanClaim": 1,
        "priority": 1,
        "bonusAvailabilityTime": 36000000,
        "bonusAvailabilityTimeBasedOn": "SIGNUP",
        "bonusExpirationTime": 36000000,
        "calculateExpirationTimeBasedOn": "ACTIVE",
        "onBonusExpiration": 'REMOVE_ALL',
        "onBonusCancellation": 'REMOVE_ALL',
        "gamesRelationType": 'EXCLUDED',
        "games": games,
        "providersRelationType": 'EXCLUDED',
        "providers": [],
        "gameWeight": [],
        "gameWeightPolicyType": "FIXED",
        "gameWeightPolicyValue": 1,
        "providerTemplateId": free_spin_template.id if free_spin_template else None,
        "onRedemptionThresholdReached": 'REDEEM_BONUS_MONEY_AND_BONUS_WINNINGS_AND_LOCKED_WINNINGS',
        "tags": []
    }
    return payload
