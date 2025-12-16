from dataclasses import dataclass


@dataclass()
class PlayerWalletBalance:
    real_money: float
    locked_money: float
    bonus_money: float
    locked_winnings: float
    bonus_winnings: float
    winnings: float
    main: float
    total: float

    @classmethod
    def from_dict(cls, data):
        return cls(
            real_money=data['realMoney'],
            locked_money=data['lockedMoney'],
            bonus_money=data['bonusMoney'],
            locked_winnings=data['lockedWinnings'],
            bonus_winnings=data['bonusWinnings'],
            winnings=data['winnings'],
            main=data['main'],
            total=data['total'],
        )
