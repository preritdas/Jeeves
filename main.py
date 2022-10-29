"""
Create the main Flask application and define the handlers to route inbound requests
to the correct app. Use threading to instantly return a response at the inbound-sms
endpoint.
"""
# External
from flask import Flask, request

# Local
import datetime as dt
import multiprocessing

# Project
import parsing
import permissions
import texts
import usage


app = Flask(__name__)


def main_handler(inbound_sms_content: dict) -> tuple[str, int]:
    """
    Handle all inbound messages.
    
    Keep this as simple as possible, with plenty of outsourcing.
    """
    sender: str = inbound_sms_content["msisdn"]

    # No concat assertion
    if parsing.is_concat(inbound_sms_content):
        texts.send_message(
            "Your message was too long. It was split by your carrier.",
            sender
        )
        return "", 204

    # Valid assertion
    if not parsing.assert_valid(inbound_sms_content):
        texts.send_message(
            "Your message was invalid and unrecognized.",
            sender
        )
        return "", 204

    # App availablity
    requested_app, app_name = parsing.requested_app(inbound_sms_content)

    if not requested_app:
        texts.send_message(
            f"That app does not exist.",
            sender
        )
        return "", 204

    # App permissions
    if not permissions.check_permissions(sender, app_name):
        texts.send_message(
            f"It seems you don't have permission to use app '{app_name}'.",
            sender
        )
        return "", 204

    # Run the app
    content, options = parsing.app_content_options(inbound_sms_content)
    options["inbound_phone"] = sender

    try:
        response = requested_app(content, options)
    except Exception as e:
        response = f"Unfortunately, that failed. '{str(e)}'"

    texts.send_message(response, sender)
    usage.log_use(
        phone_number = sender,
        app_name = app_name,
        content = content,
        options = options
    ) 

    return "", 204


@app.route("/inbound-sms", methods=["POST"])
def main_handler_wrapper():
    inbound_sms_content = request.get_json()
    print("\n", inbound_sms_content, sep="")

    if type(inbound_sms_content) is not dict:
        return "Not JSON format.", 400

    process_inbound = multiprocessing.Process(
        target = main_handler,
        kwargs = {
            "inbound_sms_content": inbound_sms_content
        }
    )
    
    process_inbound.start()  # process the message after returning success
    return "", 204


@app.route("/")
def test():
    return "All working here."
