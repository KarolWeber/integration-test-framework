import os

from dotenv import load_dotenv

load_dotenv()

PLAYER_API = os.getenv("PLAYER_API")
ADMIN_API = os.getenv("ADMIN_API")
PROVIDER_ONE_API = os.getenv("PROVIDER_ONE_API")
PROVIDER_TWO_API = os.getenv("PROVIDER_TWO_API")
EMAIL_DOMAIN = os.getenv("EMAIL_DOMAIN")
