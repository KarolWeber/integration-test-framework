from dataclasses import dataclass
from typing import List, Any


@dataclass()
class ProviderGameData:
    id: str
    rtp: Any
    has_free_spins: bool
    game_type: str
    available: bool

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            rtp=data.get('rtp'),
            has_free_spins=data.get('hasFreeSpins'),
            game_type=data.get('gameType'),
            available=data.get('available')
        )


@dataclass()
class Game:
    name: str
    id: str
    visible: bool
    provider_id: str
    provider_name: str
    provider_game_id: str
    rtp: str
    order: int
    thumb: Any
    background: Any
    slug: str
    reporting_game_group: Any
    game_weight: int
    jackpot: bool
    enabled_free_spins: bool
    has_demo: bool
    live: bool
    provider_game_data: List[ProviderGameData]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get('name'),
            id=data.get('id'),
            visible=data.get('visible'),
            provider_id=data.get('providerId'),
            provider_name=data.get('providerName'),
            provider_game_id=data.get('providerGameId'),
            rtp=data.get('rtp'),
            order=data.get('order'),
            thumb=data.get('thumb'),
            background=data.get('background'),
            slug=data.get('slug'),
            reporting_game_group=data.get('reportingGameGroup'),
            game_weight=data.get('gameWeight'),
            jackpot=data.get('jackpot'),
            enabled_free_spins=data.get('enabledFreeSpins'),
            has_demo=data.get('hasDemo'),
            live=data.get('live'),
            provider_game_data=ProviderGameData.from_dict(data.get('providerGameData'))
        )


class GamesList(list[Game]):
    @classmethod
    def from_dict(cls, data: dict):
        items = [Game.from_dict(g) for g in data.get('items', [])]
        return list(cls(items))
