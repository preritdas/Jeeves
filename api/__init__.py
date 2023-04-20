"""
Create the main FastAPI application with routes. Use the `inbound` module main handler. 
Use threading to instantly return a response at the inbound-sms
endpoint.
"""
# External
from fastapi import FastAPI

# Routers
from . import text_inbound, voice_inbound


app = FastAPI()


@app.get("/", status_code=200)
def test():
    return f"All working here."


# Include the routers
app.include_router(text_inbound.router, prefix="/texts", tags="Text Inbound")
app.include_router(voice_inbound.router, prefix="/voice", tags="Voice Inbound")