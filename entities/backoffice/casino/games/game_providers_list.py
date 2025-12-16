from dataclasses import dataclass, field


@dataclass()
class Settings:
    license: str
    key: str
    operator: str
    service_api_url: str
    game_launcher_url: str
    lobby_url: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            license=data.get('license'),
            key=data.get('key'),
            operator=data.get('operator'),
            service_api_url=data.get('serviceApiUrl'),
            game_launcher_url=data.get('gameLauncherUrl'),
            lobby_url=data.get('lobbyUrl'),
        )


@dataclass()
class SupportedFreeSpinsModes:
    wallet_free_spins: bool
    provider_free_spins: bool

    @classmethod
    def from_dict(cls, data):
        return cls(
            wallet_free_spins=data.get('walletFreeSpins'),
            provider_free_spins=data.get('providerFreeSpins')
        )


@dataclass()
class GameProvider:
    id: str
    integration_type: str
    name: str
    enabled: bool
    settings: Settings
    supported_free_spins_modes: SupportedFreeSpinsModes
    available_currencies: field(default_factory=list)

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            integration_type=data.get('integrationType'),
            name=data.get('name'),
            enabled=data.get('enabled'),
            settings=Settings.from_dict(data.get('settings')),
            supported_free_spins_modes=SupportedFreeSpinsModes.from_dict(data.get('supportedFreeSpinsModes')),
            available_currencies=data.get('availableCurrencies'),
        )


class GameProviderList(list[GameProvider]):
    @classmethod
    def from_dict(cls, data: dict):
        items = [GameProvider.from_dict(gp) for gp in data.get('items', [])]
        return cls(items)
