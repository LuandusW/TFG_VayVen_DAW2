import os

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

client_id = os.getenv("PAYPAL_CLIENT_ID")
client_secret = os.getenv("PAYPAL_CLIENT_SECRET")

environment = SandboxEnvironment(
    client_id=client_id,
    client_secret=client_secret
)

paypal_client = PayPalHttpClient(environment)