from infrastructure.config import PROVIDER_ONE_API, PROVIDER_TWO_API


class ProviderOneUrls:
    authenticate = f'{PROVIDER_ONE_API}/authenticate'
    bet = f'{PROVIDER_ONE_API}/bet'
    win = f'{PROVIDER_ONE_API}/win'
    get_funds = f'{PROVIDER_ONE_API}/balance'


class ProviderTwoUrls:
    authenticate = f'{PROVIDER_TWO_API}/authenticate'
    refresh_token = f'{PROVIDER_TWO_API}/refresh_token'
    bet = f'{PROVIDER_TWO_API}/bet'
    win = f'{PROVIDER_TWO_API}/win'
    get_funds = f'{PROVIDER_TWO_API}/balance'
    rollback = f'{PROVIDER_TWO_API}/rollback'
