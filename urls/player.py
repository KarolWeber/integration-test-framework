from infrastructure.config import PLAYER_API


class PlayerUrls:
    class Games:
        init_token = (
            f"{PLAYER_API}/example_init_link?"
            "platform={platform}&currency={currency}&userName={username}&slug={slug}"
        )
        demo_for_not_logged_player = (
            f"{PLAYER_API}/example_init_link?"
            "slug={slug}&lang={lang}&platform={platform}"
        )
        demo_for_logged_player = (
            f"{PLAYER_API}/example_init_link?"
            "slug={slug}&lang={lang}&platform={platform}"
        )

    class User:
        base = f'{PLAYER_API}/players/player'
        create = f'{base}/register_account_test'
        login = f'{base}/authenticate'
        logout = f'{base}/logout'

    class Wallet:
        base = f'{PLAYER_API}/wallet'
        check_balance = f'{base}/wallet'
        deposit = f'{base}/deposit/create'
        pay_methods = f'{base}/deposit/payment_methods'

    class Bonus:
        base = f'{PLAYER_API}/bonus'
        available_bonuses = f'{base}/available_bonus'
        current_bonuses = f'{base}/player_bonus'
        accept = f'{base}/available_bonus/claim'
        claim = f'{base}/available_bonus/accept'
