from infrastructure.config import ADMIN_API


class AdminUrls:
    class User:
        base = f'{ADMIN_API}/user'
        login = f'{base}/authenticate'
        logout = f'{base}/logout'

    class Marketing:
        class Bonuses:
            base = f'{ADMIN_API}/example_bonus'
            get = f'{base}/{{bonus_definition_id}}'
            get_list = f'{base}/list'
            create = f'{base}/create'

        class FreeSpinTemplates:
            base = f'{ADMIN_API}/example_template'
            get = f'{base}/{{template_id}}'
            edit_games = f'{base}/games/edit'
            enable = f'{base}/enabled/edit'
            list = f'{base}/list'
            create = f'{base}/create'
            delete = f'{base}/delete'

    class Casino:
        class Game:
            base = f'{ADMIN_API}/game'
            list = f'{base}/list'
            change_reporting_group = f'{base}/example_group/change'
            change_visibility = f'{base}/visibility/change'

        class ReportingGroup:
            base = f'{ADMIN_API}/game/example_game_group'
            get = f'{base}/list'

        class GameProvider:
            base = f'{ADMIN_API}/example_provider'
            sync_games = f'{base}/games/sync'
            get = f'{base}/list'

    class Technical:
        class Game:
            base = f'{ADMIN_API}/example/games/providers'
            create_custom_game = f'{base}/update'
            delete_custom_game = f'{base}/delete'

        class Bonus:
            base = f'{ADMIN_API}/example/bonus/definition'
            delete = f'{base}/delete'

    class Players:
        class Bonuses:
            base = f'{ADMIN_API}/example_player_bonuses'
            player_bonuses = f'{base}/list'

        class Wallet:
            base = f'{ADMIN_API}/example_financial_activity'
            activity = f'{base}/list'
