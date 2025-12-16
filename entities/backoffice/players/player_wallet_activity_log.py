from dataclasses import dataclass
from typing import Any


@dataclass()
class PlayerWalletActivityLogRequestHeaders:
    real_ip: Any
    hash: Any

    @classmethod
    def from_dict(cls, data):
        return cls(
            real_ip=data.get("real-ip"),
            hash=data.get("hash")
        )


@dataclass()
class PlayerWalletActivityLog:
    id: str
    type: str
    date_time: str
    description: str
    player_id: str
    wallet_id: str
    game_provider_id: Any
    game_provider_name: Any
    game_id: Any
    game_name: Any
    transaction_id: str
    bonus_definition_name: Any
    bonus_definition_type: Any
    bonus_definition_id: Any
    free_spins_quantity: Any
    free_spins_left: Any
    free_spin_value: Any
    free_spins_total_win: Any
    free_spins_distribution_bonus_money: Any
    free_spins_distribution_bonus_winnings: Any
    amount: int
    currency: str
    jackpot_amount: int
    total_balance_change: int
    total_balance_after: int
    pl_main_balance_change: int
    pl_main_balance_after: int
    pl_bonus_balance_change: int
    pl_bonus_balance_after: int
    pl_bonus_pending_winnings_change: int
    pl_bonus_pending_winnings_after: int
    round_image_url: str
    platform: str
    payment_method: Any
    payment_method_id: Any
    external_transaction_account: Any
    provider_round_id: str
    provider_transaction_id: str
    change_by_user_type: str
    change_by_username: str
    request_headers: PlayerWalletActivityLogRequestHeaders

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            type=data.get('type'),
            date_time=data.get('dateTime'),
            description=data.get('description'),
            player_id=data.get('playerId'),
            wallet_id=data.get('walletId'),
            game_provider_id=data.get('gameProviderId'),
            game_provider_name=data.get('gameProviderName'),
            game_id=data.get('gameId'),
            game_name=data.get('gameName'),
            transaction_id=data.get('transactionId'),
            bonus_definition_name=data.get('bonusDefinitionName'),
            bonus_definition_type=data.get('bonusDefinitionType'),
            bonus_definition_id=data.get('bonusDefinitionId'),
            free_spins_quantity=data.get('freeSpinsQuantity'),
            free_spins_left=data.get('freeSpinsLeft'),
            free_spin_value=data.get('freeSpinValue'),
            free_spins_total_win=data.get('freeSpinsTotalWin'),
            free_spins_distribution_bonus_money=data.get('freeSpinsDistributionBonusMoney'),
            free_spins_distribution_bonus_winnings=data.get('freeSpinsDistributionBonusWinnings'),
            amount=data.get('amount'),
            currency=data.get('currency'),
            jackpot_amount=data.get('jackpotAmount'),
            total_balance_change=data.get('totalBalanceChange'),
            total_balance_after=data.get('totalBalanceAfter'),
            pl_main_balance_change=data.get('plMainBalanceChange'),
            pl_main_balance_after=data.get('plMainBalanceAfter'),
            pl_bonus_balance_change=data.get('plBonusBalanceChange'),
            pl_bonus_balance_after=data.get('plBonusBalanceAfter'),
            pl_bonus_pending_winnings_change=data.get('plBonusPendingWinningsChange'),
            pl_bonus_pending_winnings_after=data.get('plBonusPendingWinningsAfter'),
            round_image_url=data.get('roundImageUrl'),
            platform=data.get('platform'),
            payment_method=data.get('paymentMethod'),
            payment_method_id=data.get('paymentMethodId'),
            external_transaction_account=data.get('externalTransactionAccount'),
            provider_round_id=data.get('providerRoundId'),
            provider_transaction_id=data.get('providerTransactionId'),
            change_by_user_type=data.get('changeByUserType'),
            change_by_username=data.get('changeByUsername'),
            request_headers=PlayerWalletActivityLogRequestHeaders.from_dict(data.get('requestHeaders') or {}),
        )


class PlayerWalletActivityLogList(list[PlayerWalletActivityLog]):
    @classmethod
    def from_dict(cls, data):
        items = [PlayerWalletActivityLog.from_dict(log) for log in data.get('items', [])]
        return cls(items)
