from api.services.player_service.bonus_service import BonusService
from api.services.player_service.game_service import GameService
from api.services.player_service.user_service import UserService
from api.services.player_service.wallet_service import WalletService


class PlayerService:
    """
    Serwis gracza, który umożliwia dostęp do funkcji kasyna.

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

    def __init__(self, username=None, password=None):
        self.email = None
        self.password = None
        self.token = None
        self.id = None
        self.user = UserService(context=self)
        self.user.create(username, password, identity_verified=True, iban_verified=True, max_retries=3)
        self.credentials = {"login": self.email, "password": self.password}
        self.wallet = WalletService(context=self)
        self.game = GameService(context=self)
        self.bonus = BonusService(context=self)
