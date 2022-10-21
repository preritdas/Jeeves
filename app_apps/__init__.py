"""Registered apps."""
# Project
import utils
import permissions

# Apps
import app_groceries
import app_wordhunt
import app_echo
import app_permissions
import app_jokes
import app_weather
import app_invite
import app_usage
import app_rt
import app_cocktails


@utils.app_handler(app_help = "See a list of available apps.")
def handler(content: str, options: dict):
    """Handler for apps. Filters by permissions."""
    accessible_apps: list[str] = [
        app for app in PROGRAMS.keys() if permissions.check_permissions(
            phone = options["inbound_phone"],
            app_name = app
        )
    ]
        
    available_apps = "\n".join(accessible_apps)
    return f"The following apps are available to you.\n{available_apps}"


PROGRAMS = {
    "apps": handler,
    "groceries": app_groceries.handler,
    "wordhunt": app_wordhunt.handler,
    "echo": app_echo.handler,
    "permissions": app_permissions.handler,
    "jokes": app_jokes.handler,
    "weather": app_weather.handler,
    "invite": app_invite.handler,
    "usage": app_usage.handler,
    "rt": app_rt.handler,
    "cocktails": app_cocktails.handler
}
