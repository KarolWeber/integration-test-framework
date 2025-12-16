from dataclasses import dataclass, field
from typing import List, Any


# TAGS & CONDITIONS
@dataclass()
class Tags:
    id: str
    name: str
    value_type: Any
    string_value: Any
    datetime_value: Any
    number_value: Any
    operation: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            value_type=data.get('valueType'),
            string_value=data.get('stringValue'),
            datetime_value=data.get('datetimeValue'),
            number_value=data.get('numberValue'),
            operation=data.get('operation')
        )


@dataclass()
class Conditions:
    conditions: List[Tags]

    @classmethod
    def from_dict(cls, data: dict):
        # data to np. {"conditions": [ {...}, {...} ]}
        tags = [Tags.from_dict(tag) for tag in data.get("conditions", [])]
        return cls(conditions=tags)


# GAMES / PROVIDERS / WEIGHT
@dataclass()
class Games:
    id: str
    name: str
    provider_name: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            provider_name=data.get('providerName')
        )


@dataclass()
class Providers:
    id: str
    name: str
    games_count: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            games_count=data.get('gamesCount')
        )


@dataclass()
class GameWeight:
    id: str
    name: str
    provider_name: str
    game_weight: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            provider_name=data.get('providerName'),
            game_weight=data.get('gameWeight')
        )


# BONUS SETTINGS
@dataclass()
class BonusDepositIntervals:
    min_deposit_amount: Any
    max_deposit_amount: Any
    bonus_amount: Any
    free_spins_template_id: Any
    free_spins_quantity: Any

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            min_deposit_amount=data.get('minDepositAmount'),
            max_deposit_amount=data.get('maxDepositAmount'),
            bonus_amount=data.get('bonusAmount'),
            free_spins_template_id=data.get('freeSpinsTemplateId'),
            free_spins_quantity=data.get('freeSpinsQuantity')
        )


@dataclass()
class PresentationSettings:
    locale: str
    bonus_presentation_name: str
    short_terms_and_conditions: str
    terms_and_conditions_url: str
    bonus_image_url: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            locale=data.get('locale'),
            bonus_presentation_name=data.get('bonusPresentationName'),
            short_terms_and_conditions=data.get('shortTermsAndConditions'),
            terms_and_conditions_url=data.get('termsAndConditionsUrl'),
            bonus_image_url=data.get('bonusImageUrl')
        )


@dataclass()
class BonusSettings:
    currency: str
    presentation_settings: List[PresentationSettings]
    max_bonus_amount: Any
    is_bonus_amount_fixed: bool
    bonus_deposit_intervals: List[BonusDepositIntervals]
    bonus_amount: Any
    max_bet: Any
    max_win: Any
    is_wagering_amount_fixed: bool
    wagering_amount: int
    wagering_calculated_on: str
    on_bonus_wagering_completion: str
    redemption_threshold: int
    redemption_threshold_trigger: str
    free_spins_template_id: Any
    free_spins_quantity: Any

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            currency=data.get('currency'),
            presentation_settings=[PresentationSettings.from_dict(p) for p in data.get('presentationSettings', [])],
            max_bonus_amount=data.get('maxBonusAmount'),
            is_bonus_amount_fixed=data.get('isBonusAmountFixed'),
            bonus_deposit_intervals=[BonusDepositIntervals.from_dict(bdi) for bdi in data.get('bonusDepositIntervals', [])],
            bonus_amount=data.get('bonusAmount'),
            max_bet=data.get('maxBet'),
            max_win=data.get('maxWin'),
            is_wagering_amount_fixed=data.get('isWageringAmountFixed'),
            wagering_amount=data.get('wageringAmount'),
            wagering_calculated_on=data.get('wageringCalculatedOn'),
            on_bonus_wagering_completion=data.get('onBonusWageringCompletion'),
            redemption_threshold=data.get('redemptionThreshold'),
            redemption_threshold_trigger=data.get('redemptionThresholdTrigger'),
            free_spins_template_id=data.get('freeSpinsTemplateId'),
            free_spins_quantity=data.get('freeSpinsQuantity')
        )


# BONUS LIST
@dataclass()
class BonusInList:
    id: str
    name: str
    presentation_name: str
    bonus_type: str
    offering_method: str
    claim_context: str
    is_enabled: bool
    is_active: bool
    active_from: str
    active_to: str
    created_at: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            presentation_name=data.get('presentation_name'),
            bonus_type=data.get('bonusType'),
            offering_method=data.get('offeringMethod'),
            claim_context=data.get('claimContext'),
            is_enabled=data.get('isEnabled'),
            is_active=data.get('isActive'),
            active_from=data.get('activeFrom'),
            active_to=data.get('activeTo'),
            created_at=data.get('createdAt')
        )


class BonusList(list[BonusInList]):
    @classmethod
    def from_dict(cls, data: dict):
        items = [BonusInList.from_dict(b) for b in data.get('items', [])]
        return cls(items)


# BONUS
@dataclass()
class BonusTemplate:
    id: str
    product: str
    bonus_type: str
    offering_method: str
    claim_context: str
    name: str
    description: str
    reporting_category: str
    active_from: str
    active_to: str
    is_enabled: bool
    require_acceptation: bool
    bonus_settings: List[BonusSettings]
    bonus_availability_time: int
    bonus_availability_time_based_on: str
    bonus_available_on_deposit_numbers: Any
    max_times_player_can_claim: Any
    priority: int
    bonus_expiration_time: int
    calculate_expiration_time_based_on: str
    on_bonus_expiration: str
    on_bonus_cancellation: str
    games_relation_type: str
    providers_relation_type: str
    game_weight_policy_type: str
    game_weight_policy_value: int
    on_redemption_threshold_reached: Any
    providers: List[Providers] = field(default_factory=list)
    game_weight: List[GameWeight] = field(default_factory=list)
    games: List[Games] = field(default_factory=list)
    tags: List[Conditions] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            product=data.get('product'),
            bonus_type=data.get('bonusType'),
            offering_method=data.get('offeringMethod'),
            claim_context=data.get('claimContext'),
            name=data.get('name'),
            description=data.get('description'),
            reporting_category=data.get('reportingCategory'),
            active_from=data.get('activeFrom'),
            active_to=data.get('activeTo'),
            is_enabled=data.get('isEnabled'),
            require_acceptation=data.get('requireAcceptation'),
            bonus_settings=[BonusSettings.from_dict(bs) for bs in data.get('bonusSettings', [])],
            bonus_availability_time=data.get('bonusAvailabilityTime'),
            bonus_availability_time_based_on=data.get('bonusAvailabilityTimeBasedOn'),
            bonus_available_on_deposit_numbers=data.get('bonusAvailableOnDepositNumbers'),
            max_times_player_can_claim=data.get('maxTimesPlayerCanClaim'),
            priority=data.get('priority'),
            bonus_expiration_time=data.get('bonusExpirationTime'),
            calculate_expiration_time_based_on=data.get('calculateExpirationTimeBasedOn'),
            on_bonus_expiration=data.get('onBonusExpiration'),
            on_bonus_cancellation=data.get('onBonusCancellation'),
            games_relation_type=data.get('gamesRelationType'),
            providers_relation_type=data.get('providersRelationType'),
            game_weight_policy_type=data.get('gameWeightPolicyType'),
            game_weight_policy_value=data.get('gameWeightPolicyValue'),
            on_redemption_threshold_reached=data.get('onRedemptionThresholdReached'),
            providers=[Providers.from_dict(p) for p in data.get('providers', [])],
            game_weight=[GameWeight.from_dict(gw) for gw in data.get('gameWeight', [])],
            games=[Games.from_dict(g) for g in data.get('games', [])],
            tags=[Conditions.from_dict(t) for t in data.get('tags', [])]
        )
