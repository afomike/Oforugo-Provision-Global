import os
import secrets

# Get the secret from environment variables, or generate a random one
session_secret = os.environ.get("SESSION_SECRET") or secrets.token_hex(64)

print("Your session secret is:", session_secret)
