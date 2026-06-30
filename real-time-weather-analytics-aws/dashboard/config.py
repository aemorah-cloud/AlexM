import os
from dotenv import load_dotenv

load_dotenv()

ATHENA_DATABASE = os.getenv("ATHENA_DATABASE")
ATHENA_TABLE = os.getenv("ATHENA_TABLE")
ATHENA_OUTPUT = os.getenv("ATHENA_OUTPUT")