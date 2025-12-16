from time import sleep


def wait_for_list(fetch_from, count=1, timeout=30, interval=1):
    """
    Oczekuje na pojawienie się przynajmniej `count` elementów na liście zwracanej przez funkcję `fetch_from`.
    :param fetch_from: Funkcja, która ma zostać wykonywana w celu uzyskania listy. Misu być przekazana przez `lambda :`.
    :param count: (int) Liczba elementów, która musi znajdować się na liście.
    :param timeout: (int) Liczba powtórzeń wywołania `fetch_from`.
    :param interval: (float) Czas (w sekundach) oczekiwania pomiędzy kolejnymi próbami.
    :return: Lista zwrócona przez `fetch_from`.
    """
    data = []
    for i in range(timeout):
        data = fetch_from()
        if data and len(data) >= count:
            return data
        sleep(interval)
    return data
