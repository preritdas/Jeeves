"""Handle inbound text messages."""
# External
from fastapi import Form, APIRouter

# Local
import threading

# Project
import inbound
from config import CONFIG
import parsing


router = APIRouter()


def route_to_handler(inbound_sms_content: parsing.InboundMessage) -> None:
    """
    Routes inbound sms content to the main handler, and reads the config's
    stated preference of threaded responses to either handle the inbound in a thread
    (simply start the thread) or to wait for the processing to complete.
    """
    if not CONFIG.General.threaded_inbound:
        inbound.main_handler(inbound_message=inbound_sms_content)
        return

    # Otherwise, process in a thread
    process_inbound = threading.Thread(
        target=inbound.main_handler,
        kwargs={"inbound_sms_content": inbound_sms_content}
    )
    process_inbound.start()


@router.post("/inbound-sms", status_code=204)
def main_handler_wrapper(From: str = Form(...), Body: str = Form(...)):
    """Handle the inbound, routing it to the handler."""
    # Validate the data
    inbound_model = parsing.InboundMessage(phone_number=From, body=Body)

    # Process the request
    route_to_handler(inbound_model)
    return ""
