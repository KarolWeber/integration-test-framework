from enum import Enum

import requests
from utils.logging.logger import log_request


class RequestApi:
    class HTTPMethod(Enum):
        GET = "get"
        POST = "post"
        PUT = "put"

    @staticmethod
    def execute(method: HTTPMethod, url, context=None, payload=None, files=None, additional_headers=None, timeout=None):
        """
        Wysyła żądanie HTTP do serwera i zwraca odpowiedź
        :param method: (enum) HTTPMethod metoda żądania
        :param url: (str) adres endpointa API
        :param context: Obiekt zalogowanego kontekstu
        :param payload: (dict) - Dane wymagane w żądaniu
        :param files: Pliki wymagane w żądaniu
        :param additional_headers: (dict) - Nagłówki żądania
        :param timeout: (int) Czas oczekiwania na odpowiedź
        """
        if method not in RequestApi.HTTPMethod:
            raise ValueError("Unsupported HTTP method")

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X)"
        }
        if files:
            headers.pop("Content-Type")
        if additional_headers:
            headers.update(additional_headers)

        if context and getattr(context, "token", None):
            headers["Authorization"] = "Bearer " + context.token

        try:
            if method == RequestApi.HTTPMethod.GET:
                resp = requests.get(url, headers=headers, params=payload, timeout=timeout)
            elif method == RequestApi.HTTPMethod.POST:
                resp = requests.post(url, headers=headers, json=payload, files=files, timeout=timeout)
            elif method == RequestApi.HTTPMethod.PUT:
                resp = requests.put(url, headers=headers, json=payload, timeout=timeout)
            else:
                raise ValueError("Unsupported HTTP method")
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed: {e}") from e
        log_request(url=url, payload=payload, response=resp)
        return resp
