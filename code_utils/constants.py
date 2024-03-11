from decouple import config

DOMAIN = 'http://localhost:8501' # TODO: update this url to the deployed url
SIGNUP_URL = f"{DOMAIN}/Sign_Up"
LOGIN_URL = f"{DOMAIN}/ScrapStore"
CHECKOUT_SUCCESS_URL = f"{DOMAIN}/ScrapStore"
CHECKOUT_CANCEL_URL = DOMAIN
USER_TABLE = 'users'
# TODO: switch our db over to mysql
DB_URL = f"postgresql://{config('DB_USER')}:{config('DB_PWD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"
#DB_URL = "postgresql://postgres:grapior0896@localhost:5432/postgres"
