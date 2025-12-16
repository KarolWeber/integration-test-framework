from allure_combine import combine_allure

"""
Generuje kompletny raport HTML z wyników Allure.
Instrukcja użycia:
1. Uruchomić testy z parametrem:
       pytest --alluredir=allure-results
2. Wygenerować raport Allure:
       allure generate allure-results
3. Uruchomić ten skrypt, aby utworzyć kompletny plik HTML.
"""
combine_allure("../../allure-report")
