from random import randint, choice

import allure
import pytest
from api.services.player_service.context import PlayerService
from utils.assertions.assertions import CheckAssertions
from utils.enums.bonus_types import BonusType
from utils.enums.free_spins_mode import FreeSpinsMode
from utils.mappers.mappers import PROVIDER_TWO_STATUS_MAP
from utils.waiters.wait_for_list import wait_for_list
from utils.waiters.wait_for_player_bonus_activate import \
    wait_for_bonus_activation


@pytest.mark.integration_test
@pytest.mark.integration_test_provider_two
@allure.parent_suite("Integration")
@allure.suite("Provider two")
class TestProviderTwoIntegration:
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Provider two game sync")
    def test_provider_two_game_sync(self, admin, request):
        ca = CheckAssertions(request=request)

        provider_two_games_list = admin.casino.games.list(provider="ProviderTwo", visible=True, step=False)

        provider_two_random_game = choice(provider_two_games_list)
        provider_two_filtered_games = admin.casino.games.list(provider="ProviderTwo", name=provider_two_random_game.name, visible=True)
        provider_two_game = provider_two_filtered_games[0]

        admin.technical.game.remove_game(game=provider_two_game)
        provider_two_filtered_games_after_delete_game = admin.casino.games.list(provider="ProviderTwo", name=provider_two_random_game.name, visible=True)

        admin.casino.game_providers.sync_games(provider="ProviderTwo")

        provider_two_filtered_games_after_sync = wait_for_list(
            fetch_from=lambda: admin.casino.games.list(provider="ProviderTwo", name=provider_two_random_game.name, visible=False, step=False),
            timeout=60)

        admin.casino.games.change_reporting_group(game=provider_two_filtered_games_after_sync[0], group_name=provider_two_game.reporting_game_group)
        admin.casino.games.change_visibility(games=provider_two_filtered_games_after_sync[0], is_visible=True)

        ca.assertion(name="Brak gry na liście po usunięciu", expected=provider_two_game.name,
                     current=[g.name for g in provider_two_filtered_games_after_delete_game], operator="not_in")
        ca.assertion(name="Gra na liście po synchronizacji", expected=provider_two_game.name, current=[g.name for g in provider_two_filtered_games_after_sync],
                     operator="in")
        ca.check_assertions()

    @allure.title("Provider two player authentication")
    @allure.severity(allure.severity_level.NORMAL)
    def test_provider_two_player_authentication(self, admin, player, request):
        ca = CheckAssertions(request=request)

        game = admin.technical.game.create_custom_game(game_provider="ProviderTwo")

        player_run_game = player.game.run_provider_two_game(game=game)

        ca.assertion(name="Provider two authenticate status", expected="SUCCESS", current=player_run_game.authenticate_status)
        ca.check_assertions()

    @allure.title("Provider two current funds")
    @allure.severity(allure.severity_level.NORMAL)
    def test_provider_two_current_funds(self, admin, player, request):
        ca = CheckAssertions(request=request)

        game = admin.technical.game.create_custom_game(game_provider="ProviderTwo")

        deposit_amount = float(randint(50, 500))

        player_run_game = player.game.run_provider_two_game(game=game)
        player.wallet.deposit(deposit_amount=deposit_amount)
        player_run_game.get_funds()

        ca.assertion(name="Current player balance", expected=deposit_amount, current=player_run_game.current_balance)
        ca.check_assertions()

    @allure.title("Provider two run demo not logged")
    @allure.severity(allure.severity_level.NORMAL)
    def test_provider_two_run_demo_not_logged(self, admin, request):
        ca = CheckAssertions(request=request)

        player = PlayerService()
        games = admin.casino.games.list()
        game = next(g for g in games if g.provider_name == "Provider two" and g.has_demo and "AUTOMAT" not in g.name)
        demo_game_url = player.game.run_provider_two_demo(game=game)

        ca.assertion(name="Run demo", expected=f"game={game.provider_game_data.id}", current=demo_game_url, operator="in")
        ca.check_assertions()

    @allure.title("Provider two run demo logged")
    @allure.severity(allure.severity_level.NORMAL)
    def test_provider_two_run_demo_logged(self, admin, request):
        ca = CheckAssertions(request=request)

        player = PlayerService()
        player.user.login()
        games = admin.casino.games.list()
        game = next((g for g in games if g.provider_name == "Provider two" and g.has_demo and "AUTOMAT" not in g.name), None)
        if game is None:
            raise ValueError("No Games found for ProviderTwo")
        demo_game_url = player.game.run_provider_two_demo(game=game)
        ca.assertion(name="Run demo", expected=f"game={game.provider_game_data.id}", current=demo_game_url, operator="in")
        ca.check_assertions()

    @allure.title("Provider two standard gameplay")
    @allure.severity(allure.severity_level.NORMAL)
    def test_provider_two_standard_gameplay(self, admin, player, request):
        ca = CheckAssertions(request=request)

        game = admin.technical.game.create_custom_game(game_provider="ProviderTwo")

        player.wallet.deposit(deposit_amount=50)
        run_game = player.game.run_provider_two_game(game=game)
        run_game.round(bet_amount=20, win_amount=50)

        player_wallet_history = wait_for_list(fetch_from=lambda: admin.players.wallet.activity(player), count=3, timeout=10)

        ca.assertion(name="Bet status", expected="SUCCESS", current=PROVIDER_TWO_STATUS_MAP.get(run_game.history[0]["bet"]["status"]))
        ca.assertion(name="Win status", expected="SUCCESS", current=PROVIDER_TWO_STATUS_MAP.get(run_game.history[0]["win"]["status"]))
        ca.assertion(name="Wallet log type", expected="BET", current=player_wallet_history[1].type)
        ca.assertion(name="Wallet log type", expected="WIN", current=player_wallet_history[0].type)
        ca.check_assertions()

    @allure.title("Provider two wallet free spin gameplay")
    @allure.severity(allure.severity_level.NORMAL)
    def test_provider_two_wallet_free_spin_gameplay(self, admin, player, request):
        ca = CheckAssertions(request=request)

        free_spin_template = admin.marketing.free_spins_templates.create(
            provider_integration="Provider two",
            free_spin_mode=FreeSpinsMode.wallet_free_spin,
            name=ca.test_name)
        game = choice(admin.casino.games.list(provider="ProviderTwo", visible=True, free_spins=True))
        admin.marketing.free_spins_templates.add_games(template=free_spin_template, games=[game])
        admin.marketing.free_spins_templates.set_enable(template=free_spin_template)
        free_spin_bonus = admin.marketing.bonuses.create(
            bonus_type_enum=BonusType.free_spins_auto_reload_wallet,
            bonus_name=ca.test_name,
            free_spin_template=free_spin_template)
        player.user.login()
        player_bonus = player.bonus.available_bonuses(bonus=free_spin_bonus)
        player.wallet.deposit(50, bonus=player_bonus)
        wait_for_bonus_activation(admin_context=admin, player_context=player, bonus_object=free_spin_bonus, status="ACTIVE_FREE_SPINS")
        player_free_spins_external_id = admin.players.bonuses.current_bonuses(player, bonus=free_spin_bonus).free_spins_external_id
        run_game = player.game.run_provider_two_game(game, free_spins_external_id=player_free_spins_external_id, player_bonus=player_bonus)

        run_game.wallet_free_spin_round(win_amount=20)
        player_wallet_history = wait_for_list(fetch_from=lambda: admin.players.wallet.activity(player=player), count=4, timeout=10)

        admin.technical.bonus.delete(bonus=free_spin_bonus)
        admin.marketing.free_spins_templates.delete(template=free_spin_template)

        ca.assertion(name="Bet status", expected="SUCCESS", current=PROVIDER_TWO_STATUS_MAP.get(run_game.history[0]["bet"]["status"]))
        ca.assertion(name="Win status", expected="SUCCESS", current=PROVIDER_TWO_STATUS_MAP.get(run_game.history[0]["win"]["status"]))
        ca.assertion(name="Wallet log type", expected="FREE_SPIN_BET", current=player_wallet_history[1].type)
        ca.assertion(name="Wallet log type", expected="FREE_SPIN_WIN", current=player_wallet_history[0].type)
        ca.check_assertions()

    @allure.title("Provider two provider free spin gameplay")
    @allure.severity(allure.severity_level.NORMAL)
    def test_provider_two_provider_free_spin_gameplay(self, admin, player, request):
        ca = CheckAssertions(request=request)

        free_spin_template = admin.marketing.free_spins_templates.create(
            provider_integration="Provider two",
            free_spin_mode=FreeSpinsMode.provider_free_spin,
            name=ca.test_name)
        game = choice(
            admin.casino.games.list(provider="ProviderTwo", visible=True, free_spins=True))
        admin.marketing.free_spins_templates.add_games(template=free_spin_template, games=[game])
        admin.marketing.free_spins_templates.set_enable(template=free_spin_template)
        free_spin_bonus = admin.marketing.bonuses.create(
            bonus_type_enum=BonusType.free_spins_auto_reload_provider,
            bonus_name=ca.test_name,
            free_spin_template=free_spin_template)

        player.user.login()
        player_bonus = player.bonus.available_bonuses(bonus=free_spin_bonus)
        player.wallet.deposit(deposit_amount=50, bonus=player_bonus)
        wait_for_bonus_activation(admin_context=admin, player_context=player, bonus_object=free_spin_bonus, status="ACTIVE_FREE_SPINS")
        player_free_spins_external_id = admin.players.bonuses.current_bonuses(player=player, bonus=free_spin_bonus).free_spins_external_id
        run_game = player.game.run_provider_two_game(game=game, free_spins_external_id=player_free_spins_external_id, player_bonus=player_bonus)
        run_game.provider_free_spin_round(win_amount=20)

        admin.technical.bonus.delete(bonus=free_spin_bonus)
        admin.marketing.free_spins_templates.delete(template=free_spin_template)

        player_wallet_history = wait_for_list(fetch_from=lambda: admin.players.wallet.activity(player=player), count=4, timeout=10)

        ca.assertion(name="Bet status", expected="SUCCESS", current=PROVIDER_TWO_STATUS_MAP.get(run_game.history[0]["bet"]["status"]))
        ca.assertion(name="Win status", expected="SUCCESS", current=PROVIDER_TWO_STATUS_MAP.get(run_game.history[0]["win"]["status"]))
        ca.assertion(name="Wallet log type", expected="FREE_SPIN_BET", current=player_wallet_history[1].type)
        ca.assertion(name="Wallet log type", expected="FREE_SPIN_WIN", current=player_wallet_history[0].type)
        ca.check_assertions()
