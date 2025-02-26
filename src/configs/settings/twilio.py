"""
Twilio settings for the project.
"""

from .env import env


TWILIO_ACCOUNT_SID = env.str("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env.str("TWILIO_AUTH_TOKEN")
TWILIO_MESSAGING_SERVICE_SID = env.str("TWILIO_MESSAGING_SERVICE_SID")

# Phone numbers for different countries - EXAMPLES for now
TWILIO_PHONE_NUMBERS = {
    "ua": "+38099245702",
    "us": "+18163061121",
}

DEFAULT_TWILIO_PHONE_NUMBER = TWILIO_PHONE_NUMBERS["us"]
