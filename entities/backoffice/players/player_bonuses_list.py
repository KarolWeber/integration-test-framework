from dataclasses import dataclass
from typing import Any


@dataclass()
class PlayerCurrentBonuses:
    id: str
    bonus_definition_id: str
    player_id: str
    bonus_name: str
    bonus_presentation_name: str
    type: str
    offering_method: str
    claim_context: str
    bonus_amount_granted: Any
    real_money_locked: Any
    status: str
    sub_status: str
    wagering_requirement: Any
    current_wagering: Any
    created_time: str
    activated_time: str
    deactivated_time: Any
    priority: int
    free_spins_external_id: Any
    free_spins_status: Any
    free_spins_quantity: Any
    free_spins_quantity_available: Any
    free_spins_current_win: Any
    free_spins_provider_id: Any
    free_spins_error_code: Any

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            bonus_definition_id=data.get("bonusDefinitionId"),
            player_id=data.get("playerId"),
            bonus_name=data.get("bonusName"),
            bonus_presentation_name=data.get("bonusPresentationName"),
            type=data.get("type"),
            offering_method=data.get("offeringMethod"),
            claim_context=data.get("claimContext"),
            bonus_amount_granted=data.get("bonusAmountGranted"),
            real_money_locked=data.get("realMoneyLocked"),
            status=data.get("status"),
            sub_status=data.get("subStatus"),
            wagering_requirement=data.get("wageringRequirement"),
            current_wagering=data.get("currentWagering"),
            created_time=data.get("createdTime"),
            activated_time=data.get("activatedTime"),
            deactivated_time=data.get("deactivatedTime"),
            priority=data.get("priority"),
            free_spins_external_id=data.get("freeSpinsExternalId"),
            free_spins_status=data.get("freeSpinsStatus"),
            free_spins_quantity=data.get("freeSpinsQuantity"),
            free_spins_quantity_available=data.get("freeSpinsQuantityAvailable"),
            free_spins_current_win=data.get("freeSpinsCurrentWin"),
            free_spins_provider_id=data.get("freeSpinsProviderId"),
            free_spins_error_code=data.get("freeSpinsErrorCode")
        )


class PlayerCurrentBonusesList(list[PlayerCurrentBonuses]):
    @classmethod
    def from_dict(cls, data):
        items = [PlayerCurrentBonuses.from_dict(b) for b in data.get('items', [])]
        return cls(items)
