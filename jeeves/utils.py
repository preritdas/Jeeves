"""Utilities for everything."""
from functools import wraps


def app_handler(app_help: str, app_options: dict = {}):
    """
    Handler decorator that automatically returns help options if requested in
    the handler's required `options` parameter.
    """
    app_help += "\n\n"

    def wrapper_func(function):
        @wraps(function)
        def inner(content: str, options: dict[str, str]) -> str:
            if not "help" in options:
                return function(content, options)

            if not app_options:
                return app_help + "There are no available options."

            option_messages = []
            for option, message in app_options.items():
                option_messages.append(f"- {option.lower()}: {message.lower()}")

            return app_help + "Available options:\n" + "\n".join(option_messages)

        return inner

    return wrapper_func


def validate_phone_number(phone_number: str) -> str:
    """Standardize and validate input phone number. Raise ValueError if invalid."""
    try:
        phone_number = str(phone_number)
    except ValueError:
        raise ValueError(f"Couldn't interpret {phone_number} as a string.")
        
    if not phone_number:
        raise ValueError("Phone number was given as an empty string.")

    # Remove the plus if given, ex. Twilio does
    if phone_number[0] == "+":
        phone_number = phone_number[1:]

    if not phone_number.isnumeric():
        raise ValueError(f"Resulting phone number {phone_number} is not numeric.")

    if len(phone_number) != 11:
        raise ValueError(
            f"Phone number {phone_number} isn't 11 digits. Does it have a country code?"
        )
        
    # Otherwise, if all looks good
    return phone_number


# ---- Web stuff ----

REQUEST_HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) " "Gecko/20100101 Firefox/12.0"
    ),
    "Accept-Language": "en-US",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html",
    "Referer": "https://www.google.com",
}