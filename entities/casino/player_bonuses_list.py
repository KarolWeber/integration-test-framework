from dataclasses import dataclass
from typing import Any


# CURRENT BONUSES
@dataclass()
class BonusInCurrentList:
    bonus_definition_id: str
    claim_id: str
    presentation_name: str
    short_terms: str
    full_terms: str
    description: str
    images: str
    free_spins_quantity: int
    available_to: str
    availability_type: str
    bonus_type: str
    free_spin_games: list

    @classmethod
    def from_dict(cls, data):
        return cls(
            bonus_definition_id=data.get('bonusDefinitionId'),
            claim_id=data.get('claimId'),
            presentation_name=data.get('presentationName'),
            short_terms=data.get('shortTerms'),
            full_terms=data.get('fullTerms'),
            description=data.get('description'),
            images=data.get('images'),
            free_spin_games=data.get('freeSpinGames'),
            free_spins_quantity=data.get('freeSpinsQuantity'),
            available_to=data.get('availableTo'),
            availability_type=data.get('availabilityType'),
            bonus_type=data.get('bonusType'),
        )


class PlayerAvailableBonusesList(list[BonusInCurrentList]):
    @classmethod
    def from_dict(cls, data):
        items = [BonusInCurrentList.from_dict(b) for b in data.get('items', [])]
        return cls(items)


# AVAILABLE BONUSES
@dataclass()
class BonusInPlayerAvailableList:
    id: str
    bonus_definition_id: str
    bonus_name: str
    bonus_presentation_name: str
    bonus_amount_granted: Any
    real_money_locked: Any
    wagering_requirement: Any
    current_wagering: Any
    activation_time: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            bonus_definition_id=data.get('bonusDefinitionId'),
            bonus_name=data.get('bonusName'),
            bonus_presentation_name=data.get('bonusPresentationName'),
            bonus_amount_granted=data.get('bonusAmountGranted'),
            real_money_locked=data.get('realMoneyLocked'),
            wagering_requirement=data.get('wageringRequirement'),
            current_wagering=data.get('currentWagering'),
            activation_time=data.get('activationTime')
        )


class BonusesInAvailableList(list[BonusInPlayerAvailableList]):
    @classmethod
    def from_dict(cls, data):
        items = [BonusInPlayerAvailableList.from_dict(b) for b in data.get('items', [])]
        return cls(items)
