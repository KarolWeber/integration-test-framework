from api.services.admin_service.casino_service import CasinoService
from api.services.admin_service.marketing_service import MarketingService
from api.services.admin_service.players_service import PlayersService
from api.services.admin_service.technical_service import TechnicalService
from api.services.admin_service.user_service import UserService
from infrastructure.credentials import admin_credential
from utils.enums.bonus_types import BonusType


class AdminService:
    """
    Serwis administracyjny, który umożliwia dostęp do funkcji backoffice.

    username (str): Nazwa użytkownika administratora.
    password (str): Hasło administratora.
    admin_credentials (dict): Słownik z loginem i hasłem używany do logowania.

    user (UserService): Serwis zarządzania użytkownikami.
    technical (TechnicalService): Serwis funkcji technicznych.
    marketing (MarketingService): Serwis funkcji marketingowych.
    bonus_types (Enum): Enum dostępnych typów bonusów.
    casino (CasinoService): Serwis funkcji kasyna.
    players (PlayersService): Serwis zarządzania graczami.
    """

    def __init__(self, admin_credentials=None):
        if not admin_credentials:
            admin_credentials = admin_credential
        self.username = admin_credentials['username']
        self.password = admin_credentials['password']
        self.credentials = {"login": self.username, "password": self.password}
        self.token = None

        self.user = UserService(context=self)
        self.technical = TechnicalService(context=self)
        self.marketing = MarketingService(context=self)
        self.bonus_types = BonusType
        self.casino = CasinoService(context=self)
        self.players = PlayersService(context=self)
