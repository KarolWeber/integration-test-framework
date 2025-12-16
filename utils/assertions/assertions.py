import os
from datetime import datetime
from typing import List


def get_test_path_and_name(request):
    """
    Generuje nazwę testu na podstawie pliku, klasy oraz nazwy testu.
    :param request: (pytest.FixtureRequest) Przekazywany przez pytest.
    :return: (str) Ścieżka testu w f    ormacie "plik -> klasa -> test".
    """
    node = request.node
    file_path = os.path.abspath(node.fspath)
    file_name = os.path.basename(file_path)
    class_name = node.cls.__name__ if node.cls else None
    test_name = node.name
    parts = [part for part in [file_name, class_name, test_name] if part]
    return " -> ".join(parts)


class CheckAssertions:
    """
    Klasa używana do logowania, śledzenia asercji oraz mierzenia czasu trwania testu.
    Umożliwia:
        - dodawanie wielu asercji w obrębie jednego testu,
        - zbiorcze raportowanie wyników,
        - logowanie czasu rozpoczęcia, zakończenia i trwania testu.
    :param request: (pytest.FixtureRequest) Przekazywany przez pytest.
    """

    def __init__(self, request=None):
        self.current_assertions: List[dict] = []
        self.request = request
        self.result = None
        self.info = None
        self.test_name = get_test_path_and_name(
            self.request) if self.request else "Unknown Test"
        self.start = datetime.now()

        print(f"\n{30 * '='} START TEST {30 * '='}")
        print(f"\nTEST:\t{self.test_name}")
        print("\nSTEPS:")

    def assertion(self, name, expected=None, current=None, operator="equal"):
        """
        Dodaje asercję do listy.
        :param name: (str) Nazwa lub opis asercji.
        :param expected: (Any) Wartość oczekiwana.
        :param current: (Any) Wartość otrzymana.
        :param operator: (str) Operator porównania: "equal", "not_equal", "gt", "gte", "lt", "lte", "in", "not_in", "len_equal".
        """
        operators = {
            "equal": lambda a, b: a == b,
            "not_equal": lambda a, b: a != b,
            "gt": lambda a, b: a > b,
            "gte": lambda a, b: a >= b,
            "lt": lambda a, b: a < b,
            "lte": lambda a, b: a <= b,
            "in": lambda a, b: a in b,
            "not_in": lambda a, b: a not in b,
            "len_equal": lambda a, b: len(b) == a if b is not None else False,
        }

        func = operators.get(operator)
        if func is None:
            raise ValueError(f"Unsupported operator: {operator}")

        result = func(expected, current)
        info = f"\n{name} {operator.upper().ljust(85)}result: {result}\n\tExpected: {expected}\n\tCurrent : {current}\n"
        self.current_assertions.append({"result": result, "info": info})

    def check_assertions(self):
        """
        Uruchamia sprawdzenie wszystkiech asercji na liście i generuje raport testu.
        :return:
            - wyniki poszczególnych asercji,
            - status końcowy testu,
            - czas rozpoczęcia, zakończenia i trwania testu.
        """
        self.result = all(record["result"] for record in self.current_assertions)
        self.info = ''.join(record["info"] for record in self.current_assertions)
        print(f"\nTEST RESULTS:\n{self.info}")
        try:
            assert self.result, self.info
        finally:
            end = datetime.now()
            print(f"{30 * '='} TEST TIMING {30 * '='}")
            print(f"\nTEST START AT:\t{self.start.strftime("%Y-%m-%d %H:%M:%S")}")
            print(f"TEST END AT:\t{end.strftime("%Y-%m-%d %H:%M:%S")}")
            print(f"TEST DURATION:\t{end - self.start}s\n")
            print(f"{30 * '='} END TEST {30 * '='}")
