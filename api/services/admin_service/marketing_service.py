import json
from enum import Enum

import allure
from api.clients.admin_client.marketing_client import MarketingClient
from entities.backoffice.marketing.bonus_template import BonusTemplate, \
    BonusList
from entities.backoffice.marketing.free_spin_template import FreeSpinTemplate, \
    FreeSpinTemplateList
from utils.enums.bonus_types import BonusType
from utils.enums.free_spins_mode import FreeSpinsMode
from utils.files.files_helper import file_read_binary
from utils.logging.logger import StepLogger
from utils.payloads.admin_payloads import create_free_spins_template_payload, \
    create_bonus_payload


class MarketingService:
    """
    Serwis do obsługi funkcji marketingowych w backoffice.

    Umożliwia dostęp do:
        - bonusów (GamesService),
        - szablonów free spin (GameProvidersService),
        - grup raportowych gier (GameReportingGroups).
    """

    def __init__(self, context):
        """
        Inicjalizuje serwis kasyna.

        :param context: Obiekt kontekstu zalogowanego administratora.
        """
        self._context = context
        self.bonuses = BonusService(self._context)
        self.free_spins_templates = FreeSpinsTemplateService(self._context)
        self.free_spins_mode = FreeSpinsMode


class BonusService:
    """
    Serwis do zarządzania bonusami w backoffice.
    """

    def __init__(self, context):
        """
        :param context: Obiekt kontekstu zalogowanego administratora.
        """
        self._context = context
        self.bonus_types = BonusType

    @allure.step("Admin create bonus")
    def create(self, bonus_type_enum: BonusType, bonus_name=None, campaign=False, games=None, deposit_intervals=None, free_spin_template=None,
               payload=None, step=True):
        """
        Tworzy bonus i zwraca utworzony obiekt.

        :param bonus_type_enum: (BonusType) Typ bonusu z enuma BonusType zawierający konfigurację.
        :param bonus_name: Opr (str) Nazwa bonusu.
        :param campaign: (bool) Flaga określająca czy bonus jest kampanijny.
        :param games: (list) Lista obiektów gry.
        :param deposit_intervals: (list) Lista przedziałów depozytów generowanych przez 'create_deposit_interval'.
        :param free_spin_template: Obiekt szablonu free spinów.
        :param payload: (dict, opcjonalny) Payload przygotowany wcześniej przy użyciu 'create_bonus_payload'.
        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        :return: Zwraca obiekt utworzonego bonusu.
        """
        if payload is None:
            payload = create_bonus_payload(bonus_type_enum=bonus_type_enum,
                                           bonus_name=bonus_name,
                                           campaign=campaign,
                                           games=games,
                                           deposit_intervals=deposit_intervals,
                                           free_spin_template=free_spin_template)
        file = [('dto', ('dto.json', json.dumps(payload), 'application/json'))]
        bonus_images = {
            'RELOAD_BONUS': 'reload_bonus.png',
            'BONUS_MONEY': 'bonus_money.png',
            'FREE_SPINS': 'free_spins.png',
        }
        filename = bonus_images.get(bonus_type_enum.value["bonusType"])
        file.append(('image-pln-pl', (filename, file_read_binary(filename, "bonus_images"), 'image/jpeg')))
        resp = MarketingClient.Bonuses.create(self._context, payload=payload, file=file)
        if step:
            StepLogger.log_step(f"ADMIN CREATE BONUS {payload['name']}", response=resp)
        if resp.status_code != 200:
            return resp
        return self.get(resp.json()['bonusDefinitionId'], step=False)

    @allure.step("Admin get bonus")
    def get(self, bonus_definition_id, step=True):
        """
        Pobiera bonus na podstawie podanego identyfikatora.

        :param bonus_definition_id: (uuid) Identyfikator .
        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        :return: Zwraca obiekt bonusu.
        """
        resp = MarketingClient.Bonuses.get(self._context, bonus_definition_id=bonus_definition_id)
        if step:
            StepLogger.log_step("ADMIN GET BONUS ", response=resp)
        if resp.status_code != 200:
            return resp
        return BonusTemplate.from_dict(resp.json())

    @allure.step("Admin get bonuses list")
    def list(self, step=True):
        """
        Pobiera listę bonusów.

        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        :return: Zwraca listę obiektów.
        """
        resp = MarketingClient.Bonuses.list(self._context)
        if step:
            StepLogger.log_step("ADMIN GET BONUS LIST", response=resp)
        if resp.status_code != 200:
            return resp
        return BonusList.from_dict(resp.json())


class FreeSpinsTemplateService:
    """
    Serwis do zarządzania szablonami free spin w backoffice.
    """

    def __init__(self, context):
        """
        :param context: Obiekt kontekstu zalogowanego administratora.
        """
        self._context = context

    @allure.step("Admin get free spin template")
    def get(self, template, step=True):
        """
        Pobiera szablon free spin na podstawie podanego identyfikatora.

        :param template: (uuid) Identyfikator szablonu bądź obiekt szablonu.
        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        :return: Zwraca obiekt szablonu free spin.
        """
        resp = MarketingClient.FreeSpinTemplates.get(self._context, template_id=getattr(template, "id", template))
        if step:
            StepLogger.log_step("ADMIN GET FREE SPIN TEMPLATE", response=resp)
        if resp.status_code != 200:
            return resp
        return FreeSpinTemplate.from_dict(resp.json())

    @allure.step("Admin create free spin template")
    def create(self, provider_integration, free_spin_mode, name=None, active_from_now=True, active_from=None, active_days=30, step=True):
        """
        Tworzy szablon free spin i zwraca utworzony obiekt.

        :param provider_integration: (str) Typ integracji dostawcy free spinów.
        :param free_spin_mode: (str) Tryb free spinów np z enuma BonusType.
        :param name: (str, opcjonalny) Nazwa szablonu.
        :param active_from_now: (bool) Flaga wskazująca, czy szablon ma być aktywny od teraz.
        :param active_from: (str) Data aktywacji.
        :param active_days: Liczba dni, przez które szablon ma być aktywny.
        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        :return: Zwraca obiek szablonu free spin.
        """
        if isinstance(free_spin_mode, Enum):
            free_spin_mode = free_spin_mode.value
        payload = create_free_spins_template_payload(provider_integration=provider_integration,
                                                     free_spin_mode=free_spin_mode,
                                                     name=name,
                                                     active_from_now=active_from_now,
                                                     active_from=active_from,
                                                     active_days=active_days)
        provider_free_spins = free_spin_mode == FreeSpinsMode.provider_free_spin.value
        wallet_free_spins = free_spin_mode == FreeSpinsMode.wallet_free_spin.value
        providers = self._context.casino.game_providers.list(step=False)
        provider_id = next(
            (
                provider.id for provider in providers
                if provider.integration_type == provider_integration
                   and provider.supported_free_spins_modes.provider_free_spins == provider_free_spins
                   and provider.supported_free_spins_modes.wallet_free_spins == wallet_free_spins
            ),
            None
        )
        if provider_id is None:
            raise ValueError(
                f"No provider found for {provider_integration} with mode {free_spin_mode}")
        payload["freeSpinsProviderId"] = provider_id
        resp = MarketingClient.FreeSpinTemplates.create(self._context, payload=payload)
        if step:
            StepLogger.log_step(f"ADMIN CREATE FREE SPINS TEMPLATE: {payload['name']}", response=resp)
        if resp.status_code != 200:
            return resp
        template_id = resp.json()['id']
        return self.get(template_id, step=False)

    @allure.step("Admin add games to free spin template")
    def add_games(self, template, games: list):
        """
        Dodaje gry do szablonu free spin.
        :param template: Obiekt szablonu free spin.
        :param games: (list) Lista obiektów gier.
        """
        payload = {"id": template.id, "games": [game.id for game in games]}
        resp = MarketingClient.FreeSpinTemplates.edit_games(self._context, payload=payload)
        StepLogger.log_step(f"ADMIN ADD GAMES TO FREE SPINS TEMPLATE: {template.name} → {[game.name for game in games]}", response=resp)
        return resp

    @allure.step("Admin enable/disable free spin template")
    def set_enable(self, template, enabled=True):
        """
        Aktywuje lub dezaktywuje szablon free spin.
        :param template: Obiekt szablonu.
        :param enabled: (bool) Flaga określająca status aktywności szablonu.
        """
        payload = {"id": template.id, "enabled": enabled}
        status = "ENABLED" if enabled else "DISABLED"
        resp = MarketingClient.FreeSpinTemplates.set_enabled(self._context, payload=payload)
        StepLogger.log_step(f"ADMIN SET TEMPLATE: {template.name} → {status}", response=resp)
        return resp

    @allure.step("Admin delete free spin template")
    def delete(self, template):
        """
        Usunięcie szablonu free spin.

        :param template: Obiekt szablonu free spin do usunięcia.
        """
        payload = {"id": template.id}
        resp = MarketingClient.FreeSpinTemplates.delete(self._context, payload=payload)
        StepLogger.log_step(f"ADMIN DELETE TEMPLATE: {template.name}", response=resp)
        return resp

    @allure.step("Admin get templates list")
    def list(self):
        """
        Pobiera listę szablonów free spin.

        :return: Zwraca listę obiektów szablonów free spin.
        """
        resp = MarketingClient.FreeSpinTemplates.list(self._context)
        StepLogger.log_step("ADMIN GET TEMPLATES LIST", response=resp)
        if resp.status_code != 200:
            return resp
        return FreeSpinTemplateList.from_dict(resp.json())
