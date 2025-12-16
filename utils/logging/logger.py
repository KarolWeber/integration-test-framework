import json
import logging

logger = logging.getLogger("new vegas integration tests")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(levelname)s] %(asctime)s | %(name)s | %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

request_log = []


# LOGGER
def log_request(url=None, payload=None, response=None):
    """
    Dodaje aktywność podczas testu.
    :param url: (str) Adres URL wo żądania API.
    :param payload: (dict) Dane wysyłane w żądaniu.
    :param response: Odpowiedź serwera.
    :return: Rejestruje log w globalnej liście 'request_log'.
    """
    log_item = {}
    if url:
        log_item["url"] = url
    if payload:
        log_item["payload"] = payload
    if response:
        log_item["response"] = response
    request_log.append(log_item)


def clear_log():
    """
    Usuwa wszystkie zapisane logi z globalnej listy 'request_log'.
    """
    request_log.clear()


def dump_log():
    """
    Loguje wszystkie logi zapisane w globalnej liście 'request_log'
    """
    for log_item in request_log:
        if "url" in log_item:
            logger.info("=== URL ===")
            logger.info(log_item["url"])
        if "payload" in log_item:
            logger.info("=== REQUEST ===")
            try:
                logger.info(json.dumps(log_item["payload"], indent=2))
            except (TypeError, ValueError):
                logger.info(str(log_item["payload"]))
        if "response" in log_item:
            logger.info("=== RESPONSE ===")
            try:
                logger.info(json.dumps(log_item["response"], indent=2))
            except (TypeError, ValueError):
                logger.info(str(log_item["response"]))
        logger.info(30 * "=")


# STEPS LOGGER
class StepLogger:
    """
    Generuje i przechowuje kroki dodane w funkcjach testowych
    """
    steps = []

    @staticmethod
    def log_step(step_name, payload=None, response=None):
        """
        Dodaje krok testowy do listy 'steps' i wypisuje go w konsoli.
        :param step_name: (str) Opis kroku testowego.
        :param payload: (dict) Payload wysyłany w kroku testowym.
        :param response: Odpowiedź serwera.
        :return: Krok jest dodawany do listy 'steps'.
        """
        step = step_name
        if response is not None:
            step = f"Response: {response.status_code} | {step_name}"
            if response.status_code != 200:
                if payload:
                    step += f"\nPayload:\n{payload}"
                try:
                    content = json.dumps(response.json(), indent=2)
                except ValueError:
                    content = response.text
                step += f'\nContent:\n{content}'
        print(step, flush=True)
        StepLogger.steps.append(step)
