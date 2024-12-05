"""Get currency"""
from forex_python.converter import (CurrencyRates,
                                    DecimalFloatMismatchError,
                                    RatesNotAvailableError)


class State:
    """Configuration class"""
    CONFIG_ERROR: str = "CONFIG_ERROR"


def exchange(convert_from, convert_to, amount) -> str:
    """Base convert function"""
    rate = CurrencyRates()
    try:
        return rate.convert(convert_from, convert_to, amount)

    except RatesNotAvailableError:
        return State().CONFIG_ERROR

    except DecimalFloatMismatchError:
        return State().CONFIG_ERROR


if __name__ == "__main__":
    print(exchange("EUR", "PLN", 10))
