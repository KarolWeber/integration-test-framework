from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass()
class FreeSpinGames:
    id: str
    name: str
    provider_name: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(id=data.get('id'),
                   name=data.get('name'),
                   provider_name=data.get('providerName'))


@dataclass()
class FreeSpinTemplate:
    id: str
    name: str
    description: str
    active: bool
    enabled: bool
    created_at: Optional[str]
    active_from: Optional[str]
    active_to: Optional[str]
    free_spins_mode: Optional[str]
    free_spins_provider_id: Optional[str]
    free_spins_provider_type: Optional[str]
    free_spins_provider_name: Optional[str]
    free_spins_provider_template_id: Optional[str]
    quantity: Optional[int]
    stakes: Dict[str, int]
    games: List[FreeSpinGames] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        games = [FreeSpinGames.from_dict(game) for game in data.get("games", [])]
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            created_at=data.get("createdAt"),
            active_from=data.get("activeFrom"),
            active_to=data.get("activeTo"),
            enabled=data.get("enabled"),
            active=data.get("active"),
            free_spins_mode=data.get("freeSpinsMode"),
            free_spins_provider_id=data.get("freeSpinsProviderId"),
            free_spins_provider_type=data.get("freeSpinsProviderType"),
            free_spins_provider_name=data.get("freeSpinsProviderName"),
            free_spins_provider_template_id=data.get("freeSpinsProviderTemplateId"),
            quantity=data.get("quantity"),
            stakes=data.get("stakes", {}),
            games=games,
        )


class FreeSpinTemplateList(list[FreeSpinTemplate]):
    @classmethod
    def from_dict(cls, data):
        items = [FreeSpinTemplate.from_dict(t) for t in data.get('items', [])]
        return cls(items)
